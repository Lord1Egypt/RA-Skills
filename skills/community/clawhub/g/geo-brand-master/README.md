# GEO Master - Brand AI Visibility Monitor

Automatically search AI platforms (Kimi, Xunfei, Wenxin, Zhipu, and more), detect brand keyword visibility in AI search, generate 0-100 GEM scores, AI analysis of why brand was not recommended, with Feishu push support.

## Version & Pricing

| Version | Price | Brand Limit | Platform Count | Tech |
|---------|-------|:-----------:|:--------------:|------|
| **Free** | ¥0/mo | 1/month | 3 platforms | Local Playwright |
| **Pro** | ¥99/mo | Unlimited | All 9 platforms | 🌐 Tavily API (real-time) |
| **Enterprise** | ¥399/mo | Unlimited | All 9 + deep analysis | Dedicated support |

### Pro Tier Core Advantages

- ✅ All 9 AI platforms (DeepSeek, Qwen, Doubao, Mita, Hunyuan, etc.)
- ✅ Covers **real-time search recommendations** (not training data)
- ✅ Routed through our server — no local environment needed
- ✅ Stable and efficient, no IP blocking

> Get Pro: [https://yk-global.com](https://yk-global.com)

### Free Tier Limits

- Max **1 brand** per month
- Max **3 AI platforms** (Kimi, Xunfei, Wenxin)
- Quota resets automatically on the 1st of each month

### How to Upgrade

Visit [https://yk-global.com](https://yk-global.com) to purchase Pro/Enterprise. After receiving your upgrade code:

```bash
# Upgrade to Pro
python3 scripts/geo_report.py --upgrade-pro

# Upgrade to Enterprise
python3 scripts/geo_report.py --upgrade-ent
```

## Quick Start

```bash
# Detect a single brand
python3 scripts/geo_report.py "Brand Name"

# Detect multiple brands
python3 scripts/geo_report.py "Brand A" "Brand B"

# No Feishu push (debugging)
python3 scripts/geo_report.py "Brand Name" --no-push

# Check quota status
python3 scripts/geo_report.py --status

# With API Key (Pro/Enterprise users)
python3 scripts/geo_report.py "Brand Name" --api-key YOUR_API_KEY
```

## Supported Platforms

| Platform | Free | Pro |
|----------|:----:|:---:|
| Kimi | ✅ | ✅ |
| Xunfei | ✅ | ✅ |
| Wenxin | ✅ | ✅ |
| Zhipu | ❌ | ✅ |
| DeepSeek | ❌ | ✅ |
| Qwen | ❌ | ✅ |
| Doubao | ❌ | ✅ |
| Mita | ❌ | ✅ |
| Hunyuan | ❌ | ✅ |

## Score Guide

| Score | Level | Description |
|------:|:-----:|-------------|
| 80-100 | 🟢 Excellent | AI actively recommends, strong brand exposure |
| 60-79 | 🟡 Good | Mentioned by some AI platforms |
| 30-59 | 🟠 Fair | Rare mentions, needs optimization |
| 0-29 | 🔴 Weak | Completely invisible |

## Config File

Edit `config.json`:

```json
{
  "report": {
    "push_to_feishu": true,
    "feishu_webhook": "Your Feishu group bot webhook URL"
  }
}
```

**How to get Feishu Webhook?**
Add a "Custom bot" in your Feishu group settings, copy the Webhook URL into the config above.

## Pro API Configuration

Pro users need to set Tavily API Key before running:

```bash
export TAVILY_API_KEY=your_tavily_api_key
```

Get Tavily API Key: https://tavily.com — register to get your key

## Dependencies

- Python 3.10+
- playwright (`pip install playwright && playwright install chromium`)

## Official Site

[https://yk-global.com](https://yk-global.com)

---

> For paid plans, visit [YK-Global.com](https://yk-global.com)
