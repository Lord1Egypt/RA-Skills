#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import concurrent.futures
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

IMAGE_SKILL_FILE = str(Path(__file__).resolve().parent / "modules" / "coze_generate_image.py")
IMAGE_SKILL_RUN = [sys.executable, IMAGE_SKILL_FILE]


def fail(msg: str):
    print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False, indent=2))
    sys.exit(1)


def normalize_text(raw: str) -> str:
    raw = re.sub(r"^回复\s+\S+:\s*", "", (raw or "").strip())
    prefixes = [
        "仅规划listing：", "仅规划listing:", "仅规划listing",
        "生成listing：", "生成listing:", "生成listing",
        "生成亚马逊listing：", "生成亚马逊listing:", "生成亚马逊listing",
        "生成Amazon Listing：", "生成Amazon Listing:", "生成Amazon Listing",
        "listing工厂：", "listing工厂:", "listing工厂",
    ]
    for p in prefixes:
        if raw.startswith(p):
            return raw[len(p):].strip()
    return raw


def detect_plan_only(raw: str) -> bool:
    text = (raw or "").strip()
    keys = ["仅规划listing", "只规划listing", "不生成图片", "plan only", "listing规划"]
    return any(k in text for k in keys)


def try_parse_json(text: str):
    text = (text or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def extract_urls(text: str):
    return re.findall(r'https?://[^\s,，]+', text or "")


def clean_candidate_product(text: str) -> str:
    text = (text or "").strip()
    splitters = [
        "，突出", ",突出", "，卖点", ",卖点", "，希望突出", ",希望突出",
        "，输出", ",输出", "，出图数", ",出图数", "，美国站", ",美国站",
        "，英国站", ",英国站", "，德国站", ",德国站", "，日本站", ",日本站",
        "，Amazon US", ",Amazon US", "，Amazon UK", ",Amazon UK",
        "，Amazon DE", ",Amazon DE", "，Amazon JP", ",Amazon JP", "，Amazon", ",Amazon",
    ]
    for s in splitters:
        if s in text:
            text = text.split(s, 1)[0].strip()
    text = re.sub(r'(美国站|英国站|德国站|日本站|Amazon US|Amazon UK|Amazon DE|Amazon JP|Amazon)$', '', text, flags=re.I).strip()
    text = re.sub(r'(输出\d+张图|出图数[:：]?\d+)$', '', text, flags=re.I).strip()
    return text.strip(" ，,。.？?：:")


def parse_input_rule(text: str):
    raw = normalize_text(text)
    result = {
        "product_name": "",
        "brand": "",
        "market": "Amazon US",
        "selling_points": [],
        "confirmed_facts": [],
        "image_urls": [],
        "notes": raw,
        "image_count": 6,
        "plan_only": detect_plan_only(text),
    }

    maybe_json = try_parse_json(raw)
    if isinstance(maybe_json, dict):
        result["product_name"] = maybe_json.get("product_name", "") or ""
        result["brand"] = maybe_json.get("brand", "") or ""
        result["market"] = maybe_json.get("market", "Amazon US") or "Amazon US"
        result["selling_points"] = maybe_json.get("selling_points", []) or []
        result["confirmed_facts"] = maybe_json.get("confirmed_facts", []) or []
        result["image_urls"] = maybe_json.get("image_urls", []) or []
        result["notes"] = maybe_json.get("notes", raw) or raw
        result["image_count"] = int(maybe_json.get("image_count", 6) or 6)
        result["plan_only"] = bool(maybe_json.get("plan_only", result["plan_only"]))
        return result

    urls = extract_urls(raw)
    if urls:
        result["image_urls"] = urls

    m_name = re.search(r'^(?:产品|品名|product_name)\s*[:：]\s*(.+)$', raw, re.I | re.M)
    if m_name:
        result["product_name"] = clean_candidate_product(m_name.group(1).strip())

    m_brand = re.search(r'^(?:品牌|brand)\s*[:：]\s*(.+)$', raw, re.I | re.M)
    if m_brand:
        result["brand"] = m_brand.group(1).strip()

    m_market = re.search(r'^(?:市场|站点|market)\s*[:：]\s*(.+)$', raw, re.I | re.M)
    if m_market:
        result["market"] = m_market.group(1).strip()

    if "美国站" in raw or "Amazon US" in raw or "美国" in raw:
        result["market"] = "Amazon US"
    elif "英国站" in raw or "Amazon UK" in raw or "英国" in raw:
        result["market"] = "Amazon UK"
    elif "德国站" in raw or "Amazon DE" in raw or "德国" in raw:
        result["market"] = "Amazon DE"
    elif "日本站" in raw or "Amazon JP" in raw or "日本" in raw:
        result["market"] = "Amazon JP"

    m_image_count = re.search(r'(?:出图数|image_count|输出)\s*[:：=]?\s*(2|6)', raw, re.I)
    if m_image_count:
        result["image_count"] = int(m_image_count.group(1))

    points, facts, mode = [], [], None
    for line in raw.splitlines():
        t = line.strip()
        if not t:
            continue
        if re.match(r'^(卖点|selling_points|希望突出)\s*[:：]?$', t, re.I):
            mode = "points"
            continue
        if re.match(r'^(已确认事实|confirmed_facts)\s*[:：]?$', t, re.I):
            mode = "facts"
            continue
        if re.match(r'^(产品|品名|product_name|品牌|brand|市场|站点|market|产品图|图片|image_urls|备注|notes|出图数|image_count)\s*[:：]?', t, re.I):
            mode = None
            continue
        t2 = re.sub(r'^[0-9]+[\.、)\-]\s*', '', t)
        t2 = re.sub(r'^[-*]\s*', '', t2)
        if not t2:
            continue
        if mode == "points":
            points.append(t2)
        elif mode == "facts":
            facts.append(t2)

    if not result["product_name"]:
        result["product_name"] = clean_candidate_product(raw.replace("\n", " ").strip())

    result["selling_points"] = points[:8]
    result["confirmed_facts"] = facts[:12]
    return result


def ensure_env_file():
    skill_dir = Path(__file__).resolve().parent
    env_file = skill_dir / ".env"
    env_template = skill_dir / "ENV_TEMPLATE.txt"
    if env_file.exists():
        return env_file
    if env_template.exists():
        env_file.write_text(env_template.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        env_file.write_text(
            "LISTING_API_KEY=\n"
            "LISTING_BASE_URL=\n"
            "LISTING_MODEL=\n\n"
            "COZE_TOKEN=\n"
            "COZE_WORKFLOW_ID=\n"
            "COZE_API_URL=https://api.coze.cn/v1/workflow/run\n"
            "MIHE_KEY=\n",
            encoding="utf-8",
        )
    return env_file


def load_env_file(path: Path):
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def get_config():
    env_file = ensure_env_file()
    file_env = load_env_file(env_file)
    api_key = (
        os.environ.get("LISTING_API_KEY", "").strip()
        or os.environ.get("OPENAI_API_KEY", "").strip()
        or os.environ.get("MOONSHOT_API_KEY", "").strip()
        or os.environ.get("KIMI_API_KEY", "").strip()
        or file_env.get("LISTING_API_KEY", "").strip()
        or file_env.get("OPENAI_API_KEY", "").strip()
        or file_env.get("MOONSHOT_API_KEY", "").strip()
        or file_env.get("KIMI_API_KEY", "").strip()
    )
    base_url = (
        os.environ.get("LISTING_BASE_URL", "").strip()
        or os.environ.get("OPENAI_BASE_URL", "").strip()
        or os.environ.get("MOONSHOT_BASE_URL", "").strip()
        or file_env.get("LISTING_BASE_URL", "").strip()
        or file_env.get("OPENAI_BASE_URL", "").strip()
        or file_env.get("MOONSHOT_BASE_URL", "").strip()
        or "https://api.openai.com/v1"
    ).rstrip("/")
    model = (
        os.environ.get("LISTING_MODEL", "").strip()
        or os.environ.get("OPENAI_MODEL", "").strip()
        or os.environ.get("MOONSHOT_MODEL", "").strip()
        or file_env.get("LISTING_MODEL", "").strip()
        or file_env.get("OPENAI_MODEL", "").strip()
        or file_env.get("MOONSHOT_MODEL", "").strip()
        or "gpt-4o-mini"
    )
    return {"api_key": api_key, "base_url": base_url, "model": model, "env_path": str(env_file), "file_env": file_env}


def extract_json_block(text: str):
    text = (text or "").strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(text[start:end+1])
    raise ValueError("LLM 输出不是合法 JSON")


def call_openai_compatible(messages, response_json=True):
    cfg = get_config()
    if not cfg["api_key"]:
        env_path = cfg["env_path"]
        fail(
            "未检测到文案模型配置。\n\n"
            f"请先编辑这个文件：\n{env_path}\n\n"
            "至少填写这三项：\n"
            "LISTING_API_KEY=你的key\n"
            "LISTING_BASE_URL=你的接口地址\n"
            "LISTING_MODEL=你的模型名\n\n"
            "自动生图不是必填。\n"
            "如果你想启用自动生图，再继续填写：\n"
            "COZE_TOKEN\n"
            "COZE_WORKFLOW_ID\n"
            "COZE_API_URL\n"
            "MIHE_KEY\n\n"
            "如需图片生成 Key，可前往：miheai.com/s/98707"
        )
    payload = {"model": cfg["model"], "messages": messages}
    if response_json:
        payload["response_format"] = {"type": "json_object"}
    url = f'{cfg["base_url"]}/chat/completions'
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={"Authorization": f'Bearer {cfg["api_key"]}', "Content-Type": "application/json"},
    )
    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode("utf-8")
            except Exception:
                body = str(e)
            last_error = f"HTTP {getattr(e, 'code', 'unknown')}: {body}"
            if getattr(e, "code", None) == 429 and attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            fail(f"模型请求失败：{last_error}")
        except Exception as e:
            last_error = str(e)
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            fail(f"模型请求失败：{last_error}")
    fail(f"模型请求失败：{last_error or 'unknown error'}")


def semantic_parse_input(raw_text: str, rule_result: dict):
    system_prompt = """
你是一个 Amazon Listing 输入语义识别器。

任务：
把用户自然语言输入，整理成标准 JSON 字段，供后续 listing 生成使用。

要求：
1. 只做字段识别、归一、清洗。
2. 不要脑补产品事实。
3. “卖点/希望突出”只能放入 selling_points。
4. 只有用户明确说出的事实，才能放入 confirmed_facts。
5. 市场统一归一为 Amazon US / Amazon UK / Amazon DE / Amazon JP。
6. 如果产品名称不明确，尽量从语义中提取最核心产品名，但不要把整句话当产品名。
7. 输出必须是合法 JSON。

输出 schema：
{
  "product_name": "",
  "brand": "",
  "market": "Amazon US",
  "selling_points": [],
  "confirmed_facts": [],
  "image_urls": [],
  "notes": "",
  "image_count": 6
}
""".strip()
    user_prompt = json.dumps({"raw_text": raw_text, "rule_result": rule_result}, ensure_ascii=False)
    content = call_openai_compatible([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ], response_json=True)
    parsed = extract_json_block(content)
    result = {
        "product_name": parsed.get("product_name", "") or rule_result.get("product_name", ""),
        "brand": parsed.get("brand", "") or rule_result.get("brand", ""),
        "market": parsed.get("market", "") or rule_result.get("market", "Amazon US"),
        "selling_points": parsed.get("selling_points", []) or rule_result.get("selling_points", []),
        "confirmed_facts": parsed.get("confirmed_facts", []) or rule_result.get("confirmed_facts", []),
        "image_urls": parsed.get("image_urls", []) or rule_result.get("image_urls", []),
        "notes": parsed.get("notes", "") or rule_result.get("notes", raw_text),
        "image_count": int(parsed.get("image_count", rule_result.get("image_count", 6)) or 6),
        "plan_only": bool(rule_result.get("plan_only", False)),
    }
    result["product_name"] = clean_candidate_product(result["product_name"])
    result["selling_points"] = [str(x).strip() for x in result.get("selling_points", []) if str(x).strip()][:8]
    result["confirmed_facts"] = [str(x).strip() for x in result.get("confirmed_facts", []) if str(x).strip()][:12]
    result["image_urls"] = [str(x).strip() for x in result.get("image_urls", []) if str(x).strip()]
    if result["market"] not in ["Amazon US", "Amazon UK", "Amazon DE", "Amazon JP"]:
        result["market"] = "Amazon US"
    if result["image_count"] not in [2, 6]:
        result["image_count"] = 6
    return result


def call_llm_listing(data: dict):
    system_prompt = """
你是资深 Amazon Listing 策划专家 + 亚马逊转化结构设计师 + 电商视觉导演。

你的任务：
针对任意产品，基于“已确认事实 + 卖点方向 + 参考图”，输出一整套 Amazon Listing 方案。

核心原则：
1. 这是通用类目版本，禁止默认假设固定类目。
2. 输出要更符合 Amazon 当前以“用户意图 / 购买任务 / 使用场景匹配”为核心的商品表达方式，而不是机械堆砌关键词。
3. 但“意图表达”不等于可以脑补事实。所有未确认信息都不能写成硬事实。
4. “卖点/希望突出”只能视为营销方向，不等于已确认事实。
5. 图片输出必须适合 Amazon Listing 制作流程，默认给 1 张主图 + 5 张副图结构。
6. 禁止出现强CTA，例如 Add to Cart / Buy Now / Shop Now / 立即加入购物车 / 立即购买。

严格禁止脑补：
7. 无法确认的点一律禁止脑补，包括但不限于：尺寸、容量、时长、温度保持时长、材质等级升级、医用级/食品级认证、内部结构、杯口结构、是否适配车载杯架、是否单手操作、是否可放入背包侧袋、是否适合某类饮品、是否适合某类细分场景。
8. 禁止把“营销方向”写成“产品事实”。
9. 如果某个方向没有事实支撑，只能写成抽象转化表达，不能写成具体使用承诺。

输出风格要求：
10. 标题要像 Amazon 标题，但必须克制，不要堆砌无依据关键词，不要写明显 AI 味长句。
11. Bullets 必须优先写已确认事实 + 相对安全的利益表达，不要写具体性能承诺。
12. 图片规划必须写清“这张图解决什么转化问题”，但禁止默认输出剖面图、爆炸图、结构拆解图、信息图，除非输入里明确给出结构事实。
13. 视频脚本禁止写具体未确认动作，例如放入车载杯架、单手开合、放入包中无泄漏、会议桌/健身房/车内等细场景，除非输入明确给出。
14. 默认优先输出“通用、安全、跨类目可复用”的结构，不要写成某个类目的专用模板。
15. 输出必须是合法 JSON，不允许输出解释。

输出 schema：
{
  "title": {"en": "...", "zh": "..."},
  "bullets": [
    {"en":"...","zh":"..."},
    {"en":"...","zh":"..."},
    {"en":"...","zh":"..."},
    {"en":"...","zh":"..."},
    {"en":"...","zh":"..."}
  ],
  "images": [
    {"label":"主图","bullet_index":0,"goal_zh":"...","goal_en":"...","conversion_task_zh":"...","prompt_en":"..."}
  ],
  "video_script": {
    "hook_en":"...","hook_zh":"...","scene_1_en":"...","scene_1_zh":"...","scene_2_en":"...","scene_2_zh":"...","scene_3_en":"...","scene_3_zh":"...","ending_en":"...","ending_zh":"..."
  }
}
""".strip()
    content = call_openai_compatible([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(data, ensure_ascii=False)},
    ], response_json=True)
    plan = extract_json_block(content)
    imgs = plan.get("images", []) or []
    if len(imgs) > data.get("image_count", 6):
        plan["images"] = imgs[:data.get("image_count", 6)]
    return plan


def sanitize_output_markdown(text: str) -> str:
    replacements = {
        "Add to cart today.": "Learn more about this product.",
        "Add to cart now.": "Learn more about this product.",
        "Click Add to Cart now.": "Explore product details.",
        "Buy now.": "Explore product details.",
        "Shop now.": "Explore product details.",
        "Order now.": "Explore product details.",
        "立即加入购物车。": "了解更多产品信息。",
        "立即点击加入购物车。": "了解更多产品信息。",
        "立即购买。": "了解更多产品信息。",
        "现在购买。": "了解更多产品信息。",
        "medical-grade": "high-grade",
        "food-grade": "quality-focused",
        "BPA-free": "material-focused",
        "dishwasher-safe": "easy-care oriented",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    for pattern, repl in [
        (r'\bAdd to Cart\b', 'Learn more'),
        (r'\bBuy Now\b', 'Explore details'),
        (r'\bShop Now\b', 'Explore details'),
        (r'\bOrder Now\b', 'Explore details'),
        (r'立即加入购物车', '了解更多产品信息'),
        (r'立即购买', '了解更多产品信息'),
        (r'现在购买', '了解更多产品信息'),
    ]:
        text = re.sub(pattern, repl, text, flags=re.I)
    return text


def zh_prompt_from_label(label: str, goal_zh: str) -> str:
    if label == "主图":
        return "亚马逊合规主图：只展示一个完整产品，所有功能部件都装在产品上；纯白背景，产品居中完整展示，画面占比约85%，偏正面3/4英雄角度，高写实商业产品摄影；禁止文字、箭头、信息图、剖切图、爆炸图、拆件图、额外道具、额外产品、生活场景。"
    return goal_zh or "用于亚马逊卖点副图的高端商业产品摄影图，真实电商拍摄风格。"


def call_single_image_skill(image_item: dict, image_urls: list, file_env: dict):
    prompt_en = (image_item.get("prompt_en", "") or "").strip()
    label = image_item.get("label", "") or "未命名图片"
    payload = {
        "prompt": prompt_en,
        "image_urls": image_urls,
        "key": os.environ.get("MIHE_KEY", "").strip() or file_env.get("MIHE_KEY", "").strip() or os.environ.get("COZE_IMAGE_WORKFLOW_KEY", "").strip() or file_env.get("COZE_IMAGE_WORKFLOW_KEY", "").strip(),
        "link_only": True,
        "label": label,
    }
    try:
        proc = subprocess.run(
            IMAGE_SKILL_RUN + [json.dumps(payload, ensure_ascii=False)],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(Path(__file__).resolve().parent),
        )
        stdout = (proc.stdout or "").strip()
        stderr = (proc.stderr or "").strip()
        if proc.returncode != 0:
            return {
                "ok": False,
                "label": label,
                "bullet_index": image_item.get("bullet_index", 0),
                "goal_zh": image_item.get("goal_zh", ""),
                "goal_en": image_item.get("goal_en", ""),
                "prompt_en": prompt_en,
                "prompt_zh": zh_prompt_from_label(label, image_item.get("goal_zh", "")),
                "error": stderr or stdout or f"image subprocess failed: {proc.returncode}",
            }
        raw = try_parse_json(stdout)
        if not isinstance(raw, dict):
            return {
                "ok": False,
                "label": label,
                "bullet_index": image_item.get("bullet_index", 0),
                "goal_zh": image_item.get("goal_zh", ""),
                "goal_en": image_item.get("goal_en", ""),
                "prompt_en": prompt_en,
                "prompt_zh": zh_prompt_from_label(label, image_item.get("goal_zh", "")),
                "error": stdout or "生图模块返回的不是合法 JSON",
            }
        result = {
            "ok": bool(raw.get("ok")),
            "label": label,
            "bullet_index": image_item.get("bullet_index", 0),
            "goal_zh": image_item.get("goal_zh", ""),
            "goal_en": image_item.get("goal_en", ""),
            "prompt_en": prompt_en,
            "prompt_zh": zh_prompt_from_label(label, image_item.get("goal_zh", "")),
            "raw": raw,
        }
        if raw.get("url"):
            result["url"] = raw.get("url")
        if raw.get("msg"):
            result["msg"] = raw.get("msg")
        return result
    except Exception as e:
        return {
            "ok": False,
            "label": label,
            "bullet_index": image_item.get("bullet_index", 0),
            "goal_zh": image_item.get("goal_zh", ""),
            "goal_en": image_item.get("goal_en", ""),
            "prompt_en": prompt_en,
            "prompt_zh": zh_prompt_from_label(label, image_item.get("goal_zh", "")),
            "error": str(e),
        }


def build_answer(plan: dict, image_results: list, image_state: dict):
    title = plan.get("title", {}) or {}
    bullets = plan.get("bullets", []) or []
    video = plan.get("video_script", {}) or {}
    lines = []
    lines.append("TITLE / 标题")
    lines.append("| 字段 | 内容 |")
    lines.append("|---|---|")
    lines.append(f"| EN | {title.get('en', '')} |")
    lines.append(f"| ZH | {title.get('zh', '')} |")
    lines.append("")
    lines.append("BULLETS / 五点")
    lines.append("| 序号 | EN | ZH |")
    lines.append("|---|---|---|")
    for i, b in enumerate(bullets, 1):
        lines.append(f"| {i} | {b.get('en', '')} | {b.get('zh', '')} |")
    lines.append("")
    lines.append("VIDEO SCRIPT / 主图视频脚本")
    lines.append("| 模块 | EN | ZH |")
    lines.append("|---|---|---|")
    for label, key in [("Hook", "hook"), ("Scene 1", "scene_1"), ("Scene 2", "scene_2"), ("Scene 3", "scene_3"), ("Ending", "ending")]:
        lines.append(f"| {label} | {video.get(key + '_en', '')} | {video.get(key + '_zh', '')} |")
    lines.append("")
    lines.append("IMAGE SET / 图片结果")
    lines.append("| 图名 | 对应Bullet | 中文目标 | 链接 |")
    lines.append("|---|---|---|---|")
    if image_results:
        for item in image_results:
            lines.append(f"| {item.get('label', '')} | {item.get('bullet_index', '')} | {item.get('goal_zh', '')} | {item.get('url', item.get('error', item.get('msg', ''))) } |")
    else:
        lines.append(f"| 未自动生图 | - | {image_state.get('reason', '')} | - |")
    lines.append("")
    if image_state.get("enabled") and image_results:
        lines.append("图片已生成，链接有效期以图床实际返回为准。")
    else:
        lines.append(image_state.get("reason", "未执行自动生图。"))
    return sanitize_output_markdown("\n".join(lines))


def image_env_status(file_env: dict, plan_only: bool):
    if plan_only:
        return {"enabled": False, "reason": "已识别为仅规划模式，本次不执行自动生图。", "executed": False}
    token = os.environ.get("COZE_TOKEN", "").strip() or file_env.get("COZE_TOKEN", "").strip()
    workflow_id = os.environ.get("COZE_WORKFLOW_ID", "").strip() or file_env.get("COZE_WORKFLOW_ID", "").strip()
    mihe_key = (
        os.environ.get("MIHE_KEY", "").strip() or file_env.get("MIHE_KEY", "").strip()
        or os.environ.get("COZE_IMAGE_WORKFLOW_KEY", "").strip() or file_env.get("COZE_IMAGE_WORKFLOW_KEY", "").strip()
    )
    if not token or not workflow_id or not mihe_key:
        return {"enabled": False, "reason": "未检测到图片环境变量（COZE_TOKEN / COZE_WORKFLOW_ID / MIHE_KEY）", "executed": False}
    if not os.path.exists(IMAGE_SKILL_FILE):
        return {"enabled": False, "reason": f"图片模块不存在：{IMAGE_SKILL_FILE}", "executed": False}
    return {"enabled": True, "reason": "已检测到图片环境变量，开始自动生图。", "executed": True}


def main():
    raw = sys.argv[1] if len(sys.argv) >= 2 else ""
    if not raw.strip():
        print(json.dumps({
            "ok": False,
            "error": "缺少输入参数",
            "help": "Amazon Listing Factory",
            "example_simple": 'bash run.sh "生成listing：充电宝，美国站，突出便携、大容量、安全感，输出6张图"',
            "example_structured": 'bash run.sh "生成listing\n产品：充电宝\n市场：美国站\n希望突出：\n1. 便携\n2. 大容量\n3. 安全感\n出图数：6"'
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    parsed_rule = parse_input_rule(raw)
    parsed = semantic_parse_input(raw, parsed_rule)
    if not parsed.get("product_name"):
        fail("未识别产品名称，请直接输入产品名，或使用“产品：xxx”的格式。")
    plan = call_llm_listing(parsed)
    cfg = get_config()
    file_env = cfg["file_env"]
    image_state = image_env_status(file_env, parsed.get("plan_only", False))
    image_results = []
    if image_state.get("enabled"):
        images = (plan.get("images", []) or [])[: parsed.get("image_count", 6)]
        max_workers = min(6, max(1, len(images)))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(call_single_image_skill, img, parsed.get("image_urls", []), file_env) for img in images]
            for future in concurrent.futures.as_completed(futures):
                image_results.append(future.result())
        order = {(img.get("label", ""), img.get("bullet_index", 0)): i for i, img in enumerate((plan.get("images", []) or [])[: parsed.get("image_count", 6)])}
        image_results.sort(key=lambda x: order.get((x.get("label", ""), x.get("bullet_index", 0)), 999))
    answer = build_answer(plan, image_results, image_state)
    print(json.dumps({
        "ok": True,
        "answer": answer,
        "title": plan.get("title", {}),
        "bullets": plan.get("bullets", []),
        "video_script": plan.get("video_script", {}),
        "images": image_results,
        "parsed": parsed,
        "image_generation": image_state,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
