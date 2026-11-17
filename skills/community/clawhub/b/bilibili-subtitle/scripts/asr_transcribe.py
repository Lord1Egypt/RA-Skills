#!/usr/bin/env python3
"""
录音文件识别 + 说话人分离（基于腾讯云 ASR）
将音频转写为带说话人标注的对话稿，适用于访谈、播客、会议等多人对话场景。

用法:
  # 1) 转码（把任意音频转成腾讯云 16k 单声道要求的格式）
  python asr_transcribe.py transcode --input <音频> --output <out.mp3>

  # 2) 上传 + 识别 + 轮询（一步到位，输出结构化结果）
  python asr_transcribe.py run --input <16k单声道音频> --output-dir <目录>

  # 3) 把识别结果聚合成带身份标注的对话稿
  python asr_transcribe.py build --input-dir <目录> --speaker-map "0:鲁豫,1:张泉灵"

凭证读取优先级（均不硬编码，符合公开发布规范）:
  1. 环境变量 TENCENT_SECRET_ID / TENCENT_SECRET_KEY / TENCENT_COS_BUCKET / TENCENT_COS_REGION
  2. 配置文件 asr_config.json（与本脚本同目录，见 asr_config.example.json）

依赖: tencentcloud-sdk-python, cos-python-sdk-v5, ffmpeg(系统命令)

踩坑记录（已修）:
  - CreateRecTask 没有 ResponseFormat 参数，传了会报非法参数，已移除。
  - ResTextFormat 推荐用 1（句级+标点）。用 3（词级）会把 ResultDetail 炸成几千个
    词级碎片，且 Result 字段类型在 SDK 里不稳定（有时 str 有时 list）。
  - ResultDetail 在 SDK 里是 SentenceDetail 对象列表，不能直接 json.dump / f.write，
    必须用每个对象的 _serialize() 方法转成 dict 再序列化。
"""
import os
import sys
import json
import time
import argparse
import subprocess
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def load_config():
    """读取凭证配置：环境变量优先，其次同目录 asr_config.json"""
    cfg = {
        "secret_id": os.environ.get("TENCENT_SECRET_ID", ""),
        "secret_key": os.environ.get("TENCENT_SECRET_KEY", ""),
        "bucket": os.environ.get("TENCENT_COS_BUCKET", ""),
        "region": os.environ.get("TENCENT_COS_REGION", "ap-shanghai"),
    }
    cfg_file = os.path.join(SCRIPT_DIR, "asr_config.json")
    if os.path.exists(cfg_file):
        with open(cfg_file, encoding="utf-8") as f:
            file_cfg = json.load(f)
        for k in cfg:
            if not cfg[k] and file_cfg.get(k):
                cfg[k] = file_cfg[k]
    return cfg


def check_config(cfg):
    missing = [k for k in ("secret_id", "secret_key", "bucket") if not cfg.get(k)]
    if missing:
        return {
            "ok": False,
            "error": "MISSING_CONFIG",
            "message": f"缺少配置: {', '.join(missing)}。请设置环境变量或填写 asr_config.json",
        }
    return None


def to_jsonable(v):
    """把 SDK 返回的 Result / ResultDetail 统一转成可序列化对象。
    - str 原样返回
    - list（SentenceDetail 对象）逐个 _serialize()
    - 其他对象尝试 _serialize() 或 __dict__
    """
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        out = []
        for item in v:
            if hasattr(item, "_serialize"):
                out.append(item._serialize())
            elif hasattr(item, "__dict__"):
                out.append(item.__dict__)
            else:
                out.append(str(item))
        return out
    if hasattr(v, "_serialize"):
        return v._serialize()
    if hasattr(v, "__dict__"):
        return v.__dict__
    return str(v)


# ==================== 转码 ====================

def transcode(input_path, output_path):
    """把任意音频转成腾讯云 16k_zh 引擎要求的 16kHz 单声道 mp3"""
    if not os.path.exists(input_path):
        return {"ok": False, "error": "FILE_NOT_FOUND", "message": f"文件不存在: {input_path}"}
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", input_path, "-ac", "1", "-ar", "16000",
             "-acodec", "libmp3lame", "-ab", "64k", output_path],
            check=True, capture_output=True,
        )
        size_mb = round(os.path.getsize(output_path) / 1024 / 1024, 2)
        return {"ok": True, "outputPath": output_path, "fileSizeMB": size_mb}
    except FileNotFoundError:
        return {"ok": False, "error": "NO_FFMPEG", "message": "未找到 ffmpeg，请先安装"}
    except subprocess.CalledProcessError as e:
        return {"ok": False, "error": "TRANSCODE_FAILED", "message": e.stderr.decode()[-500:]}


# ==================== 上传 COS ====================

def upload_to_cos(cfg, local_path, cos_key):
    from qcloud_cos import CosConfig, CosS3Client
    config = CosConfig(Region=cfg["region"], SecretId=cfg["secret_id"],
                       SecretKey=cfg["secret_key"], Scheme="https")
    client = CosS3Client(config)
    client.upload_file(Bucket=cfg["bucket"], LocalFilePath=local_path, Key=cos_key, EnableMD5=True)
    url = client.get_presigned_url(Method="GET", Bucket=cfg["bucket"], Key=cos_key, Expired=86400)
    return url


# ==================== 创建 ASR 任务 ====================

def create_asr_task(cfg, audio_url, speaker_number=0):
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.asr.v20190614 import asr_client, models

    cred = credential.Credential(cfg["secret_id"], cfg["secret_key"])
    hp = HttpProfile()
    hp.endpoint = "asr.tencentcloudapi.com"
    cp = ClientProfile()
    cp.httpProfile = hp
    client = asr_client.AsrClient(cred, cfg["region"], cp)

    req = models.CreateRecTaskRequest()
    req.EngineModelType = "16k_zh"       # 中文 16k 引擎
    req.ChannelNum = 1                    # 单声道
    req.SpeakerDiarization = 1           # 开启说话人分离
    req.SpeakerNumber = speaker_number   # 0=自动(16k不支持指定人数)
    req.SourceType = 0                    # 音频 URL
    req.Url = audio_url
    req.ResTextFormat = 1                # 句级 + 标点（说话人分离最友好，段数少且带 SpeakerId）
    req.FilterDirty = 0
    req.FilterModal = 0
    req.ConvertNumMode = 0

    resp = client.CreateRecTask(req)
    return resp.Data.TaskId, client, models


def poll_task(client, models, task_id, max_polls=120, interval=15):
    for i in range(max_polls):
        time.sleep(interval)
        req = models.DescribeTaskStatusRequest()
        req.TaskId = task_id
        resp = client.DescribeTaskStatus(req)
        status = resp.Data.StatusStr
        log(f"  [{i+1}/{max_polls}] 状态: {status}")
        if status == "success":
            return resp.Data
        if status == "failed":
            log(f"  任务失败: {getattr(resp.Data, 'ErrorMsg', '未知')}")
            return None
    return None


# ==================== 轮询完成后重新拉取（避免内存对象序列化问题） ====================

def fetch_result(cfg, task_id):
    """通过 task_id 重新拉取完整的 Result / ResultDetail（SDK 已反序列化为对象）"""
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.asr.v20190614 import asr_client, models

    cred = credential.Credential(cfg["secret_id"], cfg["secret_key"])
    hp = HttpProfile()
    hp.endpoint = "asr.tencentcloudapi.com"
    cp = ClientProfile()
    cp.httpProfile = hp
    client = asr_client.AsrClient(cred, cfg["region"], cp)
    req = models.DescribeTaskStatusRequest()
    req.TaskId = task_id
    resp = client.DescribeTaskStatus(req)
    return resp.Data


# ==================== 主流程 ====================

def cmd_run(input_path, output_dir, speaker_number):
    cfg = load_config()
    err = check_config(cfg)
    if err:
        print(json.dumps(err, ensure_ascii=False))
        return

    if not os.path.exists(input_path):
        print(json.dumps({"ok": False, "error": "FILE_NOT_FOUND",
                          "message": f"文件不存在: {input_path}"}, ensure_ascii=False))
        return

    os.makedirs(output_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(input_path))[0]
    cos_key = f"asr/{base}_{int(time.time())}.mp3"

    log("Step 1: 上传音频到 COS...")
    audio_url = upload_to_cos(cfg, input_path, cos_key)
    log("  上传完成")

    log("Step 2: 创建 ASR 识别任务（开启说话人分离）...")
    task_id, client, models = create_asr_task(cfg, audio_url, speaker_number)
    log(f"  TaskId: {task_id}")
    with open(os.path.join(output_dir, ".asr_task_id"), "w") as f:
        f.write(str(task_id))

    log("Step 3: 轮询任务状态（长音频约 3-5 分钟）...")
    data = poll_task(client, models, task_id)
    if not data:
        print(json.dumps({"ok": False, "error": "ASR_FAILED", "taskId": task_id,
                          "message": "识别任务未成功"}, ensure_ascii=False))
        return

    # 重新拉取一次，确保拿到完整对象（轮询返回的对象同样可序列化）
    data = fetch_result(cfg, task_id)

    log("Step 4: 保存结果...")
    result_text = to_jsonable(getattr(data, "Result", "")) or ""
    if isinstance(result_text, list):
        result_text = "\n".join(seg.get("FinalSentence", "") for seg in result_text if isinstance(seg, dict))
    result_detail = to_jsonable(getattr(data, "ResultDetail", "")) or []

    full = {"TaskId": task_id, "Result": result_text, "ResultDetail": result_detail}
    result_json = os.path.join(output_dir, "asr_result_full.json")
    with open(result_json, "w", encoding="utf-8") as f:
        json.dump(full, f, ensure_ascii=False, indent=2)
    with open(os.path.join(output_dir, "asr_result.txt"), "w", encoding="utf-8") as f:
        f.write(result_text if isinstance(result_text, str) else json.dumps(result_text, ensure_ascii=False))
    with open(os.path.join(output_dir, "asr_result_detail.json"), "w", encoding="utf-8") as f:
        json.dump(result_detail, f, ensure_ascii=False, indent=1)

    print(json.dumps({
        "ok": True, "taskId": task_id, "resultJson": result_json,
        "resultChars": len(result_text) if isinstance(result_text, str) else len(json.dumps(result_text)),
        "detailSegments": len(result_detail) if isinstance(result_detail, list) else 0,
    }, ensure_ascii=False))


# ==================== 救数据：凭 task_id 重新拉取 ====================

def cmd_rescue(output_dir):
    """当 run 的保存/解析逻辑出错（如 SDK 对象序列化失败）导致结果存空时，
    不要重跑识别（浪费额度+3~5分钟），直接凭 .asr_task_id 重新拉取结果。"""
    cfg = load_config()
    err = check_config(cfg)
    if err:
        print(json.dumps(err, ensure_ascii=False))
        return
    tid_path = os.path.join(output_dir, ".asr_task_id")
    if not os.path.exists(tid_path):
        print(json.dumps({"ok": False, "error": "NO_TASK_ID",
                          "message": f"找不到 {tid_path}，无法救援"}, ensure_ascii=False))
        return
    task_id = int(open(tid_path).read().strip())
    log(f"凭 TaskId={task_id} 重新拉取结果...")
    data = fetch_result(cfg, task_id)
    if not data or data.StatusStr != "success":
        print(json.dumps({"ok": False, "error": "FETCH_FAILED", "taskId": task_id,
                          "message": f"拉取失败，状态: {getattr(data, 'StatusStr', '未知')}"}, ensure_ascii=False))
        return

    result_text = to_jsonable(getattr(data, "Result", "")) or ""
    if isinstance(result_text, list):
        result_text = "\n".join(seg.get("FinalSentence", "") for seg in result_text if isinstance(seg, dict))
    result_detail = to_jsonable(getattr(data, "ResultDetail", "")) or []

    with open(os.path.join(output_dir, "asr_result_full.json"), "w", encoding="utf-8") as f:
        json.dump({"TaskId": task_id, "Result": result_text, "ResultDetail": result_detail},
                  f, ensure_ascii=False, indent=2)
    with open(os.path.join(output_dir, "asr_result.txt"), "w", encoding="utf-8") as f:
        f.write(result_text if isinstance(result_text, str) else json.dumps(result_text, ensure_ascii=False))
    with open(os.path.join(output_dir, "asr_result_detail.json"), "w", encoding="utf-8") as f:
        json.dump(result_detail, f, ensure_ascii=False, indent=1)
    print(json.dumps({"ok": True, "taskId": task_id,
                      "detailSegments": len(result_detail) if isinstance(result_detail, list) else 0,
                      "message": "救援成功，可继续执行 build"}, ensure_ascii=False))


# ==================== 聚合对话稿 ====================

def fmt_time(ms):
    ms = int(ms or 0)
    s = ms // 1000
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:02d}"


def parse_speaker_map(s):
    """解析 "0:鲁豫,1:张泉灵" -> {0:'鲁豫',1:'张泉灵'}"""
    if not s:
        return {}
    m = {}
    for pair in s.split(","):
        k, v = pair.split(":", 1)
        m[int(k.strip())] = v.strip()
    return m


def cmd_build(input_dir, speaker_map_str, out_name="dialogue"):
    detail_path = os.path.join(input_dir, "asr_result_detail.json")
    if not os.path.exists(detail_path):
        print(json.dumps({"ok": False, "error": "NO_DETAIL",
                          "message": f"找不到 {detail_path}，请先执行 run"}, ensure_ascii=False))
        return
    segs = json.load(open(detail_path, encoding="utf-8"))
    sp_map = parse_speaker_map(speaker_map_str)

    turns = []
    cur_sid = None
    cur_start = None
    cur_end = None
    parts = []
    for s in segs:
        sid = s.get("SpeakerId")
        txt = (s.get("FinalSentence") or s.get("SliceSentence") or "").strip()
        st = s.get("StartMs") or 0
        en = s.get("EndMs") or 0
        if sid != cur_sid:
            if cur_sid is not None and parts:
                turns.append((cur_sid, cur_start, cur_end, "".join(parts)))
            cur_sid = sid
            cur_start = st
            cur_end = en
            parts = [txt] if txt else []
        else:
            cur_end = en
            if txt:
                parts.append(txt)
    if cur_sid is not None and parts:
        turns.append((cur_sid, cur_start, cur_end, "".join(parts)))

    out_txt = os.path.join(input_dir, f"{out_name}.txt")
    out_html = os.path.join(input_dir, f"{out_name}.html")
    with open(out_txt, "w", encoding="utf-8") as f:
        for sid, st, en, txt in turns:
            name = sp_map.get(sid, f"Speaker{sid}")
            f.write(f"【{name}】 ({fmt_time(st)})\n{txt}\n\n")

    color_map = {0: "#c0392b", 1: "#2563eb", 2: "#16a34a"}
    html_parts = [f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>对话稿</title>
<style>
body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;max-width:760px;margin:0 auto;padding:24px;line-height:1.8;background:#fafafa;color:#222}}
.turn{{margin:14px 0;padding:12px 16px;border-radius:10px;background:#fff;border-left:4px solid #ccc}}
.turn .name{{font-weight:700;font-size:15px}}
.turn .time{{color:#aaa;font-size:12px;margin-left:8px}}
.turn .text{{margin-top:6px}}
</style></head><body>
<div class="sub">腾讯云 ASR 说话人分离 · 共 {len(turns)} 轮</div>
"""]
    for sid, st, en, txt in turns:
        name = sp_map.get(sid, f"Speaker{sid}")
        color = color_map.get(sid, "#666")
        html_parts.append(
            f'<div class="turn" style="border-left-color:{color}">'
            f'<span class="name" style="color:{color}">{name}</span>'
            f'<span class="time">{fmt_time(st)}</span>'
            f'<div class="text">{txt}</div></div>'
        )
    html_parts.append("</body></html>")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))

    c = Counter(); w = Counter()
    for sid, st, en, txt in turns:
        c[sid] += 1; w[sid] += len(txt)
    summary = {sp_map.get(sid, f"Speaker{sid}"): {"turns": c[sid], "chars": w[sid]} for sid in c}
    print(json.dumps({"ok": True, "txt": out_txt, "html": out_html,
                      "turns": len(turns), "summary": summary}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="录音文件识别 + 说话人分离")
    sub = parser.add_subparsers(dest="command")

    tc = sub.add_parser("transcode", help="转码为 16k 单声道 mp3")
    tc.add_argument("--input", required=True)
    tc.add_argument("--output", required=True)

    rn = sub.add_parser("run", help="上传+识别+轮询")
    rn.add_argument("--input", required=True, help="16k 单声道音频路径")
    rn.add_argument("--output-dir", required=True)
    rn.add_argument("--speaker-number", type=int, default=0, help="说话人数，0=自动")

    bd = sub.add_parser("build", help="聚合对话稿")
    bd.add_argument("--input-dir", required=True, help="含 asr_result_detail.json 的目录")
    bd.add_argument("--speaker-map", default="", help="说话人映射，如 0:鲁豫,1:张泉灵")
    bd.add_argument("--out-name", default="dialogue")

    rs = sub.add_parser("rescue", help="凭 .asr_task_id 重新拉取结果（run 保存失败时救数据）")
    rs.add_argument("--output-dir", required=True, help="含 .asr_task_id 的目录")

    args = parser.parse_args()
    if args.command == "transcode":
        print(json.dumps(transcode(args.input, args.output), ensure_ascii=False))
    elif args.command == "run":
        cmd_run(args.input, args.output_dir, args.speaker_number)
    elif args.command == "build":
        cmd_build(args.input_dir, args.speaker_map, args.out_name)
    elif args.command == "rescue":
        cmd_rescue(args.output_dir)
    else:
        parser.print_help()
