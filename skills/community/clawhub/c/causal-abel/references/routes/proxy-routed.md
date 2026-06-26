# Proxy-Routed Route

Read this file only after `SKILL.md` has already fixed:

- the request is `proxy_routed`
- auth is available
- the decision horizon is not in structural-only mode
- L0 hypotheses already exist

This file is the active workflow for `proxy_routed` reads.

## Step 3: Screen + Discover (L0.5)

### 3a. Structural screening

Map mechanisms to graph nodes (manual -> `query_node` -> capillary discovery). After `query_node`, inspect `node_kind` before choosing the next verb.

- `asset` -> keep the current observe / neighbors / paths / intervene flow
- `macro` -> use the canonical macro node id directly for `node_description` and any macro-capable structural surface; for `graph.paths` and similar checks, prefer direct `verb` calls instead of asset-only probe shortcuts that normalize to `<ticker>.price|volume`
- if the next surface is still asset-only, say so explicitly and choose a proxy route intentionally instead of silently coercing the macro node

For each structurally executable mapping:

- `graph.paths` between cause and outcome proxy
- Rank: dist <= 2 = strong, 3-4 = plausible, no path = narrative-only

Structural connection does not equal causal transmission. Many dist=2 paths are shared macro exposure, not intervention-ready mechanism.

### 3b. Capillary discovery (when observe returns 503)

1. `graph.neighbors` on the failed node -> observe neighbors
2. If no observable neighbors -> `query_node` for the economic function
3. If still nothing -> use world knowledge (what companies' revenue is this asset?)
4. All three fail -> declare sparse for this dimension

Do not declare graph-sparse before this sequence is exhausted.

### 3c. Graph-structural bias check

- Cause and outcome in the same blanket -> possible confounding
- Path runs opposite to hypothesis -> check reverse causation
- Proposed proxy is a mega-cap hub -> may be bridge noise

### 3d. Deep structural reasoning

This is where Abel's moat lives. Do not stop at a generic blanket.

Check `meta.methods` first. On the key outcome node:

- **Layer 1 blanket:** `graph.markov_blanket` to identify the immediate controlling neighborhood
- **Layer 2 blanket (REQUIRED):** run `graph.markov_blanket` on the 2 most interesting Layer 1 nodes
- **Layer 3:** if Layer 2 reveals divergence, follow the most surprising Layer 2 node one more level

Layer 1 often gives generic financial context. Layer 2 is where the question-specific mechanism usually appears. Layer 3 is for the non-obvious causal chain worth surfacing.

Also fire:

- `validate_connectivity` on the whole chain
- `discover_consensus` / `discover_deconsensus` across mechanisms
- `discover_fragility` for single points of failure

### 3e. Graph-initiated discovery

Ask: "Graph, what do YOU see that L0 did not propose?" Run `discover_consensus` with `direction="in"` on the outcome. New upstream nodes are graph-generated mechanisms.

### 3f. Surprise check + revision

Compare graph results against L0 hypotheses. If graph contradicts or extends them, revise L0 in one sentence. Max 2 rounds.

If the graph only confirms L0, actively search for graph evidence against the strongest conviction. If a contradiction appears, that contradiction is the deep insight.

## Step 4: Observe + Verify (L1 + L2)

### 4a. L1 Observe

Run `observe_predict_resolved_time` on the key nodes.

- Driver cross-check: are observe's top drivers consistent with the working mechanism?
- Multi-node coherence: does the chain move in the expected direction?

### 4b. L2 Intervene

Intervene only along real graph-supported edges, not hand-waved industry links.

From the structural pass, identify blanket parents of the outcome. Intervene on the most relevant blanket parent and measure the outcome.

- Report effect size, transmission speed, and breadth
- Match `horizon_steps` to the user's decision window
- If the first intervention is inconclusive, widen in tiers using `references/probe-usage.md`
- If no meaningful target exists, skip and say why

### 4c. Signal aggregation

Aggregate observations into one directional signal per dimension. Do not carry raw prediction decimals into the verdict layer.

## Stop Rules

- Stop when mechanisms are already decision-grade and another graph move is unlikely to change the visible conclusion
- Stop and mark a dimension graph-sparse only after capillary discovery fails
- Stop and red-team your own read when the graph only confirms the obvious story

## See Also

- `../../SKILL.md` for the shared dispatcher and hard gates
- `../probe-usage.md` for exact probe shapes and horizon handling
- `../web-grounding.md` for graph-grounded search
- `../../assets/report-guide.md` for output contract
- `../rendering.md` for label-pass and guard workflow
