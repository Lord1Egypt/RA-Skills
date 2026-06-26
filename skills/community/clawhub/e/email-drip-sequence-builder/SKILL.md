---
name: email-drip-sequence-builder
description: "Generate complete email drip sequences from product descriptions with personalization, A/B subject lines, and ESP-ready formatting. Use when the user needs email campaigns, welcome series, product launch sequences, re-engagement flows, or nurture campaigns for any industry."
version: 1.1.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY"],"bins":[]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📧"}}
---

# Email Drip Sequence Builder

## Overview

Build production-ready email drip sequences from a single product description or business context. This skill generates complete multi-email campaigns with personalization tokens, A/B subject line variants, timing recommendations, and formatting ready for any ESP (Mailchimp, ConvertKit, Brevo, ActiveCampaign, etc.).

Supports: welcome series, product launch sequences, re-engagement flows, abandoned cart recovery, onboarding drips, educational series, and seasonal campaigns.

## Quick Start

Try these prompts immediately:

```
Build a 5-email welcome sequence for a witchcraft supplies shop that sells candles, herbs, and crystals. Include a lead magnet delivery in email 1.
```

```
Create a product launch drip campaign for a new AI writing tool. 3 pre-launch emails, 1 launch day email, 2 follow-ups.
```

```
Generate a re-engagement sequence for subscribers who haven't opened emails in 30 days. Target: personal finance blog readers.
```

```
Build an abandoned cart recovery sequence for an Etsy digital products shop. 3 emails over 5 days.
```

## Capabilities

### Sequence Types
- **Welcome Series** — New subscriber onboarding (3-7 emails)
- **Product Launch** — Pre-launch hype, launch day, follow-up (4-8 emails)
- **Re-engagement** — Win back inactive subscribers (3-5 emails)
- **Abandoned Cart** — Recovery sequences with urgency (3-4 emails)
- **Educational Drip** — Value-first content series (5-10 emails)
- **Seasonal/Event** — Holiday, Black Friday, special occasions (3-6 emails)
- **Nurture Campaign** — Long-term relationship building (7-12 emails)

### Per-Email Output
Each email in the sequence includes:
- **Subject line** (primary + A/B variant)
- **Preview text** (40-90 chars, optimized for inbox display)
- **Email body** (HTML-ready with personalization tokens)
- **Send timing** (delay from previous email or trigger)
- **Segment conditions** (who should receive this email)
- **Goal/CTA** (what action you want the reader to take)

### Personalization Tokens
Outputs use standard ESP merge tags:
- `{{first_name}}` — Subscriber's first name
- `{{product_name}}` — Referenced product
- `{{company_name}}` — Your brand name
- `{{unsubscribe_url}}` — Required unsubscribe link
- Custom tokens based on your data

### A/B Testing
Every email includes two subject line variants:
- **Variant A** — Direct/benefit-focused
- **Variant B** — Curiosity/question-based
- Recommended split: 20% test, 80% winner after 4 hours

## Configuration

### Required Environment Variables
```
OPENAI_API_KEY=sk-...   # For content generation (or use Claude API)
```

### Optional Parameters
- `--tone` — Brand voice (friendly, professional, casual, authoritative)
- `--industry` — Business vertical for tailored copy
- `--email-count` — Number of emails in sequence (default: 5)
- `--esp` — Target ESP for formatting (mailchimp, convertkit, brevo, activecampaign)
- `--cta-style` — Button vs text link vs both

## Example Output

### Welcome Sequence — Email 1 of 5

**Subject A:** Welcome to [Brand]! Here's your free guide 🎁
**Subject B:** Your [Lead Magnet Name] is ready — plus a surprise inside

**Preview text:** Download your guide + discover what's coming this week

**Send timing:** Immediately after signup

**Body:**
```html
<p>Hi {{first_name}},</p>

<p>Welcome to the [Brand] community! I'm thrilled you're here.</p>

<p>As promised, here's your free guide:</p>

<p><a href="{{lead_magnet_url}}" style="display:inline-block;background:#4299e1;color:white;padding:12px 24px;border-radius:6px;text-decoration:none;">Download Your Free Guide</a></p>

<p>Over the next few days, I'll share:</p>
<ul>
  <li>📖 Our most popular [topic] tips</li>
  <li>🔧 Tools we use every day</li>
  <li>🎯 A special offer just for new subscribers</li>
</ul>

<p>Hit reply and tell me — what's your biggest challenge with [topic]?</p>

<p>Talk soon,<br>[Your Name]</p>
```

**Goal:** Deliver lead magnet, set expectations, encourage reply
**Segment:** All new subscribers

## Tips & Best Practices

1. **Timing matters** — Space emails 2-3 days apart for welcome series, 1 day for abandoned cart
2. **Front-load value** — First 3 emails should be 80% value, 20% promotion
3. **One CTA per email** — Don't dilute focus with multiple calls to action
4. **Test subject lines** — Always use the A/B variants, let data decide
5. **Personalize early** — Use first name in subject line of email 2+, not email 1
6. **Include plain text** — Always generate both HTML and plain text versions
7. **Mobile-first** — Keep paragraphs short (2-3 sentences max)

## Safety & Guardrails

This skill will NOT:
- Generate spam or misleading subject lines
- Create emails that violate CAN-SPAM/GDPR requirements
- Produce content without unsubscribe links
- Generate deceptive urgency or false scarcity claims
- Create emails impersonating other brands
- Output content that bypasses email filters

All generated emails include:
- Required unsubscribe link placeholder
- Physical address placeholder (CAN-SPAM requirement)
- Clear sender identification
- Honest subject lines matching email content

## Troubleshooting

**Q: Emails feel too generic?**
A: Provide more context — industry, target audience demographics, brand voice examples, and competitor names.

**Q: Subject lines too long?**
A: Specify `--subject-length 50` to cap at 50 characters. Mobile displays ~35 chars.

**Q: Need different ESP formatting?**
A: Specify `--esp convertkit` or `--esp mailchimp` — merge tag syntax differs between platforms.

**Q: How to handle multi-language?**
A: Generate the sequence in English first, then ask for translation. Include `{{language}}` token for dynamic routing.

**Q: Sequence too long/short?**
A: Use `--email-count N` to set exact count, or describe the campaign goal and let the skill recommend optimal length.
