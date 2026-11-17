#!/usr/bin/env python3
"""
跨平台 AI 图像生成脚本

适用于没有内置图像生成工具的平台（如 Codex CLI、TRAE Work）。
WorkBuddy 平台默认使用内置 ImageGen 工具，本脚本作为备选方案。

支持的 API：
1. 火山引擎即梦 Seedream（需要 ARK_API_KEY 或 VOLCENGINE_AK + VOLCENGINE_SK）
2. Google Gemini 3 Pro Image（需要 GEMINI_API_KEY）
3. Agnes AI（需要 AGNES_API_KEY，完全免费）
4. OpenAI DALL-E 3（需要 OPENAI_API_KEY）
5. Stability AI（需要 STABILITY_API_KEY）
6. 本地 Stable Diffusion WebUI（需要 SD_WEBUI_URL）

使用方法：
  python3 generate_image.py --prompt "描述文本" --output "image.png"
  python3 generate_image.py --prompt "描述文本" --output "image.png" --api gemini
  python3 generate_image.py --batch storyboard.json --output-dir images/

环境变量：
  IMAGE_API              - 默认使用的 API: gemini/volcengine/agnes/openai/stability/local
  ARK_API_KEY            - 火山方舟 API Key（推荐，ark- 开头，在火山方舟控制台创建）
  VOLCENGINE_AK          - 火山引擎 Access Key（备选认证方式）
  VOLCENGINE_SK          - 火山引擎 Secret Key（备选认证方式）
  GEMINI_API_KEY         - Google Gemini API Key
  AGNES_API_KEY          - Agnes AI API Key（免费注册获取）
  OPENAI_API_KEY         - OpenAI API Key
  STABILITY_API_KEY      - Stability AI API Key
  SD_WEBUI_URL           - 本地 SD WebUI 地址（默认 http://127.0.0.1:7860）
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error


# ============================================================
#  火山引擎即梦 Seedream（字节跳动）
# ============================================================
#
# API 端点: https://ark.cn-beijing.volces.com/api/v3/images/generations
# 模型: doubao-seedream-5-0-260128（推荐，Seedream 5.0 lite）
#       其他可选: doubao-seedream-5-0-pro-260628 / doubao-seedream-4-5-251128 / doubao-seedream-4-0-250828
# 认证方式（二选一）:
#   1. ARK_API_KEY（推荐）— 在火山方舟控制台 → API Key 管理 创建，ark- 开头
#   2. VOLCENGINE_AK + VOLCENGINE_SK — 火山引擎账号密钥，通过 SDK 自动签名
# 支持 watermark: false 去水印
# 支持 response_format: "url" / "b64_json"
# 支持 size: "1024x1024" / "1K" / "2K" / "2048x2048"

def _download_image_from_url(image_url: str, output_path: str):
    """从 URL 下载图片，urllib 失败时回退到 curl"""
    try:
        with urllib.request.urlopen(image_url, timeout=60) as img_resp:
            image_data = img_resp.read()
    except Exception:
        import subprocess
        subprocess.check_call(
            ["curl", "-s", "-L", "-o", output_path, "--max-time", "60", image_url],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        return output_path
    with open(output_path, "wb") as f:
        f.write(image_data)
    return output_path


def generate_with_volcengine(prompt: str, output_path: str, size: str = "1024x768"):
    """使用火山引擎即梦 Seedream 生成图像（字节跳动模型）

    支持两种认证方式：
    1. ARK_API_KEY: 火山方舟控制台创建的 API Key（HTTP 直调，零依赖，推荐）
    2. VOLCENGINE_AK + VOLCENGINE_SK: IAM 访问密钥（通过 SDK 获取临时 STS token）

    环境变量：
    - ARK_API_KEY: 火山方舟 API Key（优先使用）
    - VOLCENGINE_AK: 火山引擎 Access Key ID
    - VOLCENGINE_SK: 火山引擎 Secret Access Key（base64 编码）
    - VOLCENGINE_MODEL: 模型名称（默认 doubao-seedream-5-0-260128，即 Seedream 5.0 lite）
      可选: doubao-seedream-5-0-pro-260628 / doubao-seedream-4-5-251128 / doubao-seedream-4-0-250828
    - VOLCENGINE_PROJECT: 项目名称（默认 default，仅 AK/SK 方式需要）

    注意：使用前需在火山方舟控制台开通对应模型。
    https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement
    """
    ark_api_key = os.environ.get("ARK_API_KEY")
    ak = os.environ.get("VOLCENGINE_AK")
    sk = os.environ.get("VOLCENGINE_SK")
    project = os.environ.get("VOLCENGINE_PROJECT", "default")

    if not ark_api_key and not (ak and sk):
        raise RuntimeError(
            "未设置火山引擎凭证\n"
            "方式 1: 设置 ARK_API_KEY 环境变量（推荐）\n"
            "  → 火山方舟控制台 → API Key 管理 → 创建 API Key\n"
            "方式 2: 设置 VOLCENGINE_AK + VOLCENGINE_SK 环境变量\n"
            "  → 火山引擎控制台 → 密钥管理 → 创建访问密钥\n"
            "注意: 使用前需在火山方舟控制台开通即梦图像模型\n"
            "  → https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement"
        )

    model = os.environ.get("VOLCENGINE_MODEL", "doubao-seedream-5-0-260128")
    # 即梦各模型支持的尺寸:
    #   5.0 pro:  1K, 2K          (1024x1024 / 2048x2048)
    #   5.0 lite: 2K, 3K, 4K      (最小 3686400 像素 → 2048x2048)
    #   4.5:      2K, 4K
    #   4.0:      1K, 2K, 4K
    # 5.0 lite 最低需要 2K (3,686,400 像素)，小尺寸自动升级
    if "5-0-260128" in model or "5-0-lite" in model:
        try:
            w, h = map(int, size.split("x"))
            if w * h < 3686400:
                size = "2048x2048"
        except ValueError:
            size = "2048x2048"
    elif size == "1024x768":
        size = "1024x1024"

    # ---- 获取有效的 API Key ----
    # 方式 1: 直接使用 ARK_API_KEY
    # 方式 2: 通过 AK/SK 获取临时 STS token
    effective_api_key = ark_api_key
    if not effective_api_key:
        try:
            from volcenginesdkarkruntime import Ark
        except ImportError:
            import subprocess
            print("正在安装 volcengine-python-sdk...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install",
                 "volcengine-python-sdk[ark]", "httpx", "-q"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            from volcenginesdkarkruntime import Ark

        # AK/SK 方式: 先获取临时 STS token，再用它调图像生成 API
        # （图像生成 API 不直接支持 AK/SK 认证，需要先换取 STS token）
        ak_client = Ark(ak=ak, sk=sk)
        effective_api_key = ak_client._get_endpoint_sts_token(
            model, project_name=project,
        )

    # ---- 调用图像生成 API（HTTP 直调） ----
    url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {effective_api_key}",
    }
    data = json.dumps({
        "model": model,
        "prompt": prompt,
        "size": size,
        "response_format": "url",
        "watermark": False,
    }).encode()

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()[:500]
        if "ModelNotOpen" in err_body:
            raise RuntimeError(
                f"火山引擎模型 {model} 未开通\n"
                f"请前往火山方舟控制台开通模型:\n"
                f"  → https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement"
            ) from e
        raise RuntimeError(f"火山引擎 API 错误 (HTTP {e.code}): {err_body}") from e

    if not result.get("data"):
        raise RuntimeError(f"火山引擎 API 未返回数据: {result}")

    item = result["data"][0]
    if item.get("b64_json"):
        image_data = base64.b64decode(item["b64_json"])
        with open(output_path, "wb") as f:
            f.write(image_data)
        return output_path
    elif item.get("url"):
        return _download_image_from_url(item["url"], output_path)
    else:
        raise RuntimeError(f"火山引擎 API 返回格式异常: {item}")


# ============================================================
#  Google Gemini 3 Pro Image
# ============================================================

def generate_with_gemini(prompt: str, output_path: str, size: str = "1024x768"):
    """使用 Google Gemini 3 Pro Image 生成图像

    需要环境变量: GEMINI_API_KEY
    依赖: google-genai, pillow（自动安装）
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("未设置 GEMINI_API_KEY 环境变量")

    # 尝试安装 SDK
    try:
        from google import genai
        from google.genai import types
        from PIL import Image as PILImage
    except ImportError:
        import subprocess
        print("正在安装 google-genai pillow...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "google-genai", "pillow", "-q"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        from google import genai
        from google.genai import types
        from PIL import Image as PILImage

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        ),
    )

    from io import BytesIO

    for part in response.parts:
        if part.inline_data is not None:
            image_data = part.inline_data.data
            if isinstance(image_data, str):
                image_data = base64.b64decode(image_data)
            image = PILImage.open(BytesIO(image_data))
            if image.mode == "RGBA":
                rgb_image = PILImage.new("RGB", image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[3])
                rgb_image.save(output_path, "PNG")
            else:
                image.convert("RGB").save(output_path, "PNG")
            return output_path

    raise RuntimeError("Gemini 未返回图像数据")


# ============================================================
#  Agnes AI（完全免费，OpenAI 兼容接口）
# ============================================================
#
# 可用模型:
#   agnes-image-2.1-flash (推荐) — 最新版，质量更高
#   agnes-image-2.0-flash         — 稳定版，图生图/编辑
#
# 图像 API Base URL: https://apihub.agnes-ai.com/v1/images/generations
# 文本 API Base URL: https://apihub.agnes-ai.com/v1
# 免费注册获取 Key: https://platform.agnes-ai.com

def generate_with_agnes(prompt: str, output_path: str, size: str = "1024x768"):
    """使用 Agnes AI 生成图像（完全免费，无需绑卡）

    需要环境变量: AGNES_API_KEY（在 platform.agnes-ai.com 免费注册获取）
    默认模型: agnes-image-2.1-flash
    可通过 AGNES_MODEL 环境变量切换模型 (agnes-image-2.0-flash / agnes-image-2.1-flash)

    注意：Agnes 图像 API 只返回 URL，不返回 b64_json；本函数会从 URL 下载图片。
    若 Python urllib 在特定网络环境无法解析 CDN，会自动使用 curl 下载。
    """
    api_key = os.environ.get("AGNES_API_KEY")
    if not api_key:
        raise RuntimeError(
            "未设置 AGNES_API_KEY 环境变量\n"
            "请访问 https://platform.agnes-ai.com 免费注册获取 API Key"
        )

    model = os.environ.get("AGNES_MODEL", "agnes-image-2.1-flash")
    url = "https://apihub.agnes-ai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = json.dumps({
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
    }).encode()

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=300) as resp:
        result = json.loads(resp.read())

    if not result.get("data") or not result["data"][0].get("url"):
        raise RuntimeError(f"Agnes API 未返回图片 URL: {result}")

    image_url = result["data"][0]["url"]
    return _download_image_from_url(image_url, output_path)


# ============================================================
#  OpenAI DALL-E 3
# ============================================================

def generate_with_openai(prompt: str, output_path: str, size: str = "1024x1024"):
    """使用 OpenAI DALL-E 3 生成图像"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("未设置 OPENAI_API_KEY 环境变量")

    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = json.dumps({
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "response_format": "b64_json",
    }).encode()

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    image_data = base64.b64decode(result["data"][0]["b64_json"])
    with open(output_path, "wb") as f:
        f.write(image_data)
    return output_path


# ============================================================
#  Stability AI
# ============================================================

def generate_with_stability(prompt: str, output_path: str, size: str = "1024x1024"):
    """使用 Stability AI 生成图像"""
    api_key = os.environ.get("STABILITY_API_KEY")
    if not api_key:
        raise RuntimeError("未设置 STABILITY_API_KEY 环境变量")

    w, h = size.split("x")
    url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
    headers = {"Authorization": f"Bearer {api_key}"}

    boundary = "----FormBoundary7MA4YWxkTrZu0gW"
    body_parts = []
    body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"prompt\"\r\n\r\n{prompt}\r\n")
    body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"width\"\r\n\r\n{w}\r\n")
    body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"height\"\r\n\r\n{h}\r\n")
    body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"samples\"\r\n\r\n1\r\n")
    body_parts.append(f"--{boundary}--\r\n")
    body = "".join(body_parts).encode()

    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    image_data = base64.b64decode(result["artifacts"][0]["base64"])
    with open(output_path, "wb") as f:
        f.write(image_data)
    return output_path


# ============================================================
#  本地 Stable Diffusion WebUI
# ============================================================

def generate_with_local_sd(prompt: str, output_path: str, size: str = "1024x1024"):
    """使用本地 Stable Diffusion WebUI 生成图像"""
    base_url = os.environ.get("SD_WEBUI_URL", "http://127.0.0.1:7860")
    w, h = size.split("x")

    url = f"{base_url}/sdapi/v1/txt2img"
    data = json.dumps({
        "prompt": prompt,
        "width": int(w),
        "height": int(h),
        "steps": 30,
        "batch_size": 1,
    }).encode()

    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    image_data = base64.b64decode(result["images"][0])
    with open(output_path, "wb") as f:
        f.write(image_data)
    return output_path


# ============================================================
#  API 注册表
# ============================================================

API_PROVIDERS = {
    "volcengine": generate_with_volcengine,
    "gemini": generate_with_gemini,
    "agnes": generate_with_agnes,
    "openai": generate_with_openai,
    "stability": generate_with_stability,
    "local": generate_with_local_sd,
}

# 默认 API（可通过 IMAGE_API 环境变量覆盖）
# 注意：WorkBuddy 平台默认使用内置 ImageGen，本脚本是 CLI 备选方案
DEFAULT_API = "gemini"


def generate_image(prompt: str, output_path: str, api: str = None, size: str = "1024x768"):
    """根据指定 API 生成图像

    Args:
        prompt: 图像生成提示词
        output_path: 输出文件路径
        api: API 名称 (gemini/volcengine/agnes/openai/stability/local)
        size: 图像尺寸 (如 "1024x768")
    """
    if api is None:
        api = os.environ.get("IMAGE_API", DEFAULT_API)

    if api not in API_PROVIDERS:
        raise ValueError(
            f"不支持的 API: {api}\n"
            f"可选: {', '.join(API_PROVIDERS.keys())}\n"
            f"可通过 IMAGE_API 环境变量设置默认 API"
        )

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    return API_PROVIDERS[api](prompt, output_path, size)


def batch_generate(storyboard_path: str, output_dir: str, api: str = None, size: str = "1024x768"):
    """批量生成分镜图像

    Args:
        storyboard_path: storyboard.json 文件路径（含 list 数组，每条有 desc_promopt 字段）
        output_dir: 输出目录
        api: API 名称
        size: 图像尺寸
    """
    with open(storyboard_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        scenes = data
    else:
        scenes = data.get("list", data.get("segments", []))
    results = []
    failed = 0

    for i, scene in enumerate(scenes):
        prompt = scene.get("prompt", scene.get("desc_promopt", scene.get("desc", "")))
        output = scene.get("output", None)
        if not output:
            output = os.path.join(output_dir, f"scene_{i:03d}.png")
        try:
            generate_image(prompt, output, api, size)
            results.append(output)
            print(f"[{i+1}/{len(scenes)}] OK  {output}")
        except Exception as e:
            failed += 1
            print(f"[{i+1}/{len(scenes)}] FAIL: {e}")
            results.append(None)

    print(f"\n完成: {len(scenes) - failed}/{len(scenes)} 张成功" + (f", {failed} 张失败" if failed else ""))
    return results


# ============================================================
#  命令行入口
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="跨平台 AI 图像生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
示例:
  # 单张生成
  python3 generate_image.py --prompt "扁平插画风格..." --output scene_000.png --api volcengine

  # 批量生成（从 storyboard.json）
  python3 generate_image.py --batch storyboard.json --output-dir images/ --api gemini

  # 通过环境变量设置默认 API
  export IMAGE_API=agnes
  python3 generate_image.py --prompt "..." --output img.png
""",
    )
    parser.add_argument("--prompt", type=str, help="图像生成提示词")
    parser.add_argument("--output", type=str, default="output.png", help="输出路径")
    parser.add_argument(
        "--api", type=str,
        choices=list(API_PROVIDERS.keys()),
        help=f"API 提供商 (默认: {DEFAULT_API})",
    )
    parser.add_argument("--size", type=str, default="1024x768", help="图像尺寸 (如 1024x768)")
    parser.add_argument("--batch", type=str, help="批量模式: storyboard.json 路径")
    parser.add_argument("--output-dir", type=str, default="images", help="批量输出目录")

    args = parser.parse_args()

    if args.batch:
        batch_generate(args.batch, args.output_dir, args.api, args.size)
    elif args.prompt:
        path = generate_image(args.prompt, args.output, args.api, args.size)
        print(f"Image saved: {path}")
    else:
        parser.print_help()
        print("\n可用 API:", ", ".join(API_PROVIDERS.keys()))
        print(f"环境变量 IMAGE_API 可设置默认 API（当前默认: {DEFAULT_API}）")
        sys.exit(1)
