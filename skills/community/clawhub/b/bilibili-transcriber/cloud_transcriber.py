"""
阿里云百炼 Paraformer 云端语音转写模块
上传本地音频 → 获取临时 oss:// URL → Paraformer 异步转写 → 返回带时间戳的结果

优势：比本地 whisper 快 10-20 倍，不依赖 GPU，方言识别更准
依赖：pip install dashscope requests
"""

import os
import time
import json
import requests
from pathlib import Path
from typing import Optional, List, Dict


# 支持的音频格式
SUPPORTED_FORMATS = {
    ".aac", ".amr", ".avi", ".flac", ".flv", ".m4a",
    ".mkv", ".mov", ".mp3", ".mp4", ".mpeg", ".ogg",
    ".opus", ".wav", ".webm", ".wma", ".wmv"
}


def _get_api_key() -> str:
    """获取 API Key（优先 DASHSCOPE_API_KEY，其次 OPENAI_API_KEY）"""
    key = os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError(
            "未找到 API Key，请设置环境变量 DASHSCOPE_API_KEY 或 OPENAI_API_KEY\n"
            "例如: export DASHSCOPE_API_KEY=sk-xxxxxxxx"
        )
    return key


def upload_audio_to_dashscope(
    file_path: str,
    api_key: Optional[str] = None,
    model: str = "paraformer-v2"
) -> str:
    """
    上传本地音频文件到阿里云百炼临时存储，获取 oss:// URL

    Args:
        file_path: 本地音频文件路径
        api_key: 百炼 API Key
        model: 模型名称（用于绑定文件访问权限）

    Returns:
        oss:// 格式的临时 URL（有效期 48 小时）
    """
    api_key = api_key or _get_api_key()

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"音频文件不存在: {file_path}")

    suffix = Path(file_path).suffix.lower()
    if suffix not in SUPPORTED_FORMATS:
        raise ValueError(f"不支持的音频格式: {suffix}，支持: {', '.join(sorted(SUPPORTED_FORMATS))}")

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(f"[CloudASR] 上传音频: {Path(file_path).name} ({file_size_mb:.1f} MB)")

    # 步骤 1: 获取上传凭证
    policy_url = "https://dashscope.aliyuncs.com/api/v1/uploads"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    params = {
        "action": "getPolicy",
        "model": model
    }

    resp = requests.get(policy_url, headers=headers, params=params, timeout=30)
    if resp.status_code != 200:
        raise Exception(f"获取上传凭证失败 (HTTP {resp.status_code}): {resp.text}")

    policy_data = resp.json().get("data", {})
    if not policy_data:
        raise Exception(f"上传凭证为空: {resp.json()}")

    # 步骤 2: 上传文件到 OSS
    file_name = Path(file_path).name
    key = f"{policy_data['upload_dir']}/{file_name}"

    with open(file_path, 'rb') as f:
        files = {
            'OSSAccessKeyId': (None, policy_data['oss_access_key_id']),
            'Signature': (None, policy_data['signature']),
            'policy': (None, policy_data['policy']),
            'x-oss-object-acl': (None, policy_data['x_oss_object_acl']),
            'x-oss-forbid-overwrite': (None, policy_data['x_oss_forbid_overwrite']),
            'key': (None, key),
            'success_action_status': (None, '200'),
            'file': (file_name, f)
        }

        upload_resp = requests.post(policy_data['upload_host'], files=files, timeout=120)
        if upload_resp.status_code != 200:
            raise Exception(f"文件上传失败 (HTTP {upload_resp.status_code}): {upload_resp.text}")

    oss_url = f"oss://{key}"
    print(f"[CloudASR] 上传成功: {oss_url}")
    return oss_url


def cloud_transcribe(
    file_path: str,
    api_key: Optional[str] = None,
    model: str = "paraformer-v2",
    language_hints: Optional[List[str]] = None,
    poll_interval: float = 1.0,
    max_wait: int = 300
) -> List[Dict]:
    """
    使用阿里云百炼 Paraformer 进行云端语音转写

    Args:
        file_path: 本地音频文件路径
        api_key: 百炼 API Key
        model: ASR 模型名称（paraformer-v2, paraformer-v2-8k 等）
        language_hints: 语言提示（如 ["zh", "en"]）
        poll_interval: 轮询间隔（秒）
        max_wait: 最大等待时间（秒）

    Returns:
        带时间戳的片段列表: [{"start": float, "end": float, "text": str}, ...]
    """
    api_key = api_key or _get_api_key()
    total_start = time.time()

    # 步骤 1: 上传音频
    t0 = time.time()
    oss_url = upload_audio_to_dashscope(file_path, api_key, model)
    upload_time = time.time() - t0

    # 步骤 2: 提交转写任务
    t1 = time.time()
    submit_url = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
        "X-DashScope-OssResourceResolve": "enable"
    }

    request_body = {
        "model": model,
        "input": {
            "file_urls": [oss_url]
        },
        "parameters": {
            "language_hints": language_hints or ["zh"]
        }
    }

    print(f"[CloudASR] 提交转写任务 (模型: {model})...")
    resp = requests.post(submit_url, headers=headers, json=request_body, timeout=30)

    if resp.status_code != 200:
        raise Exception(f"提交任务失败 (HTTP {resp.status_code}): {resp.text}")

    resp_data = resp.json()
    task_id = resp_data.get("output", {}).get("task_id")
    if not task_id:
        raise Exception(f"未获取到 task_id: {resp_data}")

    submit_time = time.time() - t1
    print(f"[CloudASR] 任务已提交: {task_id}")

    # 步骤 3: 轮询等待结果
    t2 = time.time()
    query_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    query_headers = {
        "Authorization": f"Bearer {api_key}"
    }

    elapsed = 0
    while elapsed < max_wait:
        time.sleep(poll_interval)
        elapsed = time.time() - t2

        query_resp = requests.get(query_url, headers=query_headers, timeout=30)
        if query_resp.status_code != 200:
            print(f"[CloudASR] 查询失败，重试中...")
            continue

        query_data = query_resp.json()
        status = query_data.get("output", {}).get("task_status", "UNKNOWN")

        if status == "SUCCEEDED":
            wait_time = time.time() - t2
            print(f"[CloudASR] 转写完成! 等待耗时: {wait_time:.1f}s")
            break
        elif status == "FAILED":
            error_msg = query_data.get("output", {}).get("message", "未知错误")
            raise Exception(f"转写失败: {error_msg}")
        elif status == "PENDING" or status == "RUNNING":
            if int(elapsed) % 5 == 0 and elapsed > 1:
                print(f"[CloudASR] 转写中... ({elapsed:.0f}s)")
    else:
        raise TimeoutError(f"转写超时（{max_wait}秒）")

    # 步骤 4: 解析结果
    t3 = time.time()
    results_list = query_data.get("output", {}).get("results", [])
    if not results_list:
        raise Exception("未获取到转写结果")

    # 获取转写结果 URL
    transcription_url = results_list[0].get("transcription_url")
    if not transcription_url:
        raise Exception("未获取到 transcription_url")

    # 下载转写结果
    trans_resp = requests.get(transcription_url, timeout=30)
    if trans_resp.status_code != 200:
        raise Exception(f"下载转写结果失败 (HTTP {trans_resp.status_code})")

    trans_data = trans_resp.json()

    # 解析带时间戳的结果
    segments = []
    transcripts = trans_data.get("transcripts", [])

    for transcript in transcripts:
        # 逐句解析
        sentences = transcript.get("sentences", [])
        for sentence in sentences:
            start_ms = sentence.get("begin_time", 0)
            end_ms = sentence.get("end_time", 0)
            text = sentence.get("text", "").strip()
            if text:
                segments.append({
                    "start": start_ms / 1000.0,
                    "end": end_ms / 1000.0,
                    "text": text
                })

        # 如果没有 sentences，尝试用 paragraphs
        if not sentences:
            paragraphs = transcript.get("paragraphs", [])
            for para in paragraphs:
                for sentence in para.get("sentences", []):
                    start_ms = sentence.get("begin_time", 0)
                    end_ms = sentence.get("end_time", 0)
                    text = sentence.get("text", "").strip()
                    if text:
                        segments.append({
                            "start": start_ms / 1000.0,
                            "end": end_ms / 1000.0,
                            "text": text
                        })

    # 如果还是没有分句结果，提取纯文本
    if not segments:
        full_text = ""
        for transcript in transcripts:
            full_text += transcript.get("text", "")
        if full_text:
            segments.append({
                "start": 0.0,
                "end": 0.0,
                "text": full_text.strip()
            })

    parse_time = time.time() - t3
    total_time = time.time() - total_start

    print(f"\n[CloudASR] === 性能统计 ===")
    print(f"  上传耗时:   {upload_time:.1f}s")
    print(f"  提交耗时:   {submit_time:.1f}s")
    print(f"  转写等待:   {wait_time:.1f}s")
    print(f"  解析耗时:   {parse_time:.1f}s")
    print(f"  总耗时:     {total_time:.1f}s")
    print(f"  片段数量:   {len(segments)}")

    return segments


def cloud_transcribe_from_url(
    audio_url: str,
    api_key: Optional[str] = None,
    model: str = "paraformer-v2",
    language_hints: Optional[List[str]] = None,
    poll_interval: float = 1.0,
    max_wait: int = 300
) -> List[Dict]:
    """
    直接从公网 URL 进行云端转写（无需上传）

    Args:
        audio_url: 公网可访问的音频 URL
        api_key: 百炼 API Key
        model: ASR 模型名称
        language_hints: 语言提示
        poll_interval: 轮询间隔
        max_wait: 最大等待时间

    Returns:
        带时间戳的片段列表
    """
    api_key = api_key or _get_api_key()
    total_start = time.time()

    # 提交转写任务
    submit_url = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"
    }

    request_body = {
        "model": model,
        "input": {
            "file_urls": [audio_url]
        },
        "parameters": {
            "language_hints": language_hints or ["zh"]
        }
    }

    print(f"[CloudASR] 提交转写任务 (URL模式, 模型: {model})...")
    resp = requests.post(submit_url, headers=headers, json=request_body, timeout=30)

    if resp.status_code != 200:
        raise Exception(f"提交任务失败 (HTTP {resp.status_code}): {resp.text}")

    resp_data = resp.json()
    task_id = resp_data.get("output", {}).get("task_id")
    if not task_id:
        raise Exception(f"未获取到 task_id: {resp_data}")

    print(f"[CloudASR] 任务已提交: {task_id}")

    # 轮询等待
    query_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    query_headers = {"Authorization": f"Bearer {api_key}"}

    t_wait = time.time()
    elapsed = 0
    while elapsed < max_wait:
        time.sleep(poll_interval)
        elapsed = time.time() - t_wait

        query_resp = requests.get(query_url, headers=query_headers, timeout=30)
        if query_resp.status_code != 200:
            continue

        query_data = query_resp.json()
        status = query_data.get("output", {}).get("task_status", "UNKNOWN")

        if status == "SUCCEEDED":
            print(f"[CloudASR] 转写完成! 耗时: {elapsed:.1f}s")
            break
        elif status == "FAILED":
            error_msg = query_data.get("output", {}).get("message", "未知错误")
            raise Exception(f"转写失败: {error_msg}")
    else:
        raise TimeoutError(f"转写超时（{max_wait}秒）")

    # 解析结果（复用相同逻辑）
    results_list = query_data.get("output", {}).get("results", [])
    transcription_url = results_list[0].get("transcription_url") if results_list else None
    if not transcription_url:
        raise Exception("未获取到 transcription_url")

    trans_resp = requests.get(transcription_url, timeout=30)
    trans_data = trans_resp.json()

    segments = []
    for transcript in trans_data.get("transcripts", []):
        sentences = transcript.get("sentences", [])
        for sentence in sentences:
            text = sentence.get("text", "").strip()
            if text:
                segments.append({
                    "start": sentence.get("begin_time", 0) / 1000.0,
                    "end": sentence.get("end_time", 0) / 1000.0,
                    "text": text
                })
        if not sentences:
            for para in transcript.get("paragraphs", []):
                for sentence in para.get("sentences", []):
                    text = sentence.get("text", "").strip()
                    if text:
                        segments.append({
                            "start": sentence.get("begin_time", 0) / 1000.0,
                            "end": sentence.get("end_time", 0) / 1000.0,
                            "text": text
                        })

    total_time = time.time() - total_start
    print(f"[CloudASR] 总耗时: {total_time:.1f}s, 片段数: {len(segments)}")

    return segments


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python cloud_transcriber.py <音频文件路径或URL>")
        print("示例: python cloud_transcriber.py audio.m4a")
        sys.exit(1)

    target = sys.argv[1]

    if target.startswith("http://") or target.startswith("https://"):
        results = cloud_transcribe_from_url(target)
    else:
        results = cloud_transcribe(target)

    for seg in results:
        start_min = int(seg['start'] // 60)
        start_sec = int(seg['start'] % 60)
        print(f"[{start_min:02d}:{start_sec:02d}] {seg['text']}")
