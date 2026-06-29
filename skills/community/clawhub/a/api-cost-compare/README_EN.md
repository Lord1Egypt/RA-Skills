# api-cost-compare

> A CLI tool to compare LLM API pricing across providers

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

`api-cost-compare` is a lightweight CLI tool that helps you quickly compare API pricing across major LLM providers including Anthropic, OpenAI, DeepSeek, Google, OpenRouter, and Mistral.

---

## Quick Install

```bash
pip install git+https://github.com/minirr890112-byte/api-cost-compare.git
```

Or install from source:

```bash
git clone https://github.com/minirr890112-byte/api-cost-compare.git
cd api-cost-compare
pip install -e .
```

## Usage

After installation, use the `api-cost-compare` command:

```bash
api-cost-compare --help
```

### List All Models

```bash
api-cost-compare list
```

### Compare Two Models

```bash
api-cost-compare compare "GPT-4o" "deepseek-chat"
```

### Recommend Best Model

```bash
# Chat recommendations
api-cost-compare recommend --task chat

# Coding with $50 budget
api-cost-compare recommend --task coding --budget 50

# Reasoning with $100 budget
api-cost-compare recommend --task reasoning --budget 100
```

### Estimate API Cost

```bash
api-cost-compare estimate --model "GPT-4o" --input 1000 --output 500
api-cost-compare estimate --model "deepseek-chat" --input 5000 --output 2000
```

---

## Supported Providers

| Provider | Models | Notes |
|----------|--------|-------|
| **Anthropic** | 3 | Claude Opus 4 / Sonnet 4 / Haiku |
| **OpenAI** | 3 | GPT-4o / GPT-4.1 / GPT-4.1-mini |
| **DeepSeek** | 2 | deepseek-chat (V3) / deepseek-reasoner (R1) |
| **Google** | 2 | Gemini 1.5 Pro / Gemini 1.5 Flash |
| **OpenRouter** | 2 | claude-sonnet-4 / gpt-4o (different pricing) |
| **Mistral** | 2 | mistral-large / mistral-small |

---

## Features

- 📊 **Real-time pricing comparison** — All prices are latest official API pricing
- 🏷️ **Task tagging system** — Categorize by chat, coding, reasoning
- 💰 **Cost estimation** — Precise USD cost calculation for any token usage
- 🎯 **Smart recommendations** — Best model for your task and budget
- 🎨 **Beautiful output** — Colorful terminal tables powered by Rich
- 🌐 **Chinese-first interface** — Default output in Chinese (English docs available)

---

## Motivation

When choosing an LLM API, developers face multiple trade-offs: model capability, response speed, context window size, and most importantly — cost. Pricing strategies vary dramatically across providers; for instance, DeepSeek's input pricing is roughly one-tenth of GPT-4o's, while OpenRouter typically adds a margin as a middle layer.

`api-cost-compare` addresses this pain point by centralizing pricing data from all major LLM providers, helping you make informed decisions quickly.

---

## Project Structure

```
api-cost-compare/
├── api_cost_compare/
│   ├── __init__.py      # Package init
│   ├── providers.py     # Pricing data & core logic
│   └── cli.py           # CLI commands
├── pyproject.toml       # Project config
├── README.md            # Chinese docs
├── README_EN.md         # English docs
└── LICENSE              # MIT License
```

---

## Contributing

Issues and PRs are welcome! To add new providers or update pricing, edit the `get_all_pricing()` function in `api_cost_compare/providers.py`.

---

## License

MIT © 2025 minirr890112-byte
