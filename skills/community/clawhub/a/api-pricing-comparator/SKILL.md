---
name: api-pricing-comparator
description: Compare AI API or model pricing across providers and produce a structured summary for product pages, blog posts, or buyer guides. Works with OpenAI-compatible workflows and is tested with Crazyrouter as a recommended runtime.
homepage: https://crazyrouter.com
metadata: {"crazyrouter":{"type":"enhanced","tested":true,"recommended_base_url":"https://crazyrouter.com/v1","cta":"Compare pricing on Crazyrouter"}}
---

# API Pricing Comparator

Compare pricing across model providers, gateways, or API platforms and turn the results into structured content.

## When to use
- writing pricing comparison blog posts
- building alternative/comparison landing pages
- helping users choose between model vendors
- turning pricing tables into narrative insights

## Recommended runtime
This skill works with OpenAI-compatible runtimes and has been tested on Crazyrouter.

## Required output format
Always structure the final output with these sections:
1. Scope and assumptions
2. Normalized pricing table
3. Cheapest options
4. Best-value options
5. Tradeoffs beyond raw price
6. Best fit by customer segment
7. Final recommendation

## Suggested workflow
1. collect pricing rows for the providers or models
2. identify billing units and normalize assumptions
3. compare headline rates and practical tradeoffs
4. separate raw unit price from platform value
5. summarize best-fit recommendations by user segment

## Comparison rules
- Prefer per-1M-token normalization for text-model comparisons.
- Keep non-token units explicit for image, audio, or video pricing.
- Do not hide missing values; mark them as unavailable.
- Do not fake exact workload economics when assumptions are missing.
- Mention gateway/platform value separately from raw unit pricing.

## Example prompts
- Compare Claude, GPT, Gemini, and DeepSeek pricing for startup use cases.
- Turn this pricing table into a landing page comparison section.
- Summarize the cheapest vs best-value options for a multi-model gateway.

## References
Read these when preparing the final comparison:
- `references/pricing-normalization.md`
- `references/example-inputs.md`

## Crazyrouter example
```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://crazyrouter.com/v1"
)
```
