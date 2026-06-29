#!/usr/bin/env python3
"""
VOC痛点聚类模块
聚合所有产品评论的痛点，使用LLM进行聚类分析
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


def cluster_voc(
    tagged_reviews: Dict[str, List[Dict]],  # {asin: [{review, tags}, ...]}
    products: List[Dict],
    api_key: str,
    api_base: str = "https://api.openai.com/v1",
    model: str = "gpt-4o-mini",
    debug: bool = False
) -> Dict:
    """
    VOC痛点聚类分析

    Returns:
        {
            "clusters": [
                {
                    "category": "产品质量",
                    "severity": 8,
                    "frequency": 145,
                    "pain_points": ["容易坏", "材料廉价", ...],
                    "typical_reviews": ["使用两周就坏了...", ...],
                    "affected_products": ["B0XXX", "B0YYY"],
                    "improvement_direction": "提升材料质量"
                },
                ...
            ],
            "severity_summary": {
                "critical": [clusters with severity >= 8],
                "major": [severity 5-7],
                "minor": [severity < 5]
            },
            "overall_summary": "整体VOC总结"
        }
    """
    print("🎯 VOC痛点聚类分析...")

    # 收集所有痛点
    all_pain_points = []
    pain_reviews = []  # (pain_point, review_excerpt, asin)

    for asin, reviews in tagged_reviews.items():
        for item in reviews:
            tags = item.get("tags", {})
            pain_list = tags.get("pain_points", [])
            review_body = item.get("review", {}).get("body", "")
            for pp in pain_list:
                all_pain_points.append(pp)
                pain_reviews.append({
                    "pain_point": pp,
                    "review_excerpt": review_body[:200],
                    "asin": asin,
                    "rating": item.get("review", {}).get("rating", 0)
                })

    # 统计高频痛点
    pain_counter = Counter(all_pain_points)
    top_pains = pain_counter.most_common(50)

    if not top_pains:
        print("⚠️ 没有检测到足够痛点")
        return _default_voc_result()

    # 构建问题摘要
    pain_summary = "\n".join([f"  - {pain} (出现{count}次)" for pain, count in top_pains[:30]])

    # 产品信息
    products_info = "\n".join([
        f"  [{p['asin']}] {p['title'][:60]} ⭐{p['rating']}"
        for p in products[:5]
    ])

    prompt = f"""你是一位Amazon消费者洞察专家。请对以下产品的用户痛点进行聚类分析。

**产品**:
{products_info}

**高频痛点TOP30**:
{pain_summary}

**代表性评价样本**:
{chr(10).join([f'  [{pr["asin"]}] ⭐{pr["rating"]} "{pr["review_excerpt"][:100]}"' for pr in pain_reviews[:20]])}

请进行以下分析，输出JSON:

1. **clusters** (痛点聚类，5-8个):
   将相似痛点归为一个cluster，每个cluster包含:
   - category: 痛点类别名称（中文，简洁）
   - severity: 严重程度 1-10 (10=致命，影响购买决策)
   - frequency: 出现总次数
   - pain_points: 该类下的具体痛点列表
   - typical_reviews: 2-3条代表性评价原文（截取关键句）
   - affected_products: 受影响的产品ASIN
   - improvement_direction: 改进方向建议（1句话）

2. **severity_summary**: 按严重度分级
   - critical: 严重度>=8的cluster（数组）
   - major: 严重度5-7的cluster（数组）
   - minor: 严重度<5的cluster（数组）

3. **overall_summary**: 整体VOC总结（3-5句话中文）
   - 最严重的问题是什么？
   - 哪些问题影响最广？
   - 对新手卖家的最大风险是什么？

注意：
- category用中文描述
- 只输出JSON，不要其他内容

输出格式：
```json
{{
  "clusters": [...],
  "severity_summary": {{"critical": [...], "major": [...], "minor": [...]}},
  "overall_summary": "..."
}}
```

请直接输出JSON："""

    try:
        response = _call_llm(prompt, api_key, api_base, model, debug)
        result = _parse_json_response(response)

        # 如果没有LLM返回的cluster，用统计方式生成
        if not result.get("clusters"):
            result = _build_statistical_clusters(top_pains, pain_reviews)

        print(f"✅ VOC聚类完成: {len(result.get('clusters', []))} 个痛点类别")
        return result
    except Exception as e:
        print(f"⚠️ VOC聚类失败: {e}，使用统计聚类")
        return _build_statistical_clusters(top_pains, pain_reviews)


def _build_statistical_clusters(top_pains: List, pain_reviews: List) -> Dict:
    """基于统计的简单聚类（不依赖LLM）"""
    clusters = []
    for pain, count in top_pains[:15]:
        related_reviews = [pr for pr in pain_reviews if pr["pain_point"] == pain]
        affected_asins = list(set(pr["asin"] for pr in related_reviews))

        clusters.append({
            "category": pain,
            "severity": min(10, max(3, count // 3)),
            "frequency": count,
            "pain_points": [pain],
            "typical_reviews": [pr["review_excerpt"][:150] for pr in related_reviews[:2]],
            "affected_products": affected_asins[:3],
            "improvement_direction": f"解决 {pain} 问题"
        })

    critical = [c for c in clusters if c["severity"] >= 8]
    major = [c for c in clusters if 5 <= c["severity"] < 8]
    minor = [c for c in clusters if c["severity"] < 5]

    return {
        "clusters": clusters,
        "severity_summary": {
            "critical": critical,
            "major": major,
            "minor": minor
        },
        "overall_summary": f"共识别{len(clusters)}个痛点类别，其中{len(critical)}个严重问题，{len(major)}个主要问题。建议优先解决严重级别的痛点以提升产品竞争力。"
    }


def _call_llm(prompt: str, api_key: str, api_base: str, model: str, debug: bool) -> str:
    """调用LLM API"""
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
    else:
        raise Exception(f"API调用失败: HTTP {response.status_code}")


def _parse_json_response(text: str) -> Dict:
    """解析LLM返回的JSON"""
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

    raise ValueError(f"无法解析JSON")


def _default_voc_result() -> Dict:
    return {
        "clusters": [],
        "severity_summary": {"critical": [], "major": [], "minor": []},
        "overall_summary": "评论数据不足，无法进行VOC聚类分析"
    }


if __name__ == "__main__":
    print("VOC聚类模块已加载")
