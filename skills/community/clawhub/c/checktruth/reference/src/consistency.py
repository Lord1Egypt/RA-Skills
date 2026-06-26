#!/usr/bin/env python3
"""
内部一致性检测模块
检查回答本身是否自相矛盾
"""

import os
import json
import argparse
import sys
from pathlib import Path


def load_prompt(answer: str) -> str:
    """加载prompt模板"""
    prompt_path = Path(__file__).parent.parent / "prompts" / "consistency.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()
    return prompt.replace("{{ANSWER}}", answer)


def call_llm(prompt: str) -> str:
    """调用LLM API（同其他模块）"""
    api_key = os.getenv("LLM_API_KEY")
    api_base = os.getenv("LLM_API_BASE", "https://api.openai.com/v1")
    model = os.getenv("LLM_MODEL", "gpt-4o")

    if not api_key:
        raise ValueError("请设置环境变量 LLM_API_KEY")

    try:
        import openai
        client = openai.OpenAI(api_key=api_key, base_url=api_base)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=1000,
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
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 1000
        }
        resp = requests.post(
            f"{api_base}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


def parse_response(response: str) -> dict:
    """解析LLM返回的JSON"""
    text = response.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]

    return json.loads(text.strip())


def check_consistency(answer: str) -> dict:
    """
    检查回答的内部一致性
    返回：{"consistent": True/False, "contradictions": [...]}
    """
    prompt = load_prompt(answer)
    response = call_llm(prompt)
    result = parse_response(response)
    return {
        "consistent": result.get("consistent", True),
        "contradictions": result.get("contradictions", [])
    }


def main():
    parser = argparse.ArgumentParser(description="内部一致性检测")
    parser.add_argument("--answer", type=str, help="待检查的回答")
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

    result = check_consistency(answer)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
