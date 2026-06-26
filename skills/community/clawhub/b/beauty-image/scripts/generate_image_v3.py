#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
"""
V10.4 商业化图片生成器 — 意图识别 + 模板 + 结构化Prompt + 智能路由

作者: 圆规
GitHub: https://github.com/xyva-yuangui/beauty-image
License: MIT

升级要点 (vs V2):
  1. 精准意图识别: 30+场景自动匹配 (规则快速路径 + LLM深度解析)
  2. 结构化Prompt: 6层结构 (核心→主体→风格→光照→构图→技术)
  3. 30+场景模板: 名片/海报/头像/产品/水晶/毛绒/天气卡片/分镜...
  4. 15+风格词典: 赛博朋克/水墨/浮世绘/吉卜力/等距微缩...
  5. 智能引擎路由: 按场景+风格自动选wanx/seedream4/seedream5
  6. 自适应尺寸: 按场景类型自动推荐比例

用法:
  # 智能模式 (自动识别意图+模板+路由)
  uv run generate_image_v3.py --prompt "帮我做一张赛博朋克风格的个人名片"
  uv run generate_image_v3.py --prompt "画一只猫的水晶质感手办"
  uv run generate_image_v3.py --prompt "上海天气卡片"

  # 指定场景模板
  uv run generate_image_v3.py --prompt "猫" --scene 3d_crystal
  uv run generate_image_v3.py --prompt "日本武士" --scene art_ukiyoe_card --style 浮世绘

  # 指定字段 (JSON)
  uv run generate_image_v3.py --prompt "名片" --scene biz_card --fields '{"name":"圆规","title":"CEO","company":"XyvaClaw"}'

  # 兼容V2模式 (直接传prompt, 无模板)
  uv run generate_image_v3.py --prompt "一幅美丽的风景画" --raw

  # 列出可用模板/风格
  uv run generate_image_v3.py --list-scenes
  uv run generate_image_v3.py --list-styles
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 添加当前目录到path以导入模块
sys.path.insert(0, str(Path(__file__).parent))

from image_prompt_templates import (
    build_prompt, list_scenes, list_styles, resolve_scene, resolve_style,
    QUALITY_NEGATIVE, QUALITY_SUFFIX, SCENE_TEMPLATES,
)
from image_intent_parser import parse_intent, generate_confirmation_message


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# API Key 管理 (复用V2逻辑)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_wanx_key() -> str | None:
    """获取通义万相 API Key

    查找顺序:
      1. 环境变量 DASHSCOPE_API_KEY
      2. ~/.openclaw/openclaw.json → models.providers.wanxiang.apiKey
    
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


def get_deepseek_key() -> str | None:
    """获取DeepSeek API Key (用于意图解析, 可选)

    查找顺序:
      1. 环境变量 DEEPSEEK_API_KEY
      2. ~/.openclaw/openclaw.json → models.providers.deepseek.apiKey

    获取地址: https://platform.deepseek.com/api_keys
    """
    key = os.environ.get("DEEPSEEK_API_KEY")
    if key:
        return key
    try:
        config_path = Path.home() / ".openclaw" / "openclaw.json"
        with open(config_path) as f:
            config = json.load(f)
        return config.get("models", {}).get("providers", {}).get("deepseek", {}).get("apiKey")
    except Exception:
        return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 尺寸预设
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Seedream 尺寸预设 (2K/3K 高分辨率)
SIZE_PRESETS = {
    "2K": "2048x2048", "2K_16:9": "2848x1600", "2K_9:16": "1600x2848",
    "2K_4:3": "2304x1728", "2K_3:4": "1728x2304",
    "2K_2:3": "1672x2512", "2K_3:2": "2512x1672",
    "2K_1:2": "1448x2896", "2K_2:1": "2896x1448",
    "2K_21:9": "3128x1344", "2K_9:21": "1344x3128",
    "3K": "3072x3072", "3K_16:9": "4096x2304", "3K_9:16": "2304x4096",
    "3K_4:3": "3456x2592", "3K_3:4": "2592x3456",
}

# wan2.6 尺寸限制: 总像素在 [1280*1280, 1440*1440] 之间, 宽高比 [1:4, 4:1]
# 支持 15 种比例 — 官方推荐5种 + 扩展10种
WANX_SIZE_MAP = {
    # 官方推荐尺寸
    "1:1":  "1280*1280",
    "3:4":  "1104*1472",
    "4:3":  "1472*1104",
    "9:16": "960*1696",
    "16:9": "1696*960",
    # 扩展尺寸 (经过像素总量验证)
    "2:3":  "1048*1568",
    "3:2":  "1568*1048",
    "1:2":  "904*1816",
    "2:1":  "1808*912",
    "9:21": "840*1960",
    "21:9": "1952*840",
    "1:3":  "744*2224",
    "3:1":  "2216*744",
    "1:4":  "640*2560",
    "4:1":  "2560*640",
}

# 用户友好别名 → 比例名
SIZE_ALIASES = {
    # 正方形
    "正方": "1:1", "square": "1:1", "头像": "1:1",
    # 横向
    "横版": "16:9", "风景": "16:9", "landscape": "16:9",
    "宽屏": "21:9", "ultrawide": "21:9", "电影": "21:9", "cinematic": "21:9",
    "横幅": "3:1", "banner": "3:1", "横幅海报": "3:1",
    "超宽": "4:1", "全景": "4:1", "panorama": "4:1",
    # 竖向
    "竖版": "9:16", "portrait": "9:16", "手机壁纸": "9:16",
    "竖屏": "9:21", "长图": "9:21",
    "海报": "2:3", "poster": "2:3",
    "长海报": "1:3", "长图海报": "1:3",
    "超长": "1:4", "滚动长图": "1:4",
    # 常见设备
    "小红书": "3:4", "xhs": "3:4",
    "A4": "3:4", "a4": "3:4",
    "PPT": "16:9", "ppt": "16:9", "幻灯片": "16:9",
    "名片": "16:9", "card": "16:9",
}

# Seedream/通用尺寸→wanx合法尺寸的自动降级映射
WANX_SIZE_FALLBACK = {
    "2K": "1280*1280", "2K_16:9": "1696*960", "2K_9:16": "960*1696",
    "2K_4:3": "1472*1104", "2K_3:4": "1104*1472",
    "2K_2:3": "1048*1568", "2K_3:2": "1568*1048",
    "2K_1:2": "904*1816", "2K_2:1": "1808*912",
    "2K_21:9": "1952*840", "2K_9:21": "840*1960",
    "3K": "1280*1280", "3K_16:9": "1696*960", "3K_9:16": "960*1696",
    "3K_4:3": "1472*1104", "3K_3:4": "1104*1472",
}


def resolve_size(size_input: str, provider: str) -> str:
    """解析尺寸参数

    支持多种格式:
      - 比例: "1:1", "16:9", "9:16", "2:3", "1:4" 等
      - 别名: "横版", "竖版", "海报", "全景", "小红书", "PPT" 等
      - 预设: "2K", "2K_16:9", "3K" 等 (seedream用)
      - 直接尺寸: "1280*1280", "1696x960" 等
    wanx自动缩放到合法像素范围, seedream直接使用高分辨率。
    """
    import math
    normalized = size_input.strip()

    # Step 1: 别名解析
    if normalized in SIZE_ALIASES:
        normalized = SIZE_ALIASES[normalized]

    if provider == "wanx":
        # Step 2a: 直接查wanx比例表
        if normalized in WANX_SIZE_MAP:
            return WANX_SIZE_MAP[normalized]
        # Step 2b: 查seedream降级表
        if normalized in WANX_SIZE_FALLBACK:
            return WANX_SIZE_FALLBACK[normalized]
        # Step 2c: 解析预设或直接尺寸, 自动缩放
        resolved = SIZE_PRESETS.get(normalized, normalized).replace("x", "*")
        try:
            parts = resolved.split("*")
            w, h = int(parts[0]), int(parts[1])
            total = w * h
            ratio = w / h
            min_px, max_px = 1280 * 1280, 1440 * 1440
            # 检查宽高比限制
            if ratio < 0.25 or ratio > 4.0:
                return "1280*1280"
            if min_px <= total <= max_px:
                return f"{w}*{h}"
            # 缩放到合法范围 (8像素对齐)
            target = min_px
            new_h = int(math.sqrt(target / ratio))
            new_h = (new_h // 8) * 8
            new_w = int(new_h * ratio)
            new_w = (new_w // 8) * 8
            if new_w * new_h < min_px:
                new_h += 8
            return f"{new_w}*{new_h}"
        except (ValueError, IndexError):
            return "1280*1280"
    else:
        # Seedream: 支持高分辨率
        if normalized in WANX_SIZE_MAP:
            # 比例名 → seedream用对应的2K尺寸
            ratio_to_2k = {
                "1:1": "2K", "16:9": "2K_16:9", "9:16": "2K_9:16",
                "4:3": "2K_4:3", "3:4": "2K_3:4",
                "2:3": "2K_2:3", "3:2": "2K_3:2",
                "1:2": "2K_1:2", "2:1": "2K_2:1",
                "21:9": "2K_21:9", "9:21": "2K_9:21",
            }
            preset_key = ratio_to_2k.get(normalized)
            if preset_key and preset_key in SIZE_PRESETS:
                return SIZE_PRESETS[preset_key].replace("*", "x")
        resolved = SIZE_PRESETS.get(normalized, normalized)
        return resolved.replace("*", "x")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 引擎路由
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ENGINE_MODEL_MAP = {
    "wanx": "wan2.6-t2i",         # 主力: 同步调用, 新协议
    "wanx_fallback": "wan2.5-t2i-preview",  # 备选: 异步调用, 旧协议
    "seedream4": "doubao-seedream-4-0-250828",
    "seedream5": "doubao-seedream-5-0-260128",
}

# wan2.6 尺寸要求: 总像素在[1280*1280, 1440*1440]之间, 宽高比[1:4, 4:1]
# wan2.5 同wan2.6 — 完整尺寸表见上方 WANX_SIZE_MAP (15种比例)
WAN26_SIZE_PRESETS = WANX_SIZE_MAP


def select_engine(recommended: str, fallback: str, force_engine: str | None = None) -> str:
    """选择最终引擎 (检查key可用性)"""
    if force_engine:
        return force_engine

    ark_ok = bool(get_ark_key())
    wanx_ok = bool(get_wanx_key())

    if recommended.startswith("seedream") and ark_ok:
        return recommended
    if recommended == "wanx" and wanx_ok:
        return recommended

    # 降级
    if fallback.startswith("seedream") and ark_ok:
        return fallback
    if fallback == "wanx" and wanx_ok:
        return fallback

    # 最终降级
    if wanx_ok:
        return "wanx"
    if ark_ok:
        return "seedream4"

    # 无任何可用key, 仍返回wanx让后续generate_wanx给出详细错误提示
    return "wanx"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 图片生成 API 调用
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_wanx(prompt: str, negative: str, size: str, filename: str | None,
                  no_prompt_extend: bool, watermark: bool) -> dict:
    """通义万相图片生成 — wan2.6同步(主) + wan2.5异步(备)"""
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
    size_str = resolve_size(size, "wanx")

    # ── 优先: wan2.6-t2i 同步调用 (新协议, 一次请求直接返回图片) ──
    model_26 = ENGINE_MODEL_MAP["wanx"]
    print(f"🎨 [万相 {model_26}] 同步生成中...")
    print(f"  Prompt: {prompt[:100]}...")
    print(f"  Negative: {negative[:60]}...")
    print(f"  Size: {size_str}")

    payload_26 = {
        "model": model_26,
        "input": {
            "messages": [{"role": "user", "content": [{"text": prompt}]}]
        },
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

        # wan2.6失败, 尝试降级到wan2.5
        err_msg = ""
        try:
            err_msg = resp.json().get("message", resp.text[:200])
        except Exception:
            err_msg = resp.text[:200]
        print(f"  ⚠️ wan2.6失败 ({resp.status_code}: {err_msg}), 降级到wan2.5...")

    except Exception as e:
        print(f"  ⚠️ wan2.6异常 ({e}), 降级到wan2.5...")

    # ── 降级: wan2.5-t2i-preview 异步调用 (旧协议, 需轮询) ──
    return _generate_wanx_legacy(prompt, negative, size_str, filename, api_key, requests)


def _generate_wanx_legacy(prompt: str, negative: str, size_str: str,
                          filename: str | None, api_key: str, requests_mod) -> dict:
    """wan2.5-t2i-preview 异步调用 (旧协议fallback)"""
    import time

    model_25 = ENGINE_MODEL_MAP["wanx_fallback"]
    print(f"\n🎨 [万相 {model_25}] 异步生成中...")

    payload = {
        "model": model_25,
        "input": {"prompt": prompt, "negative_prompt": negative},
        "parameters": {"size": size_str, "n": 1},
    }

    resp = requests_mod.post(
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "X-DashScope-Async": "enable",
        },
        json=payload, timeout=30,
    )

    if resp.status_code != 200:
        try:
            return {"success": False, "error": f"wan2.5提交失败: {resp.json().get('message', '?')}"}
        except Exception:
            return {"success": False, "error": f"HTTP {resp.status_code}: {resp.text[:200]}"}

    task_id = resp.json().get("output", {}).get("task_id")
    if not task_id:
        return {"success": False, "error": f"未返回task_id"}

    print(f"  任务已提交: {task_id}")

    # 轮询 (最长120秒)
    for i in range(40):
        time.sleep(3)
        try:
            r = requests_mod.get(
                f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=15,
            )
            task_result = r.json()
        except Exception as e:
            print(f"  轮询异常: {e}")
            continue

        status = task_result.get("output", {}).get("task_status", "UNKNOWN")
        if i % 3 == 0:
            print(f"  等待中... ({(i+1)*3}s, 状态: {status})")

        if status == "SUCCEEDED":
            # 旧协议: output.results[0].url
            results = task_result.get("output", {}).get("results", [])
            if results and results[0].get("url"):
                return _finalize(results[0]["url"], filename, model_25, requests_mod)
            # 新协议兼容: output.choices[0].message.content[0].image
            choices = task_result.get("output", {}).get("choices", [])
            if choices:
                content = choices[0].get("message", {}).get("content", [])
                if content and content[0].get("image"):
                    return _finalize(content[0]["image"], filename, model_25, requests_mod)
            return {"success": False, "error": "任务成功但无图片URL"}

        elif status in ("FAILED", "UNKNOWN"):
            err_msg = task_result.get("output", {}).get("message", "未知错误")
            return {"success": False, "error": f"任务失败: {err_msg}"}

    return {"success": False, "error": "轮询超时 (120s)"}


def generate_seedream(prompt: str, model: str, size: str, filename: str | None,
                      watermark: bool, sequential: str, max_images: int,
                      optimize_prompt_mode: str) -> dict:
    """Seedream图片生成"""
    import requests

    api_key = get_ark_key()
    if not api_key:
        return {
            "success": False,
            "error": (
                "缺少火山引擎 ARK API Key。\n"
                "请通过以下方式之一配置:\n"
                "  1. 设置环境变量: export ARK_API_KEY=your-key\n"
                "  2. 在 ~/.openclaw/openclaw.json 中配置: models.providers.ark.apiKey\n"
                "获取地址: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey"
            ),
        }
    size_str = resolve_size(size, "seedream")

    payload = {
        "model": model,
        "prompt": prompt,
        "size": size_str,
        "watermark": watermark,
        "response_format": "url",
    }
    if sequential != "disabled":
        payload["sequential_image_generation"] = sequential
        if max_images > 1:
            payload["sequential_image_generation_options"] = {"max_images": max_images}
    if model in ("doubao-seedream-5-0-260128", "doubao-seedream-4.5", "doubao-seedream-4-0-250828"):
        payload["optimize_prompt_options"] = {"mode": optimize_prompt_mode}
    if model == "doubao-seedream-5-0-260128":
        payload["output_format"] = "png"

    model_short = model.replace("doubao-seedream-", "SD")
    print(f"🎨 [{model_short}] 生成中...")
    print(f"  Prompt: {prompt[:100]}...")
    print(f"  Size: {size_str}")

    resp = requests.post(
        "https://ark.cn-beijing.volces.com/api/v3/images/generations",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        json=payload, timeout=180,
    )

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
        return {"success": False, "error": "无返回图片"}

    images = []
    for item in data:
        if item.get("url"):
            images.append({"url": item["url"], "size": item.get("size", size_str)})
        elif item.get("error"):
            images.append({"error": item["error"].get("message", "未知错误")})

    if not images:
        return {"success": False, "error": "未解析到图片"}

    first_url = images[0].get("url")
    if filename and first_url:
        return _finalize(first_url, filename, model_short, requests, extra_images=images[1:])

    return {
        "success": True, "provider": model,
        "images": images, "image_count": len(images),
    }


def _finalize(image_url: str, filename: str | None, provider: str,
              requests_mod, extra_images: list | None = None) -> dict:
    """下载+保存+输出"""
    result = {"success": True, "provider": provider, "image_url": image_url}
    print(f"\n✅ 图片生成成功!")
    print(f"Image URL: {image_url}")

    if filename:
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
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
        for img in extra_images:
            if img.get("url"):
                print(f"MEDIA_URL: {img['url']}")

    return result


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 主流程
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def smart_generate(user_input: str, scene: str | None = None, style: str | None = None,
                   fields: dict | None = None, force_engine: str | None = None,
                   size: str | None = None, quality: str = "high",
                   filename: str | None = None, raw: bool = False,
                   no_prompt_extend: bool = False, watermark: bool = False,
                   sequential: str = "disabled", max_images: int = 1,
                   optimize_prompt: str = "standard", use_llm: bool = False) -> dict:
    """V3 智能图片生成主流程

    流程: 意图解析 → 模板匹配 → Prompt构建 → 引擎路由 → 生成
    """

    # ── Step 0: Raw模式 (兼容V2, 直接生成) ──
    if raw:
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in user_input)
        lang = "zh" if has_chinese else "en"
        suffix = QUALITY_SUFFIX.get(quality, QUALITY_SUFFIX["standard"])[lang]
        prompt = user_input
        if "8K" not in prompt and "高清" not in prompt:
            prompt += suffix
        negative = QUALITY_NEGATIVE.get(quality, QUALITY_NEGATIVE["standard"])
        engine = force_engine or ("seedream4" if get_ark_key() else "wanx")
        size = size or "2K"

        print(f"📝 [Raw模式] 直接生成")
        return _do_generate(prompt, negative, engine, size, filename,
                           no_prompt_extend, watermark, sequential, max_images, optimize_prompt)

    # ── Step 1: 意图解析 ──
    print(f"🔍 解析意图: \"{user_input[:60]}...\"")

    if scene:
        # 用户显式指定场景
        intent = {
            "scene_id": scene,
            "style": style,
            "subject": user_input,
            "fields": fields or {"subject": user_input},
            "missing_fields": [],
            "confidence": 1.0,
            "method": "explicit",
        }
    else:
        # 自动解析
        ds_key = get_deepseek_key() if use_llm else None
        if use_llm and not ds_key:
            print("⚠️ --use-llm 已启用但未找到 DEEPSEEK_API_KEY，将使用规则快速路径解析")
            print("   获取地址: https://platform.deepseek.com/api_keys")
        intent = parse_intent(user_input, use_llm=use_llm, api_key=ds_key)
        if style:
            intent["style"] = style
        if fields:
            intent["fields"].update(fields)

    scene_id = intent.get("scene_id")
    style_name = intent.get("style")
    parsed_fields = intent.get("fields", {})

    # 确保subject存在
    if "subject" not in parsed_fields:
        parsed_fields["subject"] = intent.get("subject", user_input)

    print(f"  场景: {scene_id or '通用'} | 风格: {style_name or '默认'} | 方法: {intent.get('method', '?')}")
    print(f"  置信度: {intent.get('confidence', 0):.1%}")

    # ── Step 2: 构建Prompt ──
    build_result = build_prompt(scene_id, style_name, parsed_fields, quality)

    prompt = build_result["prompt"]
    negative = build_result["negative"]
    recommended_engine = build_result["engine"]
    fallback_engine = build_result["fallback_engine"]
    recommended_size = build_result["size"]
    scene_name = build_result["scene_name"]

    print(f"\n📋 模板: {scene_name}")
    print(f"  推荐引擎: {recommended_engine} | 备选: {fallback_engine}")
    print(f"  推荐尺寸: {recommended_size}")

    # ── Step 3: 引擎路由 ──
    engine = select_engine(recommended_engine, fallback_engine, force_engine)
    final_size = size or recommended_size

    print(f"  最终引擎: {engine} | 尺寸: {final_size}")

    # ── Step 4: 生成 ──
    return _do_generate(prompt, negative, engine, final_size, filename,
                       no_prompt_extend, watermark, sequential, max_images, optimize_prompt)


def _do_generate(prompt: str, negative: str, engine: str, size: str,
                 filename: str | None, no_prompt_extend: bool, watermark: bool,
                 sequential: str, max_images: int, optimize_prompt: str) -> dict:
    """执行实际的图片生成调用"""
    try:
        if engine == "wanx":
            return generate_wanx(prompt, negative, size, filename, no_prompt_extend, watermark)
        elif engine in ("seedream4", "seedream5"):
            model = ENGINE_MODEL_MAP[engine]
            return generate_seedream(prompt, model, size, filename, watermark,
                                    sequential, max_images, optimize_prompt)
        else:
            return {"success": False, "error": f"未知引擎: {engine}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser(description="V10.4 商业化图片生成器")

    # 主参数
    parser.add_argument("--prompt", "-p", help="图片描述 / 用户自然语言输入")
    parser.add_argument("--scene", help="指定场景模板ID (如: biz_card, 3d_crystal)")
    parser.add_argument("--style", help="指定风格 (如: 赛博朋克, 水墨画, 吉卜力)")
    parser.add_argument("--fields", help="模板字段 (JSON格式, 如: '{\"name\":\"圆规\"}')")

    # 引擎/质量
    parser.add_argument("--engine", choices=["wanx", "seedream4", "seedream5"],
                        help="强制指定引擎 (默认: 模板推荐)")
    parser.add_argument("--size", "-s", help="尺寸 (如: 2K, 2K_16:9, 3K, wanx_1:1)")
    parser.add_argument("--quality", "-q", choices=["high", "standard"], default="high")

    # 模式
    parser.add_argument("--raw", action="store_true",
                        help="Raw模式: 跳过意图解析, 直接用prompt生成 (兼容V2)")
    parser.add_argument("--use-llm", action="store_true",
                        help="启用LLM意图解析 (低置信度时调用DeepSeek)")

    # 输出
    parser.add_argument("--filename", "-f", help="保存到文件")
    parser.add_argument("--no-prompt-extend", action="store_true")
    parser.add_argument("--watermark", action="store_true")

    # Seedream特有
    parser.add_argument("--sequential", choices=["auto", "disabled"], default="disabled")
    parser.add_argument("--max-images", type=int, default=1)
    parser.add_argument("--optimize-prompt", choices=["standard", "fast"], default="standard")

    # 列表
    parser.add_argument("--list-scenes", action="store_true", help="列出所有场景模板")
    parser.add_argument("--list-styles", action="store_true", help="列出所有风格")
    parser.add_argument("--list-providers", action="store_true", help="列出可用引擎")
    parser.add_argument("--list-sizes", action="store_true", help="列出所有支持的尺寸和比例")

    args = parser.parse_args()

    # ── 列表模式 ──
    if args.list_scenes:
        print("📋 可用场景模板:")
        scenes = list_scenes()
        categories = {}
        for s in scenes:
            categories.setdefault(s["category"], []).append(s)
        for cat, items in categories.items():
            print(f"\n  [{cat}]")
            for item in items:
                print(f"    {item['id']:24s} {item['name']:10s}  引擎={item['engine']:10s}  尺寸={item['size']}")
        return

    if args.list_styles:
        print("🎨 可用风格:")
        for style_name in list_styles():
            print(f"  - {style_name}")
        return

    if args.list_providers:
        wanx_ok = bool(get_wanx_key())
        ark_ok = bool(get_ark_key())
        ds_ok = bool(get_deepseek_key())
        print("可用图片生成引擎:")
        print(f"  {'✅' if wanx_ok else '❌'} wanx      — 通义万相 wan2.6-t2i (阿里云)")
        print(f"  {'✅' if ark_ok else '❌'} seedream4 — doubao-seedream-4.0 (火山引擎)")
        print(f"  {'✅' if ark_ok else '❌'} seedream5 — doubao-seedream-5-0-260128 (火山引擎, 最高画质)")
        print(f"\n可选增强:")
        print(f"  {'✅' if ds_ok else 'ℹ️'} DeepSeek  — LLM深度意图解析 (--use-llm, 可选)")
        if not wanx_ok:
            print(f"\n  💡 设置 DASHSCOPE_API_KEY 以启用万相引擎")
            print(f"     获取: https://dashscope.console.aliyun.com/apiKey")
        if not ark_ok:
            print(f"\n  💡 设置 ARK_API_KEY 以启用 Seedream 引擎")
            print(f"     获取: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey")
        if not wanx_ok and not ark_ok:
            print(f"\n  ⚠️ 至少需要配置一个 API Key 才能使用图片生成功能")
        print(f"\n  作者: 圆规 | https://github.com/xyva-yuangui/beauty-image")
        return

    if args.list_sizes:
        print("📐 支持的尺寸和比例:\n")
        print("  [wanx 万相] (总像素 1280*1280 ~ 1440*1440)")
        for ratio, size in WANX_SIZE_MAP.items():
            w, h = size.split("*")
            orient = "■" if w == h else ("▬" if int(w) > int(h) else "▮")
            print(f"    {orient} {ratio:>5s}  →  {size}")
        print(f"\n  [seedream] (2K/3K 高分辨率)")
        for name, size in SIZE_PRESETS.items():
            print(f"    {name:>10s}  →  {size}")
        print(f"\n  [中文别名] (自动映射到比例)")
        alias_groups = {}
        for alias, ratio in SIZE_ALIASES.items():
            alias_groups.setdefault(ratio, []).append(alias)
        for ratio, aliases in alias_groups.items():
            print(f"    {ratio:>5s}  ←  {', '.join(aliases)}")
        print(f"\n  用法: --size 16:9 / --size 海报 / --size 小红书 / --size 全景 / --size 1280*720")
        return

    # ── 生成模式 ──
    if not args.prompt:
        parser.error("--prompt is required for image generation")

    fields = {}
    if args.fields:
        try:
            fields = json.loads(args.fields)
        except json.JSONDecodeError:
            print(f"❌ --fields 必须是合法的JSON格式", file=sys.stderr)
            sys.exit(1)

    result = smart_generate(
        user_input=args.prompt,
        scene=args.scene,
        style=args.style,
        fields=fields,
        force_engine=args.engine,
        size=args.size,
        quality=args.quality,
        filename=args.filename,
        raw=args.raw,
        no_prompt_extend=args.no_prompt_extend,
        watermark=args.watermark,
        sequential=args.sequential,
        max_images=args.max_images,
        optimize_prompt=args.optimize_prompt,
        use_llm=args.use_llm,
    )

    if not result.get("success"):
        print(f"\n❌ 生成失败: {result.get('error', '未知错误')}", file=sys.stderr)
        sys.exit(1)

    print(f"\nRESULT_JSON: {json.dumps(result, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
