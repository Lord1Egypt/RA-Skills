#!/usr/bin/env python3
"""agnes-vision: 通过 Agnes 的 agnes-2.0-flash 多模态模型分析图片。

用法:
    python agnes_vision.py <图片> [<图片> ...] [-p "提示词"] [-m 模型] [-k key]

API key 查找顺序:
    1. --key 参数
    2. 环境变量 AGNES_API_KEY
    3. 脚本同目录下的 config.json: {"api_key": "..."}
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ENDPOINT = "https://apihub.agnes-ai.com/v1/chat/completions"
DEFAULT_MODEL = "agnes-2.0-flash"
DEFAULT_PROMPT = "请详细描述这张图片的内容。"


def log(msg):
    print(msg, file=sys.stderr)


def load_config():
    cfg_path = os.path.join(SCRIPT_DIR, "config.json")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            log(f"[agnes-vision] 警告: config.json 解析失败: {e}")
    return {}


def get_api_key(arg_key, config):
    key = arg_key or os.environ.get("AGNES_API_KEY") or config.get("api_key")
    if not key:
        sys.exit(
            "[agnes-vision] 错误: 未找到 API key。请通过以下任一方式提供:\n"
            "  1) 环境变量 AGNES_API_KEY\n"
            "  2) skill 目录下的 config.json: {\"api_key\": \"...\"}\n"
            "  3) 命令行参数 --key"
        )
    return key


def encode_image(path):
    if not os.path.exists(path):
        sys.exit(f"[agnes-vision] 错误: 图片不存在: {path}")
    mime, _ = mimetypes.guess_type(path)
    if not mime or not mime.startswith("image/"):
        mime = "image/jpeg"  # 兜底类型
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def call_api(api_key, model, prompt, image_paths, endpoint, max_tokens):
    content = [{"type": "text", "text": prompt}]
    for p in image_paths:
        content.append({
            "type": "image_url",
            "image_url": {"url": encode_image(p)},
        })

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
    }
    if max_tokens:
        payload["max_tokens"] = max_tokens

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"[agnes-vision] HTTP {e.code} 错误:\n{err_body}")
    except urllib.error.URLError as e:
        sys.exit(f"[agnes-vision] 网络错误: {e.reason}")

    try:
        result = json.loads(body)
        content_val = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        sys.exit(f"[agnes-vision] 解析响应失败: {e}\n原始响应:\n{body}")

    # 部分兼容接口会把 content 返回成数组（含 reasoning/text 等），只取文本部分
    if isinstance(content_val, list):
        parts = [
            c.get("text", "")
            for c in content_val
            if isinstance(c, dict) and c.get("type") == "text"
        ]
        content_val = "\n".join(p for p in parts if p)
    return content_val


def main():
    # Windows 默认按系统码页输出，强制 UTF-8 避免中文乱码
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    config = load_config()
    parser = argparse.ArgumentParser(
        description="通过 agnes-2.0-flash 多模态模型分析图片"
    )
    parser.add_argument("images", nargs="+", help="图片路径（可传多张）")
    parser.add_argument("-p", "--prompt", default=None, help="给模型的提示词")
    parser.add_argument("-m", "--model", default=None, help="模型名（默认 agnes-2.0-flash）")
    parser.add_argument("-k", "--key", default=None, help="API key")
    parser.add_argument("--endpoint", default=None, help="API 端点")
    parser.add_argument("--max-tokens", type=int, default=None, help="最大输出 token")
    args = parser.parse_args()

    api_key = get_api_key(args.key, config)
    model = args.model or config.get("model") or DEFAULT_MODEL
    prompt = args.prompt or config.get("prompt") or DEFAULT_PROMPT
    endpoint = args.endpoint or config.get("endpoint") or DEFAULT_ENDPOINT

    answer = call_api(api_key, model, prompt, args.images, endpoint, args.max_tokens)
    print(answer)


if __name__ == "__main__":
    main()
