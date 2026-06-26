#!/usr/bin/env python3
"""
视频生成脚本 - 支持提交、查询、等待、自动下载
"""
import requests
import json
import sys
import os
import time

API_KEY = os.environ.get("AIPING_API_KEY", "")
API_BASE = "https://aiping.cn/api/v1"


def _get_api_key() -> str:
    key = os.environ.get("AIPING_API_KEY", API_KEY)
    if not key:
        raise EnvironmentError("请设置环境变量 AIPING_API_KEY")
    return key

def generate_video(model: str, prompt: str, seconds: int = 5, 
                   mode: str = "std", aspect_ratio: str = "16:9",
                   timeout: int = 30) -> dict:
    """提交视频生成任务"""
    payload = {
        "model": model,
        "prompt": prompt,
        "seconds": str(seconds),  # 必须是字符串
        "mode": mode,
        "aspect_ratio": aspect_ratio
    }
    
    resp = requests.post(
        f"{API_BASE}/videos",
        headers={
            "Authorization": f"Bearer {_get_api_key()}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=timeout
    )
    resp.raise_for_status()
    return resp.json()

def query_video(task_id: str, timeout: int = 30) -> dict:
    """查询视频生成状态"""
    resp = requests.get(
        f"{API_BASE}/videos/{task_id}",
        headers={
            "Authorization": f"Bearer {_get_api_key()}",
            "Content-Type": "application/json"
        },
        timeout=timeout
    )
    resp.raise_for_status()
    return resp.json()

def download_video(url: str) -> str:
    """下载视频到本地 /tmp/ 目录"""
    resp = requests.get(url, timeout=120, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }, stream=True)
    resp.raise_for_status()
    
    local_path = f"/tmp/aiping_video_{os.getpid()}_{int(time.time())}.mp4"
    with open(local_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return local_path

def wait_for_video(task_id: str, poll_interval: int = 15, max_wait: int = 300,
                   auto_download: bool = True) -> dict:
    """等待视频生成完成，可选自动下载"""
    start = time.time()
    while time.time() - start < max_wait:
        result = query_video(task_id)
        status = result.get("status", "")
        elapsed = int(time.time() - start)
        print(f"[{elapsed}s] Status: {status}", file=sys.stderr)
        
        if status == "completed":
            if auto_download and result.get("video_url"):
                try:
                    local_path = download_video(result["video_url"])
                    result["local_path"] = local_path
                    print(f"[{elapsed}s] Downloaded to: {local_path}", file=sys.stderr)
                except Exception as e:
                    result["download_error"] = str(e)
                    print(f"[{elapsed}s] Download failed: {e}", file=sys.stderr)
            return result
        
        if status == "failed":
            raise Exception(f"Video generation failed: {result}")
        
        time.sleep(poll_interval)
    
    raise Exception(f"Timeout waiting for video after {max_wait}s")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法:")
        print("  python3 generate_video.py submit <model> <prompt> [seconds] [mode] [aspect_ratio]")
        print("  python3 generate_video.py query <task_id>")
        print("  python3 generate_video.py wait <task_id> [auto_download]")
        print("")
        print("示例:")
        print("  python3 generate_video.py submit Kling-V3-Omni '一只猫在草地上玩耍' 5 pro 16:9")
        print("  python3 generate_video.py wait 871747046242947116")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "submit":
        model = sys.argv[2]
        prompt = sys.argv[3]
        seconds = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        mode = sys.argv[5] if len(sys.argv) > 5 else "std"
        aspect = sys.argv[6] if len(sys.argv) > 6 else "16:9"
        
        result = generate_video(model, prompt, seconds, mode, aspect)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif action == "query":
        task_id = sys.argv[2]
        result = query_video(task_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif action == "wait":
        task_id = sys.argv[2]
        auto_download = "nodownload" not in sys.argv
        result = wait_for_video(task_id, auto_download=auto_download)
        print(json.dumps(result, ensure_ascii=False, indent=2))
