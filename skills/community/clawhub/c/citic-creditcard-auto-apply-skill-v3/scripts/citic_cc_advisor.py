#!/usr/bin/env python3
"""CITIC credit card recommender and application assistant.

No third-party dependencies.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "card_catalog.json"


def load_catalog() -> List[Dict[str, Any]]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def load_profile(args: argparse.Namespace) -> Dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.profile:
        return json.loads(Path(args.profile).read_text(encoding="utf-8"))
    raise SystemExit("请通过 --json 或 --profile 提供客户画像。")


def normalize_texts(profile: Dict[str, Any]) -> List[str]:
    buckets: List[str] = []
    for key in ("interests", "spend_categories", "needs"):
        value = profile.get(key, []) or []
        if isinstance(value, str):
            buckets.append(value.lower())
        else:
            buckets.extend(str(v).lower() for v in value)
    for key in ("occupation", "city", "hotel_preference", "airline_preference"):
        if profile.get(key):
            buckets.append(str(profile[key]).lower())
    return buckets


def annual_fee_level(profile: Dict[str, Any]) -> str:
    value = str(profile.get("annual_fee_tolerance", "")).strip().lower()
    mapping = {
        "none": "none",
        "low": "low",
        "medium": "medium",
        "high": "high",
        "不接受": "none",
        "低": "low",
        "中": "medium",
        "高": "high",
    }
    return mapping.get(value, value or "low")


def explain_add(reasons: List[str], text: str) -> None:
    if text not in reasons:
        reasons.append(text)


def score_card(card: Dict[str, Any], profile: Dict[str, Any], terms: List[str]) -> Tuple[int, List[str], List[str]]:
    score = 0
    reasons: List[str] = []
    cautions: List[str] = []

    age = int(profile.get("age") or 0)
    monthly_income = float(profile.get("monthly_income") or 0)
    assets = float(profile.get("assets_with_citic") or 0)
    annual_fee_pref = annual_fee_level(profile)
    travel = str(profile.get("travel_frequency", "")).lower()
    intl = bool(profile.get("international_travel"))
    abroad = bool(profile.get("student_abroad"))
    car_owner = bool(profile.get("car_owner"))
    ev_owner = bool(profile.get("ev_owner"))
    hotel_pref = str(profile.get("hotel_preference", "")).lower()
    airline_pref = str(profile.get("airline_preference", "")).lower()

    joined = " ".join(terms)
    wants_points = any(k in joined for k in ["积分", "points", "咖啡", "网购", "线上", "返现"])
    wants_miles = any(k in joined for k in ["里程", "航司", "国航", "凤凰知音", "机票"])
    wants_hotel = any(k in joined for k in ["酒店", "住宿", "万豪", "bonvoy"])
    wants_delay = any(k in joined for k in ["航延", "延误", "机场", "贵宾厅", "安检"])
    wants_car = any(k in joined for k in ["车", "加油", "充电", "洗车", "停车"])
    wants_overseas = any(k in joined for k in ["出国", "境外", "留学", "外币", "海外", "国际"])
    likes_theme = any(k in joined for k in ["颜值", "主题", "好看", "设计"])

    slug = card["slug"]

    if age and not (18 <= age <= 60):
        cautions.append("中信官网主卡申请年龄一般为18至60周岁，当前年龄需人工复核。")
        score -= 50

    if slug == "yan-standard-platinum":
        score += 30
        if 22 <= age <= 35:
            score += 8
            explain_add(reasons, "年龄段更贴近年轻客群/入门白金定位。")
        if annual_fee_pref in {"none", "low"}:
            score += 8
            explain_add(reasons, "首年免年费、次年刷卡达标可免年费，适合低年费偏好。")
        if likes_theme or any(k in joined for k in ["餐饮", "日常", "通用"]):
            score += 6
            explain_add(reasons, "适合日常消费和颜值偏好。")
        if wants_hotel or wants_miles or wants_car:
            score -= 3
            cautions.append("这张卡更偏通用消费，不是酒店/车主/里程强联名卡。")

    elif slug == "i-platinum":
        score += 36
        if monthly_income >= 5000:
            score += 8
            explain_add(reasons, "月收入达到官网建议申请参考线。")
        if 25 <= age <= 35:
            score += 6
            explain_add(reasons, "年龄接近官网快捷申请参考年龄。")
        if wants_points:
            score += 10
            explain_add(reasons, "1.5倍积分和网络交易积分更适合线上消费/积分需求。")
        if wants_delay or travel in {"occasional", "frequent"}:
            score += 9
            explain_add(reasons, "有2小时航延险和500万航意险，适合兼顾出行保障。")
        if annual_fee_pref == "none":
            score -= 3
            cautions.append("虽有减免机制，但并非绝对零年费卡。")

    elif slug == "yueka-gold":
        score += 32
        if wants_points:
            score += 12
            explain_add(reasons, "核心卖点是多倍积分。")
        if assets >= 50000:
            score += 12
            explain_add(reasons, "在中信有5万元以上资产时，悦卡积分价值更明显。")
        elif assets > 0:
            score += 5
            explain_add(reasons, "已有中信资产沉淀，可更好发挥悦卡积分规则。")
        else:
            cautions.append("如无中信资产、且不关注积分，悦卡优势会下降。")
        if annual_fee_pref in {"none", "low"}:
            score += 2
        if wants_hotel or wants_car:
            score -= 2

    elif slug == "yueka-platinum":
        score += 30
        if wants_points:
            score += 12
            explain_add(reasons, "白金悦卡更适合把积分回报做大。")
        if assets >= 200000:
            score += 15
            explain_add(reasons, "中信资产20万元以上时，多倍积分潜力更强。")
        elif assets >= 50000:
            score += 8
            explain_add(reasons, "已有一定资产基础，能部分发挥悦卡价值。")
        if annual_fee_pref in {"none", "low"}:
            score -= 12
            cautions.append("白金悦卡首年刚性年费，年费敏感客户需谨慎。")
        else:
            explain_add(reasons, "客户对年费容忍度较高，可接受白金权益结构。")

    elif slug == "marriott-premium":
        score += 22
        if wants_hotel or "万豪" in hotel_pref or "marriott" in hotel_pref:
            score += 24
            explain_add(reasons, "客户明确偏好万豪/酒店权益，这张卡匹配度很高。")
        if travel == "frequent":
            score += 10
            explain_add(reasons, "高频商旅更能用到会籍、房晚和免费房晚。")
        if annual_fee_pref in {"none", "low"}:
            score -= 10
            cautions.append("年费980元，不适合完全不接受年费的客户。")
        if monthly_income < 8000:
            cautions.append("如果只是普通日常消费，980元年费的性价比未必合适。")

    elif slug == "iche-pro":
        score += 18
        if car_owner or ev_owner or wants_car:
            score += 28
            explain_add(reasons, "客户存在明显车主/充电/加油/洗车需求。")
        else:
            score -= 10
            cautions.append("无车客户通常不建议优先推荐车主卡。")
        if annual_fee_pref in {"none", "low"}:
            score += 5
            explain_add(reasons, "刷卡达标免年费，年费压力相对可控。")

    elif slug == "visa-xiaoyao":
        score += 22
        if intl or abroad or wants_overseas:
            score += 28
            explain_add(reasons, "客户有境外/留学/国际出行需求，匹配这张卡的核心权益。")
        if wants_points:
            score += 4
            explain_add(reasons, "境外交易2倍积分对海外消费有帮助。")
        if not (intl or abroad or wants_overseas):
            cautions.append("如果客户几乎没有境外需求，这张卡不会是最高优先级。")

    elif slug == "feichangzhun":
        score += 24
        if travel == "frequent" or wants_delay:
            score += 24
            explain_add(reasons, "高频飞行/航延保障需求与飞常准联名卡高度匹配。")
        if annual_fee_pref in {"none", "low"}:
            score += 6
            explain_add(reasons, "刷卡达标免年费，适合控制用卡成本。")
        if any(k in joined for k in ["机场", "贵宾厅", "快速安检"]):
            score += 5
            explain_add(reasons, "客户重视机场体验，可用到贵宾厅和快速安检类权益。")

    elif slug == "guohang-ctrip":
        score += 18
        if wants_miles or any(k in airline_pref for k in ["国航", "凤凰知音", "air china"]):
            score += 30
            explain_add(reasons, "客户明确偏好国航/凤凰知音体系，里程匹配度高。")
        if any(k in joined for k in ["携程", "差旅", "机票"]):
            score += 8
            explain_add(reasons, "机票/携程/差旅场景较多，可发挥联名价值。")
        if annual_fee_pref in {"none", "low"}:
            explain_add(reasons, "可优先考虑金卡版本，刷卡免年费。")
        if not wants_miles and travel == "rare":
            cautions.append("若并非国航用户、也不积里程，这张卡优势有限。")

    return score, reasons, cautions


def rank_cards(profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    catalog = load_catalog()
    terms = normalize_texts(profile)
    ranked: List[Dict[str, Any]] = []
    for card in catalog:
        if card.get("status") != "active":
            continue
        score, reasons, cautions = score_card(card, profile, terms)
        ranked.append({
            "score": score,
            "card": card,
            "reasons": reasons,
            "cautions": cautions,
        })
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked


def recommend_markdown(profile: Dict[str, Any]) -> str:
    top = rank_cards(profile)[:3]
    lines: List[str] = []
    lines.append("# 中信银行信用卡推荐结果\n")
    lines.append(
        f"客户年龄：{profile.get('age', '未提供')}；月收入：{profile.get('monthly_income', '未提供')}；年费容忍度：{profile.get('annual_fee_tolerance', '未提供')}\n"
    )
    lines.append("## 推荐TOP 3\n")
    for idx, item in enumerate(top, 1):
        score = item["score"]
        card = item["card"]
        reasons = item["reasons"]
        cautions = item["cautions"]
        lines.append(f"### {idx}. {card['name']}  （匹配分：{score}）")
        lines.append(f"- 卡级：{card['tier']}")
        lines.append(f"- 年费：{card['annual_fee']}")
        lines.append(f"- 适合场景：{'、'.join(card['fit_tags'])}")
        lines.append(f"- 亮点：{'；'.join(card['highlights'])}")
        if reasons:
            lines.append(f"- 为什么推荐：{'；'.join(reasons[:4])}")
        if cautions:
            lines.append(f"- 提醒：{'；'.join(cautions[:3])}")
        lines.append(f"- 详情页：{card['detail_url']}")
        lines.append(f"- 申请页：{card.get('apply_url', card['detail_url'])}\n")

    lines.append("## 申请协助建议\n")
    lines.append("1. 先确认主卡申请年龄通常为18-60周岁。")
    lines.append("2. 网上申请通常需要填写工作单位信息；如无单位信息，可携带资料到网点尝试纸质申请。")
    lines.append("3. 柜台申请常见材料包括：身份证明、工作证明、财力证明。")
    lines.append("4. 进度查询可通过官网、短信 SQJD+证件号码 发送至106980095558、或官方微信/动卡空间办理。")
    lines.append("5. 最终卡种、额度、是否批核，以中信银行官方审批结果为准。")
    return "\n".join(lines)


def recommend_json(profile: Dict[str, Any]) -> Dict[str, Any]:
    ranked = rank_cards(profile)
    top = ranked[:3]
    return {
        "profile_summary": {
            "age": profile.get("age"),
            "monthly_income": profile.get("monthly_income"),
            "annual_fee_tolerance": profile.get("annual_fee_tolerance"),
        },
        "top_cards": [
            {
                "rank": idx,
                "score": item["score"],
                "slug": item["card"]["slug"],
                "name": item["card"]["name"],
                "tier": item["card"]["tier"],
                "annual_fee": item["card"]["annual_fee"],
                "fit_tags": item["card"]["fit_tags"],
                "detail_url": item["card"]["detail_url"],
                "apply_url": item["card"].get("apply_url", item["card"]["detail_url"]),
                "reasons": item["reasons"],
                "cautions": item["cautions"],
            }
            for idx, item in enumerate(top, 1)
        ],
        "recommended_card_slug": top[0]["card"]["slug"] if top else None,
    }


def assist(card_slug: str) -> str:
    catalog = load_catalog()
    matches = [c for c in catalog if c["slug"] == card_slug]
    if not matches:
        raise SystemExit(f"未找到卡片：{card_slug}")
    card = matches[0]
    lines = [f"# {card['name']} 申请协助", ""]
    lines.append(f"- 状态：{card['status']}")
    lines.append(f"- 卡级：{card['tier']}")
    lines.append(f"- 年费：{card['annual_fee']}")
    lines.append(f"- 详情页：{card['detail_url']}")
    if card.get("apply_url"):
        lines.append(f"- 申请页：{card['apply_url']}")
    if card.get("alternate_apply_url"):
        lines.append(f"- 备选申请页：{card['alternate_apply_url']}")
    lines.append("")
    lines.append("## 办理步骤")
    lines.append("1. 先确认年龄是否在18-60周岁，并准备身份证明。")
    lines.append("2. 如走线上申请，按官网页面填写个人信息、工作单位信息、联系方式等。")
    lines.append("3. 如页面或短信要求补充身份确认/面签/柜台办理，按官方提示办理。")
    lines.append("4. 如申请成功，按短信或寄卡指引激活电子卡/实体卡。")
    lines.append("")
    lines.append("## 常见材料")
    lines.append("- 身份证明：身份证、临时身份证、户口本等官方认可材料。")
    lines.append("- 工作证明：工作证复印件或单位开具的工作证明。")
    lines.append("- 财力证明：收入证明、工资流水、存款证明、房产证明等。")
    lines.append("")
    lines.append("## 进度跟踪")
    lines.append("- 官网办卡进度查询")
    lines.append("- 短信：SQJD+证件号码，发送到 106980095558")
    lines.append("- 微信公众号：中信银行信用卡（zxyhxyk）")
    lines.append("- 动卡空间 APP")
    lines.append("")
    lines.append("## 风险提示")
    lines.append("- 最终卡种、额度、年费和权益以官方申请页、条款细则和实际审批结果为准。")
    lines.append("- 对于已经停止发行的卡片，不要再推荐给新客户。")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="CITIC credit card advisor")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("recommend", help="生成推荐结果")
    p1.add_argument("--profile", help="客户画像 JSON 文件")
    p1.add_argument("--json", help="客户画像 JSON 字符串")
    p1.add_argument("--format", choices=["markdown", "json"], default="markdown", help="输出格式")

    p2 = sub.add_parser("assist", help="输出单卡申请协助说明")
    p2.add_argument("--card", required=True, help="卡片 slug")

    args = parser.parse_args()
    if args.cmd == "recommend":
        profile = load_profile(args)
        if args.format == "json":
            print(json.dumps(recommend_json(profile), ensure_ascii=False, indent=2))
        else:
            print(recommend_markdown(profile))
    elif args.cmd == "assist":
        print(assist(args.card))


if __name__ == "__main__":
    main()
