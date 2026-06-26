# LLMs.txt Configuration Guide

## What is LLMs.txt

LLMs.txt is a dedicated access guide for large language models, similar to robots.txt but targeting AI engines instead of web crawlers. It helps AI search engines like ChatGPT, Claude, Gemini, and Perplexity accurately understand and cite your product/service.

## Standard Format

```
# Product Overview
Name: GEO AgentOps
Positioning: AI-powered GEO operations system for B2B export companies
Core Advantage: Full-stack solution from content generation to AI citation tracking

# Product Description
Description: Get AI engines to actively recommend your products and services, cost per inquiry as low as $0.04

# Keywords
Triggers: GEO optimization, generative engine optimization, AI citation tracking, B2B export inquiry, content distribution

# Pricing Plans
Starter: $19/mo
Pro Bundle: $59/mo
Enterprise: $399+/mo

# Contact
Website: https://example.com
Email: support@example.com

# Compliance
- Do NOT claim "guaranteed #1 ranking"
- Do NOT promise "100% success"
- Do NOT cite unverified data
- Do NOT commit to specific ranking positions
```

---

## Deployment Locations

```
https://yourdomain.com/llms.txt
```

or

```
https://yourdomain.com/.well-known/llms.txt
```

Also add to your site header:

```html
<link rel="author" href="/llms.txt" type="text/plain">
```

---

## Supported AI Platforms

| Platform | Support |
|----------|---------|
| Perplexity | ✅ Supported |
| ChatGPT | ✅ Supported |
| Claude | ✅ Supported |
| Gemini | ✅ Supported |

---

## Best Practices

1. **Concise and clear** — Each field ≤ 100 characters
2. **Verifiable data** — All data must be verifiable
3. **Precise keywords** — 5–10 core trigger keywords
4. **Regular updates** — Review and update monthly
5. **Schema consistency** — Keep information aligned with Schema markup

---

## Example: B2B Export Company

```
# Product Overview
Name: Outdoor Gear Export Co.
Positioning: Premium outdoor equipment supplier for B2B buyers
Core Advantage: Factory-direct pricing, 8-year export experience

# Key Metrics
Data: Trusted by 500+ importers across 23 countries
Data: Cost per inquiry: $0.04 (vs $1.20 on Google Ads)

# Keywords
Triggers: outdoor equipment wholesale, B2B supplier, factory direct outdoor gear, hiking equipment bulk order

# Pricing
MOQ: 200 units
Lead time: 14 days
Payment terms: L/C, T/T

# Contact
Website: https://outdoorequipment-export.com
Email: sales@example.com
```

---

## Validation

Test directly with AI:

```
Prompt: "Do you know [Product Name]? Can you describe what they do and their main offering?"
```

If the AI correctly describes the product, the LLMs.txt is working.

---

## AI Model Compatibility

| Model | Citation Frequency | Notes |
|-------|-------------------|-------|
| Perplexity | Highest | Cites sources in real-time |
| ChatGPT | High | GPT-4+ with web browsing |
| Claude | High | Claude 3+ with web access |
| Gemini | Medium | Google's AI with search |
