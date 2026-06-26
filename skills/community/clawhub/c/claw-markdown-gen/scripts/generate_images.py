#!/usr/bin/env python3
"""
重度改写模式 - AI 配图后处理脚本

读取 LLM 生成的 Markdown（含 {{AI_IMAGE:ai_img_XXX.jpg:prompt描述}} 占位符），
调用用户透传的图片生成 API，将占位符替换为真实图片 URL，
保留 <!-- kw:ai_img_XXX.jpg:关键词 --> 注释供插件端回填 IndexedDB。

用法:
    python generate_images.py <input_md> <output_md> --api-key <KEY> --api-url <URL>

环境变量（备选）:
    IMAGE_API_KEY   - 图片生成 API Key
    IMAGE_API_URL   - 图片生成 API URL
"""

import argparse
import json
import os
import re
import sys
import time
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

AI_IMAGE_PATTERN = re.compile(r'\{\{AI_IMAGE:(ai_img_\d+\.\w+):(.+?)\}\}')


def parse_args():
    parser = argparse.ArgumentParser(description="AI 配图后处理")
    parser.add_argument("input", help="输入 Markdown 文件路径")
    parser.add_argument("output", help="输出 Markdown 文件路径")
    parser.add_argument("--api-key", default=os.environ.get("IMAGE_API_KEY", ""),
                        help="图片生成 API Key")
    parser.add_argument("--api-url", default=os.environ.get("IMAGE_API_URL", ""),
                        help="图片生成 API URL")
    parser.add_argument("--model", default="dall-e-3",
                        help="图片生成模型名称")
    parser.add_argument("--size", default="1024x1024",
                        help="图片尺寸")
    parser.add_argument("--quality", default="standard",
                        help="图片质量 (standard/hd)")
    parser.add_argument("--style", default="vivid",
                        help="图片风格 (vivid/natural)")
    parser.add_argument("--delay", type=float, default=1.0,
                        help="每次 API 调用间隔（秒）")
    return parser.parse_args()


def read_markdown(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_markdown(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def extract_placeholders(text):
    return [(m.group(1), m.group(2).strip(), m.start(), m.end()) for m in AI_IMAGE_PATTERN.finditer(text)]


def call_openai_image_api(api_key, api_url, prompt, model, size, quality, style):
    url = urljoin(api_url.rstrip("/") + "/", "v1/images/generations")
    body = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality,
        "style": style,
    }
    data = json.dumps(body).encode("utf-8")
    req = Request(url, data=data, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })
    try:
        with urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["data"][0]["url"]
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise RuntimeError(f"图片生成 API 返回错误 {e.code}: {error_body}")
    except URLError as e:
        raise RuntimeError(f"无法连接图片生成 API: {e.reason}")


def call_generic_image_api(api_key, api_url, prompt, **kwargs):
    body = {
        "prompt": prompt,
        "n": 1,
    }
    body.update({k: v for k, v in kwargs.items() if v and k not in ("delay",)})
    data = json.dumps(body).encode("utf-8")
    req = Request(api_url, data=data, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })
    try:
        with urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if "data" in result and len(result["data"]) > 0:
                item = result["data"][0]
                return item.get("url") or item.get("b64_json")
            if "url" in result:
                return result["url"]
            if "output" in result:
                return result["output"]
            raise RuntimeError(f"无法从响应中提取图片 URL: {json.dumps(result)[:200]}")
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise RuntimeError(f"图片生成 API 返回错误 {e.code}: {error_body}")
    except URLError as e:
        raise RuntimeError(f"无法连接图片生成 API: {e.reason}")


def generate_image(api_key, api_url, prompt, args):
    if not api_key:
        raise RuntimeError("未提供图片生成 API Key")
    if not api_url:
        raise RuntimeError("未提供图片生成 API URL")

    if "openai.com" in api_url or "api.openai" in api_url:
        return call_openai_image_api(
            api_key, api_url, prompt,
            args.model, args.size, args.quality, args.style,
        )
    else:
        return call_generic_image_api(
            api_key, api_url, prompt,
            model=args.model, size=args.size, quality=args.quality, style=args.style,
        )


def process(text, args):
    placeholders = extract_placeholders(text)
    if not placeholders:
        print("未发现 AI_IMAGE 占位符，无需处理")
        return text

    print(f"发现 {len(placeholders)} 个 AI 配图占位符")

    result = text
    offset = 0

    for i, (filename, prompt, start, end) in enumerate(placeholders, 1):
        print(f"[{i}/{len(placeholders)}] 生成图片 {filename}: {prompt[:60]}...")
        try:
            image_url = generate_image(args.api_key, args.api_url, prompt, args)
            replacement = f"![{prompt}]({image_url})"
        except RuntimeError as e:
            print(f"  ✗ 失败: {e}", file=sys.stderr)
            replacement = f"> ⚠️ AI 配图生成失败: {prompt}"

        real_start = start + offset
        real_end = end + offset
        result = result[:real_start] + replacement + result[real_end:]
        offset += len(replacement) - (end - start)

        print(f"  ✓ 完成")

        if i < len(placeholders):
            time.sleep(args.delay)

    return result


def main():
    args = parse_args()

    if not args.api_key:
        print("错误: 未提供 API Key（通过 --api-key 或 IMAGE_API_KEY 环境变量）", file=sys.stderr)
        sys.exit(1)
    if not args.api_url:
        print("错误: 未提供 API URL（通过 --api-url 或 IMAGE_API_URL 环境变量）", file=sys.stderr)
        sys.exit(1)

    text = read_markdown(args.input)
    result = process(text, args)
    write_markdown(args.output, result)
    print(f"完成，输出: {args.output}")


if __name__ == "__main__":
    main()
