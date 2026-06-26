#!/usr/bin/env python3
"""Configure Chinese AI model providers for OpenClaw."""

import sys
import json

# Fix encoding on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# ── Provider definitions ────────────────────────────────────────────────────

PROVIDERS = {
    "deepseek": {
        "name": "DeepSeek",
        "base_url": "https://api.deepseek.com/v1",
        "api": "openai-completions",
        "models": [
            {"id": "deepseek-chat", "name": "DeepSeek Chat", "reasoning": False, "input": ["text"], "contextWindow": 65536, "maxTokens": 8192},
            {"id": "deepseek-reasoner", "name": "DeepSeek Reasoner", "reasoning": True, "input": ["text"], "contextWindow": 65536, "maxTokens": 8192},
        ],
        "default_model": "deepseek-chat",
        "register_url": "https://platform.deepseek.com",
        "free_tier": "新用户送 ¥10",
    },
    "qwen": {
        "name": "通义千问 (Qwen)",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api": "openai-completions",
        "models": [
            {"id": "qwen-turbo", "name": "Qwen Turbo", "reasoning": False, "input": ["text"], "contextWindow": 131072, "maxTokens": 8192},
            {"id": "qwen-plus", "name": "Qwen Plus", "reasoning": False, "input": ["text"], "contextWindow": 131072, "maxTokens": 8192},
            {"id": "qwen-max", "name": "Qwen Max", "reasoning": False, "input": ["text"], "contextWindow": 32768, "maxTokens": 8192},
        ],
        "default_model": "qwen-plus",
        "register_url": "https://dashscope.aliyun.com",
        "free_tier": "免费试用额度",
    },
    "zhipu": {
        "name": "智谱 GLM",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "api": "openai-completions",
        "models": [
            {"id": "glm-4-flash", "name": "GLM-4 Flash", "reasoning": False, "input": ["text"], "contextWindow": 131072, "maxTokens": 4096},
            {"id": "glm-4-plus", "name": "GLM-4 Plus", "reasoning": False, "input": ["text"], "contextWindow": 131072, "maxTokens": 4096},
            {"id": "glm-4-long", "name": "GLM-4 Long", "reasoning": False, "input": ["text"], "contextWindow": 1048576, "maxTokens": 4096},
        ],
        "default_model": "glm-4-flash",
        "register_url": "https://open.bigmodel.cn",
        "free_tier": "glm-4-flash 完全免费",
    },
    "moonshot": {
        "name": "Moonshot (Kimi)",
        "base_url": "https://api.moonshot.cn/v1",
        "api": "openai-completions",
        "models": [
            {"id": "moonshot-v1-8k", "name": "Moonshot v1 8K", "reasoning": False, "input": ["text"], "contextWindow": 8192, "maxTokens": 4096},
            {"id": "moonshot-v1-32k", "name": "Moonshot v1 32K", "reasoning": False, "input": ["text"], "contextWindow": 32768, "maxTokens": 4096},
            {"id": "moonshot-v1-128k", "name": "Moonshot v1 128K", "reasoning": False, "input": ["text"], "contextWindow": 131072, "maxTokens": 4096},
        ],
        "default_model": "moonshot-v1-32k",
        "register_url": "https://platform.moonshot.cn",
        "free_tier": "新用户送 ¥15",
    },
    "baichuan": {
        "name": "百川 (Baichuan)",
        "base_url": "https://api.baichuan-ai.com/v1",
        "api": "openai-completions",
        "models": [
            {"id": "Baichuan3-Turbo", "name": "Baichuan3 Turbo", "reasoning": False, "input": ["text"], "contextWindow": 32768, "maxTokens": 4096},
            {"id": "Baichuan4", "name": "Baichuan4", "reasoning": False, "input": ["text"], "contextWindow": 32768, "maxTokens": 4096},
        ],
        "default_model": "Baichuan3-Turbo",
        "register_url": "https://platform.baichuan-ai.com",
        "free_tier": "免费试用",
    },
    "lingyiwanwu": {
        "name": "零一万物 (Yi)",
        "base_url": "https://api.lingyiwanwu.com/v1",
        "api": "openai-completions",
        "models": [
            {"id": "yi-medium", "name": "Yi Medium", "reasoning": False, "input": ["text"], "contextWindow": 16384, "maxTokens": 4096},
            {"id": "yi-large", "name": "Yi Large", "reasoning": False, "input": ["text"], "contextWindow": 32768, "maxTokens": 4096},
        ],
        "default_model": "yi-medium",
        "register_url": "https://platform.lingyiwanwu.com",
        "free_tier": "免费试用",
    },
}


def list_providers():
    """List all supported providers."""
    print("🤖 Supported CN AI Model Providers")
    print("=" * 60)
    for pid, info in PROVIDERS.items():
        models = ", ".join(m["id"] for m in info["models"])
        print(f"\n  {info['name']} ({pid})")
        print(f"    Models:  {models}")
        print(f"    Free:    {info['free_tier']}")
        print(f"    Sign up: {info['register_url']}")
    print()


def generate_patch(provider_id, api_key, model_ids=None):
    """Generate OpenClaw config.patch JSON for a provider."""
    info = PROVIDERS.get(provider_id)
    if not info:
        print(f"❌ Unknown provider: {provider_id}", file=sys.stderr)
        print(f"   Available: {', '.join(PROVIDERS.keys())}", file=sys.stderr)
        return None

    # Filter models if specific ones requested
    if model_ids:
        models = [m for m in info["models"] if m["id"] in model_ids]
        if not models:
            print(f"⚠️  No matching models. Available: {', '.join(m['id'] for m in info['models'])}", file=sys.stderr)
            models = info["models"]
    else:
        models = info["models"]

    patch = {
        "models": {
            "providers": {
                provider_id: {
                    "baseUrl": info["base_url"],
                    "apiKey": api_key,
                    "api": info["api"],
                    "models": models,
                }
            }
        }
    }

    return patch


def interactive_setup():
    """Interactive setup wizard."""
    print("🧭 CN API Router — Interactive Setup")
    print("=" * 60)
    print()

    providers_list = list(PROVIDERS.items())
    for i, (pid, info) in enumerate(providers_list, 1):
        free = f" 🆓 {info['free_tier']}" if "免费" in info["free_tier"] else ""
        print(f"  {i}. {info['name']}{free}")

    print()
    choice = input("Select provider (number): ").strip()
    try:
        idx = int(choice) - 1
        provider_id, info = providers_list[idx]
    except (ValueError, IndexError):
        print("❌ Invalid choice")
        return

    print(f"\n📋 {info['name']}")
    print(f"   Register: {info['register_url']}")
    print(f"   Free tier: {info['free_tier']}")
    print()

    api_key = input("Enter API key: ").strip()
    if not api_key:
        print("❌ API key is required")
        return

    patch = generate_patch(provider_id, api_key)
    if patch:
        print("\n" + "=" * 60)
        print("📝 OpenClaw config.patch JSON:")
        print("=" * 60)
        print(json.dumps(patch, indent=2, ensure_ascii=False))
        print("=" * 60)
        default_model = info["default_model"]
        print(f"\n💡 Next steps:")
        print(f"  1. Agent uses `gateway config.patch` with the JSON above")
        print(f"  2. Gateway restarts automatically")
        print(f"  3. Switch model: /model {provider_id}/{default_model}")


def main():
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print("CN API Router — 国内 AI 模型配置向导")
        print()
        print("Usage:")
        print("  setup_model.py --list                          列出所有支持的厂商")
        print("  setup_model.py --interactive                   交互式配置向导")
        print("  setup_model.py --provider deepseek --api-key sk-xxx")
        print("                                                  生成 config.patch JSON")
        print("  setup_model.py --provider deepseek --api-key sk-xxx --model deepseek-reasoner")
        print("                                                  只包含指定模型")
        print()
        print(f"Supported providers: {', '.join(PROVIDERS.keys())}")
        sys.exit(0)

    if "--list" in args:
        list_providers()
        sys.exit(0)

    if "--interactive" in args:
        interactive_setup()
        sys.exit(0)

    # Direct mode
    provider_id = None
    api_key = None
    model_ids = []

    for i, arg in enumerate(args):
        if arg == "--provider" and i + 1 < len(args):
            provider_id = args[i + 1]
        elif arg == "--api-key" and i + 1 < len(args):
            api_key = args[i + 1]
        elif arg == "--model" and i + 1 < len(args):
            model_ids.append(args[i + 1])

    if not provider_id:
        print("❌ --provider is required", file=sys.stderr)
        sys.exit(1)
    if not api_key:
        print("❌ --api-key is required", file=sys.stderr)
        sys.exit(1)

    patch = generate_patch(provider_id, api_key, model_ids or None)
    if patch:
        print(json.dumps(patch, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
