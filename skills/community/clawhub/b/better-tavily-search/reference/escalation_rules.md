# Escalation Rules

This reference describes how to escalate Tavily usage without turning every task into an expensive, high-context retrieval workflow.

## The Main Rule

Escalate in **quality**, not just in **quantity**.

Do not solve weak retrieval by blindly asking for more results.
Prefer:
1. better query
2. better profile
3. better filters
4. better depth
5. targeted extraction

## Decision Tree

### Case A: Top results are mostly irrelevant
Likely problem:
- query is under-specified
- wrong profile
- missing entity name

Do this:
- rewrite the query
- add a better entity or quoted phrase
- switch `topic` or add a domain filter

Do not do this first:
- jump to 10+ results
- add raw content immediately

### Case B: Results are relevant but shallow
Likely problem:
- snippets are too short
- source selection is okay, but granularity is weak

Do this:
- raise `search_depth` to `fast` or `advanced`
- set `chunks_per_source=2..3`
- optionally move to `extract` on top URLs

### Case C: The right site appears, but not the right page
Likely problem:
- site navigation issue, not a search issue

Do this:
- add `include_domains`
- tighten the query to the page concept
- if still noisy, use `map` on the site, then `extract`

### Case D: The question is clearly recent
Likely problem:
- retrieval is mixing timeless and recent sources

Do this:
- switch to `topic=news`
- add `time_range`
- use exact dates when the time window is known

### Case E: The query is precise and you still need more detail
Likely problem:
- source identification succeeded, but snippets are not enough

Do this:
- `extract` the top 1–3 URLs
- pass the same question as `query` for chunk reranking

### Case F: Official or primary sources matter
Likely problem:
- the open web is returning commentary instead of primary documentation

Do this:
- use `include_domains`
- keep results small
- prefer corroboration from one or two strong domains over many weak domains

## When to Use `auto_parameters`

Use `auto_parameters` only when:
- the task is semantically tricky and profile choice is uncertain
- one explicit attempt already failed
- you want Tavily to recover from an ambiguous first-pass setup

Do not use it as the first move for routine searches.

## When to Use `include_raw_content`

Use `include_raw_content` only when:
- extraction is not available
- the search result itself is the final retrieval step
- you need a quick one-shot payload from a very small number of results

Otherwise prefer `extract`.

## When to Stop

Stop when:
- you already have 1–3 strong sources
- the answer can be synthesized from snippets or extracted chunks
- further searching is unlikely to change the conclusion materially

Do not keep searching just because a tool offers more switches.
