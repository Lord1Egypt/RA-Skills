#!/usr/bin/env python3
"""
AI评论打标模块
对每条评论进行深度分析，提取结构化信息
"""

import json
import time
import requests
from typing import Dict, List, Optional


def tag_review_with_ai(
    review: Dict,
    api_key: str,
    api_base: str = "https://api.openai.com/v1",
    model: str = "gpt-4o-mini",
    debug: bool = False
) -> Dict:
    """
    用AI对单条评论进行深度打标
    
    Args:
        review: 评论数据 {"rating", "title", "body", "author", "date"}
        api_key: LLM API Key
        api_base: API Base URL
        model: 模型名称
        debug: 是否打印调试信息
    
    Returns:
        打标结果 {
            "sentiment": "positive/negative/neutral",
            "pain_points": ["痛点1", "痛点2", ...],
            "selling_points": ["卖点1", "卖点2", ...],
            "use_cases": ["场景1", "场景2", ...],
            "user_profile": "用户画像描述",
            "improvement_suggestions": ["建议1", "建议2", ...],
            "rating": 原始评分,
            "summary": "评论摘要"
        }
    """
    
    # 构建Prompt
    prompt = _build_tagging_prompt(review)
    
    if debug:
        print(f"  Tagging review: {review['title'][:30]}...")
    
    # 调用LLM API
    try:
        response = _call_llm_api(prompt, api_key, api_base, model, debug)
        tags = _parse_tagging_response(response)
        return tags
    except Exception as e:
        if debug:
            print(f"  ⚠️ AI打标失败: {e}")
        # 返回默认打标结果
        return _default_tags(review)


def tag_reviews_batch(
    reviews: List[Dict],
    api_key: str,
    api_base: str = "https://api.openai.com/v1",
    model: str = "gpt-4o-mini",
    batch_size: int = 10,
    delay: float = 0.5,
    debug: bool = False
) -> List[Dict]:
    """
    批量对评论进行AI打标
    
    Args:
        reviews: 评论列表
        api_key: LLM API Key
        api_base: API Base URL
        model: 模型名称
        batch_size: 批处理大小（暂未实现，目前逐条处理）
        delay: API调用间隔（秒）
        debug: 是否打印调试信息
    
    Returns:
        带打标结果的评论列表 [{"review": {...}, "tags": {...}}, ...]
    """
    
    print(f"🤖 开始AI打标 (共 {len(reviews)} 条评论)...")
    print(f"   模型: {model}")
    print(f"   API: {api_base}")
    
    tagged_reviews = []
    total = len(reviews)
    
    for i, review in enumerate(reviews, 1):
        if debug:
            print(f"\n[{i}/{total}] 处理中...")
        
        tags = tag_review_with_ai(review, api_key, api_base, model, debug)
        
        tagged_reviews.append({
            "review": review,
            "tags": tags
        })
        
        # 打印进度
        if i % 10 == 0 or i == total:
            print(f"  进度: {i}/{total} ({i*100//total}%)")
        
        # 避免API限流
        if i < total:
            time.sleep(delay)
    
    print(f"✅ AI打标完成：{total} 条评论")
    return tagged_reviews


def _build_tagging_prompt(review: Dict) -> str:
    """构建AI打标Prompt"""
    
    rating = review.get("rating", 0)
    title = review.get("title", "")
    body = review.get("body", "")
    
    # 限制评论长度（避免超Token）
    max_body_length = 1500
    if len(body) > max_body_length:
        body = body[:max_body_length] + "..."
    
    prompt = f"""请对以下Amazon评论进行深度分析，提取结构化信息。

**评论信息：**
- 评分：{rating}星
- 标题：{title}
- 内容：{body}

**请提取以下信息（JSON格式）：**

1. **sentiment**: 情感倾向 ("positive"/"negative"/"neutral")
2. **pain_points**: 用户提到的痛点或问题（数组，最多5个）
3. **selling_points**: 用户提到的优点或卖点（数组，最多5个）
4. **use_cases**: 使用场景（数组，最多3个）
5. **user_profile**: 用户画像描述（一句话）
6. **improvement_suggestions**: 用户希望的改进（数组，最多3个）
7. **summary**: 评论摘要（20字以内）

**注意：**
- 如果评论是英文，请翻译成中文后再分析
- 只输出JSON，不要输出其他内容
- 如果某项信息无法提取，返回空数组或空字符串

**输出格式示例：**
```json
{{
  "sentiment": "negative",
  "pain_points": ["电池续航短", "充电慢"],
  "selling_points": ["性价比高", "外观好看"],
  "use_cases": ["日常通勤", "旅行"],
  "user_profile": "注重性价比的年轻上班族",
  "improvement_suggestions": ["提升电池容量", "加快充电速度"],
  "summary": "性价比还行但续航不行"
}}
```

请直接输出JSON："""
    
    return prompt


def _call_llm_api(prompt: str, api_key: str, api_base: str, model: str, debug: bool) -> str:
    """调用LLM API（兼容OpenAI格式）"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,  # 低温度，保证输出稳定
        "max_tokens": 500
    }
    
    # 构建API URL
    if api_base.endswith("/"):
        url = f"{api_base}chat/completions"
    else:
        url = f"{api_base}/chat/completions"
    
    if debug:
        print(f"    API URL: {url}")
    
    response = requests.post(url, headers=headers, json=data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return content
    else:
        raise Exception(f"API调用失败: HTTP {response.status_code} - {response.text[:200]}")


def _parse_tagging_response(response: str) -> Dict:
    """解析AI打标返回结果（增强容错版）"""
    
    # 尝试多种解析策略
    strategies = [
        _parse_json_direct,  # 策略1：直接解析JSON
        _parse_json_from_markdown,  # 策略2：从Markdown代码块中提取
        _parse_json_from_text,  # 策略3：从文本中提取JSON
        _parse_json_fuzzy,  # 策略4：模糊匹配（找第一个{到最后一个}）
    ]
    
    for strategy in strategies:
        try:
            tags = strategy(response)
            # 验证必要字段
            required_fields = ["sentiment", "pain_points", "selling_points"]
            if all(field in tags for field in required_fields):
                return tags
        except Exception:
            continue
    
    # 所有策略都失败，返回默认结果
    print(f"  ⚠️ 解析AI返回结果失败，使用默认打标")
    return _default_tags({})


def _parse_json_direct(text: str) -> Dict:
    """策略1：直接解析JSON"""
    return json.loads(text.strip())


def _parse_json_from_markdown(text: str) -> Dict:
    """策略2：从Markdown代码块中提取JSON"""
    import re
    # 匹配 ```json ... ``` 或 ``` ... ```
    pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    match = re.search(pattern, text)
    if match:
        return json.loads(match.group(1).strip())
    raise ValueError("No markdown code block found")


def _parse_json_from_text(text: str) -> Dict:
    """策略3：从文本中提取JSON（找第一个{到最后一个}）"""
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and start < end:
        json_str = text[start:end+1]
        return json.loads(json_str)
    raise ValueError("No JSON object found in text")


def _parse_json_fuzzy(text: str) -> Dict:
    """策略4：模糊解析（尝试修复常见JSON格式错误）"""
    # 尝试修复常见错误：单引号改为双引号、去掉尾随逗号等
    import re
    
    # 提取可能的JSON片段
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON found")
    
    json_str = text[start:end+1]
    
    # 修复常见错误
    # 1. 单引号改为双引号（键名）
    json_str = re.sub(r"(\W)'(\w+)'\s*:", r'\1"\2":', json_str)
    # 2. 去掉尾随逗号
    json_str = re.sub(r",\s*}", "}", json_str)
    json_str = re.sub(r",\s*\]", "]", json_str)
    
    return json.loads(json_str)


def _default_tags(review: Dict) -> Dict:
    """生成默认打标结果（当AI打标失败时使用）"""
    rating = review.get("rating", 0)
    
    # 根据评分简单判断情感
    if rating >= 4:
        sentiment = "positive"
    elif rating <= 2:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {
        "sentiment": sentiment,
        "pain_points": [],
        "selling_points": [],
        "use_cases": [],
        "user_profile": "",
        "improvement_suggestions": [],
        "summary": review.get("title", "")[:20]
    }


if __name__ == "__main__":
    # 测试代码
    test_review = {
        "rating": 2,
        "title": "Battery life is terrible",
        "body": "I bought this product hoping it would be good, but the battery life is really bad. It only lasts 2 hours. Also, it takes forever to charge. Not recommended.",
        "author": "John D.",
        "date": "2024-01-15"
    }
    
    # 需要真实API Key才能测试
    # tags = tag_review_with_ai(test_review, "YOUR_API_KEY", debug=True)
    # print(json.dumps(tags, ensure_ascii=False, indent=2))
    
    print("AI打标模块已加载（需要API Key才能测试）")
