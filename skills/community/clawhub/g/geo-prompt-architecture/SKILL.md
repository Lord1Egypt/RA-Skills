---
name: geo-prompt-architecture
description: Use when the user wants to generate, structure, score, or audit GEO monitoring prompts for a client. Trigger when building topic-first prompt sets from a website, brand, market, customer, product lines or inferred topics, and competitors; when balancing non-brand, comparison, and brand-defense prompts; or when turning AI visibility monitoring results into prompt and content optimization actions.
---

# GEO Prompt Architecture

Build GEO prompt systems that fit the client’s real business, not generic keyword lists.

## Overview

Use this skill to generate and audit AI visibility monitoring prompts for GEO programs. It turns a client brief into a `topic -> prompt` architecture across non-brand discovery, competitor comparison, and brand defense, then helps translate monitoring results into concrete optimization actions.

When the work needs structured product inputs or outputs, use the JSON schemas in `schemas/`.
When the client model is unclear or highly verticalized, use the examples in `examples/` and the playbooks in `references/`.

## Best For

- GEO software teams onboarding new clients
- GEO agencies building prompt sets at scale
- operators who need better prompt coverage by topic, product line, and funnel stage
- teams that want to rebalance prompt libraries away from brand-heavy bias
- teams that want monitoring prompts tied to later content and asset optimization

## Start With

```text
Use $geo-prompt-architecture to generate GEO monitoring prompts for this client.
```

```text
Use $geo-prompt-architecture to review this prompt set and rebalance brand vs non-brand prompts.
```

```text
Use $geo-prompt-architecture to turn these monitoring results into prompt and content recommendations.
```

## External Access And Minimum Credentials

This skill can work from a pasted brief, screenshots, exports, or a website URL.

- no private credentials are required for basic prompt generation or review
- live browsing is helpful when the client website, topics, product lines, or competitor overlap must be validated
- do not assume access to analytics, Search Console, CRM, AI monitoring dashboards, or private docs unless explicitly provided

## Core Model

Always frame GEO prompts as a `topic-first` system:

1. `Topic map`
   Decide which problem spaces, categories, use cases, trust questions, competitor clusters, channels, and seasonal themes deserve monitoring.
2. `Non-brand discovery`
   Users do not know the brand yet. These prompts measure whether the brand can enter new answer spaces.
3. `Competitor comparison`
   Users are comparing brands, alternatives, or solution routes. These prompts measure competitive visibility.
4. `Brand defense`
   Users already know the brand and are validating fit, quality, pricing, sizing, shipping, returns, or worth. These prompts measure narrative control and decision-stage performance.

Topic sources can be:

- user-provided priority topics
- product lines turned into topic seeds
- inferred topics generated from the website, business model, use cases, competitors, channels, and weak AI surfaces

Default pack size:

- `5` topics
- `50` prompts total
- `10` prompts per topic

Default pack mix:

- `30-32` non-brand discovery prompts
- `12-15` competitor comparison prompts
- `5-8` explicit brand prompts

Recommended per-topic starting shape:

- `6` non-brand discovery prompts
- `3` competitor comparison prompts
- `1` brand defense prompt

Default target mix:

- `60-70%` non-brand discovery
- `20-25%` competitor comparison
- `10-20%` brand defense

Do not let brand prompts dominate unless the user explicitly asks for a brand-defense-only set.

## Workflow

### 1. Reconstruct the client model

Before generating prompts, identify:

- business model
- market and language
- target customer
- user-provided topics, if any
- core product lines, if any
- conversion path
- key competitors
- weak AI surfaces, if provided

Useful business-model labels:

- SaaS / software
- ecommerce / DTC
- services / consultancy
- marketplace / aggregator
- manufacturer / supplier
- content / media

If inputs are incomplete, infer carefully and label the inference.

If the user wants a standard onboarding shape, use [schemas/client-brief.schema.json](schemas/client-brief.schema.json).

If the business model is ambiguous, read [references/vertical-templates.md](references/vertical-templates.md) and compare against the sample cases in:

- [examples/coofandy-topic-first-output.md](examples/coofandy-topic-first-output.md)
- [examples/trip-com-consumer-travel-marketplace.md](examples/trip-com-consumer-travel-marketplace.md)
- [examples/movinghead-stage-lighting.md](examples/movinghead-stage-lighting.md)

### 2. Build the topic map

Do not jump straight into prompts.

First, build a topic map that explains what the monitoring system should cover.

Priority order:

1. normalize user-provided topics
2. turn product lines into topic seeds
3. infer missing topics from:
   - use cases
   - audience segments
   - competitor overlap
   - trust and evaluation questions
   - channels and marketplaces
   - seasonality and trend patterns

Useful topic types:

- product/category
- use-case
- audience/segment
- competitor/alternative
- trust/evaluation
- channel/marketplace
- seasonal/trend

Every output should make it clear whether a topic is:

- `provided`
- `derived-from-product-line`
- `inferred`

If the system identifies more than 5 valid topics, choose the top 5 by:

- business value
- monitoring value
- GEO leverage
- competitor pressure
- channel fit

### 3. Map the funnel

Prompt outputs should use the marketing-funnel labels your product shows:

- `TOFU`
- `MOFU`
- `BOFU`

Use this default mapping from the older buyer-journey model:

- `Problem awareness` -> `TOFU`
- `Solution education` -> `TOFU`
- `Category evaluation` -> `MOFU`
- `Brand comparison` -> `MOFU`
- `Purchase decision` -> `BOFU`
- `Use / implementation / expansion` -> `BOFU`

Commercial-intent override:

- if a prompt is clearly procurement-led, product-spec specific, supplier/vendor selection oriented, or near-term purchase oriented, prefer `BOFU` even if it would otherwise look like category evaluation or comparison

Read [references/prompt-framework.md](references/prompt-framework.md) when you need the full generation framework.

### 4. Generate prompt sets by topic

Generate prompts inside each topic. Keep the layers separate:

- non-brand discovery prompts
- competitor comparison prompts
- brand defense prompts

If product lines exist, use them as one grouping dimension, but do not treat them as mandatory. Some clients need prompt sets grouped by:

- topic
- business problem
- audience segment
- marketplace channel
- competitor cluster

Prompt rules:

- write natural-language user questions, not SEO fragments
- prefer prompts that fit AI conversations and recommendation flows
- include scenarios, constraints, audiences, budgets, regions, or channels when useful
- avoid low-value navigational brand variants
- keep explicit brand-name prompts sparse in the default 50-prompt pack

### 5. Add GEO judgment, not just prompts

For each prompt, include enough structure to make the set operational. Default fields:

- prompt
- topic
- topic_source
- topic_type
- layer
- funnel stage (`TOFU` / `MOFU` / `BOFU`)
- category
- product line
- target customer
- business value
- GEO priority
- monitoring value
- likely answer-entry mode
- why it matters

If the user wants a compact output, keep the fields but shorten the explanations.

If the user wants a product-ready response shape, use:

- [schemas/prompt-set-output.schema.json](schemas/prompt-set-output.schema.json)
- [schemas/prompt-scorecard.schema.json](schemas/prompt-scorecard.schema.json)

### 6. Audit and rewrite existing prompt sets

When reviewing an existing prompt list, do not regenerate everything by default. For each prompt:

- keep
- optimize
- downgrade
- delete
- replace

Common failure modes:

- no topic map before prompt generation
- too many topics with too few prompts per topic
- too many brand prompts
- no comparison prompts
- no true non-brand discovery prompts
- off-funnel or synthetic phrasing
- prompts that fit search engines better than AI answers
- prompts that mismatch the client’s real product line or market
- prompts that cluster around one topic while ignoring the real topic surface

### 7. Reverse-optimize from monitoring results

When the user brings AI monitoring results, use them to improve both content and the prompt library.

Track at least:

- was the brand mentioned?
- how was it mentioned?
- which brands replaced it?
- what source types were cited?
- what loss reason best explains the miss?

Then propose:

- content actions
- page / asset actions
- evidence / entity actions
- prompt-set changes

Read [references/reverse-optimization.md](references/reverse-optimization.md) when you need the loss-reason model or the reverse-optimization loop.
Read [references/scoring-model.md](references/scoring-model.md) when the user wants prompt-set QA, scorecards, or benchmark-style review.

## Output Patterns

Default output order:

1. client model summary
2. topic map
3. prompt strategy by layer
4. prompt set by topic
5. priority prompts
6. optional reverse-optimization actions

When auditing, prefer tables like:

| Original | Action | Final | Reason |
|---|---|---|---|
| Prompt A | Keep | Prompt A | Fits the topic, product line, and funnel |
| Prompt B | Optimize | Better Prompt B | Original is too generic or too brand-heavy |
| Prompt C | Delete | — | Low monitoring value |

## Guardrails

- Do not treat prompt generation as generic keyword research.
- Do not skip topic generation just because the client did not provide topics.
- Do not over-index on brand terms.
- Do not collapse every prompt into bottom-funnel buying language.
- Do not invent product lines, topics, channels, or competitors without labeling the inference.
- Do not assume every prompt should become an article; some should map to category pages, comparison pages, FAQs, reviews, or marketplace listings.
- When the user asks for monitoring prompts, bias toward prompts that can reveal visibility movement over time.
- Do not apply an ecommerce prompt pattern to a marketplace, SaaS, or industrial manufacturer without checking business-model fit first.
