"""
AI摘要生成器 - 调用LLM API对文章进行智能提炼
支持关键词过滤、重要性排序、中英文摘要
"""

import json
import os
import sys
from datetime import datetime


def get_llm_config():
    """从环境变量读取LLM配置"""
    return {
        "api_key": os.environ.get("LLM_API_KEY", ""),
        "base_url": os.environ.get("LLM_API_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        "model": os.environ.get("LLM_MODEL", "qwen-plus"),
    }


def call_llm(prompt, system_prompt=None, max_tokens=1000):
    """调用LLM API生成摘要
    
    优先使用OpenAI兼容接口（通义千问/DeepSeek/OpenAI均可）
    如果没有API Key，返回基于规则的简单摘要作为降级方案
    """
    config = get_llm_config()
    
    if not config["api_key"]:
        return _fallback_summary(prompt)
    
    try:
        import requests
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        resp = requests.post(
            "{}/chat/completions".format(config["base_url"]),
            headers={
                "Authorization": "Bearer {}".format(config["api_key"]),
                "Content-Type": "application/json"
            },
            json={
                "model": config["model"],
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.3
            },
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("[WARN] LLM调用失败: {}，使用降级方案".format(e))
        return _fallback_summary(prompt)


def summarize_article(article, keywords=None):
    """对单篇文章生成摘要
    
    Returns:
        dict: {"summary": str, "key_points": list[str], "relevance_score": float}
    """
    prompt = """请对以下文章生成简洁的中文摘要：

标题：{title}

内容（前2000字）：
{content_truncated}

要求：
1. 用2-3句话概括核心观点（不超过150字）
2. 提取3个关键要点（每个不超过30字）
3. 如果提供了关键词，判断相关性（高/中/低）

请严格按以下JSON格式输出（不要输出其他内容）：
{{"summary": "...", "key_points": ["...", "...", "..."], "relevance": "高/中/低"}}""".format(
        title=article.get("title", ""),
        content_trunc=(article.get("content", "") or "")[:2000]
    )
    
    system_prompt = "你是一个专业的信息筛选助手，擅长从大量文本中快速提炼关键信息。只输出JSON格式的结果。"
    
    result_text = call_llm(prompt, system_prompt)
    
    try:
        result = json.loads(result_text)
        return {
            "summary": result.get("summary", article.get("title", "")),
            "key_points": result.get("key_points", []),
            "relevance_score": {"高": 0.9, "中": 0.5, "低": 0.2}.get(result.get("relevance", "中"), 0.5)
        }
    except (json.JSONDecodeError, KeyError):
        return {
            "summary": result_text[:200],
            "key_points": [],
            "relevance_score": 0.5
        }


def generate_digest(articles, keywords=None, title="每日信息简报"):
    """生成多篇文章的结构化摘要报告
    
    Args:
        articles: list of article dicts (from monitor.py output)
        keywords: optional keyword list for filtering
        title: report title
    
    Returns:
        str: Markdown格式的完整简报
    """
    if not articles:
        return "# {}\n\n今日暂无新文章。\n".format(title)
    
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    
    lines = [
        "# 📡 {}".format(title),
        "",
        "> 生成时间: {} | 文章数: {}".format(now, len(articles)),
        "",
    ]
    
    for i, article in enumerate(articles, 1):
        summary_data = summarize_article(article, keywords)
        
        lines.append("---")
        lines.append("")
        lines.append("## {}. {}".format(i, article.get("title", "无标题")))
        lines.append("")
        lines.append("- **来源**: {}".format(article.get("source_name", "未知")))
        lines.append("- **链接**: {}".format(article.get("url", "")))
        lines.append("- **摘要**: {}".format(summary_data["summary"]))
        
        if summary_data["key_points"]:
            lines.append("- **要点**:")
            for point in summary_data["key_points"]:
                lines.append("  - {}".format(point))
        lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("*由 📡 信息源监控助手自动生成*")
    
    return "\n".join(lines)


def _fallback_summary(prompt):
    """无API时的降级方案：提取前几句作为摘要"""
    import re
    match = re.search(r'内容（前2000字）：\n(.*?)(?=要求：)', prompt, re.S)
    if match:
        text = match.group(1)[:300].replace("\n", " ")
        return json.dumps({
            "summary": text[:150],
            "key_points": [text[:30], ],
            "relevance": "中"
        }, ensure_ascii=False)
    return '{"summary": "摘要生成暂不可用", "key_points": [], "relevance": "中"}'


if __name__ == "__main__":
    test_article = {
        "title": "测试文章：AI Agent赚钱指南",
        "content": "本文介绍了如何利用AI Agent在ClawHub上发布付费Skill来赚取被动收入。关键点包括：选择正确的垂直领域、构建护城河、设计Freemium商业模式。",
        "source_name": "测试源",
        "url": "https://example.com/test"
    }
    result = summarize_article(test_article, ["AI", "Agent"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
