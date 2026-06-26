#!/usr/bin/env python3
"""
交叉验证模块
将待验证回答与多源参考答案对比，逐事实给出verdict
"""

import os
import json
import argparse
import sys
from pathlib import Path


def load_prompt(fact: str, references: list) -> str:
    """加载prompt模板，填充事实和参考来源"""
    prompt_path = Path(__file__).parent.parent / "prompts" / "verify.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    ref_text = "\n\n".join([f"【来源{i+1}】{r}" for i, r in enumerate(references)])
    return prompt.replace("{{REFERENCES}}", ref_text).replace("{{FACT}}", fact)


def call_llm(prompt: str) -> str:
    """调用LLM API（同decompose.py）"""
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


def verify_fact(fact: str, references: list) -> dict:
    """验证单个事实，返回verdict/confidence/reason"""
    prompt = load_prompt(fact, references)
    response = call_llm(prompt)
    result = parse_response(response)

    # 确保返回格式正确
    return {
        "verdict": result.get("verdict", "uncertain"),
        "confidence": result.get("confidence", 0.5),
        "reason": result.get("reason", "")
    }


def verify_facts(facts: list, references: list) -> list:
    """批量验证多个事实"""
    results = []
    for fact_item in facts:
        fact_text = fact_item["text"] if isinstance(fact_item, dict) else fact_item
        result = verify_fact(fact_text, references)
        results.append({
            "id": fact_item.get("id", 0) if isinstance(fact_item, dict) else len(results) + 1,
            "text": fact_text,
            "verdict": result["verdict"],
            "confidence": result["confidence"],
            "reason": result["reason"]
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="交叉验证事实")
    parser.add_argument("--facts", type=str, required=True, help="事实列表JSON文件")
    parser.add_argument("--references", type=str, required=True, help="参考来源JSON文件（字符串数组）")
    args = parser.parse_args()

    with open(args.facts, "r", encoding="utf-8") as f:
        facts = json.load(f)
    with open(args.references, "r", encoding="utf-8") as f:
        references = json.load(f)

    # facts可能是 {"facts": [...]} 格式
    if isinstance(facts, dict) and "facts" in facts:
        facts = facts["facts"]

    results = verify_facts(facts, references)
    print(json.dumps({"results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
