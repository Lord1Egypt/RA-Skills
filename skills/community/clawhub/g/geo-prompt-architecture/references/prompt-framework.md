# Prompt Framework

Use this reference when generating a fresh GEO monitoring prompt set.

The core rule is simple:

`do not generate prompts before you know which topics deserve monitoring`

## 1. Inputs to extract first

Before writing prompts, normalize these inputs:

- website
- brand
- business model
- market
- target customer
- user-provided priority topics, if any
- product lines, if any
- competitors
- weak AI surfaces
- optional context: pricing, channels, audience segments, use cases, regions, existing assets, seasonality

If product lines or topics are missing, do not stop. Infer carefully and label the inference.

## 2. Topic-first architecture

Always build a topic map before prompt expansion.

The topic map decides:

- what the monitoring system should care about
- which answer spaces matter most
- which clusters need non-brand discovery coverage
- which clusters need competitor pressure testing
- which clusters need brand-defense monitoring

### Topic sources

Every topic should be tagged as one of:

- `provided`
- `derived-from-product-line`
- `inferred`

### Topic types

Useful topic types:

- product/category
- use-case
- audience/segment
- competitor/alternative
- trust/evaluation
- channel/marketplace
- seasonal/trend

### How to generate topics when the client did not provide them

Infer topics from:

- the website’s core categories
- the business model
- the buyer’s main jobs to be done
- use cases and occasions
- the channel mix
- competitor overlap
- geographic or language focus
- seasonal buying patterns
- weak AI surfaces that need diagnostic coverage

### Recommended topic count

For the default monitoring pack, aim for:

- `5` priority topics
- `50` prompts total
- `10` prompts per topic

If the client needs a lightweight version, you can go smaller.
If the client needs a custom enterprise pack, you can go larger.
But the default operating assumption should be `5 topics / 50 prompts`.

Avoid topic maps that are:

- so broad they become meaningless
- so narrow they just restate one product line
- missing trust, competitor, or channel themes

## 3. Three-layer prompt architecture inside each topic

### Non-brand discovery

Use for new-answer-space coverage.

Best for:

- category discovery
- use-case discovery
- scenario and pain-point prompts
- educational prompts
- topic prompts without the brand

Typical output share in the default 50-prompt pack: `30-32` prompts

### Competitor comparison

Use for competitive visibility.

Best for:

- `brand vs competitor`
- `best alternatives to competitor`
- `which brand is better for [topic or use case]`
- competitor-cluster prompts built around user-provided rivals

Typical output share in the default 50-prompt pack: `12-15` prompts

### Brand defense

Use for narrative control and lower-funnel monitoring.

Best for:

- `is [brand] good quality`
- `is [brand] good for [topic or use case]`
- `should I buy [brand] on Amazon, Walmart, or the official site`
- `does [brand] fit [segment, weather, occasion, or channel need]`
- `[brand] vs [competitor]`

Typical output share in the default 50-prompt pack: `5-8` explicit brand prompts

In most default packs, start with only `1` brand-defense prompt per topic.

Avoid low-value brand navigation prompts unless the user explicitly wants them.

## 4. Funnel mapping

Prompt outputs should use `TOFU / MOFU / BOFU` as the visible funnel labels.

Use this default mapping from the older buyer-journey model:

- `Problem awareness` -> `TOFU`
- `Solution education` -> `TOFU`
- `Category evaluation` -> `MOFU`
- `Brand comparison` -> `MOFU`
- `Purchase decision` -> `BOFU`
- `Use / implementation / expansion` -> `BOFU`

Commercial-intent override:

- if a prompt is explicitly about vendor choice, product specs, supplier qualification, pricing, channels, returns, quality validation, or near-term buying behavior, prefer `BOFU`

Recommended bias by layer:

- non-brand discovery: mostly `TOFU`, with some `MOFU`
- competitor comparison: mostly `MOFU`, with `BOFU` for explicit purchase or procurement questions
- brand defense: mostly `BOFU`, with some `MOFU` when the prompt is still evaluation-led rather than decision-led

## 5. Topic quality rules

Strong topics:

- map to a real user problem, category, occasion, audience, or comparison space
- can produce multiple prompts with distinct monitoring value
- connect to a plausible content or asset strategy
- reveal AI visibility movement over time

Weak topics:

- are just keywords copied from SEO tools
- are too broad to guide prompt writing
- duplicate another topic with tiny wording changes
- have no business or monitoring value

## 6. Prompt quality rules

Strong prompts:

- sound like real questions asked to AI tools
- include useful context
- reveal visibility, preference, or replacement behavior
- map clearly to a topic and business goal

Weak prompts:

- are just keyword fragments
- are generic navigational brand queries
- repeat the same phrasing with tiny edits
- have no monitoring or action value

## 7. Recommended fields

For structured outputs, use:

- prompt
- topic
- topic_source
- topic_type
- layer
- funnel_stage
- category
- product_line
- target_customer
- business_value
- geo_priority
- monitoring_value
- answer_entry_mode
- why_it_matters

Useful `answer_entry_mode` values:

- direct recommendation
- candidate list
- comparison target
- alternative option
- case-study citation
- methodology citation
- review / rating citation

## 8. Priority rules

Prioritize prompts that are:

- commercially meaningful
- likely to change content or asset decisions
- likely to show visibility movement over time
- specific enough to reveal competitive substitution
- aligned to the user’s weak AI surface
- anchored to one of the client’s priority topics or inferred growth topics

## 9. Output order

Recommended output order:

1. business summary
2. topic map
3. topic strategy by layer
4. prompts grouped by topic
5. priority monitoring list
6. optional reverse-optimization notes
