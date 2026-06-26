"""AI分析模块 - 使用 OpenAI 兼容接口进行数据解读"""

import json
import requests
import pandas as pd
from typing import Optional


def analyze_data(df: pd.DataFrame, api_key: str, api_base: str = "https://api.openai.com/v1") -> str:
    """使用 AI 分析数据并生成统计解读

    Args:
        df: 数据框
        api_key: API 密钥
        api_base: API 基础 URL

    Returns:
        str: AI 生成的统计分析解读
    """
    summary = _prepare_data_summary(df)

    prompt = f"""你是一位数据分析专家，请对以下数据进行统计分析并给出简洁的解读：

数据概况：
{summary}

请提供：
1. 数据整体质量评估
2. 主要发现和特点
3. 潜在的数据问题或异常

请用中文回复，保持简洁，控制在200字以内。"""

    return _call_llm(prompt, api_key, api_base)


def generate_insights(df: pd.DataFrame, chart_descriptions: list, api_key: str, api_base: str = "https://api.openai.com/v1") -> str:
    """基于图表描述生成 AI 文字分析

    Args:
        df: 数据框
        chart_descriptions: 图表描述列表
        api_key: API 密钥
        api_base: API 基础 URL

    Returns:
        str: AI 生成的分析报告
    """
    summary = _prepare_data_summary(df)

    charts_text = "\n".join([f"- {desc}" for desc in chart_descriptions])

    prompt = f"""你是一位数据分析专家，请基于以下数据摘要和图表信息，撰写一份数据分析报告：

数据摘要：
{summary}

图表信息：
{charts_text}

请提供：
1. 关键发现（3-5条）
2. 数据趋势分析
3. 业务建议或洞察

请用中文回复，结构清晰，总字数控制在300字以内。"""

    return _call_llm(prompt, api_key, api_base)


def _prepare_data_summary(df: pd.DataFrame) -> str:
    """准备数据摘要文本"""
    row_count = len(df)
    col_count = len(df.columns)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    missing = df.isnull().sum().sum()

    lines = [
        f"行数: {row_count}, 列数: {col_count}",
        f"数值列: {', '.join(numeric_cols[:10])}" + ("..." if len(numeric_cols) > 10 else ""),
        f"缺失值总数: {missing}",
    ]

    if numeric_cols:
        desc = df[numeric_cols].describe().to_string()
        lines.append(f"\n数值列统计：\n{desc}")

    return "\n".join(lines)


def _call_llm(prompt: str, api_key: str, api_base: str, model: str = "gpt-3.5-turbo") -> str:
    """调用 LLM API"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500,
    }

    try:
        response = requests.post(
            f"{api_base.rstrip('/')}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except requests.exceptions.Timeout:
        return "[AI 分析超时，请稍后重试]"
    except requests.exceptions.RequestException as e:
        return f"[AI 分析请求失败: {str(e)}]"
    except (KeyError, IndexError):
        return "[AI 分析响应格式错误]"
