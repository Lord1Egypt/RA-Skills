# Scoring Model

Use this reference when the user wants to score, benchmark, or QA a prompt set.

The goal is not to reward bigger prompt lists. The goal is to reward prompt systems that are balanced, topic-aware, monitor-worthy, and useful for optimization.

## 1. Score Dimensions

Use a 100-point model by default.

### Topic coverage: 20 points

Check whether the set has a clear topic map before prompt expansion.

Score up when:

- the set covers the client’s real product, use-case, trust, competitor, and channel themes
- topics are distinct and meaningful
- inferred topics are labeled clearly

Score down when:

- there is no topic map
- the set does not converge into a clear top 5 topics for the default pack
- one product line dominates the whole set
- trust, comparison, or channel topics are missing
- topics duplicate each other

### Layer balance: 15 points

Check whether the set roughly follows the intended mix:

- `30-32` non-brand discovery prompts in a 50-prompt pack
- `12-15` competitor comparison prompts in a 50-prompt pack
- `5-8` explicit brand prompts in a 50-prompt pack

Score down when:

- brand prompts dominate
- there are no comparison prompts
- the set is almost entirely upper-funnel or lower-funnel

### Funnel coverage: 15 points

Check whether the set has healthy `TOFU / MOFU / BOFU` coverage.

Use this mapping logic:

- `TOFU`: awareness and education
- `MOFU`: evaluation and comparison
- `BOFU`: explicit commercial, purchase, procurement, or brand-validation intent

Score down when:

- everything collapses into BOFU
- there is no TOFU discovery coverage
- there is no MOFU comparison or evaluation coverage
- BOFU prompts are too weak to support real decision-stage monitoring

### Business-model fit: 20 points

Check whether the prompts fit the client’s real business model and conversion path.

Score down when:

- ecommerce phrasing is used for SaaS
- content-site prompts are used for industrial products
- service prompts are used for marketplaces
- the topic map ignores channel or marketplace reality

### Prompt quality: 15 points

Check whether prompts:

- sound like real AI questions
- avoid keyword-fragment phrasing
- avoid repetitive near-duplicates
- include useful context when needed

### Monitoring value: 10 points

Check whether prompts can reveal something useful over time.

Strong monitoring prompts:

- expose competitive substitution
- reveal whether the brand enters new answer spaces
- show branded trust or decision-stage shifts
- show topic-level visibility change, not just one-off phrasing wins

### Actionability: 5 points

Check whether poor performance on a prompt would point to a real optimization action.

Examples:

- add a topic-specific category page
- create a comparison page
- improve product-line entity language
- strengthen reviews or evidence
- expand or prune a topic cluster

## 2. Suggested Output

Use these score buckets:

- `90-100`: strong, benchmark-worthy set
- `75-89`: usable but needs selective tuning
- `60-74`: weak in one or two structural areas
- `<60`: not reliable enough for serious GEO monitoring

## 3. Common Reasons A Set Scores Poorly

- no topic map
- no clear `5 topics / 50 prompts` structure in the default pack
- too many branded prompts
- no real discovery prompts
- weak or missing competitor set
- no meaningful topical grouping
- funnel collapse into one stage
- low monitoring value
- prompts that cannot map to any page or asset strategy

## 4. Suggested Output Fields

Use `schemas/prompt-scorecard.schema.json` when the user wants a structured scorecard.

Recommended fields:

- overall_score
- topic_coverage_score
- layer_balance_score
- funnel_coverage_score
- business_model_fit_score
- prompt_quality_score
- monitoring_value_score
- actionability_score
- top_findings
- keep_doing
- fix_next

## 5. Important Rule

Do not confuse `high search volume` with `high GEO monitoring value`.

A strong GEO prompt set should help the team understand:

- which topics matter most
- where the brand can grow
- where the brand is losing comparisons
- where the brand narrative is weak
- what to build next
