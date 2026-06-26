# Direct Graph Route

Read this file only when the question is already about a graph node, path, neighborhood, or intervention.

## Use This Route For

- what is driving `X`
- why did `X` move
- which nodes matter around `X`
- is there a path from `X` to `Y`
- what happens if `X` changes
- whether `Y` is or is not in `X`'s drivers, parents, children, or path set

## What This Route Sets

This route sets the default first move, the preferred structural fallback, and the compact loop to use for the rest of the read.

## First Move

Pick the first move from the user's question shape:

- direct node with executable market anchor and a current directional question -> `extensions.abel.observe_predict_resolved_time`
- driver -> `graph.neighbors(scope=parents)` or `traverse.parents`
- downstream -> `graph.neighbors(scope=children)` or `traverse.children`
- transmission -> `graph.paths`
- ambiguity after one structural pass -> `graph.markov_blanket`

For driver or "why did it move" questions, prefer a quick observational read on the target node before the deeper structural pass when the node is executable. Default to a paired `price` + `volume` observational pass when the name is liquid, the mechanism may include liquidity/crowding, or surface coverage is still unknown.

For broad driver questions on liquid names, default graph stack: anchor ticker → `observe-dual` on price and volume → pick the surviving or jointly useful anchor set → inspect parents on the strongest anchor → use the other anchor to confirm whether the mechanism is informational, liquidity-led, or both → summarize into driver families (e.g., "macro proxies", "sector transmission", "liquidity channels").

## Structural Loop

Then use this compact loop:

1. If an observational read was taken, use it to decide which structural question matters most.
2. Read the returned structure.
3. State the open causal question.
4. Choose the next best tool: another graph move or a web move.
5. Stop when the user-facing mechanism is already strong enough.

Default bias:

- stay in graph unless the current unknown is clearly about dated evidence, current catalysts, or real-world mechanism
- for `recently`, `latest`, or `why now` questions, one baseline web search is allowed earlier, then come back to graph if structure is still unresolved
- if another call is unlikely to change the user-facing conclusion, stop instead of expanding the loop

For literal driver-membership or parent-list questions, stop as soon as the graph fact is clear enough to answer faithfully. Do not force a web move just to make the answer sound more intuitive.

## Pressure Test

- After the mechanism is coherent enough to stress:
- default pressure test -> `extensions.abel.intervene_time_lag`

For non-trivial direct-node or comparative reads, one `extensions.abel.intervene_time_lag` pressure test is the default before finalizing. Do not start with a pressure test for a driver question or run it before you can name the mechanism being stressed.

Before `extensions.abel.intervene_time_lag`, check whether the active mechanism shows up on `price`, `volume`, or both. If `price` is sparse or the story looks liquidity-led, probe `volume` in the first pass instead of treating it as a late fallback.

## Web Grounding Rule

Web grounding is required only when the answer depends on:

- current catalysts
- earnings or guidance
- policy or regulation
- product or adoption changes
- a real-world mechanism that the graph alone cannot explain

Web grounding is usually not needed for:

- direct driver lists
- parent or child membership checks
- path existence checks
- questions whose literal answer is already contained in graph output

Search the named companies, sectors, or mechanisms from `node_description`, not raw tickers, and then return to the loop.

If the graph answer and the intuitive real-world story do not line up, preserve both:

- first say what the graph returned
- then explain the parent or bridge through the security's own attributes when possible, such as sector, industry, liquidity profile, beta/risk appetite, credit sensitivity, or cross-asset role
- only then add any web-backed explanation or caveat

## Output Rule

- For any non-trivial direct-graph read, render the visible answer as a structured report, not as plain prose.
- Use `../../assets/report-guide.md` to make sure the report covers the right content. Natural longform prose is acceptable if it still covers the same contract fields.
- Main answer uses company names, industries, products, or roles by default.
- If the user's question is explicitly about a ticker or named investment asset, the verdict may keep that ticker or asset name, but still avoid raw node ids and prediction decimals.
- Include the pressure-test result or, if no live intervention was run, the cleanest next-step probe.
- If a repeated bridge node looks like microcap or crypto-heavy transmission noise, summarize it as noise unless external evidence says it matters.
- If the user asked for a literal graph fact, make that fact the first sentence, not the caveat.
