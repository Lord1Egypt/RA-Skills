#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
# ]
# ///
"""
aoment-visuals CLI
AI图像与视频生成服务 - 由 Aoment AI 提供支持

需要 Agent API Key 进行身份验证，通过 aoment_register.py 注册获取。

支持三种工具:
  - text-to-image: 文生图（基于 N2 模型）
  - image-to-image: 图生图（基于 N2 模型）
  - video-generation: 视频生成（基于 V1 模型）
"""

import argparse
import base64
import json
import os
import re
import sys

import requests

API_BASE = "https://www.aoment.com"

# 超时配置（秒）
IMAGE_TIMEOUT = 120
VIDEO_TIMEOUT = 660


def _auth_headers(api_key: str) -> dict:
    """构建包含 Agent API Key 的认证头"""
    return {"Authorization": f"Bearer {api_key}"}


def generate_text_to_image(api_base: str, args: argparse.Namespace) -> dict:
    """文生图 - 基于 N2 模型"""
    url = f"{api_base}/api/skills/aoment-visuals/text-to-image"

    payload = {
        "prompt": args.prompt,
        "aspectRatio": args.aspect_ratio,
        "imageSize": args.image_size,
    }

    response = requests.post(
        url, json=payload, headers=_auth_headers(args.api_key), timeout=IMAGE_TIMEOUT
    )
    result = response.json()

    if not result.get("success"):
        return {"success": False, "error": result.get("error", "文生图失败")}

    return {
        "success": True,
        "tool_type": "text-to-image",
        "data": {
            "image_url": result.get("imageUrl"),
        },
    }


def generate_image_to_image(api_base: str, args: argparse.Namespace) -> dict:
    """图生图 - 基于 N2 模型"""
    url = f"{api_base}/api/skills/aoment-visuals/image-to-image"

    ref_list = args.reference_image
    if not ref_list:
        return {"success": False, "error": "图生图模式需要提供 --reference-image 参数"}

    reference_image = ref_list[0]

    # 构建 multipart/form-data 请求
    files = {}
    data = {
        "prompt": args.prompt,
        "aspectRatio": args.aspect_ratio,
        "imageSize": args.image_size,
    }

    if reference_image.startswith("http"):
        # URL 形式的参考图
        data["image"] = reference_image
    else:
        # Base64 形式的参考图
        image_bytes = base64.b64decode(reference_image)
        files["image"] = ("reference.png", image_bytes, "image/png")

    headers = _auth_headers(args.api_key)

    if files:
        response = requests.post(
            url, data=data, files=files, headers=headers, timeout=IMAGE_TIMEOUT
        )
    else:
        response = requests.post(
            url, data=data, headers=headers, timeout=IMAGE_TIMEOUT
        )

    result = response.json()

    if not result.get("success"):
        return {"success": False, "error": result.get("error", "图生图失败")}

    return {
        "success": True,
        "tool_type": "image-to-image",
        "data": {
            "image_url": result.get("imageUrl"),
        },
    }


def generate_video(api_base: str, args: argparse.Namespace) -> dict:
    """视频生成 - 基于 V1 模型"""
    url = f"{api_base}/api/skills/aoment-visuals/video-generation"

    data = {
        "prompt": args.prompt,
        "v1Orientation": args.orientation,
        "v1Resolution": args.resolution,
        "v1Mode": args.mode,
    }

    files_list = []
    ref_list = args.reference_image or []

    for i, ref in enumerate(ref_list):
        if ref.startswith("http"):
            img_response = requests.get(ref, timeout=30)
            img_response.raise_for_status()
            files_list.append(
                ("referenceImage", (f"reference-{i}.png", img_response.content, "image/png"))
            )
        else:
            image_bytes = base64.b64decode(ref)
            files_list.append(
                ("referenceImage", (f"reference-{i}.png", image_bytes, "image/png"))
            )

    headers = _auth_headers(args.api_key)

    if files_list:
        response = requests.post(
            url, data=data, files=files_list, headers=headers, timeout=VIDEO_TIMEOUT
        )
    else:
        response = requests.post(
            url, data=data, headers=headers, timeout=VIDEO_TIMEOUT
        )

    result = response.json()

    if not result.get("success"):
        return {"success": False, "error": result.get("error", "视频生成失败")}

    return {
        "success": True,
        "tool_type": "video-generation",
        "data": {
            "video_url": result.get("videoUrl"),
        },
    }


def _read_local_version() -> str | None:
    """从 SKILL.md 中读取 version 字段（匹配第一个 'version: x.y.z' 行）"""
    try:
        skill_md = os.path.join(os.path.dirname(__file__), '..', 'SKILL.md')
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'^version:\s*(.+)$', content, re.MULTILINE)
        return match.group(1).strip() if match else None
    except Exception:
        return None


def _compare_versions(local: str, remote: str) -> int:
    """比较 semver 版本号，返回 -1(落后), 0(相同), 1(超前)"""
    def parse(v: str) -> tuple:
        parts = v.split('.')
        return tuple(int(p) for p in parts)
    try:
        l, r = parse(local), parse(remote)
        return (l > r) - (l < r)
    except Exception:
        return 0


def _check_version(api_base: str) -> None:
    """检查本地版本是否落后于远程最新版本，落后则中断"""
    local_version = _read_local_version()
    if not local_version:
        return  # 无法读取本地版本，跳过检查

    try:
        url = f"{api_base}/api/skills/aoment-visuals/version"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if not data.get('success'):
            return
        remote_version = data.get('data', {}).get('version')
        if not remote_version:
            return
        if _compare_versions(local_version, remote_version) < 0:
            result = {
                "success": False,
                "error": "update_required",
                "current_version": local_version,
                "latest_version": remote_version,
                "message": f"Skill 版本过旧（当前 {local_version}，最新 {remote_version}），请下载最新版本后重试。",
            }
            json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
            print()
            sys.exit(1)
    except Exception:
        pass  # 网络异常等情况下 fail-safe，继续执行


def main():
    parser = argparse.ArgumentParser(
        description="aoment-visuals: AI图像与视频生成服务"
    )
    parser.add_argument(
        "--api-key", "-k",
        required=True,
        help="Agent API Key（通过 aoment_register.py 注册获取）",
    )
    parser.add_argument(
        "--tool-type", "-t",
        required=True,
        choices=["text-to-image", "image-to-image", "video-generation"],
        help="工具类型",
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="提示词",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="auto",
        help="宽高比（图像工具用），默认 auto",
    )
    parser.add_argument(
        "--image-size",
        default="1K",
        help="分辨率（图像工具用），默认 1K",
    )
    parser.add_argument(
        "--reference-image",
        action="append",
        default=None,
        help="参考图片的 Base64 数据或 URL 地址（可多次指定）",
    )
    parser.add_argument(
        "--orientation",
        default="portrait",
        help="视频方向（视频用），默认 portrait",
    )
    parser.add_argument(
        "--resolution",
        default="standard",
        help="视频分辨率（视频用），默认 standard",
    )
    parser.add_argument(
        "--mode",
        default="standard",
        help="视频生成模式（视频用），默认 standard",
    )
    args = parser.parse_args()

    # 版本检查：落后时中断并提示更新
    _check_version(API_BASE)

    try:
        if args.tool_type == "text-to-image":
            result = generate_text_to_image(API_BASE, args)
        elif args.tool_type == "image-to-image":
            result = generate_image_to_image(API_BASE, args)
        elif args.tool_type == "video-generation":
            result = generate_video(API_BASE, args)
    except requests.exceptions.Timeout:
        result = {"success": False, "error": f"请求超时（工具: {args.tool_type}）"}
    except requests.exceptions.RequestException as e:
        result = {"success": False, "error": f"网络请求失败: {str(e)}"}
    except Exception as e:
        result = {"success": False, "error": f"内部错误: {str(e)}"}

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
