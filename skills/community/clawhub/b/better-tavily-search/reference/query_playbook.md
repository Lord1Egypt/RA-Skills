# Query Playbook

This reference explains how the model should plan Tavily queries.

## Philosophy

Do not treat Tavily like a chatbot.
Treat it like a retrieval system that responds best to compact, high-signal queries plus well-chosen retrieval parameters.

The model is responsible for:
- identifying the true information need
- choosing a profile
- choosing whether the task is broad, recent, official, exact, or regional
- deciding whether a second pass is necessary

The search layer is responsible for:
- executing those decisions predictably
- returning evidence in a stable format

## Query Shapes

### Discovery query
Use when the user wants broad orientation or source discovery.

Examples:
- `OpenClaw skills documentation`
- `martingale posterior copula paper`
- `BU data science MS curriculum official`

Characteristics:
- short
- high-signal nouns
- no extra explanation

### Precision query
Use when one narrow page or phrase matters.

Examples:
- `"chunks_per_source" Tavily extract`
- `"metadata.openclaw" OpenClaw skills`
- `"Bill of Digital Worker’s Rights"`

Characteristics:
- quoted key phrase
- named entity
- often paired with `exact_match=true` or `advanced`

### Official query
Use when the likely best answer comes from primary documentation.

Examples:
- `OpenClaw skills docs`
- `SEC 10-K NVIDIA fiscal 2026`
- `CDC measles symptoms`

Characteristics:
- may include `official` or `docs`
- often paired with `include_domains`

### Recency query
Use when time matters.

Examples:
- `OpenAI board changes March 2026`
- `Boston weather this week`
- `ECB rate decision March 2026`

Characteristics:
- includes explicit date terms or recent-event framing
- often paired with `topic=news` and `time_range`

### Site-navigation query
Use when the real task is locating a page inside a site.

Examples:
- `Python task group docs`
- `OpenClaw creating skills`
- `Tavily extract endpoint`

Characteristics:
- often paired with `include_domains`
- if still noisy, switch to `map -> extract`

## Rewrite Rules

### Rule 1: remove filler
Bad:
- `Please search the web and find me a trustworthy explanation of what the OpenClaw skills system is and summarize it carefully`

Better:
- `OpenClaw skills documentation`

### Rule 2: split multi-goal questions
Bad:
- `Compare Tavily search depth modes, explain exact_match, and also find pricing and rate limits`

Better as separate searches:
- `Tavily search depth modes`
- `Tavily exact_match`
- `Tavily pricing rate limits`

### Rule 3: name the entity directly
Bad:
- `that office docs thing`

Better:
- `OpenClaw skills documentation`

### Rule 4: add time only when it helps
Bad:
- `March 2026 Python asyncio docs`

Better:
- `Python asyncio task group docs`

Good use of time:
- `Federal Reserve statement March 2026`

### Rule 5: use quotes for exact text, titles, flags, or error strings
Examples:
- `"search_depth" Tavily`
- `"TAVILY_API_KEY" OpenClaw`
- `"openclaw" "requires" bins env`

### Rule 6: prefer domain filters over overstuffed queries
Instead of:
- `OpenClaw skills docs official site docs.openclaw.ai only`

Prefer:
- query: `OpenClaw skills`
- plus `include_domains=docs.openclaw.ai`

## When to Rewrite Before Escalating Depth

Rewrite first when:
- top results are topically related but too broad
- the right entity is missing from the query
- the query contains too much conversational filler
- one query is trying to answer several subproblems

Increase depth first when:
- the query is already precise
- results are relevant but too shallow
- you need better chunk selection from each source

## Recommended First-Pass Defaults

- one clear query
- `max_results=3..5`
- `search_depth=basic`
- no raw content
- no answer unless explicitly useful

## Query Checklist

Before running a search, ask:
1. What is the real information target?
2. Does time matter?
3. Does the source type matter?
4. Would domain filtering help?
5. Is this one query or multiple subqueries?
6. Do I need links, snippets, or extracted content?
