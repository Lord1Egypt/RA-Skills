"""
BenchClaw 服务端 API 模块。

负责与评测服务端的所有 HTTP 交互：
  - fetch_questions      从服务端拉取题目列表
  - upload_results_from_dict  将 summary dict 上传到服务端
  - upload_results       从文件读取后上传（兼容 CLI 用法）
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

from config import (
    CLIENT_VERSION,
    DEFAULT_API_URL,
    DEFAULT_SUBMIT_API_URL,
    UPLOAD_STDOUT_TRUNCATE_LENGTH,
    UPLOAD_STDERR_TRUNCATE_LENGTH,
)
from crypto import hybrid_encrypt_json

# 分类得分映射 → s1~s5：能力、配置、安全、硬件、权限（与官网/榜单列一致）
CATEGORY_ORDER = ["capability", "config", "security", "hardware", "permission"]

# 服务端要求固定 25 个 b/r 字段
TOTAL_QUESTIONS = 25


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

_SANITIZE_RULES: list[tuple[re.Pattern[str], str]] = [
    # Anthropic Claude API key（必须在 OpenAI sk- 规则之前）
    (re.compile(r"sk-ant-[a-zA-Z0-9\-]{20,}"), "sk-ant-***"),
    # OpenAI API key
    (re.compile(r"sk-[a-zA-Z0-9]{20,}"), "sk-***"),
    # Google Gemini API key
    (re.compile(r"AIza[a-zA-Z0-9_\-]{35}"), "AIza***"),
    # AWS Access Key ID
    (re.compile(r"AKIA[A-Z0-9]{16}"), "AKIA***"),
    # GitHub Personal Access Token
    (re.compile(r"ghp_[a-zA-Z0-9]{36}"), "ghp_***"),
    # ClaWHub token
    (re.compile(r"clh_[a-zA-Z0-9]+"), "clh_***"),
    # Feishu open_id
    (re.compile(r"ou_[a-f0-9]{32}"), "ou_***"),
    # Slack token
    (re.compile(r"xox[bpsa]-[a-zA-Z0-9\-]+"), "xox-***"),
    # 本地路径 /home/...
    (re.compile(r"/home/[^\s\"']+"), "/home/***"),
    # 本地路径 /root/...
    (re.compile(r"/root/[^\s\"']+"), "/root/***"),
    # 邮箱地址
    (re.compile(r"\b[\w.\+\-]+@[\w.\-]+\.\w+\b"), "***@***"),
]


def _sanitize_output(text: str) -> str:
    """对 stdout/stderr 文本进行正则脱敏，替换已知的敏感信息模式。"""
    for pattern, replacement in _SANITIZE_RULES:
        text = pattern.sub(replacement, text)
    return text


def _dump_to_temp(data: Any, filename: str) -> None:
    """将数据以 JSON 格式写入 tests 目录，便于调试查看。"""
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "temp")
    os.makedirs(temp_dir, exist_ok=True)
    path = os.path.join(temp_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _iso_time(ts: float) -> str:
    """将 Unix 时间戳（秒或毫秒）转为 ISO 8601 UTC 字符串。"""
    # 如果时间戳大于 1e10，认为是毫秒，转换为秒
    if ts > 1e10:
        ts = ts / 1000.0
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def _post_json(
    url: str,
    body: dict[str, Any],
    headers: dict[str, str] | None = None,
    timeout: int = 30,
    encrypt: bool = False,
) -> dict[str, Any]:
    """
    通用 POST JSON 请求，返回解析后的响应 dict。

    Parameters
    ----------
    encrypt : bool
        True 时 RSA+AES 混合加密为 {"key","gpv"}；响应 data 为明文 JSON（v2.9）。
    """
    if encrypt:
        key_b64, gpv, _aes = hybrid_encrypt_json(body)
        payload = json.dumps({"key": key_b64, "gpv": gpv}, ensure_ascii=False).encode("utf-8")
    else:
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)

    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    return json.loads(raw)


# ─────────────────────────────────────────────
# 下载题目
# ─────────────────────────────────────────────

def fetch_questions(
    bench_session_id: str,
    primary_model: str,
    api_url: str = DEFAULT_API_URL,
    openclaw_root: str = "",
) -> dict[str, Any]:
    """
    从服务端 API 获取题目列表。

    Returns
    -------
    dict：
      - questions      : list[dict]
      - session_id     : str
      - hash           : str
      - model_cost     : dict | None
    """
    out = _post_json(
        api_url,
        body={"model_name": primary_model, "client_version": CLIENT_VERSION},
        headers={"X-Bench-Session-Id": bench_session_id},
        encrypt=True,
    )

    if not out.get("success"):
        raise RuntimeError(f"API returned success=false: {out.get('message', out)}")

    data = out.get("data")
    if not isinstance(data, dict):
        raise RuntimeError(f"API data 格式错误：期望题目包 JSON 对象，实际 {type(data).__name__}")

    # 仅供调试使用：将解密后的原始数据写入 tests 目录，便于调试查看
    # _dump_to_temp(data, "fetch_questions_data.json")

    questions = data.get("questions")
    if not isinstance(questions, list):
        raise RuntimeError("API data.questions is not a list")

    return {
        "questions": questions,
        "session_id": data.get("session_id", ""),
        "hash": data.get("hash", ""),
        "model_cost": data.get("model_cost"),
    }


# ─────────────────────────────────────────────
# 上传结果
# ─────────────────────────────────────────────

def _build_upload_payload(data: dict[str, Any]) -> dict[str, Any]:
    """将 summary dict 转换为服务端上传格式。"""
    results: list[dict[str, Any]] = data.get("results", [])
    _stats = data.get("stats") or {}
    cat_stats: dict[str, dict] = _stats.get("category_stats") or data.get("category_stats", {})

    # 构建 env_info（设备环境信息，二级 JSON）
    _sys = data.get("sys_info") or {}
    import platform as _platform
    env_info: dict[str, Any] = {
        "cpu_cores":      _sys.get("cpu_cores"),
        "memory_gb":      _sys.get("ram_total_gb"),
        "os":             _platform.system().lower(),
        "python_version": _platform.python_version(),
    }
    # 去掉 None 值
    env_info = {k: v for k, v in env_info.items() if v is not None}

    payload: dict[str, Any] = {
        "session_id":     data.get("api_session_id") or data.get("session_id", ""),
        "hash":           data.get("api_hash") or data.get("hash", ""),
        "client_version": CLIENT_VERSION,
        "model_name":     data.get("model_name", ""),
        "total_score":    sum(r.get("score", 0) for r in results),
        "openclaw_name":  data.get("agent_name", ""),
        "openclaw_version": data.get("openclaw_version", ""),
        "host_type":      _sys.get("host_type", ""),
        "env_info":       env_info,
    }

    # s1~s5：按 CATEGORY_ORDER 填入各分类总分
    for idx, cat in enumerate(CATEGORY_ORDER, start=1):
        payload[f"s{idx}"] = cat_stats.get(cat, {}).get("score", 0)

    # b1~b25：每题得分，实际结果按顺序填入，未执行的题目补 0
    for idx in range(1, TOTAL_QUESTIONS + 1):
        r = results[idx - 1] if idx <= len(results) else None
        payload[f"b{idx}"] = r.get("score", 0) if r else 0

    # r1~r25：每题运行详情，未执行的题目补空值
    now_ts = time.time()
    total_duration = sum(r.get("duration_sec") or 0 for r in results)
    cursor_ts = now_ts - total_duration

    for idx in range(1, TOTAL_QUESTIONS + 1):
        r = results[idx - 1] if idx <= len(results) else None
        if r is None:
            payload[f"r{idx}"] = {
                "start_time":         "",
                "end_time":           "",
                "total_tokens":       0,
                "input_tokens":       0,
                "output_tokens":      0,
                "cache_read_tokens":  0,
                "cache_write_tokens": 0,
                "returncode":         -1,
                "error":              "",
                "stdout":             "",
                "stderr":             "",
                "accuracy_score":     0,
                "real_accuracy_score": 0,
                "tps_score":          0,
            }
            continue

        duration = r.get("duration_sec") or 0
        start_ts = cursor_ts
        end_ts   = cursor_ts + duration
        cursor_ts = end_ts

        # stdout/output 取非空值（CLI 模式用 output，WS 模式用 stdout）
        stdout_val = (r.get("stdout") or "")
        # 截断超长文本，避免 payload 过大
        if len(stdout_val) > UPLOAD_STDOUT_TRUNCATE_LENGTH:
            stdout_val = stdout_val[:UPLOAD_STDOUT_TRUNCATE_LENGTH] + "…(truncated)"
        stdout_val = _sanitize_output(stdout_val)

        stderr_val = (r.get("stderr") or "")
        if len(stderr_val) > UPLOAD_STDERR_TRUNCATE_LENGTH:
            stderr_val = stderr_val[:UPLOAD_STDERR_TRUNCATE_LENGTH] + "…(truncated)"
        stderr_val = _sanitize_output(stderr_val)

        payload[f"r{idx}"] = {
            "start_time":         _iso_time(r.get("start_time")) if r.get("start_time") else "",
            "end_time":           _iso_time(r.get("end_time"))   if r.get("end_time")   else "",
            "total_tokens":       r.get("total_tokens") or 0,
            "input_tokens":       r.get("input_tokens") or 0,
            "output_tokens":      r.get("output_tokens") or 0,
            "cache_read_tokens":  r.get("cache_read_tokens") or 0,
            "cache_write_tokens": r.get("cache_write_tokens") or 0,
            "returncode":         r.get("returncode", -1),
            "error":              r.get("error") or "",
            "stdout":             stdout_val,
            "stderr":             stderr_val,
            "accuracy_score":     r.get("accuracy_score") or 0,
            "real_accuracy_score": r.get("real_accuracy_score") or 0,
            "tps_score":          r.get("tps_score") or 0,
        }

    return payload


# ─────────────────────────────────────────────
# 上传缓存（网络失败时本地暂存，下次启动重试）
# ─────────────────────────────────────────────

_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cache")


def _cache_dir() -> str:
    os.makedirs(_CACHE_DIR, exist_ok=True)
    return _CACHE_DIR


def _save_pending_upload(body: bytes, bench_session_id: str, upload_url: str) -> str:
    """
    将上传失败的 body 连同元信息序列化写入 cache 目录。
    文件名格式：cache_<timestamp_ms>.dat
    返回写入的文件路径。
    """
    ts = int(time.time() * 1000)
    filename = f"cache_{ts}.dat"
    path = os.path.join(_cache_dir(), filename)
    record = {
        "upload_url": upload_url,
        "bench_session_id": bench_session_id,
        "body_hex": body.hex(),       # bytes 转 hex 字符串，便于 JSON 序列化
        "created_at": ts,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False)
    return path


def _do_post_body(body: bytes, bench_session_id: str, upload_url: str, timeout: int = 30) -> tuple[bool, str]:
    """发送已构建好的 body bytes，返回 (ok, msg)。"""
    req = urllib.request.Request(upload_url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("X-Bench-Session-Id", bench_session_id)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        out = json.loads(raw)
        if out.get("success"):
            return True, raw
        return False, out.get("message") or raw
    except urllib.error.HTTPError as e:
        body_err = e.read().decode("utf-8", errors="replace")
        return False, f"HTTP {e.code}: {body_err}"
    except Exception as e:
        return False, str(e)


def flush_pending_uploads() -> list[str]:
    """
    扫描 cache 目录，将所有未上报的 .dat 文件逐个重试上传。
    上传成功后删除对应文件；失败则保留留待下次重试。
    返回本次成功上传的文件路径列表。
    """
    cache = _cache_dir()
    dat_files = sorted(
        (f for f in os.listdir(cache) if f.startswith("cache_") and f.endswith(".dat")),
    )
    if not dat_files:
        return []

    succeeded: list[str] = []
    for filename in dat_files:
        path = os.path.join(cache, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                record = json.load(f)
            body = bytes.fromhex(record["body_hex"])
            bench_session_id = record.get("bench_session_id", "")
            upload_url = record.get("upload_url", DEFAULT_SUBMIT_API_URL)
        except Exception as e:
            # 文件损坏，跳过但不删除，避免误删
            print(f"[flush] 读取缓存文件失败 {filename}: {e}")
            continue

        ok, msg = _do_post_body(body, bench_session_id, upload_url)
        if ok:
            try:
                os.remove(path)
            except OSError:
                pass
            succeeded.append(path)
            print(f"[flush] 补报成功，已删除缓存: {filename}")
        else:
            print(f"[flush] 补报失败，保留缓存 {filename}: {msg}")

    return succeeded


def _parse_leaderboard(raw_response: str) -> dict[str, Any]:
    """
    从上传接口的原始响应中提取排行榜数据。

    期望响应格式：
      {"success": true, "data": {"percentiles": {"total": 91.8, "s1": 93.9, ...},
       "sample_size": 17, "leaderboard_url": "...", "note": "..."}}

    返回标准化后的排行榜 dict，解析失败时返回 {}。
    """
    try:
        out = json.loads(raw_response)
    except (json.JSONDecodeError, TypeError):
        return {}
    resp_data = out.get("data")
    if not isinstance(resp_data, dict):
        return {}
    percentiles = resp_data.get("percentiles")
    if not isinstance(percentiles, dict):
        return {}
    return {
        "percentiles":    percentiles,
        "sample_size":    resp_data.get("sample_size"),
        "leaderboard_url": resp_data.get("leaderboard_url", ""),
        "note":           percentiles.get("note") or resp_data.get("note", ""),
        "updated_at":     percentiles.get("updated_at", ""),
        "status":         percentiles.get("status", ""),
    }


def upload_results_from_dict(
    data: dict[str, Any],
    bench_session_id: str,
    hash: str,
    upload_url: str = DEFAULT_SUBMIT_API_URL,
) -> tuple[bool, str, dict[str, Any]]:
    """
    直接接受 summary dict，构建上传格式后 POST 到服务端。
    若因网络原因失败，自动将 body 缓存到 cache 目录，下次启动时补报。

    Returns
    -------
    (ok: bool, message: str, leaderboard: dict)
      leaderboard 结构示例：
        {
          "percentiles": {"total": 91.8, "s1": 93.9, "s2": 0.1, ...},
          "sample_size": 17,
          "leaderboard_url": "https://{BENCHCLAW_SITE_HOST}/leaderboard",  # 实际 URL 由服务端返回
          "note": "...",
        }
      上传失败时返回空 dict。
    """
    if not data.get("results"):
        return False, "results 列表为空，跳过上传", {}

    try:
        payload = _build_upload_payload(data)
    except Exception as e:
        return False, f"构建上传数据失败: {e}", {}

    key_b64, gpv, _aes = hybrid_encrypt_json(payload)
    body = json.dumps({"key": key_b64, "gpv": gpv}, ensure_ascii=False).encode("utf-8")

    ok, msg = _do_post_body(body, bench_session_id, upload_url)
    if ok:
        leaderboard = _parse_leaderboard(msg)
        return True, msg, leaderboard

    # 上报失败时，缓存数据
    cached_path = _save_pending_upload(body, bench_session_id, upload_url)
    return False, f"{msg}（已缓存至 {os.path.basename(cached_path)}，下次启动自动补报）", {}

def upload_results(
    results_path: str,
    bench_session_id: str,
    session_id: str,
    hash: str,
) -> tuple[bool, str, dict[str, Any]]:
    """
    从文件读取 results.json 后上传（兼容 CLI 用法）。
    """
    if not os.path.exists(results_path):
        return False, f"结果文件不存在: {results_path}", {}
    try:
        with open(results_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            data['api_session_id'] = session_id
            data['api_hash'] = hash
    except Exception as e:
        return False, f"读取结果文件失败: {e}", {}

    return upload_results_from_dict(data, bench_session_id, hash)


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────
from utils import get_bench_session_id

def test_upload():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "temp", "temp-results.json"
    )
    path = os.path.abspath(path)
    print(f"上传文件: {path}")

    # 下载题目
    try:
        bench_session_id = get_bench_session_id()
        fetch_result = fetch_questions(bench_session_id, "minimax-cn/MiniMax-M2.5")
        #questions = fetch_result["questions"]
        api_session_id = fetch_result["session_id"]
        api_hash = fetch_result["hash"]
        print("api_hash", api_hash)

        ok, msg, _ = upload_results(path, bench_session_id, api_session_id, api_hash)
        print("成功" if ok else "失败", ":", msg)
    except Exception as e:
        print(e)
        return


def test_sanitize():
    """对 _sanitize_output 的各条脱敏规则进行验证。"""
    cases = [
        # (描述, 输入, 期望包含的替换结果)
        ("Anthropic Claude API key", "token=sk-ant-abcdefghijklmnopqrst123456", "sk-ant-***"),
        ("OpenAI API key",           "key: sk-abcdefghijklmnopqrstu",            "sk-***"),
        ("Google Gemini API key",    "AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz12345678", "AIza***"),
        ("AWS Access Key ID",        "access_key=AKIAIOSFODNN7EXAMPLE",           "AKIA***"),
        ("GitHub PAT",               "ghp_" + "a" * 36,                           "ghp_***"),
        ("ClaWHub token",            "auth: clh_MySecretToken123",                "clh_***"),
        ("飞书 open_id",             "open_id: ou_" + "a1b2c3d4" * 4,             "ou_***"),
        ("Slack bot token",          "xoxb-123456789-abcdefghij",                 "xox-***"),
        ("Slack user token",         "xoxp-987654321-zyxwvutsrq",                 "xox-***"),
        ("本地路径 /home/",           "reading /home/user/.bashrc failed",         "/home/***"),
        ("本地路径 /root/",           "config at /root/.config/app.yaml",          "/root/***"),
        ("邮箱地址",                  "contact admin@example.com for help",        "***@***"),
        ("混合多条规则",
         "key=sk-abcdefghijklmnopqrstu path=/home/ci/.env email=foo@bar.com",
         None),  # None 表示只打印结果，不做单一断言
    ]

    passed = 0
    failed = 0
    for desc, text, expected in cases:
        result = _sanitize_output(text)
        if expected is None:
            print(f"  [INFO] {desc}")
            print(f"         输入  : {text}")
            print(f"         输出  : {result}")
            print()
            continue
        if expected in result and text != result:
            print(f"  [PASS] {desc}")
            print(f"         输入  : {text}")
            print(f"         输出  : {result}")
            passed += 1
        else:
            print(f"  [FAIL] {desc}")
            print(f"         输入  : {text}")
            print(f"         输出  : {result}")
            print(f"         期望含: {expected}")
            failed += 1
        print()

    print(f"结果: {passed} 通过, {failed} 失败")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sanitize":
        test_sanitize()
    else:
        test_upload()
