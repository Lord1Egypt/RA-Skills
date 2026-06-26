#!/usr/bin/env python3
"""
AIGC Generator - OpenClaw Skill
调用 AIGC 接口生成图片，下载到本地 workspace，输出路径供 agent 调用 feishu_doc 发送
"""

import requests
import time
import uuid
import json
import os
import threading
import hashlib
import glob as _glob
from urllib.parse import urlparse
from datetime import datetime, timedelta

# ========== Config Loading ==========
def _load_config():
    """从环境变量加载配置"""
    cfg = {}
    cfg['base_url']  = os.environ.get('AIGC_BASE_URL',  'https://tczlld.com/aistudio/api')
    cfg['client_id'] = os.environ.get('AIGC_CLIENT_ID', 'openclaw-default')
    cfg['provider']  = int(os.environ.get('AIGC_PROVIDER', '4'))
    cfg['api_key']   = os.environ.get('AIGC_API_KEY',   '')
    cfg['output_dir'] = os.environ.get('AIGC_OUTPUT_DIR',
                              os.path.expanduser('~/.openclaw/workspace/files/generated/images'))
    cfg['timeout']   = int(os.environ.get('AIGC_TIMEOUT', '120'))
    return cfg

CONFIG = _load_config()
# ====================================


# ========== Rate Limiting ==========
_rate_limit_lock = threading.Lock()
_rate_limit_store = {}

RATE_LIMIT_MAX    = 20
RATE_LIMIT_WINDOW = 60

def _check_rate_limit(client_id: str) -> bool:
    now = datetime.now()
    window_start = now - timedelta(seconds=RATE_LIMIT_WINDOW)
    key = hashlib.sha256(client_id.encode()).hexdigest()[:16]
    with _rate_limit_lock:
        _rate_limit_store[key] = [ts for ts in _rate_limit_store.get(key, []) if ts > window_start]
        if len(_rate_limit_store[key]) >= RATE_LIMIT_MAX:
            return False
        _rate_limit_store[key].append(now)
        return True
# ====================================


def _ensure_dir(path):
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)
    return path


def _download_image(url, timeout=30):
    """下载图片到 output_dir，返回本地文件路径"""
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    path_ext = os.path.splitext(urlparse(url).path)[1] or '.png'
    timestamp = int(time.time() * 1000)
    # 生成唯一文件名
    filename = f"aigc_{timestamp}{path_ext}"
    filepath = os.path.join(_ensure_dir(CONFIG['output_dir']), filename)
    with open(filepath, 'wb') as f:
        f.write(resp.content)
    return filepath


def _upload_to_oss(image_url):
    """上传图片到用户 OSS，返回 OSS URL（保留原 URL 作为兜底）"""
    try:
        img_resp = requests.get(image_url, timeout=30)
        img_resp.raise_for_status()
        filename = os.path.basename(urlparse(image_url).path) or f"aigc_{int(time.time()*1000)}.png"
        files = {'file': (filename, img_resp.content, 'image/png')}
        headers = {'X-API-Key': CONFIG['api_key']}
        resp = requests.post(
            f"{CONFIG['base_url']}/ai/file/upload",
            files=files, headers=headers, timeout=30
        )
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") == 200:
            return result.get("data", {}).get("url", image_url)
    except Exception as e:
        print(f"  ⚠️ OSS 上传异常: {e}", file=__import__('sys').stderr)
    return image_url


def generate(prompt, negative_prompt="", aspect_ratio=1, batch_size=1):
    """提交生成任务，返回 task_id"""
    if not _check_rate_limit(CONFIG['client_id']):
        print("❌ 频率超限: 60秒内最多 20 次", file=__import__('sys').stderr)
        return None

    request_id = str(uuid.uuid4())
    payload = {
        "clientId": CONFIG['client_id'],
        "requestId": request_id,
        "provider": CONFIG['provider'],
        "prompt": prompt,
        "negativePrompt": negative_prompt,
        "aspectRatio": aspect_ratio,
        "batchSize": batch_size,
    }

    try:
        resp = requests.post(
            f"{CONFIG['base_url']}/ai/image/generate",
            json=payload,
            headers={"X-API-Key": CONFIG['api_key']},
            timeout=10
        )
        resp.raise_for_status()
        result = resp.json()

        if result.get("code") != 200:
            print(f"❌ 生成失败: {result.get('message', 'Unknown error')}", file=__import__('sys').stderr)
            return None

        task_id = (
            result.get("data", {}).get("taskId") or
            result.get("data", {}).get("promptId")
        )
        if not task_id:
            print("❌ 未获取到任务ID", file=__import__('sys').stderr)
            return None

        print(f"✅ 任务已提交: {task_id}", flush=True)
        return task_id
    except Exception as e:
        print(f"❌ 请求失败: {e}", file=__import__('sys').stderr)
        return None


def query_task(task_id, max_wait=None):
    """轮询任务状态，下载完成图片到本地，返回本地文件路径列表"""
    if max_wait is None:
        max_wait = CONFIG['timeout']

    start = time.time()
    while time.time() - start < max_wait:
        try:
            resp = requests.get(
                f"{CONFIG['base_url']}/ai/task/query",
                params={"taskId": task_id},
                headers={"X-API-Key": CONFIG['api_key']},
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json().get("data", {})
            status = data.get("status", 0)
            progress = data.get("progress", 0)
            status_desc = data.get("statusDesc", "")
            result_urls = data.get("resultUrls") or []

            if 0 < progress < 1.0:
                print(f"⏳ 生成中... {int(progress * 100)}% ({status_desc})", flush=True)

            if status == 1 and progress >= 1.0 and result_urls:  # 成功（API status=1 表示完成）
                local_paths = []
                for url in result_urls:
                    # OSS 上传（可选，保留 URL）
                    oss_url = _upload_to_oss(url)
                    # 下载到本地
                    local_path = _download_image(url)
                    local_paths.append(local_path)
                    print(f"  ✅ 下载完成: {local_path}", flush=True)

                print(f"🎉 共 {len(local_paths)} 张图片已保存", flush=True)
                # 输出 JSON 结果供 agent 解析
                print(f"__RESULT_JSON__{json.dumps({'local_paths': local_paths, 'oss_urls': result_urls}, ensure_ascii=False)}__", flush=True)
                return local_paths

            elif status < 0:
                print(f"❌ 生成失败: {data.get('message', status_desc)}", file=__import__('sys').stderr)
                return None

            elif status == 1 and progress >= 1.0 and not result_urls:
                # 进度100%但图片还在上传中，继续等待
                print(f"⏳ 等待图片上传... ({status_desc})", flush=True)

            time.sleep(2)
        except Exception as e:
            print(f"⚠️ 查询异常: {e}", file=__import__('sys').stderr)
            time.sleep(2)

    print(f"⏱️ 超时：任务未在 {max_wait} 秒内完成", file=__import__('sys').stderr)
    return None


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AIGC Generator - OpenClaw Skill")
    parser.add_argument("prompt", help="内容描述")
    parser.add_argument("--negative", default="", help="负面提示词")
    parser.add_argument("--ratio", type=int, default=1, choices=[1,2,3,4,5],
                        help="比例: 1=1:1 2=3:4 3=4:3 4=9:16 5=16:9")
    parser.add_argument("--batch", type=int, default=1, choices=[1,2,3,4], help="生成数量")
    parser.add_argument("--timeout", type=int, default=None, help="超时秒数")
    args = parser.parse_args()

    print(f"🎨 开始生成: {args.prompt}", flush=True)
    if args.negative:
        print(f"🚫 负面提示词: {args.negative}", flush=True)

    task_id = generate(args.prompt, args.negative, args.ratio, args.batch)
    if not task_id:
        import sys
        sys.exit(1)

    result = query_task(task_id, max_wait=args.timeout)
    if not result:
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main()
