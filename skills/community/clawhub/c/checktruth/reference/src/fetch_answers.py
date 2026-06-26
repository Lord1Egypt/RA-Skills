#!/usr/bin/env python3
"""
多源答案获取模块
向多个AI模型提问，获取参考答案列表
"""

import os
import json
import argparse
import sys
from pathlib import Path


def fetch_openai(question: str, model: str = "gpt-4o") -> str:
    """调用 OpenAI API"""
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

    if not api_key:
        raise ValueError("请设置 OPENAI_API_KEY 或 LLM_API_KEY")

    try:
        import openai
        client = openai.OpenAI(api_key=api_key, base_url=api_base)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": question}],
            temperature=0.1,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except ImportError:
        import requests
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": question}],
            "temperature": 0.1,
            "max_tokens": 2000
        }
        resp = requests.post(
            f"{api_base}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


def fetch_anthropic(question: str, model: str = "claude-3-5-sonnet-20241022") -> str:
    """调用 Anthropic API"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("请设置 ANTHROPIC_API_KEY")

    import requests
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.1,
        "max_tokens": 2000
    }
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=payload,
        timeout=60
    )
    resp.raise_for_status()
    data = resp.json()
    return data["content"][0]["text"]


def fetch_gemini(question: str, model: str = "gemini-2.0-flash") -> str:
    """调用 Google Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("请设置 GEMINI_API_KEY 或 GOOGLE_API_KEY")

    import requests
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{"text": question}]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 2000
        }
    }
    resp = requests.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


def fetch_answers(question: str, sources: list = None) -> list:
    """
    获取多源答案
    sources: 列表，元素为 "openai"|"anthropic"|"gemini"
    返回：[{"source": "openai", "answer": "..."}, ...]
    """
    if sources is None:
        sources = ["openai", "anthropic", "gemini"]

    results = []
    for source in sources:
        try:
            if source == "openai":
                answer = fetch_openai(question)
            elif source == "anthropic":
                answer = fetch_anthropic(question)
            elif source == "gemini":
                answer = fetch_gemini(question)
            else:
                print(f"未知来源：{source}，跳过")
                continue
            results.append({"source": source, "answer": answer})
        except Exception as e:
            print(f"获取 {source} 答案失败：{e}")

    return results


def main():
    parser = argparse.ArgumentParser(description="获取多源AI答案")
    parser.add_argument("--question", type=str, help="问题文本")
    parser.add_argument("--file", type=str, help="从文件读取问题")
    parser.add_argument("--sources", type=str, default="openai,anthropic,gemini",
                        help="数据源，逗号分隔（openai,anthropic,gemini）")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            question = f.read()
    elif args.question:
        question = args.question
    else:
        print("请提供 --question 或 --file 参数")
        sys.exit(1)

    sources = [s.strip() for s in args.sources.split(",")]
    results = fetch_answers(question, sources)
    print(json.dumps({"answers": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
