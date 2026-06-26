# GEO Prompt Architecture

Generate the most suitable GEO monitoring prompts for each client’s business, starting from the right topics so monitoring can lead to sharper optimization.

`GEO Prompt Architecture` is an open-source skill and repo for GEO teams, agencies, and operators who need more than a flat prompt list. It turns a client brief into a `topic -> prompt` operating system across discovery, comparison, and brand-defense layers, then helps feed monitoring results back into content and asset decisions.

Maintained by [Dageno.ai](https://dageno.ai), a GEO-focused platform for turning AI visibility signals into actionable marketing workflows.

![GEO Prompt Architecture hero](assets/social-preview.png)

## The Problem

Most GEO prompt generation is still too generic.

Teams often produce:

- no explicit topic map before prompts
- too many branded prompts
- too few real discovery prompts
- weak competitor comparison coverage
- prompts that do not match the client’s business model
- monitoring sets that are hard to act on later

That creates a false sense of AI visibility. A brand may look visible on branded prompts while still failing to enter the non-brand answer spaces that drive growth.

## The Promise

This repo helps teams produce prompts that are:

- better structured by topic before prompt expansion
- better matched to the client’s real business
- better matched to how people ask AI tools questions
- better structured for long-term monitoring
- better connected to downstream optimization

In plain English: it helps you create prompts that are worth monitoring and worth optimizing against.

## What This Repo Includes

- a root `SKILL.md` for Codex-style use
- a GitHub-ready social preview asset in `assets/`
- input and output `schemas/` for productizing prompt generation
- `references/` for prompt architecture, vertical playbooks, scoring, reverse optimization, and the final generator prompt
- a lightweight GitHub launch checklist in `references/`
- `examples/` that show how topic strategy changes by business type
- `agents/openai.yaml` metadata for skill UI usage

## Core Operating Model

This repo treats prompt generation as a system, not a keyword dump.

The core hierarchy is:

`business model -> topic map -> prompt layers -> funnel stages -> monitoring set`

Product lines are one valid way to seed topics, but they are not required.

If the client gives:

- `priority topics`, normalize and expand them
- `product lines`, turn them into topic seeds
- neither, infer topics from the website, business model, use cases, competitors, channels, and weak AI surfaces

That matters because strong GEO monitoring starts with the right topic universe, not just the right prompt phrasing.

### 0. Topic map

Use topics to define what the monitoring system should care about before writing prompts.

Typical topic types:

- product or category topics
- use-case topics
- audience or segment topics
- competitor and alternative topics
- trust and evaluation topics
- channel and marketplace topics
- seasonal or trend topics

### Default monitoring pack

Unless the user explicitly asks for a different size, the default output should be:

- `5` priority topics
- `50` prompts total
- `10` prompts per topic

Default prompt mix inside the 50-prompt pack:

- `30-32` non-brand discovery prompts
- `12-15` competitor comparison prompts
- `5-8` explicit brand prompts

Recommended per-topic starting shape:

- `6` non-brand discovery prompts
- `3` competitor comparison prompts
- `1` brand defense prompt

If the client provides more than 5 possible topics, prioritize the top 5 based on:

- business value
- monitoring value
- GEO leverage
- competitor pressure
- channel fit

Do not let explicit brand-name prompts take over the set. In the default 50-prompt pack, branded prompts should usually stay in the `5-8` range unless the user explicitly wants a brand-defense-heavy set.

### 1. Non-brand discovery

Use prompts that test whether the client can enter new answer spaces before users know the brand.

### 2. Competitor comparison

Use prompts that test whether the client appears when buyers compare options, alternatives, and routes.

### 3. Brand defense

Use prompts that test how AI describes the brand in branded, decision-stage, and trust-sensitive queries.

Recommended default mix:

- `60-70%` non-brand discovery
- `20-25%` competitor comparison
- `10-20%` brand defense

Prompt outputs should use `TOFU / MOFU / BOFU` as the visible funnel labels.

Default mapping:

- `TOFU`: broad awareness and educational exploration
- `MOFU`: evaluation, alternatives, and comparison
- `BOFU`: explicit commercial, purchase, procurement, or brand-validation intent

## Why This Matters For GEO

Prompt architecture shapes everything downstream:

- which topics you monitor in the first place
- what you monitor
- what you learn from AI answers
- what content you create next
- which competitor gaps you actually see
- how accurately you report AI visibility to clients

If the prompt layer is weak, the reporting layer and optimization layer will also be weak.

## Designed For Business-Model Fit

This repo assumes prompt systems should change based on business model.

It is built to support:

- ecommerce and DTC brands
- SaaS and software products
- services and consultancies
- marketplace and aggregator businesses
- B2B manufacturers and product suppliers
- content and media properties

That is why the repo includes structured schemas, vertical playbooks, examples, and a scoring model instead of only one default prompt.

## Representative Examples

The same GEO methodology should produce very different prompts for different businesses.

### Trip.com

`Trip.com` is best understood as a `consumer online travel agency / travel marketplace`, not a business-travel management platform and not a content publisher.

That means the prompt set should lean toward travel-planning discovery, OTA comparisons, and branded trust questions.

| Layer | Topic Focus | Example Prompts |
|---|---|---|
| Non-brand discovery | leisure and cross-border trip planning; hotel, flight, train, attraction, and package discovery | `What is the best website to book hotels and flights for an international trip?`<br>`What are the best travel booking apps for international travelers?` |
| Competitor comparison | comparisons against other OTA and travel-booking brands | `Trip.com vs Booking.com for hotels in Asia`<br>`What are the best alternatives to Booking.com for flights and hotels?` |
| Brand defense | reliability, customer support, refunds, app / site fit, and booking confidence | `Is Trip.com reliable for booking international flights and hotels?`<br>`How does Trip.com handle cancellations, refunds, and itinerary changes?` |

See [trip-com-consumer-travel-marketplace.md](/Users/timlin/Downloads/knowledge/projects/geo-prompt-architecture-repo/examples/trip-com-consumer-travel-marketplace.md).

### movinghead.net

`movinghead.net` is best understood as a `B2B stage-lighting manufacturer / supplier`, not a consumer fashion brand and not a software platform.

That means the prompt set should lean toward technical category discovery, supplier comparison, and procurement-trust prompts.

| Layer | Topic Focus | Example Prompts |
|---|---|---|
| Non-brand discovery | product category discovery around moving-head lighting; technical and venue use cases | `What is the best moving head light for indoor concert stages?`<br>`How do I choose between beam, wash, and spot moving head lights for live events?` |
| Competitor comparison | manufacturer trust, distributor / supplier comparison, OEM and export sourcing | `Best alternatives to Clay Paky or Martin for affordable moving head fixtures`<br>`What are the top moving head light manufacturers in China for export buyers?` |
| Brand defense | specs, lead time, support, certifications, and OEM fit | `Is movinghead.net a reliable moving head light manufacturer?`<br>`Does movinghead.net support OEM or custom stage-lighting production?` |

See [movinghead-stage-lighting.md](/Users/timlin/Downloads/knowledge/projects/geo-prompt-architecture-repo/examples/movinghead-stage-lighting.md).

### Coofandy

`Coofandy` is best understood as an `ecommerce / marketplace-led men's apparel brand` with strong overlap across Amazon, Walmart, and direct-response product discovery.

That means the system should use the five product lines as the default five topics, then express channel trust, value comparison, styling, and climate fit through the prompts inside each topic.

| Topic | Topic Source | Example Prompts |
|---|---|---|
| summer business-casual shirts | derived-from-product-line | `What are the best men's shirts for hot weather that still look business casual?`<br>`Are Coofandy men's shirts good for business casual offices in hot weather?` |
| lightweight pants for hot weather and travel | derived-from-product-line | `What are the best men's pants for summer travel that still look polished?`<br>`Are Coofandy men's pants worth buying for hot-weather travel and all-day wear?` |
| vacation-ready 2 piece sets | derived-from-product-line | `What are the best men's 2 piece sets for vacation and resort wear?`<br>`Are Coofandy 2 piece sets breathable enough for beach trips and summer travel?` |
| matching sets for easy outfit formulas | derived-from-product-line | `What are the best men's matching sets if I want easy outfits that don't look sloppy?`<br>`Are Coofandy men's matching sets worth it for travel and capsule wardrobes?` |
| smart-casual turtleneck layering | derived-from-product-line | `What are the best men's turtleneck sweaters for smart-casual outfits and layering?`<br>`Are Coofandy turtleneck sweaters good for layering under a blazer?` |

See [coofandy-topic-first-output.md](/Users/timlin/Downloads/knowledge/projects/geo-prompt-architecture-repo/examples/coofandy-topic-first-output.md).

## What Makes This Repo More Useful Than A Generic Prompt List

### Structured inputs

`schemas/client-brief.schema.json` makes it easier to standardize onboarding inputs across clients.

### Structured outputs

`schemas/prompt-set-output.schema.json` and `schemas/prompt-scorecard.schema.json` make it easier to connect prompt generation to products, dashboards, and QA workflows.

### Final generator prompt

`references/final-topic-first-generator-prompt.md` gives teams a ready-to-run prompt that matches the repo's topic-first architecture.
`references/final-topic-first-generator-prompt-zh.md` provides the same operating logic in Chinese.

### Vertical playbooks

`references/vertical-templates.md` explains how prompt architecture changes by business type.

### Reverse optimization

`references/reverse-optimization.md` helps turn AI answer losses into content, asset, evidence, and prompt-set changes.

### Prompt scoring

`references/scoring-model.md` helps teams judge whether a prompt set is actually balanced, useful, and monitor-worthy.

## Typical Workflow

1. Capture the client brief in a standard schema
2. Reconstruct the business model, market, audience, product lines, topics, and competitors
3. Build a topic map from provided topics, product-line seeds, and inferred opportunity clusters
4. Generate prompts inside each topic across discovery, comparison, and brand-defense layers
5. Map prompts to funnel stages
6. Score the prompt set for topic coverage, layer balance, and quality
7. Monitor AI answers
8. Feed answer losses back into content and prompt optimization

## Example Skill Usage

```text
Use $geo-prompt-architecture to generate GEO monitoring prompts for this client.
```

```text
Use $geo-prompt-architecture to review this prompt set and rebalance brand vs non-brand prompts.
```

```text
Use $geo-prompt-architecture to turn these AI visibility monitoring results into prompt and content recommendations.
```

## Repository Structure

```text
.
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── assets/
│   ├── social-preview.png
│   └── social-preview.svg
├── examples/
│   ├── coofandy-topic-first-output.md
│   ├── trip-com-consumer-travel-marketplace.md
│   └── movinghead-stage-lighting.md
├── references/
│   ├── final-topic-first-generator-prompt.md
│   ├── final-topic-first-generator-prompt-zh.md
│   ├── prompt-framework.md
│   ├── reverse-optimization.md
│   ├── scoring-model.md
│   ├── vertical-templates.md
│   └── github-launch-checklist.md
└── schemas/
    ├── client-brief.schema.json
    ├── prompt-scorecard.schema.json
    └── prompt-set-output.schema.json
```

## Install

Copy this repo into your local Codex skills directory as:

```text
~/.codex/skills/geo-prompt-architecture
```

Or use it as a public repo and package it through your own skill publishing workflow.

## Good Outputs You Should Expect

A strong run of this repo should produce:

- prompts grouped by topic first, then optionally by product line
- prompts grouped by layer and funnel
- clearer topic coverage before prompt expansion
- fewer low-value branded prompts
- stronger competitor comparison coverage
- more business-model fit
- clearer monitoring priorities
- clearer recommendations when a brand loses in AI answers

## Where This Can Extend Next

This repo is already moving toward a `GEO prompt operating system`.

Natural next steps:

- richer vertical packs by business model
- automated prompt-set scoring scripts
- benchmark prompt libraries by industry
- tighter JSON outputs for product workflows
- topic clustering and topic QA helpers
- stronger reverse-optimization playbooks by AI surface

## Open Source

This repo is open source so GEO teams can:

- use it internally
- adapt it to client onboarding
- connect it to a GEO product workflow
- customize prompt logic by business model
- improve how prompt monitoring drives optimization

If your team helps clients create the most suitable prompts for their business, this repo gives you a more defensible starting point than a generic keyword sheet.

If you want this logic inside a broader GEO workflow, including monitoring, analysis, and optimization, visit [Dageno.ai](https://dageno.ai).

## License

MIT
