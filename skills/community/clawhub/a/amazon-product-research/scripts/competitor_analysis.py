#!/usr/bin/env python3
"""
竞品分析模块
多产品横向对比，生成优劣矩阵和市场定位分析
"""

import sys
import io
import json
import requests
from typing import Dict, List, Optional
from collections import Counter

# Windows GBK encoding fix
try:
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def analyze_competitors(
    products: List[Dict],
    tagged_reviews: Dict[str, List[Dict]],
    api_key: str,
    api_base: str = "https://api.openai.com/v1",
    model: str = "gpt-4o-mini",
    debug: bool = False
) -> Dict:
    """
    竞品横向对比分析

    Returns:
        {
            "comparison_matrix": [
                {
                    "asin": "B0XXX",
                    "title": "Product A",
                    "scores": {"quality": 8, "price": 7, "features": 9, ...},
                    "strengths": ["音质好", "续航长"],
                    "weaknesses": ["价格高", "重量大"],
                    "positioning": "高端旗舰"
                },
                ...
            ],
            "radar_dimensions": ["quality", "price", "features", ...],
            "market_gaps": ["价格$30-50区间缺少好产品", ...],
            "overall_summary": "市场竞争格局总结"
        }
    """
    print("📊 竞品对比分析...")

    if not products or not tagged_reviews:
        return _default_competitor_result()

    # 构建产品摘要
    product_summaries = []
    for p in products:
        asin = p["asin"]
        reviews = tagged_reviews.get(asin, [])

        # 统计该产品
        total = len(reviews)
        pos = sum(1 for r in reviews if r.get("tags", {}).get("sentiment") == "positive")
        neg = sum(1 for r in reviews if r.get("tags", {}).get("sentiment") == "negative")
        neu = total - pos - neg

        sell_points = []
        pain_points = []
        for r in reviews:
            tags = r.get("tags", {})
            sell_points.extend(tags.get("selling_points", []))
            pain_points.extend(tags.get("pain_points", []))

        top_sells = [s for s, _ in Counter(sell_points).most_common(5)]
        top_pains = [p for p, _ in Counter(pain_points).most_common(5)]

        product_summaries.append({
            "asin": asin,
            "title": p["title"][:80],
            "price": p["price"],
            "rating": p["rating"],
            "total_reviews": p["total_reviews"],
            "review_count_analyzed": total,
            "positive_pct": round(pos / max(total, 1) * 100),
            "top_selling_points": top_sells,
            "top_pain_points": top_pains
        })

    # 构建LLM Prompt
    summaries_text = ""
    for ps in product_summaries:
        summaries_text += f"""
[{ps['asin']}] {ps['title']}
  价格: {ps['price']} | 评分: ⭐{ps['rating']} | 评论数: {ps['total_reviews']}
  分析评论: {ps['review_count_analyzed']}条 | 好评率: {ps['positive_pct']}%
  核心卖点: {', '.join(ps['top_selling_points'])}
  核心痛点: {', '.join(ps['top_pain_points'])}
"""

    prompt = f"""你是一位Amazon品类竞争分析专家。请对以下竞品进行横向对比分析。

**产品列表**:
{summaries_text}

请进行分析，输出JSON:

1. **comparison_matrix** (竞品矩阵):
   每个产品包含:
   - asin: 产品ASIN
   - title: 简称
   - scores: 5维度打分 (quality, value_for_money, features, customer_satisfaction, brand_power) 1-10
   - strengths: 2-3个核心优势
   - weaknesses: 2-3个主要劣势
   - positioning: 市场定位（如"性价比之王"/"高端旗舰"/"入门款"）
   - target_audience: 目标用户群（如"预算有限的年轻用户"）

2. **radar_dimensions**: ["quality", "value_for_money", "features", "customer_satisfaction", "brand_power"]

3. **market_gaps** (市场空白，3-5个):
   - 价格区间空白
   - 功能缺失
   - 用户群体未覆盖
   每个gap包含: description, opportunity_score (1-10)

4. **overall_summary** (2-4句中文):
   - 市场竞争格局如何？
   - 哪个价位段竞争最激烈？
   - 新手卖家最有机会的点在哪里？

只输出JSON，不要其他内容。

```json
{{
  "comparison_matrix": [...],
  "radar_dimensions": [...],
  "market_gaps": [...],
  "overall_summary": "..."
}}
```"""

    try:
        response = _call_llm(prompt, api_key, api_base, model, debug)
        result = _parse_json_response(response)

        if not result.get("comparison_matrix"):
            result = _build_simple_matrix(product_summaries)

        print(f"✅ 竞品分析完成: {len(result.get('comparison_matrix', []))} 个产品对比")
        return result
    except Exception as e:
        print(f"⚠️ 竞品分析失败: {e}，使用基础矩阵")
        return _build_simple_matrix(product_summaries)


def _build_simple_matrix(product_summaries: List[Dict]) -> Dict:
    """基于数据构建简单竞品矩阵（不依赖LLM）"""
    matrix = []
    for ps in product_summaries:
        rating = ps["rating"]
        pos_pct = ps["positive_pct"]

        matrix.append({
            "asin": ps["asin"],
            "title": ps["title"],
            "scores": {
                "quality": min(10, max(3, int(rating * 2))),
                "value_for_money": min(10, max(3, int(pos_pct // 10))),
                "features": 7,
                "customer_satisfaction": min(10, max(3, int(pos_pct // 10))),
                "brand_power": min(10, max(2, int(ps["total_reviews"] // 1000)))
            },
            "strengths": ps["top_selling_points"][:3],
            "weaknesses": ps["top_pain_points"][:3],
            "positioning": "中端主流" if 3.5 <= rating <= 4.3 else ("高端" if rating > 4.3 else "入门级"),
            "target_audience": "大众消费者"
        })

    return {
        "comparison_matrix": matrix,
        "radar_dimensions": ["quality", "value_for_money", "features", "customer_satisfaction", "brand_power"],
        "market_gaps": [{"description": "需要更多数据以识别市场空白", "opportunity_score": 5}],
        "overall_summary": f"共分析{len(matrix)}个竞品。整体市场竞争取决于具体品类。建议结合真实数据做更精确的判断。"
    }


def _call_llm(prompt: str, api_key: str, api_base: str, model: str, debug: bool) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 2500
    }
    url = api_base.rstrip("/") + "/chat/completions"
    if debug:
        print(f"  API: {url} | Model: {model}")
    response = requests.post(url, headers=headers, json=data, timeout=60)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    raise Exception(f"API调用失败: HTTP {response.status_code}")


def _parse_json_response(text: str) -> Dict:
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    import re
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(text[start:end+1])
        except json.JSONDecodeError:
            pass
    raise ValueError("无法解析JSON")


def _default_competitor_result() -> Dict:
    return {
        "comparison_matrix": [],
        "radar_dimensions": ["quality", "value_for_money", "features", "customer_satisfaction", "brand_power"],
        "market_gaps": [],
        "overall_summary": "产品数据不足，无法进行竞品分析"
    }


if __name__ == "__main__":
    print("竞品分析模块已加载")
