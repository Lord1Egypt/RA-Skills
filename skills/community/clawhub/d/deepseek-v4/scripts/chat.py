#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["openai>=1.0.0"]
# ///
"""
DeepSeek multi-turn chat (non-interactive — outputs a full conversation prompt).
Usage: uv run chat.py --model flash|pro [--think] [--history "..."]
"""

import sys
import argparse
import os
import json

def get_api_key():
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        print("❌ DEEPSEEK_API_KEY not set.")
        print("   Get your key at: https://platform.deepseek.com/api_keys")
        print("   Then: export DEEPSEEK_API_KEY=your_key_here")
        sys.exit(1)
    return key

MODEL_MAP = {
    "flash": "deepseek-v4-flash",
    "pro":   "deepseek-v4-pro",
    "v4-flash": "deepseek-v4-flash",
    "v4-pro":   "deepseek-v4-pro",
}

def main():
    parser = argparse.ArgumentParser(description="DeepSeek multi-turn chat")
    parser.add_argument("--model", "-m", default="flash", help="flash or pro")
    parser.add_argument("--think", action="store_true", help="Thinking mode (pro only)")
    parser.add_argument("--system", "-s", default=None, help="System prompt")
    parser.add_argument("--messages", help="JSON array of prior messages to continue")
    parser.add_argument("--user", help="Next user message to send")
    args = parser.parse_args()

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
    if args.messages:
        try:
            messages.extend(json.loads(args.messages))
        except json.JSONDecodeError:
            print("❌ --messages must be valid JSON array")
            sys.exit(1)

    if not args.user:
        model_label = "Flash ⚡" if "flash" in model_id else "Pro 🚀"
        print(f"\nDeepSeek {model_label} — Chat Mode")
        print("Type your message and press Enter. Type 'exit' to quit.\n")
        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            if not user_input or user_input.lower() in ("exit", "quit", "bye"):
                print("Goodbye!")
                break
            messages.append({"role": "user", "content": user_input})
            print("\nDeepSeek: ", end="", flush=True)
            full = ""
            with client.chat.completions.create(
                model=model_id,
                messages=messages,
                stream=True,
            ) as stream:
                for chunk in stream:
                    delta = chunk.choices[0].delta if chunk.choices else None
                    if delta and delta.content:
                        print(delta.content, end="", flush=True)
                        full += delta.content
            print("\n")
            messages.append({"role": "assistant", "content": full})
    else:
        messages.append({"role": "user", "content": args.user})
        full = ""
        with client.chat.completions.create(
            model=model_id,
            messages=messages,
            stream=True,
        ) as stream:
            for chunk in stream:
                delta = chunk.choices[0].delta if chunk.choices else None
                if delta and delta.content:
                    print(delta.content, end="", flush=True)
                    full += delta.content
        print()
        messages.append({"role": "assistant", "content": full})
        print(f"\n# Continue conversation:\n# --messages '{json.dumps(messages)}'")

if __name__ == "__main__":
    main()
