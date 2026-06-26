---
name: blog-title-optimizer
description: AI-powered blog title optimizer. Generate SEO-friendly, click-worthy headlines that drive traffic.
version: 1.0.7
author: Matt
tags:
  - blog
  - seo
  - content
  - writing
pricing:
  type: pay-per-use
  price: 0.001
  currency: USDT
  payment_provider: skillpay.me
---

# Blog Title Optimizer

Generate SEO-friendly, click-worthy blog titles that rank and drive traffic.

## Features

- **SEO Optimization** - Keywords and search intent
- **Click-Worthy** - Psychological triggers that work
- **Multiple Options** - Get 7 title variations
- **Length Optimization** - Perfect for Google & social

## Usage

```bash
# Generate blog titles
blog-title-optimizer "how to build AI agents"

# With specific keywords
blog-title-optimizer "AI agents tutorial" --keywords "beginners,2026"
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--keywords` | Target keywords (comma-separated) | - |

## Pricing

- **Pay per use**: 0.001 USDT per generation

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SKILLPAY_MERCHANT_KEY` | Payment merchant key (optional, embedded key used by default) | No |
| `OPENCLAW_GATEWAY_TOKEN` | Gateway auth token for local API fallback | No |

## Requirements

- OpenClaw with Sloan agent (AI columnist)
- OpenClaw Gateway running locally (for API fallback)

## About Sloan

Sloan is your AI columnist - a professional content strategist specializing in SEO and headline optimization.

## Support

- GitHub: https://github.com/icepopma/blog-title-optimizer
- Discord: https://discord.gg/clawd
- Email: icepopma@hotmail.com

## License

MIT © Matt
