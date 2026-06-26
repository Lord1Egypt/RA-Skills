#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
"""
V10.2 Multi-Provider Image Generator — 多源图片生成器 (性价比优化)

作者: 圆规
GitHub: https://github.com/xyva-yuangui/beauty-image
License: MIT

支持:
  1. 通义万相 (Wanx 2.6) — 阿里云 DashScope (成本最低, 通用)
  2. doubao-seedream-4.0 — 火山引擎 ARK (性价比最佳)
  3. doubao-seedream-5.0-lite — 火山引擎 ARK (最高画质, 成本最高)

性价比排序: wanx(经济) < seedream4(均衡) < seedream5(旗舰)

auto模式智能选择:
  - standard质量 → wanx (成本最低)
  - high质量 → seedream4 (质量/成本最佳平衡)
  - 显式指定 seedream5 → seedream5 (旗舰画质)

用法:
  uv run generate_image_v2.py --prompt "描述" [--provider auto|wanx|seedream5|seedream4] [--quality high|standard]
  uv run generate_image_v2.py --prompt "描述" --provider seedream5 --size 3K --quality high
  uv run generate_image_v2.py --prompt "描述" --provider seedream5 --sequential auto --max-images 4
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# API Key 管理
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_wanx_key() -> str | None:
    """获取通义万相 API Key

    查找顺序:
      1. 环境变量 DASHSCOPE_API_KEY
      2. ~/.openclaw/openclaw.json → models.providers.wanxiang.apiKey
    
    注意: Bailian Coding Plan key (sk-sp-) 不支持万相图片生成API, 会自动跳过。
    获取地址: https://dashscope.console.aliyun.com/apiKey
    """
    key = os.environ.get("DASHSCOPE_API_KEY")
    if key:
        return key
    try:
        config_path = Path.home() / ".openclaw" / "openclaw.json"
        with open(config_path) as f:
            config = json.load(f)
        key = config.get("models", {}).get("providers", {}).get("wanxiang", {}).get("apiKey")
        if key and not key.startswith("sk-sp-"):
            return key
    except Exception:
        pass
    return None


def get_ark_key() -> str | None:
    """获取火山引擎 ARK API Key (Seedream 模型)

    查找顺序:
      1. 环境变量 ARK_API_KEY 或 VOLC_API_KEY
      2. ~/.openclaw/openclaw.json → models.providers.ark.apiKey

    获取地址: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey
    """
    key = os.environ.get("ARK_API_KEY") or os.environ.get("VOLC_API_KEY")
    if key:
        return key
    try:
        config_path = Path.home() / ".openclaw" / "openclaw.json"
        with open(config_path) as f:
            config = json.load(f)
        for provider_name in ["ark", "volcengine", "doubao"]:
            key = config.get("models", {}).get("providers", {}).get(provider_name, {}).get("apiKey")
            if key:
                return key
    except Exception:
        pass
    return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 质量优化 Prompt 增强
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUALITY_ENHANCERS = {
    "high": {
        "prefix": "",
        "suffix_zh": "，高清细腻，光影层次丰富，构图精美，色彩和谐，专业摄影级画质，8K超高清",
        "suffix_en": ", ultra high definition, rich lighting and shadows, exquisite composition, harmonious colors, professional photography quality, 8K UHD",
        "negative": "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，AI感明显，构图混乱，文字模糊扭曲，噪点，模糊，过曝，欠曝",
    },
    "standard": {
        "prefix": "",
        "suffix_zh": "，画面清晰，构图合理",
        "suffix_en": ", clear image, good composition",
        "negative": "低分辨率，低画质，肢体畸形，手指畸形，蜡像感，构图混乱，文字模糊",
    },
}

SIZE_PRESETS = {
    # Seedream 5.0 lite / 4.5 / 4.0
    "2K": "2048x2048",
    "2K_16:9": "2848x1600",
    "2K_9:16": "1600x2848",
    "2K_4:3": "2304x1728",
    "2K_3:4": "1728x2304",
    "3K": "3072x3072",
    "3K_16:9": "4096x2304",
    "3K_9:16": "2304x4096",
    "3K_4:3": "3456x2592",
    "3K_3:4": "2592x3456",
    # Wanx sizes (use * separator)
    "wanx_16:9": "1664*928",
    "wanx_1:1": "1024*1024",
    "wanx_9:16": "720*1280",
}


def enhance_prompt(prompt: str, quality: str = "high") -> str:
    """增强 prompt 以提高图片质量"""
    enhancer = QUALITY_ENHANCERS.get(quality, QUALITY_ENHANCERS["standard"])
    # 检测语言
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in prompt)
    suffix = enhancer["suffix_zh"] if has_chinese else enhancer["suffix_en"]
    # 避免重复追加
    if "8K" in prompt or "高清" in prompt or "UHD" in prompt:
        return prompt
    return prompt + suffix


def resolve_size(size_input: str, provider: str) -> str:
    """解析尺寸参数"""
    if size_input in SIZE_PRESETS:
        resolved = SIZE_PRESETS[size_input]
    else:
        resolved = size_input

    # Wanx 使用 * 分隔符
    if provider == "wanx":
        return resolved.replace("x", "*")
    # Seedream 使用 x 分隔符
    return resolved.replace("*", "x")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Provider: 通义万相 (Wanx 2.6)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_wanx(prompt: str, size: str, quality: str, filename: str | None,
                  no_prompt_extend: bool, watermark: bool) -> dict:
    """通义万相图片生成"""
    import requests

    api_key = get_wanx_key()
    if not api_key:
        return {
            "success": False,
            "error": (
                "缺少通义万相 API Key (DASHSCOPE_API_KEY)。\n"
                "请通过以下方式之一配置:\n"
                "  1. 设置环境变量: export DASHSCOPE_API_KEY=your-key\n"
                "  2. 在 ~/.openclaw/openclaw.json 中配置: models.providers.wanxiang.apiKey\n"
                "获取地址: https://dashscope.console.aliyun.com/apiKey"
            ),
        }

    enhanced = enhance_prompt(prompt, quality)
    negative = QUALITY_ENHANCERS[quality]["negative"]
    size_str = resolve_size(size, "wanx")

    # ── 优先: wan2.6-t2i 同步调用 (新协议) ──
    model_26 = "wan2.6-t2i"
    print(f"🎨 [万相 {model_26}] 同步生成中...")
    print(f"  Prompt: {enhanced[:80]}...")
    print(f"  Size: {size_str}")

    payload_26 = {
        "model": model_26,
        "input": {"messages": [{"role": "user", "content": [{"text": enhanced}]}]},
        "parameters": {
            "negative_prompt": negative,
            "prompt_extend": not no_prompt_extend,
            "watermark": watermark,
            "size": size_str,
            "n": 1,
        },
    }

    try:
        resp = requests.post(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
            json=payload_26, timeout=120,
        )
        if resp.status_code == 200:
            result = resp.json()
            choices = result.get("output", {}).get("choices", [])
            if choices:
                content = choices[0].get("message", {}).get("content", [])
                if content and content[0].get("image"):
                    return _finalize(content[0]["image"], filename, model_26, requests)
            return {"success": False, "error": f"wan2.6响应无图片: {result}"}

        err_msg = ""
        try:
            err_msg = resp.json().get("message", resp.text[:200])
        except Exception:
            err_msg = resp.text[:200]
        print(f"  ⚠️ wan2.6失败 ({resp.status_code}: {err_msg}), 降级到wan2.5...")
    except Exception as e:
        print(f"  ⚠️ wan2.6异常 ({e}), 降级到wan2.5...")

    # ── 降级: wan2.5-t2i-preview 异步调用 (旧协议) ──
    import time
    model_25 = "wan2.5-t2i-preview"
    print(f"\n🎨 [万相 {model_25}] 异步生成中...")

    payload_25 = {
        "model": model_25,
        "input": {"prompt": enhanced, "negative_prompt": negative},
        "parameters": {"size": size_str, "n": 1},
    }

    try:
        resp = requests.post(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}", "X-DashScope-Async": "enable"},
            json=payload_25, timeout=30,
        )
        if resp.status_code != 200:
            return {"success": False, "error": f"wan2.5提交失败: {resp.json().get('message', '?')}"}

        task_id = resp.json().get("output", {}).get("task_id")
        if not task_id:
            return {"success": False, "error": "未返回task_id"}

        print(f"  任务已提交: {task_id}")
        for i in range(40):
            time.sleep(3)
            r = requests.get(
                f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}",
                headers={"Authorization": f"Bearer {api_key}"}, timeout=15,
            )
            task_result = r.json()
            status = task_result.get("output", {}).get("task_status", "UNKNOWN")
            if i % 3 == 0:
                print(f"  等待中... ({(i+1)*3}s, 状态: {status})")
            if status == "SUCCEEDED":
                results = task_result.get("output", {}).get("results", [])
                if results and results[0].get("url"):
                    return _finalize(results[0]["url"], filename, model_25, requests)
                return {"success": False, "error": "任务成功但无图片URL"}
            elif status in ("FAILED", "UNKNOWN"):
                return {"success": False, "error": f"任务失败: {task_result.get('output', {}).get('message', '?')}"}

        return {"success": False, "error": "轮询超时 (120s)"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Provider: Seedream (火山引擎 ARK)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_seedream(prompt: str, model: str, size: str, quality: str,
                      filename: str | None, watermark: bool,
                      sequential: str, max_images: int,
                      optimize_prompt_mode: str) -> dict:
    """Seedream 5.0 lite / 4.0 图片生成"""
    import requests

    api_key = get_ark_key()
    if not api_key:
        return {
            "success": False,
            "error": "缺少火山引擎 ARK API Key。请设置环境变量 ARK_API_KEY 或在 openclaw.json 中配置 models.providers.ark.apiKey。获取地址: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey",
        }

    enhanced = enhance_prompt(prompt, quality)
    size_str = resolve_size(size, "seedream")

    api_url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    payload = {
        "model": model,
        "prompt": enhanced,
        "size": size_str,
        "watermark": watermark,
        "response_format": "url",
    }

    # 组图配置
    if sequential != "disabled":
        payload["sequential_image_generation"] = sequential
        if max_images > 1:
            payload["sequential_image_generation_options"] = {"max_images": max_images}

    # 提示词优化
    if model in ("doubao-seedream-5.0-lite", "doubao-seedream-4.5", "doubao-seedream-4.0"):
        payload["optimize_prompt_options"] = {"mode": optimize_prompt_mode}

    # 输出格式 (仅5.0支持)
    if model == "doubao-seedream-5.0-lite":
        payload["output_format"] = "png"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    model_short = model.replace("doubao-seedream-", "SD")
    print(f"🎨 [{model_short}] 生成中...")
    print(f"  Prompt: {enhanced[:80]}...")
    print(f"  Size: {size_str}")
    if sequential != "disabled":
        print(f"  组图模式: {sequential} (max={max_images})")

    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=180)

        if resp.status_code != 200:
            try:
                err = resp.json()
                return {"success": False, "error": f"HTTP {resp.status_code}: {err.get('error', {}).get('message', resp.text[:200])}"}
            except Exception:
                return {"success": False, "error": f"HTTP {resp.status_code}: {resp.text[:200]}"}

        result = resp.json()

        if result.get("error"):
            return {"success": False, "error": result["error"].get("message", str(result["error"]))}

        data = result.get("data", [])
        if not data:
            return {"success": False, "error": "无返回图片", "raw": result}

        # 处理多图
        images = []
        for i, item in enumerate(data):
            if item.get("url"):
                images.append({"url": item["url"], "size": item.get("size", size_str)})
            elif item.get("b64_json"):
                images.append({"b64_json": item["b64_json"][:50] + "...", "size": item.get("size", size_str)})
            elif item.get("error"):
                images.append({"error": item["error"].get("message", "未知错误")})

        if not images:
            return {"success": False, "error": "未解析到图片"}

        # 下载第一张 (如指定filename)
        first_url = images[0].get("url") if images else None
        if filename and first_url:
            return _finalize(first_url, filename, model_short, requests, extra_images=images[1:])

        # 输出usage
        usage = result.get("usage", {})

        return {
            "success": True,
            "provider": model,
            "images": images,
            "image_count": len(images),
            "usage": {
                "generated_images": usage.get("generated_images", len(images)),
                "output_tokens": usage.get("output_tokens", 0),
            },
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 通用工具
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _finalize(image_url: str, filename: str | None, provider: str, requests_mod,
              extra_images: list | None = None) -> dict:
    """下载+保存+输出"""
    result = {"success": True, "provider": provider, "image_url": image_url}

    print(f"\n✅ 图片生成成功!")
    print(f"Image URL: {image_url}")

    if filename:
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        print("Downloading image...")
        img_resp = requests_mod.get(image_url, timeout=60)
        img_resp.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(img_resp.content)
        full_path = output_path.resolve()
        result["local_path"] = str(full_path)
        print(f"Saved to: {full_path}")
        print(f"MEDIA: {full_path}")
    else:
        print(f"MEDIA_URL: {image_url}")

    if extra_images:
        result["extra_images"] = extra_images
        for i, img in enumerate(extra_images, 2):
            if img.get("url"):
                print(f"MEDIA_URL: {img['url']}")

    return result


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser(description="V10 Multi-Provider Image Generator")
    parser.add_argument("--prompt", "-p", required="--list-providers" not in sys.argv, help="图片描述")
    parser.add_argument("--provider", choices=["wanx", "seedream5", "seedream4", "auto"],
                        default="auto", help="图片生成引擎 (默认auto: 有ARK Key用seedream5, 否则wanx)")
    parser.add_argument("--size", "-s", default="2K",
                        help="尺寸: 2K, 3K, 2K_16:9, 2K_9:16, 或具体WxH如2048x2048")
    parser.add_argument("--quality", "-q", choices=["high", "standard"], default="high",
                        help="质量级别 (默认high: 8K级增强prompt)")
    parser.add_argument("--filename", "-f", help="输出文件名 (不指定则仅返回URL)")
    parser.add_argument("--no-prompt-extend", action="store_true", help="禁用平台侧prompt增强")
    parser.add_argument("--watermark", action="store_true", help="添加水印")
    parser.add_argument("--sequential", choices=["auto", "disabled"], default="disabled",
                        help="组图模式 (仅Seedream, auto=自动判断)")
    parser.add_argument("--max-images", type=int, default=1, help="最大图片数 (组图模式, 1-15)")
    parser.add_argument("--optimize-prompt", choices=["standard", "fast"], default="standard",
                        help="Seedream提示词优化模式")
    parser.add_argument("--list-providers", action="store_true", help="列出可用引擎")
    args = parser.parse_args()

    if args.list_providers:
        wanx_ok = bool(get_wanx_key())
        ark_ok = bool(get_ark_key())
        print("可用图片生成引擎:")
        print(f"  {'✅' if wanx_ok else '❌'} wanx      — 通义万相 wan2.6-t2i (阿里云)")
        print(f"  {'✅' if ark_ok else '❌'} seedream5 — doubao-seedream-5.0-lite (火山引擎, 最高画质)")
        print(f"  {'✅' if ark_ok else '❌'} seedream4 — doubao-seedream-4.0 (火山引擎)")
        if not wanx_ok:
            print("\n  💡 设置 DASHSCOPE_API_KEY 以启用万相引擎")
            print("     获取: https://dashscope.console.aliyun.com/apiKey")
        if not ark_ok:
            print("\n  💡 设置 ARK_API_KEY 以启用 Seedream 引擎")
            print("     获取: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey")
        if not wanx_ok and not ark_ok:
            print("\n  ⚠️ 至少需要配置一个 API Key 才能使用图片生成功能")
        return

    # V10.2: 性价比优化的auto选择
    provider = args.provider
    if provider == "auto":
        ark_key = get_ark_key()
        if args.quality == "high" and ark_key:
            # 高画质 + 有ARK Key → seedream4 (性价比最佳)
            provider = "seedream4"
        elif args.quality == "standard" or not ark_key:
            # 标准画质 或 无ARK Key → wanx (成本最低)
            provider = "wanx"
        else:
            provider = "seedream4"
        print(f"💡 auto选择: {provider} (quality={args.quality})")
    elif provider == "seedream5":
        print(f"💡 旗舰模式: seedream5 (最高画质, 成本较高)")

    if provider == "wanx":
        result = generate_wanx(args.prompt, args.size, args.quality, args.filename,
                               args.no_prompt_extend, args.watermark)
    elif provider == "seedream5":
        result = generate_seedream(args.prompt, "doubao-seedream-5.0-lite", args.size,
                                   args.quality, args.filename, args.watermark,
                                   args.sequential, args.max_images, args.optimize_prompt)
    elif provider == "seedream4":
        result = generate_seedream(args.prompt, "doubao-seedream-4-0-250828", args.size,
                                   args.quality, args.filename, args.watermark,
                                   args.sequential, args.max_images, args.optimize_prompt)
    else:
        print(f"未知 provider: {provider}", file=sys.stderr)
        sys.exit(1)

    if not result.get("success"):
        print(f"\n❌ 生成失败: {result.get('error', '未知错误')}", file=sys.stderr)
        sys.exit(1)

    # 输出JSON结果供程序解析
    print(f"\nRESULT_JSON: {json.dumps(result, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
