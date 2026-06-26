#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.0.0"]
# ///
"""
DeepSeek one-shot query.
Usage: uv run ask.py "your question" [--model flash|pro|v4-flash|v4-pro] [--think]
"""

import sys
import argparse
import os

def get_api_key():
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        print("❌ DEEPSEEK_API_KEY not set.")
        print("   Get your key at: https://platform.deepseek.com/api_keys")
        print("   Then run: export DEEPSEEK_API_KEY=your_key_here")
        sys.exit(1)
    return key

MODEL_MAP = {
    "flash":    "deepseek-v4-flash",
    "pro":      "deepseek-v4-pro",
    "v4-flash": "deepseek-v4-flash",
    "v4-pro":   "deepseek-v4-pro",
    "v3":       "deepseek-v4-flash",  # v4-flash replaces v3/chat
    "r1":       "deepseek-v4-pro",    # v4-pro replaces r1/reasoner
    "chat":     "deepseek-v4-flash",
    "reasoner": "deepseek-v4-pro",
}

PRICING = {
    "deepseek-v4-flash": {"input": 0.014, "output": 0.028, "cache": 0.0014},
    "deepseek-v4-pro":   {"input": 0.174, "output": 0.348, "cache": 0.0174},
}

def main():
    parser = argparse.ArgumentParser(description="Ask DeepSeek a question")
    parser.add_argument("prompt", nargs="?", help="Your question or prompt")
    parser.add_argument("--model", "-m", default="flash",
                        help="Model: flash (default), pro, v4-flash, v4-pro (default: flash)")
    parser.add_argument("--think", action="store_true",
                        help="Enable thinking/reasoning mode (forces pro model)")
    parser.add_argument("--system", "-s", default=None, help="System prompt")
    parser.add_argument("--no-stream", action="store_true", help="Disable streaming")
    args = parser.parse_args()

    if not args.prompt:
        print("Usage: uv run ask.py \"your question\" [--model flash|pro] [--think]")
        sys.exit(1)

    from openai import OpenAI

    model_id = MODEL_MAP.get(args.model, args.model)
    if args.think:
        model_id = "deepseek-v4-pro"

    client = OpenAI(
        api_key=get_api_key(),
        base_url="https://api.deepseek.com/v1",
    )

    messages = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": args.prompt})

    model_label = "⚡ Flash" if "flash" in model_id else "🚀 Pro"
    think_label = " [thinking]" if args.think else ""
    print(f"\nDeepSeek {model_label}{think_label}\n{'─' * 40}")

    if args.no_stream:
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
        )
        content = response.choices[0].message.content
        print(content)

        usage = response.usage
        if usage and model_id in PRICING:
            p = PRICING[model_id]
            cost = (usage.prompt_tokens / 1e6 * p["input"]) + \
                   (usage.completion_tokens / 1e6 * p["output"])
            print(f"\n{'─' * 40}")
            print(f"Tokens: {usage.prompt_tokens} in / {usage.completion_tokens} out | "
                  f"Cost: ~${cost:.5f}")
    else:
        with client.chat.completions.create(
            model=model_id,
            messages=messages,
            stream=True,
        ) as stream:
            full = ""
            reasoning = ""
            in_think = False
            for chunk in stream:
                delta = chunk.choices[0].delta if chunk.choices else None
                if not delta:
                    continue
                # Handle thinking tokens (pro model)
                if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                    if not in_think:
                        print("\n[Thinking...]", flush=True)
                        in_think = True
                    reasoning += delta.reasoning_content
                    print(delta.reasoning_content, end="", flush=True)
                if delta.content:
                    if in_think:
                        print(f"\n{'─' * 40}\n[Answer]", flush=True)
                        in_think = False
                    print(delta.content, end="", flush=True)
                    full += delta.content
            print()

    print()

if __name__ == "__main__":
    main()
