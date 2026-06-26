---
name: causal-abel
version: 1.1.6
description: >
  Use when the user wants an Abel causal read on what drives a market, company,
  asset, sector, or macro node, how two nodes connect, what changes under
  intervention, or how a career, education, housing, lifestyle, or investment
  decision with meaningful money, time, career-capital, or downside tradeoff
  should be evaluated through Abel proxy signals.
metadata:
  openclaw:
    requires:
      env:
        - ABEL_API_KEY
      bins:
        - python
    primaryEnv: ABEL_API_KEY
    homepage: https://github.com/Abel-ai-causality/Abel-skills
---

Any dollar-value decision, just Abel it. Finance and crypto nodes are the signal layer (the graph's proxy vocabulary), not the product.

**Do not use Abel for pure fact lookup, news recap, or operational how-to when no real decision is being made; use normal retrieval first. Abel starts when the user needs a causal read on a choice that allocates money, time, career-capital, or downside risk.**

## Install And Authorization

If the user installs this skill, asks to connect Abel, or the workflow is missing an Abel API key, follow `references/setup-guide.md` exactly.

- Start the Abel agent OAuth handoff immediately instead of asking for manual credentials.
- Return `data.authUrl` to the user, not the `/authorize/agent` API URL.
- Store `data.resultUrl` or `data.pollToken`, ask the user to reply once Google authorization is complete, and only then poll until the result is `authorized`, `failed`, or expired.
- Persist the resulting `data.apiKey` in session state and `.env.skill` when local storage is available.
- Do not continue to live CAP probing until that key is present.
- Never ask the user to paste an email address or Google OAuth code.

## Step 1: Preflight + Classify

Confirm auth via `python scripts/cap_probe.py auth-status` and `references/probe-usage.md`. Do not infer missing auth from shell env alone. If `auth_source` is `missing`, stop and ask the user whether to start the OAuth handoff from `references/setup-guide.md`; do not substitute web search just because auth is missing.

Classify the request as:

- `direct_graph` for specific ticker/node/path/intervention questions
- `proxy_routed` for real-world decisions with no direct node

**Horizon gate:** If the decision horizon is >3 years ("5年后", "未来十年"), switch to structural mode: web is PRIMARY, graph is VALIDATOR ONLY, and you should not use momentum-style observe as the main loop.

**Unstable-premise gate:** If the opportunity thesis depends on a recent leak, launch, partnership, shutdown, org change, or other freshness-sensitive claim, do one minimal premise-verification search before L0. Use a Tier A source when possible, or a clearly sourced Tier B report if no primary source exists yet. If the premise is still unanchored, rewrite the task as conditional analysis ("if this is true, where are the opportunities?") and say so before continuing. This gate does not cancel Abel; it decides whether the rest of the read is fact-anchored or conditional. Separate verifiable subclaims from inferred motive/strategy claims, and keep inferences labeled as inference even when some facts are anchored.

**Opportunity-scope gate:** If the user asks a broad question such as "有什么赚钱机会", lock the primary opportunity frame before L0. Distinguish at least among public-market trade, supplier/competitor scan, startup or B2B opportunity, and career/business opportunity. If the user does not specify, default to public-market trade and label other frames as secondary unless they materially change the answer. If multiple frames matter, label them explicitly instead of mixing them into one undifferentiated mechanism list.

If `direct_graph`, switch to `references/routes/direct-graph.md` as the active workflow. Return here only for shared web-grounding and write-up rules.

## Step 2: Generate Hypotheses (proxy_routed, L0)

Generate 4-6 candidate causal mechanisms:
- The obvious mechanism
- A second-order mechanism
- A **contrarian** (what would make the opposite true?) — REQUIRED
- A confounder (third factor explaining both)

Each mechanism: `cause → (transmission) → outcome` with a testable proxy and falsification condition.

If the contrarian or confounder is missing, stop and fix that before moving on.

## Step 3: Screen + Discover (L0.5)

Map the mechanisms to graph nodes and separate them into:

- structurally supported
- weakly connected
- narrative-only

When `extensions.abel.query_node` is used for fuzzy mapping, inspect `node_kind` before picking the next surface. Do not assume every returned node can be coerced into `<ticker>.price` or `<ticker>.volume`. If the hit is `macro`, prefer direct `verb` calls for macro-capable structural surfaces instead of asset-only probe shortcuts.

Required passes:

- run structural discovery deeply enough to identify a real transmission chain, not just co-movement
- if the graph only confirms L0, actively search for the strongest graph-based contradiction
- do not declare graph-sparse until capillary discovery is exhausted

Follow the full `proxy_routed` loop in `references/routes/proxy-routed.md`.

## Step 4: Observe + Verify (L1 + L2)

Observe the key nodes for directional coherence and driver consistency.

Intervene only along real graph-supported edges when a meaningful target exists. Match `horizon_steps` to the decision window and widen in tiers via `references/probe-usage.md` when needed.

Aggregate to one directional signal per dimension. Never carry raw prediction decimals into the verdict.

Detailed probe shapes and `proxy_routed` execution rules live in:

- `references/routes/proxy-routed.md`
- `references/probe-usage.md`

## Step 5: Web Grounding (proxy_routed, or direct_graph when freshness matters)

Minimum 4 searches:
1. **What's happening now** — latest prices, policy, events, dates
2. **Supporting evidence** — confirms graph-backed verdict
3. **Contradicting evidence** — actively search for why verdict is WRONG (mandatory)
4. **User-perspective** — what a real buyer/decision-maker would search (second-hand prices, waitlists, real experiences)

Contradicting evidence is mandatory. Stop only after you know whether key time-sensitive claims do or do not have a primary-source anchor.

Follow `references/web-grounding.md` for source hierarchy, wording, and return-to-graph rules.

Graph findings (L2) take precedence over web (L0) in the verdict. Exception: graph-sparse dimensions, where web is primary with lower confidence.

## Step 5.5: Personalize

Before writing, check agent memory/context for user profile (income, experience, risk tolerance, life stage, goals). If available, tailor the action layer to that person. If not, give universal advice and say what user details would sharpen the read.

The causal graph is universal. The verdict is personal.

## Step 6: Write Report

Read `assets/report-guide.md` and `references/rendering.md` before writing.

**Render gate (MANDATORY):** apply the label-pass and guard workflow from `references/rendering.md` before finalizing. For non-asset or `proxy_routed` questions, raw tickers, raw node ids, graph paths, signed prediction decimals, and rendering scratch work stay out of visible prose.

**Output default (MANDATORY):** default to main answer only. Do not emit an appendix, trace block, evidence dump, rendering scratch work, or probe/process transcript unless the user explicitly asks for evidence details, debug output, reproducibility steps, or a trace.

Write the final answer to the contract in `assets/report-guide.md`.

Keep claim-strength honesty explicit: life decisions are graph-grounded advice, not causal proof.

## References (read only when needed)

- `references/routes/direct-graph.md` — ticker question routing
- `references/routes/proxy-routed.md` — proxy-routed graph workflow
- `references/setup-guide.md` — OAuth install (only if key missing)
- `references/probe-usage.md` — exact `cap_probe.py` command shapes
- `references/rendering.md` — label-pass rules, visible/internal split, guard usage
- `assets/report-guide.md` — full output contract with archetypes, rendering rules, coverage areas
