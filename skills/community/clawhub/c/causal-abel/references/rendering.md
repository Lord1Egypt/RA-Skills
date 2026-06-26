# Rendering Rules

Use this file after analysis is complete and before writing the final report.

The goal is simple: visible prose should read like an economic explanation, not like internal graph scratch work.

Do a label pass on shortlisted anchors, draft from semantic labels, and keep any rendering scratch work internal. Do not print it unless the user explicitly asks for trace, debug, or evidence details.

## When This Rule Is Hard

Treat rendering as a hard gate for:

- `proxy_routed`
- `Broad macro`
- life-decision questions
- any non-asset question where graph nodes are only proxy anchors

For these cases, raw tickers in the visible layer are not a style issue. They mean the report is not ready.

## Label Pass

Before writing visible prose, translate shortlisted anchors into semantic labels:

```text
XOM.price -> integrated oil majors
LMT.price -> prime missile contractors
DAL.price -> commercial airlines
ECCX.price -> CLO credit-risk appetite
```

Rules:

- Use the graph anchor only to think.
- Use the semantic label to write.
- Keep raw anchors in internal notes only unless the user explicitly asks for evidence details.
- Keep the label pass lightweight. Do not turn it into a named artifact in the normal answer.

## Visible Layer vs Internal Notes

Visible layer:

- verdict
- body paragraphs
- challenge section
- action / implication section

Internal notes stay internal by default:
- raw graph identifiers
- raw market symbols used only as proxy anchors
- graph paths and verb payload details
- numeric prediction outputs
- temporary analysis or labeling notes

Only expose these details when the user explicitly asks for trace, evidence details, debug output, or reproducibility.

Do not let the normal answer read like a tool trace, analysis transcript, or protocol dump.


## Allowed Exceptions

Ticker names are allowed in visible prose only when the user's question is explicitly about that named asset, for example:

- "what drives NVDA"
- "should I buy BTC"
- "what happens to XOM if..."

Even then:

- keep supporting mechanisms semantic where possible
- keep raw node ids and prediction decimals out of normal visible prose

## Guard Workflow

1. Shortlist final nodes and bridges.
2. Run `extensions.abel.node_description` on that shortlist.
3. Do a label pass from raw anchors to semantic labels.
4. Draft the visible answer from semantic labels only.
5. Run `scripts/render_guard.py` on the visible draft.
6. If it fails, rewrite and re-run.

## Guard Usage

Example:

```bash
python scripts/render_guard.py \
  --mode proxy_routed \
  --text-file /tmp/visible.txt \
  --forbid-token XOM \
  --forbid-token LMT \
  --forbid-token DAL \
  --forbid-token ECCX
```

What the guard checks:

- raw node ids like `NVDA.price`
- signed prediction decimals like `-0.0013`
- explicit forbidden raw tickers from your shortlist

## Fast Self-Check

Before finalizing, ask:

- Could a reader understand the mechanism without seeing a ticker?
- Does the visible layer sound like market/economic explanation rather than debug output?
- Are all raw graph identifiers confined to internal notes unless the user explicitly asked for them?
- If this is proxy-routed, would a screenshot still make sense to someone who never saw the graph?
