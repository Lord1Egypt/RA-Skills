---
name: content-generator
description: "Commerce content generator. Input a product brief, evidence, audience, and channel; output Xiaohongshu notes, Douyin scripts, ad/email/listing variants, and a claims checklist. Evidence-aware: does not invent unsupported claims and flags missing proof."
---
# Content Generator

Create platform-ready commerce content without inventing unsupported claims.

## Workflow

1. Capture the product brief:
   - product name, category, price or price range
   - target audience and use scenario
   - benefits, differentiators, proof points, limitations
   - platform, tone, length, conversion goal
   - forbidden claims or regulated categories
2. If the brief is thin, ask for the missing business-critical facts. If the user wants speed, continue with explicit assumptions and mark `待补充证据`.
3. Select the right output pack:
   - Xiaohongshu: personal discovery note, practical list, comparison note
   - Douyin: short-video hook, spoken script, captions, CTA
   - Live selling: opening, demo flow, objections, close
   - Moments: concise social recommendation
   - Zhihu: rational evaluation and purchase advice
   - Marketplace: title, bullets, detail-page sections
   - Ads: A/B angle variants and CTA options
4. Draft using only user-provided facts or clearly labeled assumptions.
5. Run a quality pass before final output: evidence, platform fit, claim safety, specificity, and next data needed.

## Deterministic Pack Generator

When the user wants a structured first draft, batch variants, or repeatable output, use:

```bash
node scripts/generate_content_pack.js --input product.json --format markdown
```

The input JSON can include:

```json
{
  "name": "HydraGlow Cream",
  "category": "美妆",
  "price": "299",
  "audience": "commuters with dry skin",
  "scenario": "winter office skincare",
  "benefits": ["light texture", "long-lasting moisture"],
  "evidence": ["user test: 8-hour office day"],
  "limitations": ["not a medical treatment"],
  "tone": "calm and trustworthy",
  "platforms": ["xiaohongshu", "douyin", "marketplace"]
}
```

Read `references/platform-playbook.md` when platform details matter. Read `references/quality-checklist.md` before publishing, reviewing risky copy, or handling health, finance, legal, children, food, supplements, or high-priced products.

## Output Contract

For user-facing answers, prefer this shape:

- `Brief`: product, audience, goal, assumptions.
- `Content`: platform-specific drafts.
- `Quality Notes`: unsupported claims, risky phrases, missing evidence.
- `Next Iteration`: what data would improve conversion or trust.

Do not claim guaranteed outcomes, medical effects, investment returns, legal compliance, official endorsement, scarcity, or comparative superiority unless the user supplied reliable evidence.
