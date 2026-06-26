#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数字人视频生成主脚本

全流程：[TTS可选] → 读取文件转base64 → 提交(AEP /video2) → 智能轮询TOS URL → 输出结果JSON

/video2 接口将生成的视频上传到火山引擎 TOS，返回公开可访问的 URL。
skill 通过 HTTP HEAD 轮询该 URL 判断是否就绪。
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

import requests


# ====================== 默认配置 ======================

# AEP — 走 /video2（异步立即返回，结果上传 TOS）
DEFAULT_AEP_BASE_URL = "https://aep.focusaim.com"
DEFAULT_AEP_SERVICE_ID = "infinitetalk"
DEFAULT_AEP_ROUTE_URI = "/video2"

# 视频服务直连（测试用，绕过 AEP）
DEFAULT_DIRECT_URL = "http://192.168.25.10:32004"


# TTS — 走 AEP 网关
DEFAULT_TTS_AEP_SERVICE_ID = "speech_generation_service_pre"
DEFAULT_TTS_AEP_ROUTE_URI = "/v1/tts"
DEFAULT_VOICE_PRESET = "中文女"

# 轮询
DEFAULT_POLL_TIMEOUT = 3600  # 60 分钟（与 SKILL.md 一致）


# ====================== 参数解析 ======================

SECRET_KEY_NAME = "aim-secret-key"

# 密钥唯一来源：skill 根目录的 .env 文件。不再读进程环境、不再摸家目录、不再跨 agent 找。
_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def resolve_secret() -> tuple[str, str]:
    """从 <skill>/.env 里读 aim-secret-key。返回 (value, source)。"""
    if not _ENV_FILE.is_file():
        return "", ""
    try:
        for raw in _ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            if key.strip() != SECRET_KEY_NAME:
                continue
            cleaned = value.strip().strip('"').strip("'")
            if cleaned:
                return cleaned, f"file:{_ENV_FILE}"
    except OSError:
        pass
    return "", ""


def resolve_secret_value() -> str:
    return resolve_secret()[0]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="数字人视频生成")

    # 启动前自检
    p.add_argument("--check-config", action="store_true",
                   help="只检查 aim-secret-key 是否已配置，输出 JSON 后退出")
    p.add_argument("--list-tasks", action="store_true",
                   help="打印本地任务状态表（pending/ready/expired），输出 JSON 后退出")

    # 必填（check-config 模式下除外）
    p.add_argument("--image-path", required=False, help="人物图片本地路径")

    # 音频来源 (三选一)
    audio_group = p.add_argument_group("音频来源 (三选一)")
    audio_group.add_argument("--audio-path", default="", help="现成音频文件路径")
    audio_group.add_argument("--text", default="", help="要说的文案（需配合语音选项）")
    audio_group.add_argument("--voice-sample", default="", help="克隆语音样本路径（5-10秒）")
    audio_group.add_argument("--voice-sample-text", default="", help="语音样本对应的文字")
    audio_group.add_argument("--voice-preset", default="", help="预设语音: 中文男/中文女/英文男/英文女")

    # 可选
    p.add_argument("--task-name", default="digital-human", help="任务名称，用于本地文件命名")
    p.add_argument("--prompt", default="", help="动作描述提示词（可选）")
    p.add_argument("--quality", default="", help="视频质量: high/normal")
    p.add_argument("--user-id", default=os.getenv("AEP_USER_ID", "aim_user"))
    p.add_argument("--test", action="store_true", default=True, help="使用测试环境（服务端FFS）")
    p.add_argument("--prod", action="store_true", help="使用正式环境")

    # aim-secret-key —— 展示/存储用这个规范名；读取时宽容接受常见变体
    aep_group = p.add_argument_group("aim-secret-key 配置")
    aep_group.add_argument("--aep-base-url", default=os.getenv("AEP_BASE_URL", DEFAULT_AEP_BASE_URL))
    aep_group.add_argument("--aim-secret-key", default=resolve_secret_value())

    # TTS
    tts_group = p.add_argument_group("TTS 配置")
    tts_group.add_argument("--tts-service-id", default=os.getenv("TTS_AEP_SERVICE_ID", DEFAULT_TTS_AEP_SERVICE_ID),
                           help="TTS 的 AEP 服务 ID")

    # 轮询
    p.add_argument("--poll-timeout", type=int, default=DEFAULT_POLL_TIMEOUT)

    args = p.parse_args()
    if args.prod:
        args.test = False
    return args


# ====================== 时间预估 ======================

def get_audio_duration(audio_path: str) -> float:
    """用 ffprobe 获取音频时长（秒），失败返回 -1"""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
            capture_output=True, text=True, timeout=10
        )
        return float(result.stdout.strip())
    except Exception:
        return -1


def estimate_generation_time(audio_duration: float) -> tuple[int, int]:
    """根据音频时长估算视频生成时间范围（秒）

    经验数据（4.8s 音频 → 150~270s，约 25~50 倍）：
    - overhead: FFS 上传下载、队列调度等固定开销 ~30s
    - 处理倍率: 25~50x 音频时长

    Returns:
        (est_min, est_max) 预估最小和最大秒数
    """
    if audio_duration <= 0:
        return 60, 360  # 无法获取时长时给保守范围

    overhead = 30
    est_min = int(audio_duration * 25) + overhead
    est_max = int(audio_duration * 50) + overhead
    return max(60, est_min), max(120, est_max)


# ====================== TTS 语音合成 ======================

def generate_tts_audio(args: argparse.Namespace) -> str:
    """调用 TTS 服务生成音频，返回临时音频文件路径。

    TTS 固定走 AEP 网关，复用 aim-secret-key 鉴权。
    语音来源：
    1. 有 voice-sample + voice-sample-text → 克隆语音
    2. 有 voice-preset → 预设语音
    3. 都没有 → 默认预设语音（中文女）
    """
    if not args.aim_secret_key:
        raise ValueError(_missing_secret_message("TTS"))

    print(f"[TTS] 开始语音合成，文案: {args.text[:50]}...")

    request_data: dict = {"text": args.text}

    if args.voice_sample and args.voice_sample_text:
        sample_path = Path(args.voice_sample)
        if not sample_path.exists():
            raise FileNotFoundError(f"语音样本不存在: {sample_path}")
        with open(sample_path, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")
        request_data["references"] = [{
            "audio": audio_b64,
            "text": args.voice_sample_text,
        }]
        print(f"[TTS] 使用克隆语音，样本: {sample_path.name}")
    else:
        preset = args.voice_preset or DEFAULT_VOICE_PRESET
        request_data["reference_id"] = preset
        print(f"[TTS] 使用预设语音: {preset}")

    tts_url = f"{args.aep_base_url.rstrip('/')}/{args.tts_service_id}{DEFAULT_TTS_AEP_ROUTE_URI}"
    headers = {
        "X-AEP-CONSUMER-SECRET": args.aim_secret_key,
        "X-AEP-SERVICE-ID": args.tts_service_id,
        "X-AEP-REQUEST-ID": str(uuid.uuid4()),
    }
    print(f"[TTS] 走 AEP: {tts_url}")

    resp = requests.post(tts_url, json=request_data, headers=headers, timeout=120,
                         proxies={"http": None, "https": None})
    if resp.status_code != 200:
        raise RuntimeError(f"[TTS] 请求失败，状态码: {resp.status_code}, 内容: {resp.text[:200]}")

    resp_data = resp.json()
    if resp_data.get("success") != 1:
        raise RuntimeError(f"[TTS] 合成失败: {resp_data.get('msg', '未知错误')}")

    audio_b64 = resp_data["data"]["audio_base64"]
    audio_bytes = base64.b64decode(audio_b64)

    tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_file.write(audio_bytes)
    tmp_file.close()
    print(f"[TTS] 语音合成成功，保存到: {tmp_file.name}")
    return tmp_file.name


# ====================== 文件读取 ======================

def file_to_base64(file_path: str) -> str:
    """读取文件并返回 base64 编码字符串。"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")
    with path.open("rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def smart_poll_url(
    video_url: str,
    est_min: int,
    est_max: int,
    timeout: int,
) -> None:
    """智能轮询 TOS URL：用 HTTP HEAD 检测视频是否就绪

    策略：
    - 阶段1（0 ~ est_min*0.7）: 每 15s 轮询，大概率还没好
    - 阶段2（est_min*0.7 ~ est_max）: 每 5s 轮询，快要好了
    - 阶段3（est_max ~ timeout）: 每 3s 轮询，应该随时出结果
    """
    phase1_end = int(est_min * 0.7)
    phase2_end = est_max
    start = time.time()

    print(f"[轮询] 预估 {est_min}~{est_max}s，前 {phase1_end}s 每15s检查，之后加速")
    print(f"[轮询] URL: {video_url}")

    while True:
        elapsed = int(time.time() - start)

        try:
            resp = requests.head(video_url, timeout=10, allow_redirects=True,
                                 proxies={"http": None, "https": None})
            if resp.status_code == 200:
                content_length = resp.headers.get("Content-Length", "?")
                print(f"[轮询] {elapsed}s - 视频已就绪！Content-Length: {content_length}")
                return
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass

        if elapsed >= timeout:
            raise TimeoutError(f"轮询超时（{timeout}s），URL: {video_url}")

        if elapsed < phase1_end:
            interval = 15
            phase = "等待中"
        elif elapsed < phase2_end:
            interval = 5
            phase = "接近完成"
        else:
            interval = 3
            phase = "应该快了"

        if elapsed == 0 or elapsed % 30 == 0:
            pct = min(100, int(elapsed / est_min * 100)) if est_min > 0 else 0
            print(f"[轮询] {elapsed}s - {phase}（~{pct}%），{interval}s后重试")

        time.sleep(interval)


# ====================== 提交任务 ======================

def _missing_secret_message(caller: str) -> str:
    return (
        f"[{caller}] aim-secret-key 未配置。\n"
        f"  1. 访问 https://tools.mentarc.cn/aim-skills/ 注册获取密钥\n"
        f"  2. 把密钥粘给 agent，由它写入 {_ENV_FILE}\n"
        f"     格式：一行 aim-secret-key=<你的密钥>"
    )


def submit_to_aep(args: argparse.Namespace, payload: dict) -> dict:
    """通过 AEP 网关提交 /video2（异步立即返回，结果上传 TOS）。"""
    secret = args.aim_secret_key
    if not secret:
        raise ValueError(_missing_secret_message("AEP"))

    request_id = str(uuid.uuid4())
    target_url = f"{args.aep_base_url.rstrip('/')}/{DEFAULT_AEP_SERVICE_ID}{DEFAULT_AEP_ROUTE_URI}"

    headers = {
        "X-AEP-CONSUMER-SECRET": secret,
        "X-AEP-REQUEST-ID": request_id,
    }

    print(f"[AEP] 提交到: {target_url}")
    print(f"[AEP] request_id: {request_id}")

    resp = requests.post(target_url, json=payload, headers=headers, timeout=30,
                         proxies={"http": None, "https": None})

    if not resp.text.strip():
        raise RuntimeError(f"[AEP] 服务返回空响应，status={resp.status_code}")
    try:
        resp_data = resp.json()
    except Exception:
        raise RuntimeError(f"[AEP] 响应非JSON，status={resp.status_code}, body={resp.text[:300]}")

    print(f"[AEP] 响应 [{resp.status_code}]: {json.dumps(resp_data, ensure_ascii=False)[:200]}")
    return {
        "mode": "aep",
        "status_code": resp.status_code,
        "data": resp_data,
        "request_id": request_id,
        "target_url": target_url,
    }


# ====================== 主流程 ======================

def _check_config_report() -> dict:
    """给 agent 用的启动前自检。"""
    value, source = resolve_secret()
    return {
        "aim_secret_key_configured": bool(value),
        "resolved_from": source or None,
        "env_file": str(_ENV_FILE),
        "env_file_exists": _ENV_FILE.is_file(),
        "key_name_in_env": SECRET_KEY_NAME,
        "isolation_policy": "本脚本只读 skill 目录下的 .env，不看环境变量、不读家目录、不跨 agent 复用密钥",
        "next_action": (
            "ready"
            if value
            else f"引导用户到 https://tools.mentarc.cn/aim-skills/ 注册取到密钥后，写入 {_ENV_FILE} 的 {SECRET_KEY_NAME} 字段"
        ),
    }


# ====================== 任务状态表 ======================
# 本地 JSONL 文件，记录每次提交的生成任务。用途：
#   - 单次轮询 60 分钟超时后，任务以 "pending" 状态留存
#   - 后续运行脚本会先回扫所有 pending 任务，对 TOS URL 做一次 HEAD
#   - HEAD 200 → 标记 "ready"；仍 404 且距提交 ≥ 24h → 标记 "expired"（真的失败）

_TASK_HISTORY_FILE = Path(__file__).resolve().parent.parent / ".task-history.jsonl"
_TASK_EXPIRY_HOURS = 24


def _load_task_history() -> list[dict]:
    if not _TASK_HISTORY_FILE.is_file():
        return []
    entries: list[dict] = []
    try:
        for line in _TASK_HISTORY_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    except OSError:
        return []
    return entries


def _save_task_history(entries: list[dict]) -> None:
    try:
        tmp = _TASK_HISTORY_FILE.with_suffix(_TASK_HISTORY_FILE.suffix + ".tmp")
        tmp.write_text(
            "\n".join(json.dumps(e, ensure_ascii=False) for e in entries) + ("\n" if entries else ""),
            encoding="utf-8",
        )
        os.replace(tmp, _TASK_HISTORY_FILE)
    except OSError as exc:
        print(f"[状态表] 写入失败: {exc}")


def _upsert_task(entry: dict) -> None:
    entries = _load_task_history()
    idx = next((i for i, e in enumerate(entries) if e.get("uuid") == entry.get("uuid")), None)
    if idx is not None:
        entries[idx] = {**entries[idx], **entry}
    else:
        entries.append(entry)
    _save_task_history(entries)


def _record_task(uuid: str, task_name: str, video_url: str,
                 audio_duration: float, est_range: str, status: str) -> None:
    now = time.time()
    entry = {
        "uuid": uuid,
        "task_name": task_name,
        "video_url": video_url,
        "audio_duration": round(audio_duration, 1),
        "est_range": est_range,
        "status": status,
        "submitted_at": now,
        "last_checked_at": now,
    }
    if status == "ready":
        entry["finished_at"] = now
    _upsert_task(entry)


def _mark_task(uuid: str, **updates) -> None:
    entries = _load_task_history()
    for e in entries:
        if e.get("uuid") == uuid:
            e.update(updates)
            e["last_checked_at"] = time.time()
    _save_task_history(entries)


def _scan_pending_tasks(verbose: bool = True) -> dict:
    """HEAD 每一个 pending 任务的 TOS URL，更新其状态。"""
    entries = _load_task_history()
    pending = [e for e in entries if e.get("status") == "pending"]
    summary = {"pending_before": len(pending), "newly_ready": [],
               "still_pending": [], "newly_expired": []}
    if not pending:
        return summary

    now = time.time()
    if verbose:
        print(f"[状态表] 回扫 {len(pending)} 个 pending 任务...")

    for e in pending:
        url = e.get("video_url", "")
        age_hours = (now - e.get("submitted_at", now)) / 3600
        try:
            resp = requests.head(url, timeout=10, allow_redirects=True,
                                 proxies={"http": None, "https": None})
            status_code = resp.status_code
        except Exception:
            status_code = None

        e["last_checked_at"] = now

        if status_code == 200:
            e["status"] = "ready"
            e["finished_at"] = now
            summary["newly_ready"].append(e)
        elif age_hours >= _TASK_EXPIRY_HOURS:
            e["status"] = "expired"
            summary["newly_expired"].append(e)
        else:
            summary["still_pending"].append(e)

    _save_task_history(entries)

    if verbose:
        for e in summary["newly_ready"]:
            print(f"  ✓ ready: {e['task_name']} → {e['video_url']}")
        for e in summary["newly_expired"]:
            age_h = (now - e.get("submitted_at", now)) / 3600
            print(f"  ✗ expired (age={age_h:.1f}h): {e['task_name']} → {e['video_url']}")
        for e in summary["still_pending"]:
            age_h = (now - e.get("submitted_at", now)) / 3600
            print(f"  · still pending (age={age_h:.1f}h): {e['task_name']}")
    return summary


def _list_tasks_report() -> dict:
    entries = _load_task_history()
    return {
        "history_file": str(_TASK_HISTORY_FILE),
        "total": len(entries),
        "by_status": {
            s: [e for e in entries if e.get("status") == s]
            for s in ("pending", "ready", "expired", "failed_submit")
        },
    }


def main() -> None:
    args = parse_args()

    # ---- 启动前自检 ----
    if args.check_config:
        report = _check_config_report()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(0 if report["aim_secret_key_configured"] else 2)

    if args.list_tasks:
        print(json.dumps(_list_tasks_report(), ensure_ascii=False, indent=2, default=str))
        sys.exit(0)

    # 正常运行前先保证密钥就位，避免走到 TTS / AEP 才报错
    if not args.aim_secret_key:
        raise ValueError(_missing_secret_message("启动前自检"))

    # 先回扫之前挂起的任务，刷新状态
    scan_result = _scan_pending_tasks(verbose=True)
    if scan_result["newly_ready"]:
        print(f"[状态表] {len(scan_result['newly_ready'])} 个旧任务已就绪，可直接使用上面列出的 URL\n")

    # 校验输入
    if not args.image_path:
        raise ValueError("必须提供 --image-path")
    if not Path(args.image_path).exists():
        raise FileNotFoundError(f"图片不存在: {args.image_path}")
    if not args.audio_path and not args.text:
        raise ValueError("必须提供 --audio-path（现成音频）或 --text（文案）")

    tts_tmp_file = None
    start_time = time.time()

    try:
        # ---- Step 1: TTS（如果需要）----
        audio_path = args.audio_path
        if not audio_path:
            audio_path = generate_tts_audio(args)
            tts_tmp_file = audio_path

        if not Path(audio_path).exists():
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")

        # ---- Step 2: 获取音频时长 & 预估生成时间 ----
        audio_duration = get_audio_duration(audio_path)
        est_min, est_max = estimate_generation_time(audio_duration)

        if audio_duration > 0:
            print(f"\n[时间预估] 音频时长: {audio_duration:.1f}s，预估生成: {est_min}~{est_max}s")
        else:
            print(f"\n[时间预估] 无法获取音频时长，使用默认: {est_min}~{est_max}s")

        # ---- Step 3: 读取文件转 base64 ----
        print("\n[Step 3] 读取文件")
        image_b64 = file_to_base64(args.image_path)
        audio_b64 = file_to_base64(audio_path)
        print(f"  图片 base64 长度: {len(image_b64)}")
        print(f"  音频 base64 长度: {len(audio_b64)}")

        # ---- Step 4: 构建请求 ----
        upstream_uuid = f"dh_{uuid.uuid4().hex[:12]}"

        payload: dict = {
            "uuid": upstream_uuid,
            "userId": args.user_id,
            "imageBase64": image_b64,
            "audioBase64": audio_b64,
            "prompt": args.prompt,
            "test": args.test,
        }
        if args.quality:
            payload["quality"] = args.quality

        print(f"\n[Step 4] 请求参数:")
        print(f"  uuid: {upstream_uuid}")

        # ---- Step 5: 提交任务 ----
        print(f"\n[Step 5] 通过 AEP 提交任务")
        submit_result = submit_to_aep(args, payload)

        resp_data = submit_result["data"]

        if submit_result["status_code"] not in (200, 202):
            raise RuntimeError(f"提交失败: status={submit_result['status_code']}, "
                               f"body={json.dumps(resp_data, ensure_ascii=False)[:200]}")

        # 从响应中提取 videoUrl（TOS 公开 URL）
        video_url = None
        if isinstance(resp_data, dict):
            data_field = resp_data.get("data")
            if isinstance(data_field, dict):
                video_url = data_field.get("videoUrl")

        if not video_url:
            raise RuntimeError(f"响应中未找到 videoUrl: {json.dumps(resp_data, ensure_ascii=False)[:200]}")

        print(f"  TOS URL: {video_url}")

        # 提交成功立刻落盘为 pending
        _record_task(upstream_uuid, args.task_name, video_url,
                     audio_duration, f"{est_min}~{est_max}s", status="pending")

        # ---- Step 6: 智能轮询 TOS URL ----
        print(f"\n[Step 6] 智能轮询 TOS URL 等待视频就绪")
        try:
            smart_poll_url(
                video_url=video_url,
                est_min=est_min, est_max=est_max,
                timeout=args.poll_timeout,
            )
        except TimeoutError as poll_exc:
            # 轮询超时不等于任务失败 —— 上游任务还在生成，留在 pending，下次运行会回扫
            print(f"\n[状态表] 本次轮询超时，任务保留为 pending，{_TASK_EXPIRY_HOURS}h 内再跑脚本会自动回查")
            print(f"[状态表] 手工检查：curl -sI {video_url}")
            result = {
                "success": False,
                "reason": "poll_timeout",
                "taskName": args.task_name,
                "uuid": upstream_uuid,
                "videoUrl": video_url,
                "error": str(poll_exc),
                "nextAction": f"在 {_TASK_EXPIRY_HOURS}h 内重新运行本脚本，或用 --list-tasks 查状态",
            }
            print(f"\n{'=' * 60}")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(2)

        total_time = int(time.time() - start_time)

        # 轮询成功，状态转为 ready
        _mark_task(upstream_uuid, status="ready", finished_at=time.time())

        # ---- 输出结果 ----
        result = {
            "success": True,
            "taskName": args.task_name,
            "uuid": upstream_uuid,
            "videoUrl": video_url,
            "totalSeconds": total_time,
            "audioDuration": round(audio_duration, 1),
            "estimatedRange": f"{est_min}~{est_max}s",
        }

        print(f"\n{'=' * 60}")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as exc:
        error_result = {
            "success": False,
            "error": str(exc),
            "taskName": args.task_name,
        }
        print(f"\n{'=' * 60}")
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)

    finally:
        if tts_tmp_file and Path(tts_tmp_file).exists():
            try:
                Path(tts_tmp_file).unlink()
                print(f"[清理] 已删除 TTS 临时文件: {tts_tmp_file}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
