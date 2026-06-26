---
name: aeo-keyword-selector
description: select a single aeo blog keyword in question format from a business topic, with architecture-first sitemap-plus-page-intent checks to avoid cannibalization, using semrush as a validation layer for dense clusters. use when an agent needs to choose a keyword autonomously before writing a new blog article, especially for saas, ecommerce, or service brands. this skill is for keyword qualification and page-targeting decisions, not article drafting. it should be used before any writing skill whenever the task starts from a business topic, product area, service line, or content pillar and the agent must decide whether to create a new url.
---

# AEO Keyword Selector

## Overview

Use this skill before article creation. The goal is to return exactly one question-format keyword that is safe to target with a new article, or decide that no new article should be created yet.

This skill is opinionated:
- semrush is the primary validation layer unless the topic area is broad and undercovered
- sitemap discovery plus fetched page intent is the cannibalization check
- zero-volume keywords are allowed only when they are clearly ai-native, logically askable, and non-cannibalizing
- the output is a single decision, not a brainstorm list

## Dense Cluster Decision Policy

For dense topic clusters such as HomeLock, evaluate existing site coverage before proposing any new keyword.

Required decision order:
1. review existing URLs and classify current page intent
2. determine whether the requested topic is already substantially covered
3. if multiple adjacent queries map to an existing page, return `expand-existing`
4. if no clear gap exists, return `no-go`
5. return `new-url` only when there is one clearly distinct unanswered question that is materially separate from existing page intent

Non-negotiable rules:
- do not brainstorm adjacent variants
- do not rotate phrasing across runs
- do not treat slight wording changes as a new opportunity
- for the same business topic plus the same site evidence, the decision must be identical across runs

Priority order:
- architecture integrity
- deterministic outcomes
- anti-cannibalization
- only then keyword expansion

## Core Output Contract

Return exactly one final decision block with these fields:
- `selected_keyword`
- `business_topic`
- `best_existing_url_match`
- `cannibalization_risk`
- `decision`
- `reasoning`

Rules:
- `selected_keyword` must be a single question-format query, but for `expand-existing` it is only a section-level absorbed query, not a standalone article target
- `decision` must be one of: `new-url`, `expand-existing`, `no-go`
- if `decision` is not `new-url`, do not hand a keyword into a writing workflow
- if `decision` is `expand-existing`, `selected_keyword` may name the query being absorbed, but it must not be treated as a net-new article target and must be explicitly framed as content for the existing page
- if `decision` is `no-go`, set `selected_keyword` to an empty string

## Workflow

### Step 1: Validate the starting point

Expected input is a business topic, not a finished keyword list.

Examples:
- `homeowner enablement platform`
- `documenting for disaster`
- `homelock`
- `truevalue index`
- `proprtax`

If the user gives a keyword instead of a business topic, translate it into the broader topic cluster first.

For DomiDocs work, consult `references/domidocs-profile.md`.
For other companies later, swap or supplement that reference with a different company profile.

### Step 2: Check architecture before keyword expansion

For dense topic clusters, do not begin with open-ended keyword discovery.

First:
- review existing site coverage from the sitemap
- identify the closest existing urls for the business topic
- infer the intent each existing page already owns
- decide whether the topic is already substantially covered

Only use semrush after that review, and only to validate or sharpen the decision.

Use semrush as a validation layer, not an ideation engine, when:
- the cluster is dense
- multiple adjacent phrasings could map to the same page
- the topic already has obvious site coverage

For non-dense or genuinely open topic areas, semrush may still be used earlier for candidate discovery.

Do not explore multiple adjacent keyword variants just because semrush shows them.
Do not let semrush volume create a false case for a new URL where the existing architecture already has a strong owner page.

### Step 3: Apply the ai-native exception carefully

A zero-volume keyword may still qualify when all three conditions are true:
1. it is a natural language question a real person would plausibly ask in chatgpt, gemini, perplexity, or google ai overviews
2. it is a logical derivative of the business topic or nearby semrush-supported query cluster
3. it does not cannibalize an existing url after sitemap and page-intent review

If any one of those fails, do not use the zero-volume keyword.

Browser SERP inspection is allowed as a supporting check for:
- people also ask questions
- ai overview-style phrasing
- long-tail language patterns
- crowded serps where semrush trails real-world query behavior

Do not let browser SERP inspection override architecture review or create a false case for a new URL.

### Step 4: Parse the sitemap

Use the site sitemap as the discovery layer for existing coverage.

For DomiDocs, the current sitemap is listed in `references/domidocs-profile.md`.
Use `scripts/parse_sitemap.py` when helpful to flatten sitemap indexes into a clean url list.

From the sitemap, shortlist the top 3 to 5 urls most likely to overlap with the candidate keyword using:
- slug similarity
- title similarity
- obvious entity match
- obvious product/topic match

Do not make a cannibalization decision from sitemap alone.

### Step 5: Fetch and compare page intent

For each shortlisted url, fetch the page and inspect at minimum:
- title tag or visible page title
- h1
- intro / first definition block
- main headings
- overall page purpose

The question to answer is not “is this related?”
The question is:
`would a new url targeting this keyword compete with this existing url for the same primary ranking intent?`

Use `references/verdict-rubric.md` for the forced decision standard.

### Step 5b: Resolve canonical owner page deterministically

If multiple existing URLs could absorb the query, choose a single canonical owner page before making the final decision.

Use these tie-break rules in order:
1. prefer the primary product or feature page over FAQ or support pages when the query is about core product intent
2. treat definitional, mechanism, monitoring, and “how it works” queries as core product intent
3. use the FAQ page as the owner only when the query is clearly an edge-case clarification, support-style objection, or narrow question already better housed in FAQ format
4. if both pages are plausible and no rule clearly overrides, default to the main product page

For HomeLock, default canonical owner priority is:
- `https://domidocs.com/homelock/`
- then `https://domidocs.com/home-lock-faq/` only for clearly FAQ-native queries

Do not switch owner pages across runs for the same query unless the site evidence materially changes.

### Step 6: Make the decision

Choose exactly one:

#### `new-url`
Use only when:
- the keyword is strong enough to justify a standalone article
- the intent is clear
- no fetched existing url already owns the same primary ranking intent
- the keyword is in question format or can be cleanly rewritten into one

#### `expand-existing`
Use when:
- the best keyword belongs inside an existing page
- a new article would compete with an existing url
- the opportunity is real but should be handled as a section, faq, or content refresh instead of a new post

#### `no-go`
Use when:
- the candidate set is weak
- the likely keyword is too cannibalistic
- intent is too muddy
- the only available angles are better handled elsewhere

Never invent a weak `new-url` just to keep the pipeline moving.

## Decision Standards

### Cannibalization meaning

In this skill, cannibalization means:
- two urls would try to rank for the same primary ranking intent or keyword cluster
- the new url would dilute the existing url's ability to rank for that intent

It does not mean simple topical relatedness.

### Confidence bias

Bias toward protecting site architecture over producing more content.

If uncertain between `new-url` and `expand-existing`, prefer `expand-existing`.
If uncertain between `expand-existing` and `no-go`, prefer `no-go` unless the gap is clearly actionable.

Return only the final response block and nothing else.
Do not include preambles, progress notes, reasoning traces, tool narration, status updates, conversational filler, or any text before or after the block.
Do not say that you are checking, reviewing, using a skill, or gathering evidence.
Perform all analysis silently.

Do not include citations, citation placeholders, contentReference markers, footnotes, or source annotations in the final block.

For HomeLock dense-cluster prevention, detection, monitoring, title theft, deed fraud, and adjacent mechanism queries:
- default the canonical owner page to https://domidocs.com/homelock/
- do not select the FAQ as `best_existing_url_match` when the query is fundamentally product-intent or mechanism-intent
- use the FAQ only as supporting evidence for `expand-existing`, not as the canonical owner page
- if both the FAQ and product page are relevant, the product page wins

## Final Response Format

Use this exact structure:

```text
selected_keyword: <question-format query; for `expand-existing`, this is a section-level absorbed query; for `no-go`, empty>
business_topic: <topic>
best_existing_url_match: <url or none>
cannibalization_risk: low | medium | high
decision: new-url | expand-existing | no-go
reasoning: <3-6 sentences explaining why>
```

Additional rules:
- no brainstorm lists
- no “other keyword ideas” section
- no hedging language like “maybe” or “could be promising”
- no article outline generation here
- no draft writing here

## Resources

- `references/domidocs-profile.md` — current DomiDocs business-topic and sitemap profile
- `references/semrush-playbook.md` — semrush-first research guidance and ai-native exception handling
- `references/verdict-rubric.md` — exact rubric for `new-url`, `expand-existing`, and `no-go`
- `scripts/parse_sitemap.py` — recursive sitemap parser for sitemap index and urlset xml files
