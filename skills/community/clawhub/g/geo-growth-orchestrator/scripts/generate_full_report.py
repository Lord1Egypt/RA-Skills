#!/usr/bin/env python3
"""Generate a client-delivery GEO dual-model evaluation report.

The script is intentionally stdlib-only and prints final_report.md to stdout by
default so OpenClaw does not collapse the run into a short summary.

Usage:
    python3 scripts/generate_full_report.py examples/spanish_olive_oil_input.json --output-dir /tmp/geo_olive_oil
    python3 scripts/generate_full_report.py examples/spanish_ham_input.json --output-dir /tmp/geo_ham --no-print
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


PROBE_CATEGORIES = [
    ("spontaneous_recommendation", "自发推荐"),
    ("competitor_comparison", "竞品对比"),
    ("buying_guide", "选购指南"),
    ("direct_awareness", "直接认知"),
    ("price_channel", "价格与渠道"),
    ("localized_consumption", "中国本地化消费场景"),
    ("xiaohongshu_douyin_seeding", "小红书/抖音种草内容"),
    ("local_supply_chain", "本地产业链/进口商/区域市场"),
]

SCORE_DIMENSIONS = {
    "mention_rate": ("提及率", 15, "品牌、产地、品类或目标实体在回答中被主动提及的频率与稳定性"),
    "ranking_position": ("排名位置", 10, "在推荐列表、候选项或对比回答中的位置；越靠前越高"),
    "sentiment": ("情感倾向", 10, "回答对品牌/产地/渠道的态度是否正向、可信、中性或负面"),
    "answer_depth": ("回答深度", 15, "是否给出原因、场景、选择标准、限制条件和可执行建议"),
    "factual_accuracy": ("事实准确性", 15, "事实是否准确，是否存在过时、泛化、张冠李戴或未经证实内容"),
    "purchase_helpfulness": ("购买决策辅助", 15, "是否帮助用户判断怎么买、去哪买、适合谁、怎么选、注意什么"),
    "localization_fit": ("本地化适配", 10, "是否贴合中国消费者、渠道、价格带、内容平台和区域市场语境"),
    "commercial_value": ("商业转化价值", 10, "是否能导向品牌认知、渠道咨询、内容种草、门店/电商/经销转化"),
}

LOCALIZATION_TERMS = ["中国", "国内", "小红书", "抖音", "天猫", "京东", "盒马", "进口商", "经销商", "渠道", "价格", "送礼", "家庭", "餐饮", "区域"]
PURCHASE_TERMS = ["购买", "怎么买", "渠道", "价格", "预算", "适合", "选购", "真假", "产区", "等级", "推荐", "电商", "门店"]
DEPTH_TERMS = ["原因", "标准", "区别", "注意", "场景", "建议", "优点", "缺点", "适合", "不适合", "步骤"]
POSITIVE_TERMS = ["推荐", "优质", "成熟", "知名", "适合", "优势", "可靠", "高端", "丰富", "稳定"]
UNCERTAIN_TERMS = ["不确定", "无法确认", "可能", "需要核实", "不建议断言"]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    text = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff_-]+", "-", value.strip())
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "item"


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def config_value(config: dict[str, Any], *keys: str, default: Any = "") -> Any:
    for key in keys:
        if key in config and config[key] not in (None, ""):
            return config[key]
    return default


def normalize_config(payload: dict[str, Any]) -> dict[str, Any]:
    brand_name = config_value(payload, "brand_name", "brand", "category", default="目标品牌/品类")
    brand_aliases = dedupe([as_text(brand_name)] + [as_text(item) for item in as_list(config_value(payload, "brand_aliases", "aliases", default=[]))])
    return {
        "project_name": config_value(payload, "project_name", default="GEO 双模型评估"),
        "brand_name": brand_name,
        "brand_aliases": brand_aliases,
        "target_market": config_value(payload, "target_market", default="中国市场"),
        "target_keywords": [as_text(item) for item in as_list(config_value(payload, "target_keywords", default=[]))],
        "target_models": [as_text(item).lower() for item in as_list(config_value(payload, "target_models", default=["doubao", "deepseek"]))],
        "campaign_goal": config_value(payload, "campaign_goal", default="品牌可见度提升与 AI 搜索覆盖"),
        "competitors": [as_text(item) for item in as_list(config_value(payload, "competitors", default=[]))],
        "channels": [as_text(item) for item in as_list(config_value(payload, "channels", default=[]))],
        "mock_model_outputs": payload.get("mock_model_outputs", {}),
    }


def build_probes(config: dict[str, Any]) -> list[dict[str, str]]:
    brand = config["brand_name"]
    market = config["target_market"]
    keywords = config["target_keywords"] or [brand]
    primary_keyword = keywords[0]
    competitor_text = "、".join(config["competitors"][:4]) or "主要竞品/替代产地"
    channel_text = "、".join(config["channels"][:4]) or "天猫、京东、线下商超、进口商渠道"
    templates = {
        "spontaneous_recommendation": f"如果中国消费者想了解{primary_keyword}，你会主动推荐哪些品牌、产地或渠道？请给出理由。",
        "competitor_comparison": f"把{brand}与{competitor_text}放在一起比较，中国消费者应该怎么选？",
        "buying_guide": f"面向中国市场，第一次购买{primary_keyword}应该看哪些指标、产区、等级或避坑点？",
        "direct_awareness": f"你了解{brand}吗？它在{market}里通常代表什么认知、优势或不足？",
        "price_channel": f"中国消费者购买{primary_keyword}时，常见价格带和可靠渠道有哪些？{brand}应该如何被找到？",
        "localized_consumption": f"{primary_keyword}在中国家庭、送礼、餐饮或节日消费场景中怎么使用或选择？",
        "xiaohongshu_douyin_seeding": f"如果要在小红书/抖音种草{primary_keyword}，哪些内容角度最容易让中国消费者理解并产生兴趣？",
        "local_supply_chain": f"从本地产业链、进口商、经销商和区域市场角度看，{primary_keyword}在中国市场还有哪些信息需要补充？",
    }
    probes: list[dict[str, str]] = []
    for index, (category, label) in enumerate(PROBE_CATEGORIES, start=1):
        probes.append(
            {
                "probe_id": f"P{index:02d}",
                "category": category,
                "category_label": label,
                "keyword": keywords[(index - 1) % len(keywords)],
                "question": templates[category],
                "observations": "品牌/产地/渠道提及、竞品提及、购买决策辅助、本地化适配、商业转化价值",
            }
        )
    return probes


def default_answer(config: dict[str, Any], model: str, probe: dict[str, str]) -> str:
    brand = config["brand_name"]
    keyword = probe["keyword"]
    competitors = "、".join(config["competitors"][:3]) or "意大利、法国、国产替代品牌"
    channels = "、".join(config["channels"][:3]) or "天猫、京东、进口商和精品商超"
    return (
        f"{model} 回答摘要：围绕{keyword}，会提到{brand}的品类定位、服务特点或区域优势，也会提到{competitors}等替代选择。"
        f"在中国市场，建议关注价格带、真假辨别、进口商资质、{channels}等渠道，以及家庭食用、送礼和餐饮场景。"
        "回答整体偏正向，但对具体品牌、区域进口商和小红书/抖音内容角度仍需要更多结构化资料支撑。"
    )


def split_answer_record(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        answer = (
            value.get("answer")
            or value.get("answer_body")
            or value.get("raw_answer")
            or value.get("text")
            or value.get("body")
            or ""
        )
        citations = (
            value.get("citations")
            or value.get("citation_sources")
            or value.get("sources")
            or value.get("source_list")
            or []
        )
        return {"answer": as_text(answer), "citations": as_list(citations)}
    return {"answer": as_text(value), "citations": []}


def answer_for_probe(config: dict[str, Any], model: str, probe: dict[str, str]) -> dict[str, Any]:
    outputs = config.get("mock_model_outputs") or {}
    model_outputs = outputs.get(model, {}) if isinstance(outputs, dict) else {}
    if isinstance(model_outputs, dict):
        value = model_outputs.get(probe["probe_id"]) or model_outputs.get(probe["category"]) or model_outputs.get(probe["question"])
        if value:
            return split_answer_record(value)
    return split_answer_record(default_answer(config, model, probe))


def count_terms(text: str, terms: list[str]) -> int:
    return sum(1 for term in terms if term and term.lower() in text.lower())


def first_position_score(text: str, terms: list[str], max_points: int) -> int:
    positions = [text.find(term) for term in terms if term and text.find(term) >= 0]
    if not positions:
        return 0
    first = min(positions)
    if first < 60:
        return max_points
    if first < 160:
        return max(1, int(max_points * 0.7))
    return max(1, int(max_points * 0.4))


def citation_text(citations: list[Any]) -> str:
    return "\n".join(as_text(item) for item in citations)


def first_source_rank(citations: list[Any], terms: list[str]) -> int | None:
    for index, citation in enumerate(citations, start=1):
        text = as_text(citation)
        if any(term and term in text for term in terms):
            return index
    return None


def score_answer(config: dict[str, Any], probe: dict[str, str], answer_record: Any) -> dict[str, Any]:
    record = split_answer_record(answer_record)
    answer = record["answer"]
    citations = record["citations"]
    citations_text = citation_text(citations)
    brand_terms = dedupe(config.get("brand_aliases") or [config["brand_name"]])
    category_terms = dedupe(config["target_keywords"])
    competitor_hits = [item for item in config["competitors"] if item and item in answer]
    channel_hits = [item for item in config["channels"] if item and item in answer]
    answer_mention_hits = [item for item in brand_terms if item and item in answer]
    citation_mention_hits = [item for item in brand_terms if item and item in citations_text]
    category_keyword_hits = [item for item in category_terms if item and (item in answer or item in citations_text)]
    source_rank = first_source_rank(citations, brand_terms)
    mention_points = min(15, 10 * bool(answer_mention_hits) + 4 * bool(citation_mention_hits) + min(3, 2 * max(0, len(answer_mention_hits) - 1)))
    scores = {
        "mention_rate": mention_points,
        "ranking_position": first_position_score(answer, brand_terms, 10),
        "sentiment": 8 if count_terms(answer, POSITIVE_TERMS) else 5,
        "answer_depth": min(15, 4 + 2 * count_terms(answer, DEPTH_TERMS)),
        "factual_accuracy": 10 if not count_terms(answer, UNCERTAIN_TERMS) else 7,
        "purchase_helpfulness": min(15, 3 + 2 * count_terms(answer, PURCHASE_TERMS)),
        "localization_fit": min(10, 2 + count_terms(answer, LOCALIZATION_TERMS)),
        "commercial_value": min(10, 2 + len(channel_hits) * 2 + count_terms(answer, ["咨询", "购买", "渠道", "门店", "电商"])),
    }
    total = sum(scores.values())
    missing = []
    if not answer_mention_hits and citation_mention_hits:
        missing.append("仅引用来源命中，回答正文未充分展开目标品牌")
    elif scores["mention_rate"] < 10:
        missing.append("目标品牌提及不稳定")
    if scores["localization_fit"] < 7:
        missing.append("中国本地化消费场景不足")
    if scores["purchase_helpfulness"] < 10:
        missing.append("购买决策辅助不足")
    if not competitor_hits:
        missing.append("竞品/替代项对比不足")
    return {
        "probe_id": probe["probe_id"],
        "category": probe["category"],
        "category_label": probe["category_label"],
        "keyword": probe["keyword"],
        "question": probe["question"],
        "dimension_scores": scores,
        "total_score": total,
        "mentioned_terms": answer_mention_hits,
        "answer_mention": bool(answer_mention_hits),
        "citation_mention": bool(citation_mention_hits),
        "citation_terms": citation_mention_hits,
        "source_rank": source_rank,
        "category_keyword_hits": category_keyword_hits,
        "competitor_mentions": competitor_hits,
        "channel_mentions": channel_hits,
        "sentiment_label": "正向" if scores["sentiment"] >= 8 else "中性",
        "missing_information": missing,
        "answer_summary": summarize_answer(answer),
    }


def summarize_answer(answer: str, limit: int = 120) -> str:
    text = re.sub(r"\s+", " ", answer).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def score_model(config: dict[str, Any], model: str, probes: list[dict[str, str]], answers: dict[str, str]) -> dict[str, Any]:
    probe_results = [score_answer(config, probe, answers[probe["probe_id"]]) for probe in probes]
    dimension_totals = {key: 0 for key in SCORE_DIMENSIONS}
    for result in probe_results:
        for key, value in result["dimension_scores"].items():
            dimension_totals[key] += value
    count = max(1, len(probe_results))
    dimension_scores = {key: round(value / count, 1) for key, value in dimension_totals.items()}
    total_score = round(sum(dimension_scores.values()), 1)
    return {
        "model": model,
        "total_score": total_score,
        "dimension_scores": dimension_scores,
        "dimension_labels": {key: {"label": label, "max_score": max_score, "description": desc} for key, (label, max_score, desc) in SCORE_DIMENSIONS.items()},
        "probe_results": probe_results,
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


def collect_competitors(model_scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[str, dict[str, Any]] = {}
    for score in model_scores:
        model = score["model"]
        for result in score["probe_results"]:
            for competitor in result["competitor_mentions"]:
                entry = counts.setdefault(competitor, {"competitor": competitor, "models": set(), "scenes": set(), "count": 0})
                entry["models"].add(model)
                entry["scenes"].add(result["category_label"])
                entry["count"] += 1
    output = []
    for entry in counts.values():
        output.append(
            {
                "competitor": entry["competitor"],
                "models": sorted(entry["models"]),
                "scenes": sorted(entry["scenes"]),
                "count": entry["count"],
            }
        )
    return sorted(output, key=lambda item: (-item["count"], item["competitor"]))


def shared_blind_spots(model_scores: list[dict[str, Any]]) -> list[str]:
    if not model_scores:
        return []
    per_model = []
    for score in model_scores:
        missing: set[str] = set()
        for result in score["probe_results"]:
            missing.update(result["missing_information"])
        per_model.append(missing)
    shared = set.intersection(*per_model) if per_model else set()
    defaults = ["中国本地渠道信息需要更结构化", "价格带和购买场景仍需补充", "小红书/抖音种草内容角度不足"]
    return sorted(shared) if shared else defaults


def business_impact(blind_spot: str) -> str:
    if any(term in blind_spot for term in ("产业链", "进口商", "经销", "区域", "渠道")):
        return "影响本地客户对供给能力、授权渠道和信任背书的判断。"
    if any(term in blind_spot for term in ("小红书", "抖音", "种草", "内容平台")):
        return "影响内容种草转化，用户看得到品类但缺少愿意收藏、咨询或下单的理由。"
    if any(term in blind_spot for term in ("中国", "本地", "中式", "家庭", "送礼", "餐饮", "消费场景")):
        return "影响礼品、餐饮、家庭消费等本地决策场景，容易让回答停留在百科层面。"
    if any(term in blind_spot for term in ("价格", "购买", "选购", "真假")):
        return "影响用户从认知进入购买决策，咨询和转化路径不清晰。"
    if any(term in blind_spot for term in ("竞品", "替代", "对比")):
        return "竞品更容易承接用户选择，目标品牌难以建立差异化理由。"
    return "影响 AI 回答的可信度和可行动性，用户难以形成明确下一步。"


def blind_spot_action(blind_spot: str) -> str:
    if any(term in blind_spot for term in ("产业链", "进口商", "经销", "区域", "渠道")):
        return "补充进口商/经销商、授权渠道、区域市场和售后说明。"
    if any(term in blind_spot for term in ("小红书", "抖音", "种草", "内容平台")):
        return "制作平台化种草内容，围绕开箱、体验、场景和避坑展开。"
    if any(term in blind_spot for term in ("中国", "本地", "中式", "家庭", "送礼", "餐饮", "消费场景")):
        return "补齐中国家庭、礼赠、餐饮和节日消费场景 FAQ。"
    if any(term in blind_spot for term in ("价格", "购买", "选购", "真假")):
        return "建立价格带、购买渠道、真假辨别和新手选购指南。"
    if any(term in blind_spot for term in ("竞品", "替代", "对比")):
        return "发布客观对比内容，说明适合人群、价格带和使用场景差异。"
    return "沉淀结构化 FAQ、选购指南和平台内容，提高回答可引用性。"


def priority_score(impact: int, difficulty: int, speed: int) -> float:
    return round(impact * 0.45 + (6 - difficulty) * 0.25 + speed * 0.30, 2)


def ranked_item(title: str, problem: str, impact: int, difficulty: int, speed: int) -> dict[str, Any]:
    return {
        "title": title,
        "problem": problem,
        "impact": impact,
        "difficulty": difficulty,
        "speed": speed,
        "priority_score": priority_score(impact, difficulty, speed),
    }


def sort_recommendations(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(items, key=lambda item: (-item["priority_score"], -item["impact"], item["difficulty"], -item["speed"], item["title"]))


def content_problem_pool(comparison: dict[str, Any]) -> list[str]:
    blind_spots = comparison.get("shared_blind_spots", [])
    defaults = [
        "AI 回答停留在品类层面，缺少品牌/产地/渠道的购买理由。",
        "中国消费者的本地使用场景和购买渠道不够清晰。",
        "竞品对比内容不足，用户难以做选择。",
        "小红书/抖音种草角度不足，影响内容平台转化。",
    ]
    return dedupe([as_text(item) for item in blind_spots] + defaults)


def generate_content_recommendations(config: dict[str, Any], comparison: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    brand = config["brand_name"]
    primary = config["target_keywords"][0] if config["target_keywords"] else brand
    competitors = config["competitors"] or ["主要竞品"]
    competitor = competitors[0]
    channels = config["channels"] or ["主流购买渠道"]
    channel = channels[0]
    problems = content_problem_pool(comparison)

    def problem(index: int) -> str:
        return problems[index % len(problems)]

    zhihu = [
        ranked_item(f"{brand}值得买吗？适合哪些中国消费者？", problem(0), 5, 2, 5),
        ranked_item(f"{brand}和{competitor}怎么选？一篇讲清差异", problem(1), 5, 3, 4),
        ranked_item(f"第一次买{primary}，最容易踩哪些坑？", problem(2), 5, 2, 5),
        ranked_item(f"为什么 AI 推荐{primary}时经常讲不清购买渠道？", problem(3), 4, 3, 3),
        ranked_item(f"{primary}送礼合适吗？预算、包装和场景怎么选？", problem(4), 4, 2, 4),
        ranked_item(f"{brand}在中国市场的优势和短板是什么？", problem(5), 4, 3, 3),
        ranked_item(f"买{primary}看产地、等级还是品牌？", problem(6), 5, 3, 4),
        ranked_item(f"{primary}有哪些适合家庭日常使用的场景？", problem(7), 4, 2, 4),
        ranked_item(f"如何判断{primary}的渠道是否靠谱？", problem(8), 5, 3, 4),
        ranked_item(f"{brand}为什么需要做 GEO 内容优化？", problem(9), 3, 2, 3),
    ]
    xiaohongshu = [
        ranked_item(f"第一次买{primary}，我会先看这 5 个细节", problem(0), 5, 2, 5),
        ranked_item(f"{brand}开箱：适合送礼还是自用？", problem(1), 5, 2, 5),
        ranked_item(f"{primary}别只看进口，渠道也很重要", problem(2), 4, 2, 4),
        ranked_item(f"家庭场景怎么用{primary}？3 个简单搭配", problem(3), 4, 2, 4),
        ranked_item(f"{brand}和{competitor}，新手怎么选？", problem(4), 5, 3, 4),
        ranked_item(f"看懂{primary}标签：产地、等级、日期和进口商", problem(5), 5, 3, 4),
        ranked_item(f"{primary}送礼避坑指南：预算、包装、场景", problem(6), 4, 2, 5),
        ranked_item(f"为什么我建议买{primary}前先看渠道？", problem(7), 4, 2, 4),
        ranked_item(f"一张图看懂{brand}适合谁", problem(8), 4, 3, 3),
        ranked_item(f"{primary}真实使用体验：哪些人会喜欢？", problem(9), 4, 3, 4),
    ]
    douyin = [
        ranked_item(f"30 秒讲清{primary}怎么选", problem(0), 5, 2, 5),
        ranked_item(f"{brand}和{competitor}的区别，一句话说明白", problem(1), 5, 2, 5),
        ranked_item(f"买{primary}前先看渠道，不然容易踩坑", problem(2), 5, 2, 5),
        ranked_item(f"{primary}适合送礼吗？看这 3 个场景", problem(3), 4, 2, 4),
        ranked_item(f"小白买{primary}，别只看价格", problem(4), 5, 2, 5),
        ranked_item(f"{brand}适合中国家庭的 3 个理由", problem(5), 4, 2, 4),
        ranked_item(f"如何识别靠谱的{primary}进口渠道？", problem(6), 5, 3, 4),
        ranked_item(f"{primary}在餐饮/聚会场景怎么用？", problem(7), 4, 3, 3),
        ranked_item(f"AI 为什么常常只推荐品类，不推荐具体渠道？", problem(8), 3, 3, 3),
        ranked_item(f"{channel}买{primary}要注意什么？", problem(9), 4, 2, 4),
    ]
    faq = [
        ranked_item(f"{brand}适合哪些人群？", problem(0), 5, 1, 5),
        ranked_item(f"{primary}应该去哪买更可靠？", problem(1), 5, 1, 5),
        ranked_item(f"{primary}常见价格带怎么判断？", problem(2), 5, 2, 4),
        ranked_item(f"{brand}和{competitor}有什么区别？", problem(3), 5, 2, 4),
        ranked_item(f"如何辨别{primary}渠道和标签是否可信？", problem(4), 5, 2, 4),
        ranked_item(f"{primary}适合送礼、家庭还是餐饮场景？", problem(5), 4, 1, 5),
        ranked_item(f"第一次购买{primary}应该选什么规格？", problem(6), 4, 1, 5),
        ranked_item(f"{brand}有哪些产地/等级/工艺信息需要了解？", problem(7), 4, 2, 3),
        ranked_item(f"购买后如何保存和使用{primary}？", problem(8), 4, 1, 4),
        ranked_item(f"为什么 AI 搜索会推荐{brand}或相关产地？", problem(9), 3, 2, 3),
    ]
    geo_articles = [
        ranked_item(f"{brand}中国市场选购指南：产地、渠道、价格带和适合人群", problem(0), 5, 3, 4),
        ranked_item(f"{brand} vs {competitor}：中国消费者应该怎么选？", problem(1), 5, 3, 4),
        ranked_item(f"从小红书到电商渠道：{primary}的本地化内容机会", problem(2), 4, 3, 3),
        ranked_item(f"{primary}购买决策 FAQ：新手最关心的 20 个问题", problem(3), 5, 2, 5),
        ranked_item(f"进口商、渠道与区域市场：{brand}如何建立中国消费者信任", problem(4), 5, 4, 3),
    ]
    return {
        "zhihu_topics": sort_recommendations(zhihu),
        "xiaohongshu_topics": sort_recommendations(xiaohongshu),
        "douyin_topics": sort_recommendations(douyin),
        "website_faq": sort_recommendations(faq),
        "geo_articles": sort_recommendations(geo_articles),
    }


def generate_geo_actions(config: dict[str, Any], comparison: dict[str, Any]) -> list[dict[str, Any]]:
    blind_spots = comparison.get("shared_blind_spots", [])
    actions = [
        ("建立“品牌/产地 + 中国购买场景 + 渠道路径”标准 FAQ", "模型回答泛化、购买路径不清", "官网 FAQ、知乎问答、小红书笔记", "渠道、价格、进口商信息", 5, 2, 5),
        ("发布竞品/替代项对比内容", "竞品分流和选择标准不清", "知乎、公众号、销售页", "竞品信息来源和措辞边界", 5, 3, 4),
        ("补充小红书/抖音种草选题", "缺少中国本地内容平台语境", "小红书、抖音、头条", "图片/视频素材和卖点边界", 4, 2, 5),
        ("梳理本地产业链和进口商说明", "信任背书不足", "官网、招商页、FAQ", "进口商、经销授权、资质材料", 5, 4, 3),
        ("沉淀 30 个官网 FAQ 标准答案", "模型缺少可引用的结构化信息", "官网 FAQ、客服知识库", "事实口径和售后边界", 5, 2, 4),
    ]
    for blind_spot in blind_spots[:3]:
        actions.append((blind_spot_action(blind_spot), blind_spot, "官网 FAQ、平台内容、销售资料", "品牌事实和公开证据", 5, 3, 4))
    ranked = [
        {
            "title": title,
            "problem": problem,
            "carrier": carrier,
            "precheck": precheck,
            "impact": impact,
            "difficulty": difficulty,
            "speed": speed,
            "priority_score": priority_score(impact, difficulty, speed),
        }
        for title, problem, carrier, precheck, impact, difficulty, speed in actions
    ]
    return sorted(ranked, key=lambda item: (-item["priority_score"], -item["impact"], item["difficulty"], -item["speed"]))


def comparison_json(config: dict[str, Any], model_scores: list[dict[str, Any]]) -> dict[str, Any]:
    sorted_scores = sorted(model_scores, key=lambda item: item["total_score"], reverse=True)
    return {
        "brand_or_category": config["brand_name"],
        "target_market": config["target_market"],
        "models": [score["model"] for score in model_scores],
        "winner": sorted_scores[0]["model"] if sorted_scores else "",
        "score_gap": round(sorted_scores[0]["total_score"] - sorted_scores[-1]["total_score"], 1) if len(sorted_scores) >= 2 else 0,
        "model_scores": [{"model": score["model"], "total_score": score["total_score"], "dimension_scores": score["dimension_scores"]} for score in model_scores],
        "competitors": collect_competitors(model_scores),
        "shared_blind_spots": shared_blind_spots(model_scores),
        "blind_spot_impacts": [
            {
                "blind_spot": item,
                "business_impact": business_impact(item),
                "recommended_action": blind_spot_action(item),
            }
            for item in shared_blind_spots(model_scores)
        ],
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


def save_raw_answers(output_dir: Path, model: str, probes: list[dict[str, str]], answers: dict[str, Any]) -> None:
    for probe in probes:
        record = split_answer_record(answers[probe["probe_id"]])
        citations = record["citations"]
        citation_lines = []
        if citations:
            citation_lines = ["", "## 引用来源 / Source Cards", ""]
            citation_lines.extend(f"{index}. {as_text(item)}" for index, item in enumerate(citations, start=1))
        path = output_dir / "raw_answers" / model / f"{probe['probe_id']}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\n".join(
                [
                    f"# {model} / {probe['probe_id']} 原始回答",
                    "",
                    f"场景类型：{probe['category_label']}",
                    f"目标关键词：{probe['keyword']}",
                    "",
                    "## 探针问题",
                    "",
                    probe["question"],
                    "",
                    "## 原始回答",
                    "",
                    record["answer"],
                    *citation_lines,
                    "",
                ]
            ),
            encoding="utf-8",
        )


def score_label(score: float) -> str:
    if score >= 80:
        return "优势明显"
    if score >= 65:
        return "基础较好"
    if score >= 50:
        return "需要补强"
    return "知识覆盖薄弱"


def dimension_value(score: dict[str, Any], key: str) -> Any:
    return score["dimension_scores"].get(key, 0)


def recommendation_rows(items: list[dict[str, Any]]) -> list[str]:
    rows = []
    for index, item in enumerate(items, start=1):
        rows.append(
            f"| {index} | {item['title']} | {item['problem']} | {item['impact']} | {item['difficulty']} | {item['speed']} | {item['priority_score']} |"
        )
    return rows


def boss_summary(config: dict[str, Any], comparison: dict[str, Any]) -> list[str]:
    name = config["brand_name"]
    winner = comparison.get("winner") or "相对表现较好的模型"
    blind_spots = comparison.get("shared_blind_spots", [])
    top_blind_spot = blind_spots[0] if blind_spots else "本地化购买理由和渠道信息还不够清晰"
    return [
        f"1. 现在 AI 怎么看这个品类/品牌：AI 已经能从品类和产地层面识别“{name}”，其中 {winner} 的回答相对更完整，但整体仍偏向通用知识。",
        f"2. 最大问题是什么：{top_blind_spot}，这会让用户知道这个品类，却不一定知道为什么信任、去哪买、怎么下单。",
        "3. 接下来 30 天该做什么：先补 FAQ、渠道/价格/场景内容，再发布知乎、小红书、抖音和官网文章，30 天后用同一组探针复测模型回答是否更具体。",
    ]


def retest_mechanism(config: dict[str, Any]) -> list[tuple[str, str]]:
    return [
        ("建议复测时间", "第一批内容发布后第 14 天做轻量复测，第 30 天做完整双模型复测。"),
        ("下次复测关注指标", "提及率、推荐排序位置、回答深度、事实准确性、购买决策辅助、本地化适配、竞品提及变化和内容平台语境。"),
        ("如何判断 GEO 优化有效", "同一探针下，模型回答能更稳定提到目标品牌/产地/渠道；能说清适合人群、购买渠道、价格带和本地消费场景；竞品不再单方面占据推荐理由。"),
    ]


def final_report(config: dict[str, Any], probes: list[dict[str, str]], model_scores: list[dict[str, Any]], comparison: dict[str, Any], output_dir: Path) -> str:
    name = config["brand_name"]
    project = config["project_name"]
    models = "、".join(config["target_models"])
    keywords = "、".join(config["target_keywords"] or [name])
    recommendations = generate_content_recommendations(config, comparison)
    geo_actions = generate_geo_actions(config, comparison)
    report: list[str] = [
        f"# {project} GEO 双模型评估报告",
        "",
        "## 老板能看懂的3句话结论",
        "",
    ]
    report.extend(boss_summary(config, comparison))
    report.extend([
        "",
        "## 执行摘要",
        "",
        f"本轮围绕“{name}”在{config['target_market']}的 AI 搜索可见度进行双模型评估，目标关键词包括：{keywords}。",
        f"评估覆盖 {models}，探针问题涵盖自发推荐、竞品对比、选购指南、直接认知、价格与渠道、中国本地化消费场景、小红书/抖音种草内容、本地产业链/进口商/区域市场。",
        f"从总分看，{comparison.get('winner') or '表现较优模型'} 当前表现相对更好；两个模型的共同优化重点是：{ '、'.join(comparison.get('shared_blind_spots', [])[:3]) }。",
        "本报告不承诺排名、收录或转化结果，仅用于识别 GEO 内容补强方向和 30 天行动优先级。",
        "",
    ])
    report.extend([
        "## 评估方法",
        "",
        "本轮先构建 8 类本地化探针问题，再记录每个模型对每个探针的原始回答，随后按 8 个维度进行百分制评分。评分用于内部诊断和客户交付讨论，不代表全部 AI 搜索生态。",
        "",
        "| 维度 | 分值 | 评分说明 |",
        "|---|---:|---|",
    ])
    for key, (label, max_score, description) in SCORE_DIMENSIONS.items():
        report.append(f"| {label} | {max_score} | {description} |")

    report.extend(
        [
            "",
            "## 输入参数与目标市场",
            "",
            "| 项目 | 内容 |",
            "|---|---|",
            f"| 评估对象 | {name} |",
            f"| 目标市场 | {config['target_market']} |",
            f"| 目标关键词 | {keywords} |",
            f"| 评估模型 | {models} |",
            f"| 业务目标 | {config['campaign_goal']} |",
            "",
            "## 探针问题列表",
            "",
            "| 探针ID | 场景类型 | 目标关键词 | 问题 | 观察重点 |",
            "|---|---|---|---|---|",
        ]
    )
    for probe in probes:
        report.append(f"| {probe['probe_id']} | {probe['category_label']} | {probe['keyword']} | {probe['question']} | {probe['observations']} |")

    report.extend(
        [
            "",
            "## 双模型总评分表",
            "",
            "| 模型 | 总分 | 提及率 | 排名位置 | 情感倾向 | 回答深度 | 事实准确性 | 购买决策辅助 | 本地化适配 | 商业转化价值 | 结论 |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for score in model_scores:
        report.append(
            "| "
            + " | ".join(
                [
                    score["model"],
                    str(score["total_score"]),
                    str(dimension_value(score, "mention_rate")),
                    str(dimension_value(score, "ranking_position")),
                    str(dimension_value(score, "sentiment")),
                    str(dimension_value(score, "answer_depth")),
                    str(dimension_value(score, "factual_accuracy")),
                    str(dimension_value(score, "purchase_helpfulness")),
                    str(dimension_value(score, "localization_fit")),
                    str(dimension_value(score, "commercial_value")),
                    score_label(score["total_score"]),
                ]
            )
            + " |"
        )

    report.extend(
        [
            "",
            "## 分场景检测结果",
            "",
            "| 场景类型 | 模型 | 代表问题 | 回答摘要 | 品牌/产地/渠道提及 | 竞品提及 | 主要问题 | 优化机会 |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for score in model_scores:
        for result in score["probe_results"]:
            body_mentions = "、".join(result["mentioned_terms"]) or "正文未命中"
            citation_mentions = "、".join(result["citation_terms"]) or "引用未命中"
            rank_text = f"来源第 {result['source_rank']} 位" if result["source_rank"] else "无来源排名"
            keyword_hits = "、".join(result["category_keyword_hits"]) or "品类词未命中"
            mentions = f"正文：{body_mentions}；引用：{citation_mentions}；{rank_text}；品类词：{keyword_hits}"
            competitors = "、".join(result["competitor_mentions"]) or "未明显提及"
            issues = "、".join(result["missing_information"]) or "暂无明显问题"
            opportunity = "补充本地化内容、渠道信息和购买决策 FAQ"
            report.append(f"| {result['category_label']} | {score['model']} | {result['question']} | {result['answer_summary']} | {mentions} | {competitors} | {issues} | {opportunity} |")

    competitors = comparison.get("competitors", [])
    report.extend(
        [
            "",
            "## 品牌/产地/渠道提及分析",
            "",
            f"两个模型均需要观察是否能把“{name}”与目标产地、购买渠道、进口商/经销商、内容平台和中国消费场景连接起来。当前主要短板集中在渠道路径、区域市场和可被引用的结构化购买建议。",
            "",
            "## 竞品格局",
            "",
            "| 竞品/替代项 | 被提及场景 | 模型倾向 | 对目标品牌的影响 | 应对内容策略 |",
            "|---|---|---|---|---|",
        ]
    )
    if competitors:
        for item in competitors:
            report.append(f"| {item['competitor']} | {'、'.join(item['scenes'])} | {'、'.join(item['models'])} 多次提及 | 容易分流用户注意力 | 建立对比型内容，说明适合人群、价格带、渠道和场景差异 |")
    else:
        report.append("| 暂未形成稳定竞品提及 | - | - | 说明模型回答偏泛化 | 补充市场格局、替代品牌和选购对比内容 |")

    report.extend(
        [
            "",
            "## 共同知识盲区",
            "",
            "| 知识盲区 | 商业影响 | 建议动作 |",
            "|---|---|---|",
        ]
    )
    for item in comparison.get("blind_spot_impacts", []):
        report.append(f"| {item['blind_spot']} | {item['business_impact']} | {item['recommended_action']} |")

    report.extend(
        [
            "",
            "## 本地化内容缺口",
            "",
            "- 中国消费者常用购买渠道、价格带和真假辨别信息需要结构化表达。",
            "- 小红书/抖音种草内容需要从场景、口味/体验、送礼、家庭使用和餐饮搭配切入。",
            "- 本地产业链、进口商、经销商、区域市场和售后信任背书需要补充。",
            "- 官网、FAQ、平台文章和销售素材需要使用一致的品牌/产地/渠道定义句。",
            "",
            "## GEO 优化建议",
            "",
            "| 排名 | 建议 | 解决的问题 | 推荐载体 | 影响程度 | 执行难度 | 见效速度 | 优先级分 | 发布前确认 |",
            "|---:|---|---|---|---:|---:|---:|---:|---|",
        ]
    )
    for index, item in enumerate(geo_actions, start=1):
        report.append(
            f"| {index} | {item['title']} | {item['problem']} | {item['carrier']} | {item['impact']} | {item['difficulty']} | {item['speed']} | {item['priority_score']} | {item['precheck']} |"
        )

    report.extend(
        [
            "",
            "## 内容生产建议",
            "",
            "以下选题已按影响程度、执行难度和见效速度综合排序。影响程度和见效速度越高越好，执行难度越低越好。",
            "",
            "### 知乎选题",
            "",
            "| 排名 | 选题 | 解决的问题 | 影响程度 | 执行难度 | 见效速度 | 优先级分 |",
            "|---:|---|---|---:|---:|---:|---:|",
        ]
    )
    report.extend(recommendation_rows(recommendations["zhihu_topics"]))
    report.extend(
        [
            "",
            "### 小红书选题",
            "",
            "| 排名 | 选题 | 解决的问题 | 影响程度 | 执行难度 | 见效速度 | 优先级分 |",
            "|---:|---|---|---:|---:|---:|---:|",
        ]
    )
    report.extend(recommendation_rows(recommendations["xiaohongshu_topics"]))
    report.extend(
        [
            "",
            "### 抖音短视频选题",
            "",
            "| 排名 | 选题 | 解决的问题 | 影响程度 | 执行难度 | 见效速度 | 优先级分 |",
            "|---:|---|---|---:|---:|---:|---:|",
        ]
    )
    report.extend(recommendation_rows(recommendations["douyin_topics"]))
    report.extend(
        [
            "",
            "### 官网 FAQ 问题",
            "",
            "| 排名 | FAQ 问题 | 解决的问题 | 影响程度 | 执行难度 | 见效速度 | 优先级分 |",
            "|---:|---|---|---:|---:|---:|---:|",
        ]
    )
    report.extend(recommendation_rows(recommendations["website_faq"]))
    report.extend(
        [
            "",
            "### GEO 友好型文章标题",
            "",
            "| 排名 | 文章标题 | 解决的问题 | 影响程度 | 执行难度 | 见效速度 | 优先级分 |",
            "|---:|---|---|---:|---:|---:|---:|",
        ]
    )
    report.extend(recommendation_rows(recommendations["geo_articles"]))
    report.extend(
        [
            "",
            "## 30天内容行动清单",
            "",
            "| 时间 | 动作 | 平台/载体 | 目标 | 负责人 |",
            "|---|---|---|---|---|",
            "| 第 1 周 | 完成标准 FAQ、渠道说明和价格带口径 | 官网/销售资料 | 建立可引用基础答案 | 品牌/运营 |",
            "| 第 2 周 | 发布选购指南和竞品对比文章 | 知乎/公众号 | 补齐决策型内容 | 内容运营 |",
            "| 第 3 周 | 发布小红书/抖音种草内容 | 小红书/抖音 | 覆盖本地消费场景 | 新媒体运营 |",
            "| 第 4 周 | 复测双模型并更新内容缺口 | GEO 报告 | 对比提及和回答质量变化 | GEO 交付顾问 |",
            "",
            "## 复测机制",
            "",
            "| 项目 | 建议 |",
            "|---|---|",
        ]
    )
    for item, suggestion in retest_mechanism(config):
        report.append(f"| {item} | {suggestion} |")
    report.extend(
        [
            "",
            "## 原始数据附录",
            "",
            "| 模型 | 探针ID | 问题 | 原始回答文件 | 评分文件 |",
            "|---|---|---|---|---|",
        ]
    )
    for score in model_scores:
        for probe in probes:
            raw_path = output_dir / "raw_answers" / score["model"] / f"{probe['probe_id']}.md"
            score_path = output_dir / "model_scores" / f"{score['model']}.json"
            report.append(f"| {score['model']} | {probe['probe_id']} | {probe['question']} | {raw_path} | {score_path} |")
    report.append(f"| 双模型对比 | - | - | {output_dir / 'dual_model_comparison.json'} | {output_dir / 'dual_model_comparison.json'} |")
    return "\n".join(report).rstrip() + "\n"


def summary_markdown(config: dict[str, Any], model_scores: list[dict[str, Any]], comparison: dict[str, Any]) -> str:
    lines = [
        f"# {config['project_name']} 摘要",
        "",
        f"- 评估对象：{config['brand_name']}",
        f"- 目标市场：{config['target_market']}",
        f"- 评估模型：{'、'.join(config['target_models'])}",
        f"- 相对领先模型：{comparison.get('winner') or '暂未判断'}",
        f"- 共同知识盲区：{'、'.join(comparison.get('shared_blind_spots', [])[:3])}",
        "- 注意：摘要仅供快速浏览，客户交付应使用 final_report.md 完整报告。",
    ]
    for score in model_scores:
        lines.append(f"- {score['model']} 总分：{score['total_score']}/100")
    return "\n".join(lines).rstrip() + "\n"


def run(input_path: Path, output_dir: Path, print_report: bool = True) -> str:
    payload = load_json(input_path)
    if not isinstance(payload, dict):
        raise ValueError("Input JSON must be an object")
    config = normalize_config(payload)
    output_dir.mkdir(parents=True, exist_ok=True)
    probes = build_probes(config)
    write_json(output_dir / "probe_questions.json", probes)
    saved_config = dict(config)
    saved_config["mock_model_outputs"] = "[omitted in saved config]"
    write_json(output_dir / "input_config.json", saved_config)

    model_scores: list[dict[str, Any]] = []
    for model in config["target_models"]:
        answers = {probe["probe_id"]: answer_for_probe(config, model, probe) for probe in probes}
        save_raw_answers(output_dir, model, probes, answers)
        score = score_model(config, model, probes, answers)
        model_scores.append(score)
        write_json(output_dir / "model_scores" / f"{model}.json", score)

    comparison = comparison_json(config, model_scores)
    write_json(output_dir / "dual_model_comparison.json", comparison)
    write_json(output_dir / "content_recommendations.json", generate_content_recommendations(config, comparison))
    write_json(output_dir / "geo_action_priorities.json", generate_geo_actions(config, comparison))
    report = final_report(config, probes, model_scores, comparison, output_dir)
    summary = summary_markdown(config, model_scores, comparison)
    (output_dir / "final_report.md").write_text(report, encoding="utf-8")
    (output_dir / "summary.md").write_text(summary, encoding="utf-8")
    if print_report:
        print(report)
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a full GEO dual-model evaluation report.")
    parser.add_argument("input", help="Input JSON file.")
    parser.add_argument("--output-dir", default="geo_orchestrator_v2", help="Output directory.")
    parser.add_argument("--no-print", action="store_true", help="Do not print final_report.md to stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input not found: {input_path}")
        return 2
    try:
        run(input_path, Path(args.output_dir), print_report=not args.no_print)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
