# 🎯 GEO Quick Hook — AI Brand Visibility Audit for Sales

A fast pre-sales tool that shows clients how poorly their brand ranks in AI search engines compared to competitors — in minutes. Part of the GEO (Generative Engine Optimization) toolkit for [OpenClaw](https://openclaw.ai).

## What It Does

Give it a brand name + competitors → it queries AI engines → outputs a comparison card showing who's visible and who's invisible in AI-generated answers.

**Perfect for:** Sales teams, marketing consultants, brand managers

## Setup

### 1. Install

```bash
clawhub install geo-quick-hook
```

### 2. Set Environment Variables

```bash
export LLM_API_KEY="your-api-key-here"
export LLM_BASE_URL="https://api.openai.com/v1"   # or any OpenAI-compatible endpoint
export LLM_MODEL="gpt-4o"                          # or your preferred model
```

Works with any OpenAI-compatible API: OpenAI, Azure OpenAI, local models via Ollama, etc.

### 3. Trigger via OpenClaw

> "售前钩子", "快速分析", "geo-quick-hook", "客户现在多差"

## Output

An HTML comparison card showing:
- 🟢 Competitors dominating AI search results
- 🔴 Client's brand — highlighted at the bottom, clearly losing

One glance creates urgency. Perfect for closing deals.

## Part of the GEO Toolkit

| Tool | Purpose |
|------|---------|
| **geo-quick-hook** (this) | Pre-sales: show the gap |
| GEO Visibility Audit | Full brand visibility audit |
| 拓词 | Keyword opportunity mapping |
| Geo After-Sale | Monthly tracking & ROI proof |

## Requirements

- Python 3.8+
- OpenClaw
- An OpenAI-compatible LLM API key

## License

MIT License — free to use and modify.

## Contact

Built with ❤️ using [OpenClaw](https://openclaw.ai).

Interested in the full GEO toolkit (brand audits, keyword mapping, monthly tracking)?  
📧 **hhw2012@uw.edu**  
Or find me on the [OpenClaw Discord](https://discord.com/invite/clawd).
