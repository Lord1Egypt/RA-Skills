#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


def output(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def normalize_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r'^回复\s+\S+:\s*', '', text)
    text = re.sub(r'^/\S+\s*', '', text)
    text = re.sub(r'@[\w\-\u4e00-\u9fa5]+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


COUNTRY_MAP = {
    "美国": "US美国",
    "us": "US美国",
    "usa": "US美国",
    "united states": "US美国",
    "英国": "UK英国",
    "uk": "UK英国",
    "united kingdom": "UK英国",
    "德国": "德国",
    "germany": "德国",
    "日本": "日本",
    "japan": "日本",
    "法国": "法国",
    "france": "法国",
    "加拿大": "加拿大",
    "canada": "加拿大",
    "澳大利亚": "澳大利亚",
    "australia": "澳大利亚",
    "意大利": "意大利",
    "italy": "意大利",
    "西班牙": "西班牙",
    "spain": "西班牙",
    "墨西哥": "墨西哥",
    "mexico": "墨西哥",
    "马来西亚": "马来西亚",
    "malaysia": "马来西亚",
    "新加坡": "新加坡",
    "singapore": "新加坡"
}

PLATFORMS = {
    "amazon": "Amazon",
    "亚马逊": "Amazon",
    "shopee": "Shopee",
    "lazada": "Lazada",
    "tiktok shop": "TikTok Shop",
    "tiktok": "TikTok Shop",
    "temu": "Temu",
    "walmart": "Walmart"
}

SOP_SECTIONS = [
    "1. 市场宏观分析",
    "2. 电商平台竞争结构",
    "3. 头部品牌分析",
    "4. Amazon竞品分析",
    "5. 关键词需求分析",
    "6. 用户需求分析",
    "7. 用户评价分析",
    "8. 产品成本结构",
    "9. 认证要求",
    "10. 专利风险",
    "11. 用户画像",
    "12. 使用场景",
    "13. 产品机会分析",
    "14. 风险分析",
    "15. SWOT分析",
    "16. PEST分析",
    "17. 市场进入评分",
    "18. 最终建议",
]


def split_kv_segments(text: str):
    parts = re.split(r'[\n；;]+', text)
    return [p.strip() for p in parts if p.strip()]


def parse_structured_input(text: str):
    product_name = ""
    market_country = ""
    platform = ""

    for line in split_kv_segments(text):
        parts = re.split(r'[:：]', line, maxsplit=1)
        if len(parts) != 2:
            continue

        key = parts[0].strip().lower()
        value = parts[1].strip()

        if any(k in key for k in ["商品名称", "产品名称", "产品", "品名", "product"]):
            product_name = value
        elif any(k in key for k in ["目标市场", "国家", "市场", "market", "country"]):
            market_country = value
        elif any(k in key for k in ["销售平台", "平台", "platform"]):
            platform = value

    return product_name, market_country, platform


def detect_platform(text: str) -> str:
    lower = text.lower()
    for k, v in PLATFORMS.items():
        if k in lower:
            return v
    return "Amazon"


def detect_country(text: str) -> str:
    lower = text.lower()
    for k, v in COUNTRY_MAP.items():
        if k in lower:
            return v
    return ""


def guess_product_name_from_english(text: str) -> str:
    lower = text.lower().strip()

    patterns = [
        r'^(?:research|analyze|analyse|study|check)\s+(.+?)\s+in\s+(?:the\s+)?(?:us|usa|united states|uk|united kingdom|germany|japan|france|canada|australia|italy|spain|mexico|malaysia|singapore)\s+(?:amazon|shopee|lazada|temu|walmart|tiktok shop)?\s*market?$',
        r'^(?:research|analyze|analyse|study|check)\s+(.+?)\s+for\s+(?:amazon|shopee|lazada|temu|walmart|tiktok shop)\s+in\s+(?:the\s+)?(?:us|usa|united states|uk|united kingdom|germany|japan|france|canada|australia|italy|spain|mexico|malaysia|singapore)\s*$',
    ]

    for pattern in patterns:
        m = re.search(pattern, lower, re.IGNORECASE)
        if m:
            candidate = m.group(1).strip(" ,.?;:")
            if candidate:
                return candidate

    cleaned = re.sub(
        r'\b(research|analyze|analyse|study|check|market|for|in|amazon|shopee|lazada|temu|walmart|tiktok shop)\b',
        ' ',
        lower,
        flags=re.IGNORECASE
    )
    cleaned = re.sub(
        r'\b(us|usa|united states|uk|united kingdom|germany|japan|france|canada|australia|italy|spain|mexico|malaysia|singapore|the)\b',
        ' ',
        cleaned,
        flags=re.IGNORECASE
    )
    cleaned = re.sub(r'\s+', ' ', cleaned).strip(" ,.?;:")
    return cleaned


def guess_product_name(text: str) -> str:
    patterns = [
        r'调研一下\s*(.*?)\s*在',
        r'分析一下\s*(.*?)\s*在',
        r'分析\s*(.*?)\s*在',
        r'我想做\s*(.*?)\s*，',
        r'我想做\s*(.*?)\s*在',
        r'帮我做一个\s*(.*?)\s*在',
        r'帮我调研\s*(.*?)\s*在',
        r'帮我研究\s*(.*?)\s*在',
        r'看看\s*(.*?)\s*在',
        r'看一下\s*(.*?)\s*在',
        r'研究一下\s*(.*?)\s*在',
        r'做一份\s*(.*?)\s*在',
    ]

    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            candidate = m.group(1).strip(" ，,。.？?：:")
            if candidate:
                return candidate

    if re.search(r'[A-Za-z]', text):
        candidate = guess_product_name_from_english(text)
        if candidate:
            return candidate

    cleaned = text
    cleaned = re.sub(
        r'帮我|给我|做一份|做个|做一个|调研一下|调研|分析一下|分析|研究一下|研究|看看|看一下|值不值得做|能不能做|市场调研|选品分析|报告',
        '',
        cleaned,
        flags=re.IGNORECASE
    )
    cleaned = re.sub(
        r'Amazon|amazon|亚马逊|Shopee|shopee|Lazada|lazada|TikTok Shop|tiktok shop|Temu|temu|Walmart|walmart',
        '',
        cleaned,
        flags=re.IGNORECASE
    )
    cleaned = re.sub(
        r'美国|英国|德国|日本|法国|加拿大|澳大利亚|意大利|西班牙|墨西哥|马来西亚|新加坡|US|USA|UK|Germany|Japan|France|Canada|Australia|Italy|Spain|Mexico|Malaysia|Singapore',
        '',
        cleaned,
        flags=re.IGNORECASE
    )
    cleaned = re.sub(r'在.*$', '', cleaned).strip(" ，,。.？?：:")
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def normalize_market(market: str) -> str:
    if not market:
        return ""
    lower = market.strip().lower()
    return COUNTRY_MAP.get(lower, market.strip())


def normalize_platform(platform: str) -> str:
    if not platform:
        return ""
    lower = platform.strip().lower()
    return PLATFORMS.get(lower, platform.strip())


def parse_input(text: str):
    normalized = normalize_text(text)

    product_name, market_country, platform = parse_structured_input(text)

    if not market_country:
        market_country = detect_country(normalized)

    if not platform:
        platform = detect_platform(normalized)

    if not product_name:
        product_name = guess_product_name(normalized)

    market_country = normalize_market(market_country)
    platform = normalize_platform(platform)

    return product_name, market_country, platform, normalized


def get_config():
    skill_dir = Path(__file__).resolve().parent
    env_path = skill_dir / ".env"

    api_key = os.environ.get("MARKET_API_KEY", "").strip()
    base_url = os.environ.get("MARKET_BASE_URL", "").strip().rstrip("/")
    model = os.environ.get("MARKET_MODEL", "").strip()

    if not base_url:
        base_url = "https://api.moonshot.cn/v1"
    if not model:
        model = "kimi-k2.5"

    return {
        "api_key": api_key,
        "base_url": base_url,
        "model": model,
        "env_path": str(env_path),
        "skill_dir": str(skill_dir),
    }


def extract_json(text: str) -> dict:
    text = (text or "").strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    m = re.search(r'\{.*\}', text, re.S)
    if m:
        candidate = m.group(0)
        try:
            return json.loads(candidate)
        except Exception:
            pass

    return {
        "title": "Amazon 市场调研报告",
        "one_line_conclusion": "模型已返回内容，但未能解析为标准 JSON，已降级输出。",
        "decision": "谨慎进入",
        "score": "N/A",
        "price_band": "当前公开数据不足，需要进一步调研",
        "reasons": ["模型输出格式异常，已降级处理"],
        "risks": ["需要检查模型输出格式是否严格遵循 JSON 要求"],
        "directions": ["建议重新生成一次报告"],
        "full_report_markdown": text
    }


def call_market_model(product: str, market: str, platform: str, raw_text: str, cfg: dict) -> dict:
    if not cfg["api_key"]:
        return {
            "error": (
                "首次使用前请先配置模型环境变量。\n\n"
                "请在当前 skill 目录下编辑 .env 文件，并填写：\n"
                "MARKET_API_KEY=你的key\n"
                "MARKET_BASE_URL=https://api.moonshot.cn/v1\n"
                "MARKET_MODEL=kimi-k2.5\n\n"
                "如果没有 .env，第一次运行 run.sh 时会自动生成。"
            )
        }

    system_prompt = """
你是一名资深跨境电商产品开发经理与 Amazon 市场调研专家。

你的任务：
根据用户输入的商品名称、目标市场、销售平台，输出一份专业级 Amazon 市场调研 JSON 结果。

必须严格保留并覆盖以下 18 条 SOP 分析框架：

1. 市场宏观分析
2. 电商平台竞争结构
3. 头部品牌分析
4. Amazon 竞品分析
5. 关键词需求分析
6. 用户需求分析
7. 用户评价分析
8. 产品成本结构
9. 认证要求
10. 专利风险
11. 用户画像
12. 使用场景
13. 产品机会分析
14. 风险分析
15. SWOT 分析
16. PEST 分析
17. 市场进入评分
18. 最终建议

输出必须严格为 JSON 对象，禁止输出任何额外说明，字段如下：

{
  "title": "标题",
  "one_line_conclusion": "一句话结论",
  "decision": "建议开发/谨慎进入/不建议进入",
  "score": "0-10 或 0-100 都可以，但要明确",
  "price_band": "建议价格带",
  "reasons": ["进入理由1", "进入理由2", "进入理由3"],
  "risks": ["核心风险1", "核心风险2", "核心风险3"],
  "directions": ["推荐切入方向1", "推荐切入方向2", "推荐切入方向3"],
  "full_report_markdown": "完整18条SOP报告，使用纯文本和稳定标题格式，不要表格"
}

额外强制要求：
1. 不要输出 Markdown 表格
2. 不要输出代码块
3. full_report_markdown 中必须完整包含 18 条 SOP
4. 每个模块必须包含：
   - 结论
   - 关键依据
   - 风险/备注
5. 标题统一写成：【1. 市场宏观分析】 这种格式
6. 语气要像商业报告，不像聊天
7. 不要在 full_report_markdown 前面再写摘要
""".strip()

    user_prompt = f"""
用户原始需求：
{raw_text}

识别参数：
商品名称：{product}
目标市场：{market}
销售平台：{platform}

现在请基于以上信息，输出完整市场调研 JSON。
""".strip()

    payload = {
        "model": cfg["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    req = urllib.request.Request(
        url=f"{cfg['base_url']}/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {cfg['api_key']}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"].strip()
            return extract_json(content)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        return {"error": f"调用市场调研模型失败（HTTP {e.code}）：{body[:1200]}"}
    except Exception as e:
        return {"error": f"调用市场调研模型失败：{e}"}


def strip_markdown_tables(text: str) -> str:
    lines = text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if "|" in line:
            block = []
            j = i
            while j < len(lines) and "|" in lines[j]:
                block.append(lines[j].strip())
                j += 1
            for row in block:
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                cells = [c for c in cells if c]
                if not cells:
                    continue
                if all(set(c) <= set("-: ") for c in cells):
                    continue
                if len(cells) == 1:
                    out.append(f"- {cells[0]}")
                else:
                    out.append(f"- {' | '.join(cells)}")
            i = j
            continue
        out.append(line)
        i += 1
    return "\n".join(out).strip()


def prettify_report(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r'[ \t]+\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    if "【1. 市场宏观分析】" in text:
        return text.strip()

    replacements = [
        (r'^\s*#?\s*Amazon市场调研快照\s*$', ''),
        (r'^\s*##?\s*1[）\.\s]+市场宏观分析', '【1. 市场宏观分析】'),
        (r'^\s*##?\s*2[）\.\s]+电商平台竞争结构', '【2. 电商平台竞争结构】'),
        (r'^\s*##?\s*3[）\.\s]+头部品牌分析', '【3. 头部品牌分析】'),
        (r'^\s*##?\s*4[）\.\s]+Amazon竞品分析', '【4. Amazon竞品分析】'),
        (r'^\s*##?\s*5[）\.\s]+关键词需求分析', '【5. 关键词需求分析】'),
        (r'^\s*##?\s*6[）\.\s]+用户需求分析', '【6. 用户需求分析】'),
        (r'^\s*##?\s*7[）\.\s]+用户评价分析', '【7. 用户评价分析】'),
        (r'^\s*##?\s*8[）\.\s]+产品成本结构', '【8. 产品成本结构】'),
        (r'^\s*##?\s*9[）\.\s]+认证要求', '【9. 认证要求】'),
        (r'^\s*##?\s*10[）\.\s]+专利风险', '【10. 专利风险】'),
        (r'^\s*##?\s*11[）\.\s]+用户画像', '【11. 用户画像】'),
        (r'^\s*##?\s*12[）\.\s]+使用场景', '【12. 使用场景】'),
        (r'^\s*##?\s*13[）\.\s]+产品机会分析', '【13. 产品机会分析】'),
        (r'^\s*##?\s*14[）\.\s]+风险分析', '【14. 风险分析】'),
        (r'^\s*##?\s*15[）\.\s]+SWOT分析', '【15. SWOT分析】'),
        (r'^\s*##?\s*16[）\.\s]+PEST分析', '【16. PEST分析】'),
        (r'^\s*##?\s*17[）\.\s]+市场进入评分', '【17. 市场进入评分】'),
        (r'^\s*##?\s*18[）\.\s]+最终建议', '【18. 最终建议】'),
    ]

    for pat, repl in replacements:
        text = re.sub(pat, repl, text, flags=re.M)

    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def ensure_full_18_sections(text: str) -> str:
    current = text
    missing = []
    for section in SOP_SECTIONS:
        if f"【{section}】" not in current:
            missing.append(section)

    if not missing:
        return current

    appendix = ["", "【结构完整性补全说明】", "以下模块模型未完整输出，已自动补齐占位结构：", ""]
    for section in missing:
        appendix.extend([
            f"【{section}】",
            "结论：",
            "当前模型未完整返回该模块，建议重新生成或二次深挖。",
            "",
            "关键依据：",
            "当前返回内容不足。",
            "",
            "风险/备注：",
            "该模块缺失会影响完整决策质量。",
            ""
        ])
    return (current.rstrip() + "\n\n" + "\n".join(appendix).strip()).strip()


def safe_filename(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r'[\s/]+', '_', name)
    name = re.sub(r'[^a-zA-Z0-9_\u4e00-\u9fa5-]+', '', name)
    return name[:80] or "market_research"


def save_report(product: str, report_text: str, cfg: dict) -> str:
    filename = f"{safe_filename(product)}_research_report.md"
    path = Path(cfg["skill_dir"]) / filename
    path.write_text(report_text, encoding="utf-8")
    return filename


def main():
    raw_input = sys.argv[1] if len(sys.argv) >= 2 else ""

    if not raw_input.strip():
        output({
            "ok": False,
            "error": "缺少输入参数",
            "help": "Amazon Market Research",
            "example_feishu": "/amazon-market-research 调研一下午餐盒在美国Amazon市场值不值得做",
            "example_local": "bash ~/.openclaw/workspace/skills/amazon-market-research/run.sh \"调研一下午餐盒在美国Amazon市场值不值得做\"",
        })
        return

    product, market, platform, normalized_text = parse_input(raw_input)

    if not product:
        output({
            "ok": False,
            "message": "未识别商品名称，请补充更明确的产品名称，例如：Lunch Box、Pet Water Fountain、Wireless Charger Stand。"
        })
        return

    if not market:
        output({
            "ok": False,
            "message": "未识别目标市场，请补充国家，例如：美国、德国、英国、日本、马来西亚。"
        })
        return

    if not platform:
        platform = "Amazon"

    cfg = get_config()
    result = call_market_model(product, market, platform, normalized_text, cfg)

    if "error" in result:
        output({
            "ok": False,
            "message": result["error"],
            "meta": {
                "product_name": product,
                "market_country": market,
                "platform": platform
            }
        })
        return

    full_report = prettify_report(strip_markdown_tables(result.get("full_report_markdown", "")))
    full_report = ensure_full_18_sections(full_report)

    title = result.get("title", f"{product} {market} {platform} 市场调研报告").strip()
    final_answer = f"📊 {title}\n\n{full_report}".strip()

    report_file = save_report(product, final_answer, cfg)

    output({
        "ok": True,
        "answer": final_answer,
        "message": final_answer,
        "report_file": report_file,
        "meta": {
            "product_name": product,
            "market_country": market,
            "platform": platform,
            "report_file": report_file
        }
    })


if __name__ == "__main__":
    main()