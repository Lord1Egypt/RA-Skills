#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包 TTS - 火山引擎异步长文本语音合成脚本（V3 API）

基于最新 /api/v3/tts/submit 和 /api/v3/tts/query 接口实现。
支持异步长文本合成（单次最高 10 万字符）、情感设置、SSML、字幕时间戳等。
"""

import argparse
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path

import requests
from dotenv import load_dotenv

# ============================================================
# 常量定义
# ============================================================

# V3 接口地址
SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/tts/submit"
QUERY_URL = "https://openspeech.bytedance.com/api/v3/tts/query"

# Resource-Id 常量
RESOURCE_ID_V1 = "seed-tts-1.0"              # 豆包语音合成模型 1.0
RESOURCE_ID_V2 = "seed-tts-2.0"              # 豆包语音合成模型 2.0

# 默认音色（温柔妈妈 2.0，适合哄睡故事）
DEFAULT_VOICE_TYPE = "zh_female_wenroumama_uranus_bigtts"
DEFAULT_FORMAT = "mp3"

# 轮询配置
POLL_INITIAL_INTERVAL = 3
POLL_MAX_INTERVAL = 15
POLL_INTERVAL_STEP = 3
POLL_TIMEOUT = 1800

# V3 API 状态码
CODE_SUCCESS = 20000000
TASK_RUNNING = 1
TASK_SUCCESS = 2
TASK_FAILURE = 3


# ============================================================
# 环境变量加载
# ============================================================

def load_env_config():
    """按优先级加载环境变量：全局配置 → 项目目录 → 系统环境变量"""
    global_env = Path.home() / ".config" / "doubao-tts" / ".env"
    if global_env.exists():
        load_dotenv(global_env)
    local_env = Path.cwd() / ".env"
    if local_env.exists():
        load_dotenv(local_env, override=True)


def get_credentials():
    """获取火山引擎凭证"""
    app_id = os.getenv("VOLCENGINE_APP_ID")
    access_key = os.getenv("VOLCENGINE_ACCESS_TOKEN")

    if not app_id:
        print("❌ 错误: 未设置 VOLCENGINE_APP_ID", flush=True)
        sys.exit(1)
    if not access_key:
        print("❌ 错误: 未设置 VOLCENGINE_ACCESS_TOKEN", flush=True)
        sys.exit(1)

    return app_id, access_key


# ============================================================
# 文本预处理
# ============================================================

def strip_markdown(text):
    """将 Markdown 格式文本转换为纯文本，保留可朗读内容"""
    text = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=re.DOTALL)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    text = re.sub(r'~~(.+?)~~', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    text = re.sub(r'!\[.*?\]\(.+?\)', '', text)
    text = re.sub(r'^[\s]*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[\s]*\d+\.\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^---+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\*\*\*+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def prepare_text(input_text, is_file=False):
    """准备待合成的文本内容"""
    if is_file:
        file_path = Path(input_text)
        if not file_path.exists():
            print(f"❌ 错误: 文件不存在 — {file_path}", flush=True)
            sys.exit(1)
        raw_text = file_path.read_text(encoding="utf-8")
        if file_path.suffix.lower() in (".md", ".markdown"):
            text = strip_markdown(raw_text)
            print(f"📄 已加载 Markdown 文件: {file_path.name}", flush=True)
            print(f"   原始 {len(raw_text)} 字符 → 纯文本 {len(text)} 字符", flush=True)
        else:
            text = raw_text.strip()
            print(f"📄 已加载文件: {file_path.name} ({len(text)} 字符)", flush=True)
    else:
        text = input_text.strip()
        print(f"📝 输入文本: {len(text)} 字符", flush=True)

    if not text:
        print("❌ 错误: 输入文本为空", flush=True)
        sys.exit(1)
    if len(text) > 100000:
        print(f"⚠️  警告: 文本 ({len(text)} 字符) 超过 10 万限制，将截断", flush=True)
        text = text[:100000]
    return text


# ============================================================
# V3 API 调用
# ============================================================

def build_headers(app_id, access_key, resource_id):
    """构建 V3 API 请求头"""
    return {
        "Content-Type": "application/json",
        "X-Api-App-Id": app_id,
        "X-Api-Access-Key": access_key,
        "X-Api-Resource-Id": resource_id,
        "X-Api-Request-Id": str(uuid.uuid4()),
    }


def submit_task(app_id, access_key, text, args, resource_id):
    """提交异步长文本合成任务（V3 API）"""
    headers = build_headers(app_id, access_key, resource_id)

    # 构建请求体（V3 结构）
    unique_id = str(uuid.uuid4())
    audio_params = {
        "format": args.format,
        "sample_rate": args.sample_rate,
    }

    # 情感设置
    if args.emotion:
        audio_params["emotion"] = args.emotion
    if args.emotion_scale:
        audio_params["emotion_scale"] = args.emotion_scale

    # 语速和音量
    if args.speed != 0:
        audio_params["speech_rate"] = args.speed
    if args.volume != 0:
        audio_params["loudness_rate"] = args.volume

    # 时间戳/字幕
    if args.subtitle:
        audio_params["enable_timestamp"] = True

    req_params = {
        "speaker": args.voice_type,
        "audio_params": audio_params,
    }

    # SSML vs 纯文本（注意：模型 2.0 暂不支持 SSML）
    if args.ssml:
        if args.model == "2.0":
            print("❌ 错误: 豆包语音合成模型 2.0 暂不支持 SSML", flush=True)
            print("   请切换为 --model 1.0 或去掉 --ssml 参数", flush=True)
            sys.exit(1)
        req_params["ssml"] = text
        print("📊 文本类型: SSML", flush=True)
    else:
        req_params["text"] = text
        print("📊 文本类型: plain", flush=True)

    payload = {
        "user": {"uid": "openclaw_tts"},
        "unique_id": unique_id,
        "namespace": "BidirectionalTTS",
        "req_params": req_params,
    }

    print(f"🎙️  音色: {args.voice_type}", flush=True)
    print(f"📦 格式: {args.format} / {args.sample_rate}Hz", flush=True)
    print(f"🏷️  模型: 豆包语音合成 {args.model}", flush=True)
    print(f"🔑 Resource-Id: {resource_id}", flush=True)
    if args.subtitle:
        print("📋 字幕: 已启用", flush=True)
    if args.emotion:
        print(f"🎭 情感: {args.emotion} (强度: {args.emotion_scale})", flush=True)

    print(f"\n⏳ 正在提交合成任务...", flush=True)

    try:
        response = requests.post(SUBMIT_URL, headers=headers,
                                 data=json.dumps(payload), timeout=30)
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}", flush=True)
        sys.exit(1)

    try:
        result = response.json()
    except json.JSONDecodeError:
        print(f"❌ 响应解析失败 (status={response.status_code})", flush=True)
        print(f"   响应: {response.text[:500]}", flush=True)
        sys.exit(1)

    code = result.get("code")
    if code != CODE_SUCCESS:
        print(f"❌ 提交失败 (code={code}): {result.get('message', '')}", flush=True)
        print(f"   完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}", flush=True)
        sys.exit(1)

    task_id = result.get("data", {}).get("task_id", unique_id)
    text_len = result.get("data", {}).get("req_text_length", "?")
    print(f"✅ 任务提交成功", flush=True)
    print(f"   任务 ID: {task_id}", flush=True)
    print(f"   文本字数: {text_len}", flush=True)

    return task_id


def query_task(app_id, access_key, task_id, resource_id):
    """查询异步合成任务状态（V3 API，POST 请求）"""
    headers = build_headers(app_id, access_key, resource_id)
    payload = {"task_id": task_id}

    try:
        response = requests.post(QUERY_URL, headers=headers,
                                 data=json.dumps(payload), timeout=30)
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        print(f"⚠️  查询网络异常: {e}", flush=True)
        return None
    except json.JSONDecodeError:
        print(f"⚠️  查询响应解析失败 (status={response.status_code}): {response.text[:300]}", flush=True)
        return None


def poll_until_done(app_id, access_key, task_id, resource_id, timeout):
    """轮询查询任务状态，直到合成完成或超时"""
    elapsed = 0
    interval = POLL_INITIAL_INTERVAL

    print(f"\n⏳ 等待合成完成（最长 {timeout // 60} 分钟）...", flush=True)

    while elapsed < timeout:
        time.sleep(interval)
        elapsed += interval

        result = query_task(app_id, access_key, task_id, resource_id)

        if result is None:
            print(f"   [{elapsed}s] 查询失败，将重试...", flush=True)
            continue

        code = result.get("code")
        if code != CODE_SUCCESS:
            print(f"   [{elapsed}s] ❌ 服务端错误 (code={code}): {result.get('message', '')}", flush=True)
            print(f"   完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}", flush=True)
            print("\n   排查建议:", flush=True)
            print("   1. 检查 voice_type 是否已在控制台开通", flush=True)
            print("   2. 确认 X-Api-Resource-Id 与模型版本匹配", flush=True)
            print("   3. 确认 APP_ID 和 ACCESS_TOKEN 正确且未过期", flush=True)
            sys.exit(1)

        data = result.get("data", {})
        task_status = data.get("task_status")

        if task_status == TASK_SUCCESS:
            print(f"   [{elapsed}s] ✅ 合成完成!", flush=True)
            return data
        elif task_status == TASK_FAILURE:
            print(f"   [{elapsed}s] ❌ 合成失败", flush=True)
            print(f"   响应: {json.dumps(result, ensure_ascii=False, indent=2)}", flush=True)
            sys.exit(1)
        else:
            synth_len = data.get("synthesize_text_length", 0)
            req_len = data.get("req_text_length", "?")
            print(f"   [{elapsed}s] ⏳ 处理中 (已合成 {synth_len}/{req_len} 字符)", flush=True)

        interval = min(interval + POLL_INTERVAL_STEP, POLL_MAX_INTERVAL)

    print(f"❌ 等待超时（{timeout // 60} 分钟）", flush=True)
    print(f"   任务 ID: {task_id}", flush=True)
    sys.exit(1)


# ============================================================
# 文件下载与保存
# ============================================================

def download_audio(data, output_path):
    """从合成结果中下载音频文件"""
    audio_url = data.get("audio_url")
    if not audio_url:
        print("❌ 错误: 未找到音频下载链接", flush=True)
        print(f"   data: {json.dumps(data, ensure_ascii=False)[:500]}", flush=True)
        sys.exit(1)

    print(f"\n⬇️  正在下载音频...", flush=True)

    try:
        resp = requests.get(audio_url, timeout=300, stream=True)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ 音频下载失败: {e}", flush=True)
        sys.exit(1)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_size = 0
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
            total_size += len(chunk)

    size_mb = total_size / (1024 * 1024)
    print(f"✅ 音频已保存: {output_path} ({size_mb:.2f} MB)", flush=True)
    return output_path


def save_subtitle(data, output_path):
    """保存字幕数据（V3 API 返回 sentences 数组）"""
    sentences = data.get("sentences")
    if not sentences:
        return

    output_path = Path(output_path)
    base_name = output_path.stem

    # 保存原始 JSON
    json_path = output_path.parent / f"{base_name}.subtitle.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sentences, f, ensure_ascii=False, indent=2)
    print(f"📋 字幕 JSON 已保存: {json_path}", flush=True)

    # 转换为 SRT
    srt_lines = []
    for idx, sent in enumerate(sentences, start=1):
        text = sent.get("text", "").strip()
        if not text:
            continue
        start_s = sent.get("startTime", 0)
        end_s = sent.get("endTime", 0)
        srt_lines.append(str(idx))
        srt_lines.append(f"{_sec_to_srt(start_s)} --> {_sec_to_srt(end_s)}")
        srt_lines.append(text)
        srt_lines.append("")

    if srt_lines:
        srt_path = output_path.parent / f"{base_name}.srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(srt_lines))
        print(f"📋 字幕 SRT 已保存: {srt_path}", flush=True)


def _sec_to_srt(seconds):
    """秒转 SRT 时间格式 HH:MM:SS,mmm"""
    ms = int(seconds * 1000)
    h = ms // 3600000
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    mil = ms % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{mil:03d}"


# ============================================================
# 主流程
# ============================================================

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="豆包 TTS - 火山引擎异步长文本语音合成 (V3 API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s "你好，这是一段测试文本"
  %(prog)s story.md --voice-type BV700_streaming
  %(prog)s story.md --subtitle --emotion happy --output story.mp3

推荐音色 (模型 2.0):
  zh_female_wenroumama_uranus_bigtts       温柔妈妈（默认，适合哄睡）
  zh_female_shaoergushi_uranus_bigtts      少儿故事
  zh_female_cancan_uranus_bigtts           知性灿灿
  zh_female_xiaoxue_uranus_bigtts          儿童绘本
  zh_female_vv_uranus_bigtts               Vivi（多语种）
        """,
    )

    parser.add_argument("input", help="待合成的文本，或文件路径（.md/.txt）")
    parser.add_argument("--voice-type", "-v", default=DEFAULT_VOICE_TYPE,
                        help=f"音色 ID（默认: {DEFAULT_VOICE_TYPE}）")
    parser.add_argument("--format", "-f", default=DEFAULT_FORMAT,
                        choices=["mp3", "wav", "pcm", "ogg_opus"],
                        help=f"音频格式（默认: {DEFAULT_FORMAT}）")
    parser.add_argument("--sample-rate", type=int, default=24000,
                        choices=[8000, 16000, 22050, 24000, 32000, 44100, 48000],
                        help="采样率（默认: 24000）")
    parser.add_argument("--output", "-o", default=None, help="输出文件路径")
    parser.add_argument("--ssml", action="store_true", help="文本格式为 SSML")
    parser.add_argument("--emotion", default=None, help="情感设置，如 happy/sad/angry")
    parser.add_argument("--emotion-scale", type=int, default=4, choices=range(1, 6),
                        help="情绪强度 1~5（默认: 4）")
    parser.add_argument("--subtitle", action="store_true", help="启用字幕时间戳")
    parser.add_argument("--speed", type=int, default=0,
                        help="语速 [-50,100]，100=2x，-50=0.5x（默认: 0）")
    parser.add_argument("--volume", type=int, default=0,
                        help="音量 [-50,100]，100=2x，-50=0.5x（默认: 0）")
    parser.add_argument("--model", default="2.0", choices=["1.0", "2.0"],
                        help="模型版本（默认: 2.0）")
    parser.add_argument("--resource-id", default=None,
                        help="自定义 X-Api-Resource-Id（覆盖 --model 的默认值）")
    parser.add_argument("--timeout", type=int, default=POLL_TIMEOUT,
                        help=f"最长等待秒数（默认: {POLL_TIMEOUT}）")
    return parser.parse_args()


def determine_output_path(args):
    """确定输出文件路径"""
    if args.output:
        return args.output
    input_path = Path(args.input)
    if input_path.is_file():
        return str(input_path.parent / f"{input_path.stem}.{args.format}")
    return f"output.{args.format}"


def main():
    args = parse_args()
    load_env_config()
    app_id, access_key = get_credentials()

    input_path = Path(args.input)
    is_file = input_path.is_file()

    print("=" * 50, flush=True)
    print("🔥 豆包 TTS - 火山引擎语音合成 (V3 API)", flush=True)
    print("=" * 50, flush=True)

    text = prepare_text(args.input, is_file=is_file)
    output_path = determine_output_path(args)

    # 确定 Resource-Id：优先使用用户指定，否则按 model 版本选择
    if args.resource_id:
        resource_id = args.resource_id
    else:
        resource_id = RESOURCE_ID_V2 if args.model == "2.0" else RESOURCE_ID_V1

    task_id = submit_task(app_id, access_key, text, args, resource_id)
    data = poll_until_done(app_id, access_key, task_id, resource_id, args.timeout)

    download_audio(data, output_path)

    if args.subtitle:
        save_subtitle(data, output_path)

    synth_len = data.get("synthesize_text_length", "?")
    print(f"\n{'=' * 50}", flush=True)
    print(f"🎉 合成完成! 实际合成 {synth_len} 字符", flush=True)
    print(f"{'=' * 50}", flush=True)


if __name__ == "__main__":
    main()
