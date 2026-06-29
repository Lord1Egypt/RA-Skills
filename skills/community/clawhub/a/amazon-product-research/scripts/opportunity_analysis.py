#!/usr/bin/env python3
"""
新品机会分析模块
基于VOC、竞品分析、市场空白，推荐新品切入方向
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


def analyze_opportunities(
    products: List[Dict],
    tagged_reviews: Dict[str, List[Dict]],
    voc_result: Dict,
    competitor_result: Dict,
    api_key: str,
    api_base: str = "https://api.openai.com/v1",
    model: str = "gpt-4o-mini",
    debug: bool = False
) -> Dict:
    """
    新品机会分析

    Args:
        products: 产品列表
        tagged_reviews: 打标评论
        voc_result: VOC聚类结果
        competitor_result: 竞品分析结果
        api_key: LLM API Key
        api_base: API Base URL
        model: 模型名
        debug: 调试模式

    Returns:
        {
            "opportunities": [
                {
                    "title": "机会名称",
                    "description": "机会描述",
                    "opportunity_score": 8,
                    "target_market": "目标市场",
                    "estimated_demand": "高/中/低",
                    "competitive_intensity": "高/中/低",
                    "price_range": "$20-30",
                    "key_differentiator": "核心差异化",
                    "risks": ["风险1", "风险2"],
                    "entry_difficulty": "低/中/高"
                },
                ...
            ],
            "top_recommendation": {
                "direction": "推荐方向",
                "reasoning": "推荐理由",
                "action_items": ["下一步行动1", ...]
            },
            "risk_assessment": "整体风险评估",
            "summary": "新品机会总结"
        }
    """
    print("💡 新品机会分析...")

    # 构建输入
    products_text = "\n".join([
        f"  [{p['asin']}] {p['title'][:60]} | {p['price']} | ⭐{p['rating']} | {p['total_reviews']}条评论"
        for p in products[:5]
    ])

    # VOC关键问题
    voc_text = ""
    if voc_result.get("clusters"):
        critical = [c for c in voc_result["clusters"] if c.get("severity", 0) >= 8]
        major = [c for c in voc_result["clusters"] if 5 <= c.get("severity", 0) < 8]
        voc_text = f"严重问题({len(critical)}个): {', '.join([c['category'] for c in critical])}\n"
        voc_text += f"主要问题({len(major)}个): {', '.join([c['category'] for c in major])}"
    else:
        voc_text = "暂无VOC数据"

    # 市场空白
    gaps_text = ""
    gaps = competitor_result.get("market_gaps", [])
    if gaps:
        gaps_text = "\n".join([f"  - {g.get('description', g)}" for g in gaps[:5]])
    else:
        gaps_text = "暂无市场空白数据"

    prompt = f"""你是一位Amazon选品和产品策略专家。请基于以下数据，分析新品切入机会。

**当前市场产品**:
{products_text}

**用户痛点(VOC)**:
{voc_text}

**市场空白**:
{gaps_text}

请输出JSON，包含以下内容:

1. **opportunities** (新品机会，3-5个):
   每个机会包含:
   - title: 机会名称（中文）
   - description: 详细描述（2-3句）
   - opportunity_score: 机会评分 1-10
   - target_market: 目标细分市场
   - estimated_demand: "高"/"中"/"低"
   - competitive_intensity: "高"/"中"/"低"
   - price_range: 建议价格区间
   - key_differentiator: 核心差异化卖点
   - risks: 2-3个风险点
   - entry_difficulty: "低"/"中"/"高"

2. **top_recommendation**: 
   - direction: 最推荐方向（中文，1句话）
   - reasoning: 推荐理由（3-5句）
   - action_items: 下一步行动（3-5个具体步骤）

3. **risk_assessment**: 整体风险评估（2-3句中文）
4. **summary**: 新品机会总结（3-5句中文）

只输出JSON。

```json
{{
  "opportunities": [...],
  "top_recommendation": {{...}},
  "risk_assessment": "...",
  "summary": "..."
}}
```"""

    try:
        response = _call_llm(prompt, api_key, api_base, model, debug)
        result = _parse_json_response(response)

        if not result.get("opportunities"):
            result = _build_simple_opportunities(products, voc_result)

        print(f"✅ 机会分析完成: {len(result.get('opportunities', []))} 个机会点")
        return result
    except Exception as e:
        print(f"⚠️ 机会分析失败: {e}，使用基础分析")
        return _build_simple_opportunities(products, voc_result)


def _build_simple_opportunities(products: List[Dict], voc_result: Dict) -> Dict:
    """基于数据构建简单机会分析（不依赖LLM）"""
    opportunities = []

    # 从VOC找机会
    if voc_result.get("clusters"):
        for cluster in voc_result["clusters"][:3]:
            opportunities.append({
                "title": f"解决「{cluster['category']}」的差异化产品",
                "description": f"当前市场产品在「{cluster['category']}」方面存在明显不足（严重度{cluster.get('severity',5)}/10），可以通过针对性改进建立差异化优势。",
                "opportunity_score": min(10, cluster.get("severity", 5) + 1),
                "target_market": "对品质有要求的消费者",
                "estimated_demand": "中",
                "competitive_intensity": "中",
                "price_range": "中高端",
                "key_differentiator": f"重点解决{cluster['category']}问题",
                "risks": ["改进成本可能较高", "用户教育成本"],
                "entry_difficulty": "中"
            })

    # 基础机会
    if products:
        avg_price = 50  # 默认
        opportunities.append({
            "title": "高性价比入门款",
            "description": f"当前市场存在中低端空白，可以推出功能精简但质量可靠的入门款产品。",
            "opportunity_score": 7,
            "target_market": "预算有限的首次购买者",
            "estimated_demand": "高",
            "competitive_intensity": "低",
            "price_range": "$15-30",
            "key_differentiator": "极致性价比",
            "risks": ["利润空间薄", "可能引发价格战"],
            "entry_difficulty": "低"
        })

        opportunities.append({
            "title": "高端专业升级款",
            "description": f"面向专业用户的升级版产品，增加高级功能和更优质的材料。",
            "opportunity_score": 6,
            "target_market": "专业用户/发烧友",
            "estimated_demand": "低",
            "competitive_intensity": "高",
            "price_range": "$80-150",
            "key_differentiator": "专业级品质和功能",
            "risks": ["市场接受度不确定", "研发投入大"],
            "entry_difficulty": "高"
        })

    return {
        "opportunities": opportunities,
        "top_recommendation": {
            "direction": opportunities[0]["title"] if opportunities else "需要更多数据进行判断",
            "reasoning": "基于当前VOC数据和市场竞争格局，该方向的机会评分最高，风险可控。",
            "action_items": [
                "深入研究目标用户画像",
                "分析供应链方案和成本结构",
                "制定差异化产品规格",
                "准备Listing和关键词策略",
                "小批量试产测试市场反应"
            ]
        },
        "risk_assessment": f"整体风险中等。主要风险来自市场竞争和供应链不确定性。建议从小批量开始，快速验证市场假设。",
        "summary": f"基于对{len(products)}个竞品的分析，共发现{len(opportunities)}个潜在机会。建议优先选择差异化明显的方向，避免与现有大卖直接价格竞争。"
    }


def _call_llm(prompt: str, api_key: str, api_base: str, model: str, debug: bool) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
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


if __name__ == "__main__":
    print("新品机会分析模块已加载")
