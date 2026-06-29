#!/usr/bin/env python3
"""
关键词扩展模块
基于评论数据 + LLM，生成高频搜索词、长尾关键词、关联搜索词
"""

import sys
import io
import json
import requests
from typing import Dict, List, Optional

# Windows GBK encoding fix
try:
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def expand_keywords(
    products: List[Dict],
    tagged_reviews: Dict[str, List[Dict]],  # {asin: [{review, tags}, ...]}
    api_key: str,
    api_base: str = "https://api.openai.com/v1",
    model: str = "gpt-4o-mini",
    debug: bool = False
) -> Dict:
    """
    基于产品和评论数据，扩展关键词

    Returns:
        {
            "high_frequency_keywords": [{"keyword": "xxx", "frequency": "high", "source": "reviews"}, ...],
            "long_tail_keywords": [{"keyword": "xxx", "volume": "medium", "competition": "low"}, ...],
            "related_terms": [{"term": "xxx", "relation": "substitute/complement/...", "weight": 0.8}, ...],
            "category_trends": ["trend1", "trend2", ...],
            "summary": "关键词策略总结"
        }
    """
    print("🔑 关键词扩展分析...")

    # 构建输入摘要
    products_summary = _build_products_summary(products)
    reviews_summary = _build_reviews_summary(tagged_reviews)

    prompt = f"""你是一位Amazon关键词策略专家。请基于以下产品信息和用户评论，进行关键词扩展分析。

**市场**: Amazon US
**搜索品类**: {products[0].get('title', 'Unknown')[:80]}

**产品列表**:
{products_summary}

**用户评论关键洞察**:
{reviews_summary}

请从以下4个维度进行分析，输出JSON:

1. **high_frequency_keywords** (高频搜索词，10-15个): 
   结合评论中用户常提到的词和搜索习惯，按搜索量/相关性排列
   - keyword: 关键词
   - frequency: "very_high"/"high"/"medium"
   - source: 来源（"reviews"/"category"/"competitor"）
   - monthly_searches_estimate: 估算月搜索量（数字）

2. **long_tail_keywords** (长尾关键词，8-12个):
   - keyword: 长尾词（3-5个词组成）
   - volume: "medium"/"low"
   - competition: "low"/"medium"/"high"
   - conversion_potential: "high"/"medium"/"low"
   - monthly_searches_estimate: 估算月搜索量

3. **related_terms** (关联词/互补词，6-10个):
   - term: 关联词
   - relation: "substitute"/"complement"/"accessory"/"use_case"
   - weight: 0.0-1.0

4. **category_trends** (品类趋势，3-5个):
   - 基于评论反映的品类趋势描述

5. **summary**: 关键词策略总结（2-3句话中文）

注意：
- 所有关键词使用英文（Amazon搜索习惯）
- 搜索量估算基于品类常识，不需要精确
- 只输出JSON，不要其他内容

输出格式示例：
```json
{{
  "high_frequency_keywords": [...],
  "long_tail_keywords": [...],
  "related_terms": [...],
  "category_trends": [...],
  "summary": "..."
}}
```

请直接输出JSON："""

    try:
        response = _call_llm(prompt, api_key, api_base, model, debug)
        result = _parse_json_response(response)
        print(f"✅ 关键词扩展完成: {len(result.get('high_frequency_keywords', []))} 高频词 + {len(result.get('long_tail_keywords', []))} 长尾词")
        return result
    except Exception as e:
        print(f"⚠️ 关键词扩展失败: {e}")
        return _default_keyword_result()


def _build_products_summary(products: List[Dict]) -> str:
    """构建产品摘要"""
    lines = []
    for i, p in enumerate(products[:5], 1):
        lines.append(f"  {i}. {p['title'][:80]} | ⭐{p['rating']} | {p['total_reviews']} reviews | {p['price']}")
    return "\n".join(lines)


def _build_reviews_summary(tagged_reviews: Dict[str, List[Dict]]) -> str:
    """构建评论摘要"""
    all_pain_points = []
    all_selling_points = []
    all_use_cases = []

    for reviews in tagged_reviews.values():
        for item in reviews[:30]:  # 每产品取30条
            tags = item.get("tags", {})
            all_pain_points.extend(tags.get("pain_points", []))
            all_selling_points.extend(tags.get("selling_points", []))
            all_use_cases.extend(tags.get("use_cases", []))

    # 统计高频词
    from collections import Counter
    pain_counter = Counter(all_pain_points)
    sell_counter = Counter(all_selling_points)
    case_counter = Counter(all_use_cases)

    lines = [
        f"Top 5 用户痛点: {', '.join([w for w, _ in pain_counter.most_common(5)])}",
        f"Top 5 产品卖点: {', '.join([w for w, _ in sell_counter.most_common(5)])}",
        f"Top 5 使用场景: {', '.join([w for w, _ in case_counter.most_common(5)])}",
    ]
    return "\n".join(lines)


def _call_llm(prompt: str, api_key: str, api_base: str, model: str, debug: bool) -> str:
    """调用LLM API"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 2000
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
    """解析LLM返回的JSON（多策略）"""
    # 策略1: 直接解析
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # 策略2: 从markdown提取
    import re
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 策略3: 找{}范围
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(text[start:end+1])
        except json.JSONDecodeError:
            pass

    raise ValueError(f"无法解析JSON: {text[:200]}")


def _default_keyword_result() -> Dict:
    """默认关键词结果"""
    return {
        "high_frequency_keywords": [],
        "long_tail_keywords": [],
        "related_terms": [],
        "category_trends": ["产品评论数据不足以生成趋势分析"],
        "summary": "需要更多评论数据以生成关键词策略"
    }


if __name__ == "__main__":
    print("关键词扩展模块已加载")
