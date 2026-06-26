#!/usr/bin/env python3
"""
原子事实分解模块
将回答分解为独立的原子事实，便于逐条验证
"""

import os
import json
import argparse
import sys
from pathlib import Path


def load_prompt(answer: str) -> str:
    """加载prompt模板并填充答案"""
    prompt_path = Path(__file__).parent.parent / "prompts" / "decompose.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()
    return prompt.replace("{{ANSWER}}", answer)


def call_llm(prompt: str) -> str:
    """
    调用LLM API
    支持 OpenAI / Anthropic / Google 等
    通过环境变量配置：LLM_API_KEY, LLM_API_BASE, LLM_MODEL
    """
    api_key = os.getenv("LLM_API_KEY")
    api_base = os.getenv("LLM_API_BASE", "https://api.openai.com/v1")
    model = os.getenv("LLM_MODEL", "gpt-4o")

    if not api_key:
        raise ValueError("请设置环境变量 LLM_API_KEY")

    # 使用 OpenAI SDK（兼容模式）
    try:
        import openai
        client = openai.OpenAI(api_key=api_key, base_url=api_base)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except ImportError:
        # 如果没有openai SDK，使用requests直接调用
        import requests
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
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


def parse_response(response: str) -> list:
    """解析LLM返回的JSON，提取facts列表"""
    # 尝试从回复中提取JSON（可能包含markdown代码块）
    text = response.strip()

    # 移除可能的markdown代码块标记
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]

    data = json.loads(text.strip())
    return data.get("facts", [])


def decompose(answer: str) -> list:
    """
    将回答分解为原子事实
    返回：[{"id": 1, "text": "..."}, ...]
    """
    prompt = load_prompt(answer)
    response = call_llm(prompt)
    facts = parse_response(response)
    return facts


def main():
    parser = argparse.ArgumentParser(description="原子事实分解")
    parser.add_argument("--answer", type=str, help="待分解的回答")
    parser.add_argument("--file", type=str, help="从文件读取回答")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            answer = f.read()
    elif args.answer:
        answer = args.answer
    else:
        print("请提供 --answer 或 --file 参数")
        sys.exit(1)

    facts = decompose(answer)
    print(json.dumps({"facts": facts}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
