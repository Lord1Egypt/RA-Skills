#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "dashscope>=1.25.8",
#   "requests>=2.31.0",
# ]
# ///
"""
阿里云百炼图像 CLI
用法见 SKILL.md

支持功能：
  text2img    千问文生图（qwen-image-2.0-pro / qwen-image-2.0）
  wan26       万相2.6图像编辑/文生图（wan2.6-image / wan2.6-t2i）
"""

import argparse
import os
import sys
import time
from pathlib import Path

# ── Helpers ────────────────────────────────────────────────────────────────────

def get_api_key(args_key=None):
    key = args_key or os.getenv("DASHSCOPE_API_KEY")
    if not key:
        print("错误: 未找到 API Key。请设置环境变量 DASHSCOPE_API_KEY 或使用 --api-key 参数。", file=sys.stderr)
        sys.exit(1)
    return key

def get_base_url(region="cn"):
    if region == "us":
        return "https://dashscope-us.aliyuncs.com/api/v1"
    if region == "intl":
        return "https://dashscope-intl.aliyuncs.com/api/v1"
    return "https://dashscope.aliyuncs.com/api/v1"

def save_images(urls: list, output_dir: str, prefix: str = "output") -> list:
    import requests
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    saved = []
    ts = time.strftime("%Y%m%d-%H%M%S")
    for i, url in enumerate(urls):
        ext = url.split("?")[0].rsplit(".", 1)[-1] if "." in url.split("?")[0].split("/")[-1] else "png"
        fname = f"{ts}-{prefix}-{i+1}.{ext}"
        path = str(Path(output_dir) / fname)
        img = requests.get(url, timeout=60).content
        with open(path, "wb") as f:
            f.write(img)
        saved.append(path)
        print(f"已保存: {path}")
    return saved


# ── 功能实现 ────────────────────────────────────────────────────────────────────

def cmd_text2img(args, api_key, base_url):
    """千问文生图（qwen-image-2.0-pro / qwen-image-2.0 / qwen-image-max / qwen-image-plus / qwen-image）"""
    import dashscope
    from dashscope import MultiModalConversation
    dashscope.base_http_api_url = base_url

    model = args.model or "qwen-image-2.0-pro"
    print(f"文生图中 model={model} …")
    call_kwargs = dict(
        api_key=api_key,
        model=model,
        messages=[{"role": "user", "content": [{"text": args.prompt}]}],
        result_format="message",
        stream=False,
        watermark=args.watermark,
        prompt_extend=not args.no_extend,
        n=args.n,
        size=args.size or "2048*2048",
        negative_prompt=args.negative_prompt or "",
    )
    if args.seed is not None:
        call_kwargs["seed"] = args.seed
    response = MultiModalConversation.call(**call_kwargs)
    if response.status_code != 200:
        print(f"错误: {response.status_code} {response.message}", file=sys.stderr)
        sys.exit(1)
    urls = [item["image"] for item in response.output.choices[0].message.content if item.get("image")]
    return save_images(urls, args.output_dir, "text2img")


def cmd_edit(args, api_key, base_url):
    """千问图像编辑（qwen-image-2.0-pro / qwen-image-2.0 / qwen-image-edit-max / qwen-image-edit-plus / qwen-image-edit）"""
    import dashscope
    from dashscope import MultiModalConversation
    dashscope.base_http_api_url = base_url

    images = args.images or []
    if not images:
        print("错误: edit 命令至少需要 1 张输入图（--images）", file=sys.stderr)
        sys.exit(1)
    if len(images) > 3:
        print("错误: edit 命令最多支持 3 张输入图", file=sys.stderr)
        sys.exit(1)

    model = args.model or "qwen-image-2.0-pro"
    content = [{"image": img} for img in images] + [{"text": args.prompt}]

    print(f"图像编辑中 model={model}，{len(images)} 张输入图 …")
    call_kwargs = dict(
        api_key=api_key,
        model=model,
        messages=[{"role": "user", "content": content}],
        result_format="message",
        stream=False,
        watermark=args.watermark,
        prompt_extend=not args.no_extend,
        n=args.n,
        negative_prompt=args.negative_prompt or "",
    )
    if args.size:
        call_kwargs["size"] = args.size
    if args.seed is not None:
        call_kwargs["seed"] = args.seed
    response = MultiModalConversation.call(**call_kwargs)
    if response.status_code != 200:
        print(f"错误: {response.status_code} {response.message}", file=sys.stderr)
        sys.exit(1)
    urls = [item["image"] for item in response.output.choices[0].message.content if item.get("image")]
    return save_images(urls, args.output_dir, "edit")


def cmd_wan26(args, api_key, base_url):
    """万相2.6图像编辑/文生图（wan2.6-image / wan2.6-t2i）"""
    import dashscope
    from dashscope.aigc.image_generation import ImageGeneration
    from dashscope.api_entities.dashscope_response import Message
    dashscope.base_http_api_url = base_url

    model = args.model or "wan2.6-image"
    images = args.images or []

    # wan2.6-t2i 只支持文生图（无图输入）
    if model == "wan2.6-t2i" and images:
        print("错误: wan2.6-t2i 为纯文生图模型，不支持 --images 输入", file=sys.stderr)
        sys.exit(1)

    if model == "wan2.6-t2i":
        # 纯文生图模式：不使用 enable_interleave，同步调用
        print(f"万相2.6文生图中 model={model} …")
        message = Message(role="user", content=[{"text": args.prompt}])
        call_kwargs = dict(
            model=model,
            api_key=api_key,
            messages=[message],
            n=args.n or 1,
            negative_prompt=args.negative_prompt or "",
            prompt_extend=not args.no_extend,
            watermark=args.watermark,
        )
        if args.size:
            call_kwargs["size"] = args.size
        if args.seed is not None:
            call_kwargs["seed"] = args.seed

        rsp = ImageGeneration.call(**call_kwargs)
        if rsp.status_code != 200:
            print(f"错误: {rsp.status_code} {rsp.message}", file=sys.stderr)
            sys.exit(1)

        image_urls = []
        for choice in (rsp.output.choices or []):
            for item in (choice.message.content or []):
                if item.get("type") == "image":
                    image_urls.append(item["image"])
        return save_images(image_urls, args.output_dir, "wan26")

    # wan2.6-image：有图→图像编辑，无图或 --interleave→图文混排
    enable_interleave = (len(images) == 0) or args.interleave

    if enable_interleave and len(images) > 1:
        print("错误: 图文混排模式最多支持 1 张输入图（图像编辑模式请去掉 --interleave）", file=sys.stderr)
        sys.exit(1)
    if not enable_interleave and len(images) == 0:
        print("错误: 图像编辑模式必须提供 1~4 张输入图（--images）", file=sys.stderr)
        sys.exit(1)

    content = [{"text": args.prompt}]
    for img in images:
        content.append({"image": img})
    message = Message(role="user", content=content)

    call_kwargs = dict(
        model=model,
        api_key=api_key,
        messages=[message],
        enable_interleave=enable_interleave,
        negative_prompt=args.negative_prompt or "",
        watermark=args.watermark,
    )
    if args.size:
        call_kwargs["size"] = args.size
    if args.seed is not None:
        call_kwargs["seed"] = args.seed

    if enable_interleave:
        # 图文混排/文生图：同步流式
        print(f"万相2.6图文混排生成中 model={model} …")
        call_kwargs["stream"] = True
        call_kwargs["max_images"] = args.max_images or 5

        stream_res = ImageGeneration.call(**call_kwargs)
        text_buf = []
        image_urls = []
        for chunk in stream_res:
            if chunk.status_code != 200:
                print(f"\n错误: {chunk.status_code} {chunk.message}", file=sys.stderr)
                sys.exit(1)
            for choice in (chunk.output.choices or []):
                for item in (choice.message.content or []):
                    if item.get("type") == "text":
                        text_buf.append(item.get("text", ""))
                        print(item.get("text", ""), end="", flush=True)
                    elif item.get("type") == "image":
                        image_urls.append(item["image"])
        print()

        if text_buf:
            ts = time.strftime("%Y%m%d-%H%M%S")
            Path(args.output_dir).mkdir(parents=True, exist_ok=True)
            text_path = str(Path(args.output_dir) / f"{ts}-wan26-text.txt")
            with open(text_path, "w", encoding="utf-8") as f:
                f.write("".join(text_buf))
            print(f"已保存文本: {text_path}")

        return save_images(image_urls, args.output_dir, "wan26")

    else:
        # 图像编辑模式：同步
        print(f"万相2.6图像编辑中 model={model}，{len(images)} 张输入图 …")
        call_kwargs["n"] = args.n or 1
        call_kwargs["prompt_extend"] = not args.no_extend

        rsp = ImageGeneration.call(**call_kwargs)
        if rsp.status_code != 200:
            print(f"错误: {rsp.status_code} {rsp.message}", file=sys.stderr)
            sys.exit(1)

        image_urls = []
        for choice in (rsp.output.choices or []):
            for item in (choice.message.content or []):
                if item.get("type") == "image":
                    image_urls.append(item["image"])
        return save_images(image_urls, args.output_dir, "wan26")


# ── CLI ────────────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        description="阿里云百炼图像 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--api-key", help="DashScope API Key（可用 DASHSCOPE_API_KEY 环境变量）")
    parser.add_argument("--region", default="cn", choices=["intl", "cn", "us"],
                        help="地域：cn=北京（默认），intl=新加坡，us=弗吉尼亚")
    parser.add_argument("--output-dir", default=".", help="输出目录（默认当前目录）")

    sub = parser.add_subparsers(dest="cmd", required=True)

    # text2img
    p = sub.add_parser("text2img", help="千问文生图")
    p.add_argument("--prompt", required=True, help="提示词（最多800字符）")
    p.add_argument("--model", default="qwen-image-2.0-pro",
                   choices=["qwen-image-2.0-pro", "qwen-image-2.0",
                            "qwen-image-max", "qwen-image-plus", "qwen-image"],
                   help="模型（默认 qwen-image-2.0-pro）")
    p.add_argument("--size", default=None,
                   help="分辨率，如 2048*2048（默认）/ 1536*2688 / 2688*1536 等")
    p.add_argument("--n", type=int, default=1,
                   help="生成数量（qwen-image-2.0系列最多6张；其余固定1张，默认1）")
    p.add_argument("--negative-prompt", help="反向提示词")
    p.add_argument("--no-extend", action="store_true", help="禁用提示词自动扩写")
    p.add_argument("--seed", type=int, default=None, help="随机数种子 [0, 2147483647]")
    p.add_argument("--watermark", action="store_true", help="添加 Qwen-Image 水印")

    # edit
    p = sub.add_parser("edit", help="千问图像编辑（1-3 张输入图 + 文字指令）")
    p.add_argument("--prompt", required=True, help="编辑指令（最多800字符）")
    p.add_argument("--images", nargs="+", required=True,
                   help="输入图 URL 或本地路径（1-3 张）")
    p.add_argument("--model", default="qwen-image-2.0-pro",
                   choices=["qwen-image-2.0-pro", "qwen-image-2.0",
                            "qwen-image-edit-max", "qwen-image-edit-plus", "qwen-image-edit"],
                   help="模型（默认 qwen-image-2.0-pro）")
    p.add_argument("--size", default=None,
                   help="分辨率（总像素 512×512~2048×2048，如 1024*1024）；默认跟随最后一张输入图")
    p.add_argument("--n", type=int, default=1,
                   help="输出图数量（qwen-image-edit 固定1张；其余最多6张，默认1）")
    p.add_argument("--negative-prompt", help="反向提示词")
    p.add_argument("--no-extend", action="store_true", help="禁用提示词自动扩写")
    p.add_argument("--seed", type=int, default=None, help="随机数种子 [0, 2147483647]")
    p.add_argument("--watermark", action="store_true", help="添加 Qwen-Image 水印")

    # wan26
    p = sub.add_parser("wan26", help="万相2.6图像编辑/文生图（wan2.6-image / wan2.6-t2i）")
    p.add_argument("--prompt", required=True, help="提示词（中英文，最多2000字符）")
    p.add_argument("--model", default="wan2.6-image",
                   choices=["wan2.6-image", "wan2.6-t2i"],
                   help="模型（默认 wan2.6-image；wan2.6-t2i 仅支持文生图）")
    p.add_argument("--images", nargs="+",
                   help="输入图 URL（图像编辑模式 1-4 张；wan2.6-t2i 不支持）")
    p.add_argument("--interleave", action="store_true",
                   help="强制启用图文混排输出模式（有图时默认为图像编辑模式）")
    p.add_argument("--n", type=int, default=1, help="图像编辑模式生成图片数（1-4，默认 1）")
    p.add_argument("--max-images", type=int, default=5,
                   help="图文混排模式最多生成图片数（1-5，默认 5）")
    p.add_argument("--size", default=None,
                   help="分辨率（编辑模式：1K/2K 或 宽*高；混排/文生图：宽*高 如 1280*1280）")
    p.add_argument("--negative-prompt", help="反向提示词")
    p.add_argument("--no-extend", action="store_true", help="禁用提示词自动扩写（仅图像编辑模式）")
    p.add_argument("--seed", type=int, default=None, help="随机数种子 [0, 2147483647]")
    p.add_argument("--watermark", action="store_true", help="添加 AI 生成水印")

    return parser


HANDLERS = {
    "text2img": cmd_text2img,
    "edit":     cmd_edit,
    "wan26":    cmd_wan26,
}

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    api_key = get_api_key(args.api_key)
    base_url = get_base_url(args.region)
    saved = HANDLERS[args.cmd](args, api_key, base_url)
    print(f"\n完成！共 {len(saved)} 张图片已保存。")
