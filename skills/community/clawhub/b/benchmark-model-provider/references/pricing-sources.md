# Pricing Sources Policy

## Purpose

This file defines how the skill should resolve pricing, estimate missing prices, and communicate pricing confidence.

---

## 1. Source precedence

Resolve pricing in this order:

1. Official public pricing page
2. Official provider documentation
3. Closest matching public tier estimate
4. Local infrastructure estimate

---

## 2. Provider guidance

### OpenAI-family models
Use official public pricing when available.

### Anthropic / Claude-family models
Use official Anthropic pricing or the closest matching public tier estimate.

### Gemini-family models
Use official Google Gemini pricing or the closest matching public tier estimate.

### Local models
Do not present local inference cost as an official API bill. Mark it as a local or infrastructure estimate.

---

## 3. Confidence labels

Each resolved price should carry a confidence label:

- `official`
- `near-match-estimate`
- `local-estimate`
- `unknown`

---

## 4. Cost calculation

When token pricing is available, use a formula like:

```text
cost =
  (input_tokens / 1_000_000) * input_price_per_million +
  (output_tokens / 1_000_000) * output_price_per_million
```

If pricing is flat or non-token-based, record the rule used.

---

## 5. Required transparency

Always record:

- pricing source
- confidence label
- whether the price is estimated
- the formula or assumption used when estimation is required

---

## 6. Design rule

If exact pricing cannot be confirmed, prefer transparent estimation over false precision.
