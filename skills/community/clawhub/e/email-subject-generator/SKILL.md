---
name: email-subject-generator
description: AI-powered email subject line generator. Create subject lines that get opened.
version: 1.0.7
author: Matt
tags:
  - email
  - marketing
  - copywriting
pricing:
  type: pay-per-use
  price: 0.001
  currency: USDT
  payment_provider: skillpay.me
---

# Email Subject Line Generator

Generate email subject lines that get opened, clicked, and converted.

## Features

- **High Open Rates** - Psychological triggers that work
- **Personalization** - Dynamic placeholders
- **Multiple Variations** - Get 10 subject line options
- **Spam-Free** - Avoid trigger words

## Usage

```bash
# Generate email subjects
email-subject-generator "product launch announcement"

# For specific purpose
email-subject-generator "newsletter" --purpose newsletter
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--purpose` | Email purpose (newsletter, sales, announcement) | - |

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

Sloan is your AI columnist - a professional email marketing expert specializing in subject line optimization.

## Support

- GitHub: https://github.com/icepopma/email-subject-generator
- Discord: https://discord.gg/clawd
- Email: icepopma@hotmail.com

## License

MIT © Matt
