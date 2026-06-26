#!/usr/bin/env python3
"""
Free AI Bot - 免费 AI 聚合器
自动选择最佳免费方案，支持本地模型 + 云端免费 API
"""

import os
import sys
import json
import argparse
from typing import Optional

# 配置
DEFAULT_LOCAL_MODEL = "llama3.2"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

PROVIDERS = ["ollama", "cloudflare", "groq"]


def call_ollama(prompt: str, model: str = DEFAULT_LOCAL_MODEL) -> Optional[str]:
    """调用本地 Ollama 模型"""
    try:
        import requests
        url = f"{OLLAMA_HOST}/api/generate"
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        resp = requests.post(url, json=data, timeout=120)
        if resp.status_code == 200:
            return resp.json().get("response", "").strip()
    except Exception as e:
        print(f"[Ollama] 失败: {e}", file=sys.stderr)
    return None


def call_cloudflare(prompt: str) -> Optional[str]:
    """调用 Cloudflare Workers AI"""
    try:
        import requests
        account_id = os.getenv("CF_ACCOUNT_ID")
        api_token = os.getenv("CF_API_TOKEN")
        if not account_id or not api_token:
            print("[Cloudflare] 未配置", file=sys.stderr)
            return None
        
        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id/ai/run/@cf/meta/llama-3.1-8b-instruct"
        headers = {"Authorization": f"Bearer {api_token}"}
        data = {"prompt": prompt}
        
        resp = requests.post(url, json=data, headers=headers, timeout=60)
        if resp.status_code == 200:
            return resp.json().get("result", {}).get("response", "").strip()
    except Exception as e:
        print(f"[Cloudflare] 失败: {e}", file=sys.stderr)
    return None


def call_groq(prompt: str) -> Optional[str]:
    """调用 Groq 免费 API"""
    try:
        import requests
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("[Groq] 未配置", file=sys.stderr)
            return None
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512
        }
        
        resp = requests.post(url, json=data, headers=headers, timeout=60)
        if resp.status_code == 200:
            return resp.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    except Exception as e:
        print(f"[Groq] 失败: {e}", file=sys.stderr)
    return None


def smart_route(prompt: str, preferred: str = "auto") -> str:
    """智能路由 - 自动选择最佳方案"""
    providers = [preferred] if preferred != "auto" else PROVIDERS
    
    for provider in providers:
        print(f"尝试 {provider}...", file=sys.stderr)
        
        if provider == "ollama":
            result = call_ollama(prompt)
        elif provider == "cloudflare":
            result = call_cloudflare(prompt)
        elif provider == "groq":
            result = call_groq(prompt)
        else:
            continue
        
        if result:
            return result
    
    return "抱歉，所有免费方案都不可用。请检查配置或稍后重试。"


def main():
    parser = argparse.ArgumentParser(description="Free AI Bot - 免费 AI 聚合器")
    parser.add_argument("prompt", help="要询问的问题")
    parser.add_argument("--provider", "-p", default="auto", choices=["auto"] + PROVIDERS, help="指定 Provider")
    parser.add_argument("--model", "-m", default=DEFAULT_LOCAL_MODEL, help="Ollama 模型名称")
    
    args = parser.parse_args()
    
    # 设置全局默认模型
    global DEFAULT_LOCAL_MODEL
    DEFAULT_LOCAL_MODEL = args.model
    
    result = smart_route(args.prompt, args.provider)
    print(result)


if __name__ == "__main__":
    main()
