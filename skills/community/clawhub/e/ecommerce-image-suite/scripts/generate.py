#!/usr/bin/env python3
"""
generate.py
调用图像生成 API，支持 5 个供应商，输出图片到指定目录。

用法：
  python3 generate.py \
    --product '{"product_description_for_prompt": "white T-shirt...", "selling_points": [...]}' \
    --provider openai \
    --api-key "sk-..." \
    --base-url "https://custom-proxy.example.com/v1" \
    --model "dall-e-3" \
    --types white_bg,key_features,material \
    --output-dir ./output/raw/

也可通过环境变量传入 key / base-url / model：
  OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL (默认 dall-e-3)
  GEMINI_API_KEY / GEMINI_BASE_URL / GEMINI_MODEL (默认 gemini-3.1-flash-image-preview)
  STABILITY_API_KEY / STABILITY_BASE_URL / STABILITY_MODEL (默认 core)
  DASHSCOPE_API_KEY / DASHSCOPE_BASE_URL / DASHSCOPE_MODEL (默认 qwen-image-2.0-pro)
  ARK_API_KEY / ARK_BASE_URL / ARK_MODEL (默认 doubao-seedream-5-0-260128)
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("请先安装 requests：pip install requests", file=sys.stderr)
    sys.exit(1)


# ── Default URLs ───────────────────────────────────────────────────────────

DEFAULT_URLS = {
    "openai":    "https://api.openai.com/v1/images/generations",
    "gemini":    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent",
    "stability": "https://api.stability.ai/v2beta/stable-image/generate/core",
    "tongyi":    "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
    "doubao":    "https://ark.cn-beijing.volces.com/api/v3/images/generations",
}


# ── Prompt 构建 ────────────────────────────────────────────────────────────

def build_prompt(type_id: str, desc: str, selling_points: list) -> str:
    """Build prompt from image-types.md templates with product description injected."""
    quality = (
        "Photorealistic, ultra-high definition, 8K resolution, commercial photography quality, "
        "sharp details, professional lighting. "
        "CRITICAL: keep the product EXACTLY the same — same print, same proportions, same color, "
        "do not modify any design detail."
    )
    prompts = {
        "white_bg": (
            f"{desc}, displayed centered on pure white background (RGB 255,255,255), "
            "product occupies 90% of frame, front view or slight 45-degree angle, "
            "clean studio lighting with very subtle natural shadow underneath, "
            f"no props, no decorations, no text. {quality}"
        ),
        "key_features": (
            f"Clean product feature infographic with light background. "
            f"Left side shows complete front view of {desc} (45% of frame). "
            "Right side has 3 minimalist outline icons vertically arranged representing "
            f"{', '.join(sp.get('en_title', sp.get('en', '')) for sp in selling_points[:3])}. "
            f"Balanced layout, clean typography space for labels, modern commercial design style. {quality}"
        ),
        "selling_pt": (
            f"Cozy bedroom interior, soft bokeh background. "
            f"{desc} laid flat on soft bed OR worn by faceless model showing oversized silhouette. "
            "Focus on loose fit, dropped shoulders, relaxed drape. "
            f"Soft warm lighting, casual lifestyle mood. Text overlay space on left side. {quality}"
        ),
        "material": (
            f"Macro photography style, {desc} partially folded at center. "
            "Directional side lighting highlighting knit fabric texture and softness. "
            "Cotton plant props in background to emphasize natural material. "
            "High clarity, sharp fabric surface texture, soft focus bokeh background. "
            f"Text overlay space on right side. {quality}"
        ),
        "lifestyle": (
            "Sunny campus green lawn or café wooden table surface, shallow depth of field lifestyle scene. "
            f"{desc} paired with canvas bag, laptop or vintage headphones. "
            "Young, casual, carefree atmosphere, bright natural lighting. "
            f"Scene conveys youthful everyday styling. Text overlay space on left side. {quality}"
        ),
        "model": (
            "Outdoor park with abundant sunlight. "
            "Young Chinese female model with bright smile, confidently walking. "
            f"Wearing {desc} with light blue denim shorts. "
            "Product is absolute visual focus, youthful and energetic mood. "
            f"Natural lighting, commercial fashion photography style. {quality}"
        ),
        "multi_scene": (
            "Split-screen image divided by a clean white vertical line at center. "
            f"LEFT HALF: cozy warm home interior, soft diffused lighting, {desc} in relaxed lounging setting. "
            f"RIGHT HALF: bright outdoor park, abundant natural sunlight, {desc} in vibrant outdoor setting. "
            f"Keep top-center and bottom corners lighter for text overlay. {quality}"
        ),
    }
    return prompts.get(type_id, f"{desc}. {quality}")


# ── Provider Implementations ────────────────────────────────────────────────

def generate_openai(key: str, prompt: str, base_url: str = "", model: str = "") -> bytes:
    url = (base_url.rstrip("/") + "/images/generations") if base_url else DEFAULT_URLS["openai"]
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "prompt": prompt, "size": "1024x1024", "quality": "hd", "response_format": "b64_json", "n": 1},
        timeout=120,
    )
    resp.raise_for_status()
    return base64.b64decode(resp.json()["data"][0]["b64_json"])


def generate_gemini(key: str, prompt: str, base_url: str = "", model: str = "") -> bytes:
    """Gemini 原生图像生成，兼容官方 API 和代理。

    鉴权策略：
      - 官方 API（generativelanguage.googleapis.com）→ x-goog-api-key + ?key= query
      - 代理 API（自定义 base_url）→ Authorization: Bearer（多数代理的标准方式）
    """
    is_official = not base_url
    # ── 拼接 URL ──
    if base_url:
        url = base_url
    elif model and model != DEFAULT_MODELS["gemini"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    else:
        url = DEFAULT_URLS["gemini"]

    # ── 鉴权头 ──
    if is_official:
        # 官方用 x-goog-api-key header + query param
        req_url = f"{url}?key={key}" if "?" not in url else url
        headers = {"x-goog-api-key": key, "Content-Type": "application/json"}
    else:
        # 代理一般走 Bearer token
        req_url = url
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    resp = requests.post(
        req_url,
        headers=headers,
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
                "imageConfig": {
                    "aspectRatio": "1:1",
                    "imageSize": "2K",
                },
            },
        },
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    # 从 candidates 中找到 inlineData 图片部分
    for part in data["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])
    raise RuntimeError("Gemini 响应中未找到图片数据")


def generate_stability(key: str, prompt: str, base_url: str = "", model: str = "") -> bytes:
    url = base_url or DEFAULT_URLS["stability"]
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
        files={"none": ""},
        data={"prompt": prompt, "output_format": "jpeg", "aspect_ratio": "1:1"},
        timeout=120,
    )
    resp.raise_for_status()
    return base64.b64decode(resp.json()["image"])


def generate_tongyi(key: str, prompt: str, base_url: str = "", model: str = "") -> bytes:
    """通义千问图像生成 — 同步接口（推荐，适用于 qwen-image-2.0-pro 等模型）。"""
    url = base_url or DEFAULT_URLS["tongyi"]
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "input": {
                "messages": [
                    {"role": "user", "content": [{"text": prompt}]}
                ]
            },
            "parameters": {
                "size": "1024*1024",
                "n": 1,
                "prompt_extend": False,
                "watermark": False,
            },
        },
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    # 同步接口直接返回图片 URL
    img_url = data["output"]["choices"][0]["message"]["content"][0]["image"]
    return requests.get(img_url, timeout=60).content


def generate_doubao(key: str, prompt: str, base_url: str = "", model: str = "") -> bytes:
    """豆包 Seedream（火山方舟）— 使用 ARK_API_KEY 鉴权。"""
    url = base_url or DEFAULT_URLS["doubao"]
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "prompt": prompt,
            "size": "1024x1024",
            "response_format": "url",
            "watermark": False,
            "n": 1,
        },
        timeout=120,
    )
    resp.raise_for_status()
    img_url = resp.json()["data"][0]["url"]
    return requests.get(img_url, timeout=60).content


GENERATORS = {
    "openai":    generate_openai,
    "gemini":    generate_gemini,
    "stability": generate_stability,
    "tongyi":    generate_tongyi,
    "doubao":    generate_doubao,
}

ENV_KEYS = {
    "openai":    "OPENAI_API_KEY",
    "gemini":    "GEMINI_API_KEY",
    "stability": "STABILITY_API_KEY",
    "tongyi":    "DASHSCOPE_API_KEY",
    "doubao":    "ARK_API_KEY",
}

ENV_URLS = {
    "openai":    "OPENAI_BASE_URL",
    "gemini":    "GEMINI_BASE_URL",
    "stability": "STABILITY_BASE_URL",
    "tongyi":    "DASHSCOPE_BASE_URL",
    "doubao":    "ARK_BASE_URL",
}

ENV_MODELS = {
    "openai":    "OPENAI_MODEL",
    "gemini":    "GEMINI_MODEL",
    "stability": "STABILITY_MODEL",
    "tongyi":    "DASHSCOPE_MODEL",
    "doubao":    "ARK_MODEL",
}

DEFAULT_MODELS = {
    "openai":    "dall-e-3",
    "gemini":    "gemini-3.1-flash-image-preview",
    "stability": "core",
    "tongyi":    "qwen-image-2.0-pro",
    "doubao":    "doubao-seedream-5-0-260128",
}


def resolve_model(provider: str, cli_model: str = "") -> str:
    """CLI --model > 环境变量 > 默认值"""
    return cli_model or os.environ.get(ENV_MODELS[provider], "") or DEFAULT_MODELS[provider]


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="电商套图图像生成脚本")
    parser.add_argument("--product",    required=True, help="商品 JSON 字符串")
    parser.add_argument("--provider",   required=True, choices=list(GENERATORS.keys()))
    parser.add_argument("--api-key",    default="", help="API Key（也可通过环境变量传入）")
    parser.add_argument("--base-url",   default="", help="自定义 Base URL（也可通过环境变量传入）")
    parser.add_argument("--model",      default="", help="模型名称（也可通过环境变量传入，否则用默认值）")
    parser.add_argument("--types",      default="white_bg,key_features,selling_pt,material,lifestyle,model,multi_scene",
                        help="逗号分隔的套图类型")
    parser.add_argument("--output-dir", default="./output/raw/")
    args = parser.parse_args()

    # Resolve API key
    api_key = args.api_key or os.environ.get(ENV_KEYS[args.provider], "")
    if not api_key:
        print(f"❌ 未找到 {args.provider} 的 API Key。请通过 --api-key 参数或环境变量 {ENV_KEYS[args.provider]} 传入。", file=sys.stderr)
        sys.exit(1)

    # Resolve base URL
    base_url = args.base_url or os.environ.get(ENV_URLS[args.provider], "")

    # Resolve model
    model = resolve_model(args.provider, args.model)
    print(f"📦 供应商: {args.provider}  模型: {model}")

    product = json.loads(args.product)
    desc = product.get("product_description_for_prompt", "product")
    selling_points = product.get("selling_points", [])
    types = [t.strip() for t in args.types.split(",")]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    generator = GENERATORS[args.provider]
    results = {}

    for type_id in types:
        print(f"⏳ 生成 [{type_id}]...", flush=True)
        try:
            prompt = build_prompt(type_id, desc, selling_points)
            img_bytes = generator(api_key, prompt, base_url, model)
            out_path = output_dir / f"{type_id}_raw.jpg"
            out_path.write_bytes(img_bytes)
            results[type_id] = {"status": "ok", "path": str(out_path)}
            print(f"  ✅ 已保存到 {out_path}")
        except Exception as e:
            results[type_id] = {"status": "error", "error": str(e)}
            print(f"  ❌ 失败: {e}", file=sys.stderr)

    # Output summary JSON for downstream scripts
    summary_path = output_dir / "generate_result.json"
    with open(summary_path, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n📋 生成结果摘要已保存到 {summary_path}")

    ok = [k for k, v in results.items() if v["status"] == "ok"]
    fail = [k for k, v in results.items() if v["status"] == "error"]
    print(f"✅ 成功 {len(ok)} 张，❌ 失败 {len(fail)} 张")


if __name__ == "__main__":
    main()
