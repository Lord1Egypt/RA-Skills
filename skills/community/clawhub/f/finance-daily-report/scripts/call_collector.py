#!/usr/bin/env python3
"""
External Collector Caller — invokes LLM models as data collectors.
Primary: kimi-k2.5 (DashScope)
Backup: doubao-seed-2-0-mini-260215 (Volcengine)

Usage:
    python3 call_collector.py --prompt "采集任务描述" --model primary
    python3 call_collector.py --prompt "..." --model backup
    python3 call_collector.py --prompt "..." --auto  # try primary, fallback to backup
"""

import json
import sys
import os
import urllib.request
import urllib.error
import argparse

# Model configs (keys from environment variables)
PRIMARY = {
    "name": "kimi-k2.5",
    "url": "https://coding.dashscope.aliyuncs.com/v1/chat/completions",
    "key": os.environ.get("DASHSCOPE_API_KEY", ""),
    "model": "kimi-k2.5",
}

BACKUP = {
    "name": "doubao-seed-mini",
    "url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "key": os.environ.get("DOUBAO_API_KEY", ""),
    "model": "doubao-seed-2-0-mini-260215",
}


def call_llm(config, prompt, timeout=120):
    """Call an LLM and return the response content."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['key']}",
    }
    
    # System prompt emphasizes NO markdown, pure JSON
    system_prompt = """你是专业的金融数据采集助手。任务：从原始数据中提取结构化信息。

输出要求：
1. 只输出纯 JSON，不要用 ```json 或 ``` 包裹
2. 不要有任何额外文字、解释、注释
3. JSON 必须是合法可解析的
4. 数据缺失用 null 表示，不要编造"""

    payload = {
        "model": config["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 4000,
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(config["url"], data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            content = body.get("choices", [{}])[0].get("message", {}).get("content", "")
            usage = body.get("usage", {})
            
            return {
                "status": "success",
                "model": config["name"],
                "content": content,
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return {
            "status": "error",
            "model": config["name"],
            "error": f"HTTP {e.code}: {e.reason}",
            "error_body": error_body[:500],
        }
    except Exception as e:
        return {
            "status": "error",
            "model": config["name"],
            "error": str(e),
        }


def extract_json(content):
    """Extract JSON from response content (may have markdown or extra text)."""
    # Try to find JSON block
    content = content.strip()
    
    # Remove markdown code blocks if present
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    
    content = content.strip()
    
    # Find first { and last }
    start = content.find("{")
    end = content.rfind("}") + 1
    
    if start >= 0 and end > start:
        json_str = content[start:end]
        try:
            return json.loads(json_str), None
        except json.JSONDecodeError as e:
            return None, f"JSON parse error: {e}"
    
    return None, "No JSON found in response"


def main():
    parser = argparse.ArgumentParser(description="Call external LLM as data collector")
    parser.add_argument("--prompt", required=True, help="Collector prompt")
    parser.add_argument("--model", choices=["primary", "backup", "auto"], default="auto",
                        help="Which model to use")
    parser.add_argument("--output", choices=["json", "raw", "status"], default="status",
                        help="Output format")
    args = parser.parse_args()
    
    result = None
    
    if args.model == "primary":
        result = call_llm(PRIMARY, args.prompt)
    elif args.model == "backup":
        result = call_llm(BACKUP, args.prompt)
    else:  # auto
        # Try primary first
        result = call_llm(PRIMARY, args.prompt)
        if result["status"] != "success":
            print(f"Primary failed: {result.get('error', 'unknown')}, trying backup...", file=sys.stderr)
            result = call_llm(BACKUP, args.prompt)
    
    # Output
    if args.output == "status":
        if result["status"] == "success":
            print(f"✅ {result['model']} | Tokens: {result['total_tokens']}")
        else:
            print(f"❌ {result['model']}: {result.get('error', 'unknown')}")
            if result.get("error_body"):
                print(f"   Detail: {result['error_body'][:200]}")
    elif args.output == "raw":
        print(result.get("content", result.get("error", "")))
    elif args.output == "json":
        if result["status"] == "success":
            parsed, err = extract_json(result["content"])
            if parsed:
                print(json.dumps(parsed, ensure_ascii=False, indent=2))
            else:
                print(f"Error: {err}", file=sys.stderr)
                print(result["content"], file=sys.stdout)
        else:
            print(f"Error: {result.get('error', 'unknown')}", file=sys.stderr)
    
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main() or 0)
