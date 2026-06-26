from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError as exc:  # pragma: no cover - runtime dependency check
    raise SystemExit(
        "缺少 psycopg。请先安装：python -m pip install psycopg[binary]"
    ) from exc

from render_report import ReportRenderer, ratio, sanitize_filename, star_score
from send_dingtalk import DingTalkWebhookClient, build_summary_markdown
from upload_oss import OssUploader


FEATURE_KEYWORDS = {
    "四季通用": ["四季", "四季通用"],
    "硅胶": ["硅胶"],
    "纱布": ["纱布"],
    "护脊": ["护脊", "护颈"],
    "可水洗": ["可水洗", "机洗", "水洗"],
    "分区": ["分区"],
    "记忆棉": ["记忆棉"],
    "蚕丝": ["蚕丝", "桑蚕丝"],
    "乳胶": ["乳胶"],
    "云朵": ["云朵"],
    "IP": ["ip", "卡通", "童话", "图案"],
}

NEED_KEYWORDS = {
    "柔软舒服": ["柔软", "舒服", "舒适"],
    "质量好": ["质量", "做工", "品质"],
    "尺寸大/够宽": ["尺寸", "够大", "够宽"],
    "护脊/护颈": ["护脊", "护颈"],
    "透气不闷汗": ["透气", "闷汗", "不闷"],
    "颜值高": ["颜值", "好看", "漂亮"],
    "可水洗/机洗": ["机洗", "水洗", "可水洗"],
    "高低合适": ["高度", "高低", "厚度"],
    "材质安全": ["安全", "异味小", "无毒"],
    "回购": ["回购", "复购"],
}

PAIN_KEYWORDS = {
    "异味": ["异味", "气味", "味道大"],
    "性价比/价格": ["贵", "价格", "性价比"],
    "缩水/变形": ["缩水", "变形", "塌陷"],
    "高度不合适": ["太高", "太低", "高度", "厚度"],
    "孩子不爱用": ["不爱用", "不用", "不喜欢"],
}

QA_BARRIERS = {
    "质量好吗": ["质量", "做工", "品质"],
    "适合多大年龄": ["年龄", "几岁", "多大"],
    "软硬度": ["软硬", "偏软", "偏硬"],
    "高度/厚度": ["高度", "厚度", "多高"],
    "怎么清洗": ["清洗", "机洗", "水洗"],
    "透气性": ["透气", "闷汗"],
    "味道": ["味道", "异味", "气味"],
}

ADVANTAGES = [
    ("纱布材质", "透气不闷汗", "⭐⭐⭐⭐⭐"),
    ("童话IP", "颜值与情感表达", "⭐⭐⭐⭐⭐"),
    ("小红书种草能力", "新品冷启动", "⭐⭐⭐⭐"),
    ("原创设计团队", "产品视觉差异化", "⭐⭐⭐⭐"),
    ("成熟供应链", "品质稳定性", "⭐⭐⭐⭐"),
    ("可水洗特性", "便捷清洁", "⭐⭐⭐⭐⭐"),
]


@dataclass
class CategoryDataset:
    category: str
    products: list[dict[str, Any]]
    reviews: list[dict[str, Any]]
    qas: list[dict[str, Any]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="BBT 竞品分析报告 CLI")
    parser.add_argument("--dsn", default=os.getenv("COMPETITIVE_ANALYSIS_DSN"), help="PostgreSQL DSN")
    parser.add_argument("--category", default=None, help="只分析指定 category")
    parser.add_argument("--since-months", type=int, default=6, help="统计窗口（月）")
    parser.add_argument("--limit", type=int, default=20, help="单次最多消费多少条 trigger")
    parser.add_argument("--brand", default="BUBBLETREE", help="报告品牌名")
    parser.add_argument("--reporter", default="自动分析任务", help="报告人")
    return parser.parse_args()


class CompetitiveAnalysisRepository:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn

    def connect(self):
        return psycopg.connect(self.dsn, row_factory=dict_row)

    def ensure_trigger_columns(self, conn: psycopg.Connection) -> None:
        query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'competitive_crawl_trigger'
          AND column_name IN (
              'is_consumed',
              'consumed_at',
              'consume_status',
              'consume_attempts',
              'consume_error',
              'last_report_path'
          )
        """
        with conn.cursor() as cur:
            cur.execute(query)
            present = {row["column_name"] for row in cur.fetchall()}
        required = {
            "is_consumed",
            "consumed_at",
            "consume_status",
            "consume_attempts",
            "consume_error",
            "last_report_path",
        }
        missing = required - present
        if missing:
            missing_text = ", ".join(sorted(missing))
            raise RuntimeError(
                f"competitive_crawl_trigger 缺少消费字段：{missing_text}。"
                "请先补齐数据库表结构后再运行该 skill。"
            )

    def fetch_pending_trigger_ids(self, conn: psycopg.Connection, limit: int) -> list[int]:
        sql = """
        SELECT id
        FROM competitive_crawl_trigger
        WHERE status = 'success'
          AND COALESCE(is_consumed, FALSE) = FALSE
        ORDER BY update_time ASC, id ASC
        LIMIT %s
        """
        with conn.cursor() as cur:
            cur.execute(sql, (limit,))
            return [row["id"] for row in cur.fetchall()]

    def increment_attempts(self, conn: psycopg.Connection, trigger_ids: list[int]) -> None:
        if not trigger_ids:
            return
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE competitive_crawl_trigger
                SET consume_attempts = COALESCE(consume_attempts, 0) + 1,
                    consume_status = 'pending'
                WHERE id = ANY(%s)
                """,
                (trigger_ids,),
            )

    def mark_success(self, conn: psycopg.Connection, trigger_ids: list[int], manifest_path: str) -> None:
        if not trigger_ids:
            return
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE competitive_crawl_trigger
                SET is_consumed = TRUE,
                    consumed_at = CURRENT_TIMESTAMP,
                    consume_status = 'success',
                    consume_error = NULL,
                    last_report_path = %s
                WHERE id = ANY(%s)
                """,
                (manifest_path, trigger_ids),
            )

    def mark_failure(self, conn: psycopg.Connection, trigger_ids: list[int], error_text: str) -> None:
        if not trigger_ids:
            return
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE competitive_crawl_trigger
                SET consume_status = 'failed',
                    consume_error = %s
                WHERE id = ANY(%s)
                """,
                (error_text[:2000], trigger_ids),
            )

    def fetch_categories(self, conn: psycopg.Connection, since_date: date, category_filter: str | None) -> list[str]:
        sql = """
        SELECT DISTINCT category
        FROM competitive_product_list
        WHERE category IS NOT NULL
          AND COALESCE(etl_date, etl_time::date) >= %s
        """
        params: list[Any] = [since_date]
        if category_filter:
            sql += " AND category = %s"
            params.append(category_filter)
        sql += " ORDER BY category ASC"
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return [row["category"] for row in cur.fetchall()]

    def fetch_dataset(self, conn: psycopg.Connection, category: str, since_date: date) -> CategoryDataset:
        products_sql = """
        SELECT product_id, category, shop_name, product_url, product_name, etl_date, etl_time
        FROM competitive_product_list
        WHERE category = %s
          AND COALESCE(etl_date, etl_time::date) >= %s
        """
        reviews_sql = """
        SELECT r.product_id, r.review_time, r.review_content, r.etl_date, r.etl_time
        FROM competitive_review r
        JOIN competitive_product_list p ON p.product_id = r.product_id
        WHERE p.category = %s
          AND COALESCE(r.review_time::date, r.etl_date, r.etl_time::date) >= %s
        """
        qa_sql = """
        SELECT q.product_id, q.question, q.answer, q.etl_date, q.etl_time
        FROM competitive_qa q
        JOIN competitive_product_list p ON p.product_id = q.product_id
        WHERE p.category = %s
          AND COALESCE(q.etl_date, q.etl_time::date) >= %s
        """
        with conn.cursor() as cur:
            cur.execute(products_sql, (category, since_date))
            products = cur.fetchall()
            cur.execute(reviews_sql, (category, since_date))
            reviews = cur.fetchall()
            cur.execute(qa_sql, (category, since_date))
            qas = cur.fetchall()
        return CategoryDataset(category=category, products=products, reviews=reviews, qas=qas)


def months_ago(months: int) -> date:
    return date.today() - timedelta(days=max(months, 1) * 30)


def normalize_brand(value: str | None) -> str:
    if not value:
        return "未识别品牌"
    result = value.strip()
    for suffix in ("旗舰店", "官方旗舰店", "官方店", "专营店", "专卖店", "企业店", "店"):
        result = result.replace(suffix, "")
    result = re.sub(r"\s+", "", result)
    return result[:20] or "未识别品牌"


def infer_brand(product: dict[str, Any]) -> str:
    shop_name = normalize_brand(product.get("shop_name"))
    if shop_name != "未识别品牌":
        return shop_name
    product_name = product.get("product_name") or ""
    token = re.split(r"[\s/|·,【】（）()\-]", product_name)[0]
    return normalize_brand(token)


def collect_texts(dataset: CategoryDataset) -> list[str]:
    texts: list[str] = []
    for product in dataset.products:
        texts.append(product.get("product_name") or "")
    for review in dataset.reviews:
        texts.append(review.get("review_content") or "")
    for qa in dataset.qas:
        texts.append(qa.get("question") or "")
        texts.append(qa.get("answer") or "")
    return texts


def count_keyword_map(texts: list[str], mapping: dict[str, list[str]]) -> Counter[str]:
    counter: Counter[str] = Counter()
    joined = "\n".join(texts).lower()
    for label, keywords in mapping.items():
        for keyword in keywords:
            counter[label] += joined.count(keyword.lower())
    return counter


def brand_feature_profile(products: list[dict[str, Any]]) -> dict[str, Counter[str]]:
    profile: dict[str, Counter[str]] = defaultdict(Counter)
    for product in products:
        brand = infer_brand(product)
        text = (product.get("product_name") or "").lower()
        for label, keywords in FEATURE_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    profile[brand][label] += 1
    return profile


def infer_positioning(feature_counter: Counter[str], brand_name: str) -> tuple[str, str]:
    brand_lower = brand_name.lower()
    if feature_counter["蚕丝"] > 0:
        return "高端型", "高端材质驱动"
    if feature_counter["IP"] > 0 or feature_counter["云朵"] > 0:
        return "外观型", "视觉或情绪表达"
    if feature_counter["护脊"] > 0 or feature_counter["分区"] > 0:
        return "功能型", "强调功能和支撑"
    if "官方" in brand_lower or feature_counter["可水洗"] > 0:
        return "便捷型", "强调便捷和基础功能"
    return "舒适型", "基础舒适诉求"


def top_rows(counter: Counter[str], label_name: str, total: int, limit: int = 10) -> list[dict[str, Any]]:
    rows = []
    for index, (name, count) in enumerate(counter.most_common(limit), start=1):
        rows.append({"排序": index, label_name: name, "频次": count, "占比": ratio(count, total)})
    return rows


def placeholder_price_distribution(brands: list[str]) -> list[dict[str, Any]]:
    brands = brands or ["待补充品牌"]
    return [{"品牌": brand, "主价格带": "未采集价格字段", "价格策略": "待补充"} for brand in brands[:10]]


def price_band_placeholder() -> list[dict[str, Any]]:
    return [
        {"价格带": "100元以下", "竞争状况": "未采集价格字段", "机会评估": "待补充"},
        {"价格带": "100-150元", "竞争状况": "未采集价格字段", "机会评估": "待补充"},
        {"价格带": "150-200元", "竞争状况": "未采集价格字段", "机会评估": "待补充"},
        {"价格带": "200-300元", "竞争状况": "未采集价格字段", "机会评估": "待补充"},
        {"价格带": "300元以上", "竞争状况": "未采集价格字段", "机会评估": "待补充"},
    ]


def build_report(dataset: CategoryDataset, brand: str, reporter: str, since_months: int) -> dict[str, Any]:
    texts = collect_texts(dataset)
    feature_counts = count_keyword_map(texts, FEATURE_KEYWORDS)
    need_counts = count_keyword_map([row.get("review_content") or "" for row in dataset.reviews], NEED_KEYWORDS)
    pain_counts = count_keyword_map([row.get("review_content") or "" for row in dataset.reviews], PAIN_KEYWORDS)
    qa_counts = count_keyword_map([row.get("question") or "" for row in dataset.qas], QA_BARRIERS)

    brands = Counter(infer_brand(product) for product in dataset.products)
    brand_profiles = brand_feature_profile(dataset.products)
    total_reviews = len(dataset.reviews)
    total_products = len(dataset.products)
    total_qas = len(dataset.qas)
    brand_total = sum(brands.values())

    dominant_material = feature_counts.most_common(1)[0][0] if feature_counts else "未明显集中"
    top_pain = pain_counts.most_common(1)[0][0] if pain_counts else "暂无明显痛点"
    whitespace_candidates = []
    if feature_counts["纱布"] == 0:
        whitespace_candidates.append(("纱布材质", 5, "当前样本中未发现明显纱布卖点"))
    if feature_counts["IP"] == 0:
        whitespace_candidates.append(("IP故事", 5, "样本缺少情绪化故事表达"))
    if feature_counts["可水洗"] == 0:
        whitespace_candidates.append(("整枕清洗", 4, "便捷清洗卖点较弱"))
    whitespace_candidates.append(("价格带洞察", 3, "当前缺少价格字段，建议补采后确认空白带"))

    if not whitespace_candidates:
        whitespace_candidates.append(("细分功能组合", 3, "可从人群与场景组合中继续寻找机会"))

    brand_ranking = []
    for index, (brand_name, count) in enumerate(brands.most_common(10), start=1):
        brand_ranking.append(
            {"排名": index, "品牌": brand_name, "商品数": count, "占比": ratio(count, brand_total)}
        )

    brand_matrix = []
    positioning_groups: dict[str, list[str]] = defaultdict(list)
    for brand_name, count in brands.most_common(10):
        features = brand_profiles.get(brand_name, Counter())
        positioning, positioning_summary = infer_positioning(features, brand_name)
        feature_labels = "、".join(name for name, _ in features.most_common(3)) or "待补充"
        diff_label = "、".join(name for name, _ in features.most_common(2)) or "待补充"
        brand_matrix.append(
            {
                "品牌": brand_name,
                "指标值": count,
                "占比": ratio(count, brand_total),
                "商品数": count,
                "定位": positioning,
                "核心功能": feature_labels,
                "差异化标签": diff_label,
            }
        )
        positioning_groups[positioning].append(brand_name)

    positioning_rows = []
    for positioning, names in positioning_groups.items():
        sample_counter = brand_profiles.get(names[0], Counter())
        _, core_characteristic = infer_positioning(sample_counter, names[0])
        positioning_rows.append(
            {
                "定位类型": positioning,
                "代表品牌": "、".join(names[:3]),
                "核心特点": core_characteristic,
                "机会分析": "保留结构化定位，但需结合价格与销量补强判断",
            }
        )

    whitespace_rows = [
        {"空白点": name, "机会等级": star_score(level), "说明": note}
        for name, level, note in whitespace_candidates[:5]
    ]

    feature_frequency = []
    for feature_name, count in feature_counts.most_common(10):
        feature_frequency.append(
            {"功能": feature_name, "出现次数": count, "占比": ratio(count, max(len(texts), 1)), "备注": "关键词命中"}
        )

    user_needs = top_rows(need_counts, "需求", max(total_reviews, 1))
    pain_points = []
    severity_map = {"异味": "高", "性价比/价格": "中", "缩水/变形": "中", "高度不合适": "中", "孩子不爱用": "低"}
    for index, (label, count) in enumerate(pain_counts.most_common(10), start=1):
        pain_points.append(
            {"排序": index, "痛点": label, "频次": count, "严重程度": severity_map.get(label, "中")}
        )

    purchase_barriers = []
    for label, count in qa_counts.most_common(10):
        purchase_barriers.append({"问题类型": label, "频次": count, "占比": ratio(count, max(total_qas, 1))})

    fallback_summary = (
        f"基于最近 {since_months} 个月 `{dataset.category}` 类目数据，"
        f"共纳入 {total_products} 个竞品商品、{total_reviews} 条评论、{total_qas} 条问答。"
        f"当前样本显示 `{dominant_material}` 相关卖点更常见，用户集中关注 "
        f"`{user_needs[0]['需求'] if user_needs else '舒适与安全'}`，"
        f"同时 `{top_pain}` 是最突出痛点。"
    )

    fallback_suggestions = [
        f"围绕 `{dataset.category}` 的高频需求做清晰卖点组合，优先强化 {user_needs[0]['需求'] if user_needs else '舒适与安全'}。",
        "价格字段当前待补充，建议先补齐价格与销量后再细化价格带决策。",
        "将评论痛点和问答疑虑前置到详情页与客服话术中，降低转化阻力。",
    ]
    fallback_feature_insights = [
        f"`{dominant_material}` 相关词在样本中更常见，可视为当前市场主流表达。",
        f"`{top_pain}` 是评论端最明显的问题，应优先纳入差异化改进。",
        f"`{whitespace_rows[0]['空白点']}` 可作为下一步重点验证方向。",
    ]
    fallback_product_definition = (
        f"围绕 `{dataset.category}` 构建“核心舒适体验 + 易清洁/易理解卖点 + 情绪化表达”的产品方案，"
        "价格待补充后再锁定主攻价格带。"
    )
    fallback_risk_controls = [
        "先小规模验证样本判断，再扩大生产和投放。",
        "补采价格、销量、年龄段字段，避免策略建立在信息缺口上。",
        "把评论高频痛点纳入质检和客服 SOP，降低上市初期负反馈。",
    ]

    report = {
        "title": f"{brand}{dataset.category}市场机会分析报告",
        "brand": brand,
        "category": dataset.category,
        "reporter": reporter,
        "analysis_date": datetime.now().strftime("%Y年%m月%d日"),
        "data_source": f"竞品商品({total_products}个) + 竞品评论({total_reviews}条) + 买家问答({total_qas}条)",
        "executive_summary": fallback_summary,
        "key_findings": [
            {"维度": "市场机会", "核心结论": whitespace_rows[0]["说明"]},
            {"维度": "材质趋势", "核心结论": f"{dominant_material} 相关表达更常见"},
            {"维度": "最大痛点", "核心结论": top_pain},
            {"维度": "竞品短板", "核心结论": "价格与品牌定位信息仍需补采，当前市场表达同质化"},
            {"维度": "你们优势", "核心结论": "纱布、IP、内容种草能力可作为差异化抓手"},
        ],
        "core_suggestions": fallback_suggestions[:3],
        "sample_overview": [
            {"数据类型": "竞品样本", "数量": total_products, "说明": f"{dataset.category} 商品清单"},
            {"数据类型": "买家评论", "数量": total_reviews, "说明": "评论文本采集"},
            {"数据类型": "买家问答", "数量": total_qas, "说明": "问答文本采集"},
            {"数据类型": "品牌数", "数量": len(brands), "说明": "按店铺/标题启发式推断"},
        ],
        "brand_ranking": brand_ranking or [{"排名": 1, "品牌": "待补充", "商品数": 0, "占比": "0.0%"}],
        "brand_matrix": brand_matrix or [{"品牌": "待补充", "指标值": 0, "占比": "0.0%", "商品数": 0, "定位": "待补充", "核心功能": "待补充", "差异化标签": "待补充"}],
        "brand_positioning": positioning_rows or [{"定位类型": "待补充", "代表品牌": "待补充", "核心特点": "待补充", "机会分析": "待补充"}],
        "price_distribution": placeholder_price_distribution([name for name, _ in brands.most_common(10)]),
        "brand_strategy": [
            {"打法": "功能表达", "代表品牌": "、".join(name for name, _ in brands.most_common(3)) or "待补充", "你们的应对": "围绕高频需求做更清晰的组合卖点"},
            {"打法": "材质表达", "代表品牌": dominant_material, "你们的应对": "用差异材质或触感体验形成记忆点"},
            {"打法": "详情页答疑", "代表品牌": "头部竞品", "你们的应对": "把 QA 高频问题前置到内容与客服话术"},
        ],
        "whitespace": whitespace_rows,
        "feature_frequency": feature_frequency or [{"功能": "待补充", "出现次数": 0, "占比": "0.0%", "备注": "无数据"}],
        "feature_insights": fallback_feature_insights[:5],
        "price_band_analysis": price_band_placeholder(),
        "user_needs": user_needs or [{"排序": 1, "需求": "待补充", "频次": 0, "占比": "0.0%"}],
        "pain_points": pain_points or [{"排序": 1, "痛点": "待补充", "频次": 0, "严重程度": "中"}],
        "purchase_barriers": purchase_barriers or [{"问题类型": "待补充", "频次": 0, "占比": "0.0%"}],
        "advantages": [{"你们的优势": name, "对应用户需求": need, "匹配度": score} for name, need, score in ADVANTAGES],
        "differentiation": [
            {"差异化维度": whitespace_rows[0]["空白点"], "竞品现状": whitespace_rows[0]["说明"], "你们机会": "优先验证并占位", "强度": whitespace_rows[0]["机会等级"]},
            {"差异化维度": "用户痛点修复", "竞品现状": f"当前突出痛点为 {top_pain}", "你们机会": "将痛点反向设计为核心卖点", "强度": "⭐⭐⭐⭐"},
            {"差异化维度": "内容表达", "竞品现状": "问答端顾虑分散", "你们机会": "用种草内容与详情页统一解释", "强度": "⭐⭐⭐⭐"},
        ],
        "product_definition": fallback_product_definition,
        "sku_suggestions": [
            {"SKU": "基础款", "定价": "待补充", "目标年龄": "待补充", "规格": f"{dataset.category}基础配置"},
            {"SKU": "升级款", "定价": "待补充", "目标年龄": "待补充", "规格": f"{dataset.category}差异化配置"},
        ],
        "selling_points": [
            f"解决 `{top_pain}` 的明确方案",
            f"围绕 `{user_needs[0]['需求'] if user_needs else '舒适与安全'}` 做一眼可懂的表达",
            "用内容化或 IP 化叙事提升记忆点",
        ],
        "product_actions": [
            {"阶段": "P0", "行动": "确认核心卖点与采样验证", "时间": "1-2周", "负责人": "产品"},
            {"阶段": "P1", "行动": "完成样品和体验验证", "时间": "2周", "负责人": "研发"},
            {"阶段": "P2", "行动": "整理详情页和客服答疑素材", "时间": "1周", "负责人": "运营"},
        ],
        "go_to_market_actions": [
            {"阶段": "P3", "行动": "内容种草测试", "时间": "2周", "渠道": "小红书/抖音"},
            {"阶段": "P4", "行动": "详情页迭代和首轮投放", "时间": "2周", "渠道": "电商平台"},
            {"阶段": "P5", "行动": "复盘评论与 QA 反馈", "时间": "持续", "渠道": "全渠道"},
        ],
        "goals": [
            {"指标": "转化效率", "3个月目标": "建立稳定基线", "6个月目标": "形成可复制打法"},
            {"指标": "内容验证", "3个月目标": "完成首轮卖点测试", "6个月目标": "沉淀高转化素材"},
            {"指标": "用户反馈", "3个月目标": "降低高频痛点", "6个月目标": "形成口碑词"},
        ],
        "risks": [
            {"风险": "关键字段缺失", "概率": "中", "影响": "高", "应对": "补采价格、销量、年龄层字段"},
            {"风险": "启发式品牌识别偏差", "概率": "中", "影响": "中", "应对": "补品牌主数据校准"},
            {"风险": "重复消费 trigger", "概率": "低", "影响": "中", "应对": "依赖消费字段和状态回写"},
        ],
        "risk_controls": fallback_risk_controls[:5],
        "methods": [
            "竞品商品清单聚合",
            "评论关键词统计与痛点提取",
            "买家问答意图分类",
            "启发式品牌与功能标签识别",
        ],
        "sources": [
            "competitive_product_list",
            "competitive_review",
            "competitive_qa",
            "competitive_crawl_trigger",
        ],
        "host_analysis_context": {
            "instruction": "该文件由脚本完成取数与基础聚合，执行摘要、建议、机会判断等深度分析应由 skill 宿主基于本上下文和 references/report-outline.md 继续生成。",
            "category": dataset.category,
            "since_months": since_months,
            "counts": {
                "product_count": total_products,
                "review_count": total_reviews,
                "qa_count": total_qas,
                "brand_count": len(brands),
            },
            "derived_insights": {
                "dominant_material": dominant_material,
                "top_need": user_needs[0]["需求"] if user_needs else "舒适与安全",
                "top_pain": top_pain,
                "whitespace": whitespace_rows,
            },
        },
    }
    return report


def write_analysis_context(report: dict[str, Any], rendered_dir: Path) -> Path:
    context_path = rendered_dir / "analysis_context.json"
    context_payload = {
        "title": report["title"],
        "brand": report["brand"],
        "category": report["category"],
        "analysis_date": report["analysis_date"],
        "data_source": report["data_source"],
        "report_outline_source": "skills/competitive_analysis/references/report-outline.md",
        "host_analysis_context": report["host_analysis_context"],
        "report_payload": report,
    }
    context_path.write_text(json.dumps(context_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return context_path


def main() -> int:
    args = parse_args()
    if not args.dsn:
        raise SystemExit("缺少 PostgreSQL DSN，请通过 --dsn 或 COMPETITIVE_ANALYSIS_DSN 传入。")

    repository = CompetitiveAnalysisRepository(args.dsn)
    oss_uploader = OssUploader.from_env()
    if not oss_uploader:
        raise SystemExit(
            "缺少 OSS 配置，请设置 "
            "OSS_ENDPOINT/OSS_BUCKET/OSS_ACCESS_KEY_ID/OSS_ACCESS_KEY_SECRET。"
        )

    webhook = os.getenv("DINGTALK_WEBHOOK")
    secret = os.getenv("DINGTALK_SECRET")
    if not webhook:
        raise SystemExit("缺少 DINGTALK_WEBHOOK。")
    dingtalk = DingTalkWebhookClient(webhook, secret)

    since_date = months_ago(args.since_months)
    with TemporaryDirectory(prefix="competitive-analysis-") as temp_dir:
        output_root = Path(temp_dir).resolve() / datetime.now().strftime("%Y%m%d-%H%M%S")
        output_root.mkdir(parents=True, exist_ok=True)
        renderer = ReportRenderer(output_root)

        with repository.connect() as conn:
            repository.ensure_trigger_columns(conn)
            trigger_ids = repository.fetch_pending_trigger_ids(conn, args.limit)
            if not trigger_ids:
                print("没有待消费的 success trigger，退出。")
                return 0

            repository.increment_attempts(conn, trigger_ids)
            conn.commit()

            try:
                categories = repository.fetch_categories(conn, since_date, args.category)
                reports_manifest: dict[str, Any] = {
                    "generated_at": datetime.now().isoformat(),
                    "trigger_ids": trigger_ids,
                    "since_date": since_date.isoformat(),
                    "categories": [],
                }

                if not categories:
                    reports_manifest["message"] = "分析窗口内无可分析 category"
                else:
                    for category in categories:
                        dataset = repository.fetch_dataset(conn, category, since_date)
                        report = build_report(dataset, args.brand, args.reporter, args.since_months)
                        rendered = renderer.render(report)
                        context_path = write_analysis_context(report, rendered.markdown_path.parent)

                        rel_base = f"{output_root.name}/{rendered.markdown_path.parent.name}"
                        md_key = oss_uploader.key_for(f"{rel_base}/report.md")
                        html_key = oss_uploader.key_for(f"{rel_base}/report.html")
                        ctx_key = oss_uploader.key_for(f"{rel_base}/analysis_context.json")
                        uploaded = {
                            "report_md": oss_uploader.upload_file(rendered.markdown_path, md_key).public_url,
                            "report_html": oss_uploader.upload_file(rendered.html_path, html_key).public_url,
                            "analysis_context": oss_uploader.upload_file(context_path, ctx_key).public_url,
                        }

                        summary = build_summary_markdown(
                            report_title=report["title"],
                            category=category,
                            executive_summary=report["executive_summary"],
                            key_findings=report["key_findings"],
                            markdown_url=uploaded["report_md"],
                            html_url=uploaded["report_html"],
                        )
                        result = dingtalk.send_markdown(report["title"], summary)
                        if not result.ok:
                            raise RuntimeError(f"钉钉发送失败：{result.response}")

                        manifest_entry: dict[str, Any] = {
                            "category": category,
                            "report_dir": rendered.markdown_path.parent.name,
                            "oss": uploaded,
                        }
                        reports_manifest["categories"].append(manifest_entry)

                manifest_path = output_root / f"{sanitize_filename(args.brand)}-manifest.json"
                manifest_path.write_text(json.dumps(reports_manifest, ensure_ascii=False, indent=2), encoding="utf-8")

                manifest_key = oss_uploader.key_for(f"{output_root.name}/{manifest_path.name}")
                manifest_url = oss_uploader.upload_file(manifest_path, manifest_key).public_url

                repository.mark_success(conn, trigger_ids, manifest_url)
                conn.commit()

                print(f"Manifest URL: {manifest_url}")
                print("报告生成、上传并发送完成，本地临时文件已清理。")
                return 0
            except Exception as exc:
                repository.mark_failure(conn, trigger_ids, str(exc))
                conn.commit()
                raise


if __name__ == "__main__":
    sys.exit(main())
