---
name: geo-master
description: "GEO Master · Brand AI Visibility Monitor — automatically search AI platforms (Kimi/Xunfei/Zhipu/Wenxin/DeepSeek/etc.), detect brand keyword visibility, generate 0-100 GEM score, AI analysis of why brand was not recommended, Feishu push support."
triggers:
  - GEO
  - AI visibility
  - brand monitoring
  - AI search visibility
  - competitor monitoring
allowed-tools: Bash(python3)
---

# GEO Master - Brand AI Visibility Monitor

Detect your brand's visibility across AI search platforms, generate scores and optimization recommendations.

## Version & Pricing

| Version | Price | Brand Limit | Platform Count | Tech |
|---------|-------|:-----------:|:--------------:|------|
| **Free** | ¥0/mo | 1/month | 3 platforms | Local Playwright |
| **Standard** | ¥29/mo | Unlimited | All 9 platforms | Local Playwright |
| **Pro** | ¥99/mo | Unlimited | All 9 platforms | 🌐 Tavily API (real-time) |
| **Enterprise** | ¥399/mo | Unlimited | All 9+ deep analysis | Dedicated support |

### Free Tier Limits

- Max **1 brand** per month
- Max **3 AI platforms** (Kimi, Xunfei, Wenxin)
- Quota resets automatically on the 1st of each month

### Pro Tier Core Advantage (🌐 Tavily Real-time Search)

Pro users get real-time search results via **Tavily Search API**:

- ✅ All 9 AI platforms (DeepSeek/Qwen/Doubao/Mita/Hunyuan, etc.)
- ✅ Covers **real-time search recommendations** (not training data)
- ✅ Routed through our server — no local environment needed
- ✅ Stable and efficient, no IP blocking

> After purchasing Pro/Enterprise, get your API key at [https://yk-global.com](https://yk-global.com) and use `--api-key YOUR_KEY` to unlock all features. Verification: `POST https://api.yk-global.com/v1/verify`. On failure, auto-downgrades to Free — no disruption.

## Supported AI Platforms

| Platform | Free | Standard | Pro | Tech |
|----------|:----:|:--------:|:---:|------|
| Kimi | ✅ | ✅ | ✅ | Playwright direct |
| Xunfei | ✅ | ✅ | ✅ | Playwright direct |
| Wenxin | ✅ | ✅ | ✅ | Playwright direct |
| Zhipu | ❌ | ✅ | ✅ | Playwright direct |
| DeepSeek | ❌ | ✅ | ✅ | 🌐 Tavily API |
| Qwen | ❌ | ✅ | ✅ | 🌐 Tavily API |
| Doubao | ❌ | ✅ | ✅ | 🌐 Tavily API |
| Mita | ❌ | ✅ | ✅ | 🌐 Tavily API |
| Hunyuan | ❌ | ✅ | ✅ | 🌐 Tavily API |

**Pro tier detection**: Training data indexed + real-time search results (full coverage)

## Quick Start

```bash
# Detect a single brand
python3 scripts/geo_report.py "Brand Name"

# Detect multiple brands (including competitors)
python3 scripts/geo_report.py "Brand A" "Brand B"

# No Feishu push (for debugging)
python3 scripts/geo_report.py "Brand Name" --no-push

# Check quota status
python3 scripts/geo_report.py --status

# With API Key (Pro/Enterprise users)
python3 scripts/geo_report.py "Brand Name" --api-key YOUR_API_KEY

# Upgrade to Pro / Enterprise
python3 scripts/geo_report.py --upgrade-pro
python3 scripts/geo_report.py --upgrade-ent
```

## Score Guide

| Score | Level | Description |
|------:|:-----:|-------------|
| 80-100 | 🟢 Excellent | AI actively recommends, strong brand exposure |
| 60-79 | 🟡 Good | Mentioned by some AI platforms |
| 30-59 | 🟠 Fair | Rare mentions, needs optimization |
| 0-29 | 🔴 Weak | Completely invisible |

## Config File

Config is at `config.json`:

```json
{
  "platforms": {
    "kimi": {"enabled": true, "weight": 1.0},
    "xinhuo": {"enabled": true, "weight": 0.9},
    "yiyan": {"enabled": true, "weight": 0.9},
    "zhipu": {"enabled": true, "weight": 0.8},
    "deepseek": {"enabled": false},
    "qianwen": {"enabled": false},
    "doubao": {"enabled": false},
    "mita": {"enabled": false},
    "hunyuan": {"enabled": false},
    "xunfei": {"enabled": false}
  },
  "report": {
    "push_to_feishu": true,
    "feishu_webhook": "Your Feishu group bot webhook URL"
  }
}
```

> **How to get Feishu Webhook**: Feishu group settings → Add bot → Custom bot → copy the Webhook URL.

## Environment Variables (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `GEO_QUOTA_FILE` | `.geo_quota.json` | Quota file path (recommended to keep default) |
| `GEO_API_KEY` | (empty) | Pro API key (from yk-global.com) |
| `TAVILY_API_KEY` | (required for Pro) | Tavily Search API key |

```bash
export GEO_QUOTA_FILE=/your/custom/path/.geo_quota.json
```

## AI Analysis

GEO AI reason analysis uses local analysis framework by default. To connect an external AI (e.g. MiniMax), edit `scripts/geo_analyzer.py`, find the `AI_ENDPOINT` field and fill in your AI endpoint.

## Development Progress

- [x] Phase 0: Technical validation (2026-04-15)
- [x] Phase 1: MVP development
  - [x] geo_searcher.py - Core crawler module
  - [x] geo_analyzer.py - AI reason analysis
  - [x] geo_report.py - Report generation
  - [x] geo_quota.py - Quota management (Free tier limits)
  - [x] SKILL.md - This file
- [x] Phase 2: Manual validation testing (2026-04-16)
  - [x] Xunfei CSS selector fix (textarea)
  - [x] Wenxin CSS selector fix (div[contenteditable])
  - [x] DeepSeek/Qwen login wall handling (disabled)
  - [x] Feishu Webhook config
- [x] Phase 3: Code polish
  - [x] xinhuo/xunfei merge (avoid duplicate detection)
  - [x] Free tier quota system (1 brand + 3 platforms/month)
  - [x] SKILL.md status sync
- [x] Phase 4: ClawHub listing (v1.0.0)
- [x] Phase 4 Update: Security scan fixes (v1.0.1)
- [x] Phase 5: Pro Tavily API architecture (v1.0.2)

## Official Site

[https://yk-global.com](https://yk-global.com)
