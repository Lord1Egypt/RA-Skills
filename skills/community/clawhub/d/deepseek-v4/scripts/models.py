#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Show DeepSeek V4 models, pricing, and usage guide."""

def main():
    print("""
DeepSeek V4 — Models & Pricing
═══════════════════════════════════════════════════════

Model              ID                   Input      Output     Context
────────────────── ──────────────────── ─────────  ─────────  ────────
V4 Flash  ⚡       deepseek-v4-flash    $0.014/M   $0.028/M   1M tok
V4 Pro    🚀       deepseek-v4-pro      $0.174/M   $0.348/M   1M tok

Cache hit prices are 10× cheaper (Flash: $0.0014/M, Pro: $0.0174/M)
Limited-time 75% discount on V4-Pro through May 5, 2026.

Legacy model aliases (deprecated 2026-07-24):
  deepseek-chat      →  deepseek-v4-flash
  deepseek-reasoner  →  deepseek-v4-pro

─────────────────────────────────────────────────────
When to use which model:

⚡ V4 Flash  — everyday tasks, fast responses, low cost
   Best for: Q&A, summaries, writing, code generation,
             translation, classification

🚀 V4 Pro   — complex reasoning, hard problems, thinking mode
   Best for: math, coding challenges, deep analysis,
             multi-step reasoning, research

─────────────────────────────────────────────────────
Quick start:

  export DEEPSEEK_API_KEY=your_key_here

  # Ask Flash (fast & cheap)
  uv run {baseDir}/scripts/ask.py "Explain quantum entanglement"

  # Ask Pro
  uv run {baseDir}/scripts/ask.py "Solve this math problem: ..." --model pro

  # Use thinking mode (Pro with reasoning trace)
  uv run {baseDir}/scripts/ask.py "Prove that sqrt(2) is irrational" --think

  # Multi-turn chat
  uv run {baseDir}/scripts/chat.py --model flash

─────────────────────────────────────────────────────
API key: https://platform.deepseek.com/api_keys
Docs:    https://api-docs.deepseek.com
""")

if __name__ == "__main__":
    main()
