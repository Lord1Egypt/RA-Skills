# Causal Abel Report Guide

Use this guide to make sure a report covers the right substance: how the user's original question maps to graph nodes, what the graph and web work found, and what those findings mean. This is not a rigid output template.

Do not center the report on commands, payloads, script flags, or call mechanics unless the user explicitly asks for reproducible invocation details.

## Report Goal

Every strong report should make these things clear. They do not need to appear as fixed sections or in exactly this wording:

1. What is the user's real causal question?
2. Which graph nodes are being used to represent that question?
3. What did the graph verbs return?
4. What did graph-grounded web evidence clarify about the current mechanism?
5. What did the red-team pass fail to disprove?
6. What pressure test or next-step probe would most change the answer?
7. What do those combined findings mean for the original question?

## Dollar-Value Decision Archetypes

Beyond `direct_graph` and `proxy_routed`, recognize these question archetypes that require specific handling:

- **Survival/replacement** → Route through automation exposure indices, labor demand proxies, skill-premium trends. Never binary — decompose into sub-skills. For open-ended "what survives?", scan 3-5 skill categories and rank by resilience.
- **ROI/worth-it** → Cost-benefit with proxy-measurable upside and opportunity cost. Name non-financial returns (fulfillment, identity) as graph-invisible but decision-relevant.
- **Timing** → Route through pricing cycle proxies, inventory/supply signals, product release cadence. Must include a specific trigger signal.
- **Allocation** → Multi-node portfolio analysis. Concrete ratio with per-slice reasoning. For multi-horizon (education 5yr vs retirement 30yr), split by time horizon. For products Abel can't model directly (insurance), use underlying macro drivers.
- **Regret minimization** → Forward-looking scan across asset classes and sectors by causal momentum strength. Ranked shortlist with confidence levels.
- **Cross-market comparison** → Compare within-market momentum, explicitly name cross-market uncontrollables (currency, regulation, capital controls).
- **Broad macro** → Decompose into 3-5 measurable proxy dimensions first. **Horizon rule:** >3 years → structural trend analysis (web) with graph as validator, not predictor.
- **Graph-sparse** → Before declaring, search for capillary proxies (see Step 3b in SKILL.md). Every human activity has an economic shadow in equity markets. Only declare graph-sparse after capillary search fails. When truly sparse, graph = economic context, web = primary answer.

### Archetype Answer Shapes

Each archetype demands a different answer structure and rendering rule:

| Archetype | Answer structure | Rendering |
|-----------|-----------------|-----------|
| Survival/replacement | Decompose sub-skills, rate automation risk, rank resilience | ticker-free |
| ROI/worth-it | Quantify measurable + name non-measurable + breakeven condition | ticker-free |
| Timing | Specific trigger signal, never "it depends" | ticker-free for life, tickers OK for investment |
| Regret minimization | Ranked shortlist by causal momentum + confidence | tickers OK |
| Allocation | Concrete ratio + per-slice reasoning + rebalance trigger | tickers OK |
| Cross-market | Within-market signals + named uncontrollables | tickers OK for investment, ticker-free for lifestyle |
| Broad macro | Decompose 3-5 dimensions first, synthesize last | ticker-free in synthesis |
| Graph-sparse | Graph = context, web = primary (only after capillary search fails) | ticker-free |

## Two-Layer Rendering Rule

Every report has two layers conceptually. The user sees the verdict layer. Raw evidence details remain internal unless the user explicitly asks for them.

**Default rule:** The verdict layer uses human-readable economic roles, not raw tickers or prediction decimals. Raw node IDs, predictions, graph paths, label-pass notes, and probe transcripts stay out of the normal answer.

**One exception:** When the user's question is explicitly about a ticker or investment asset (e.g., "what drives NVDA," "should I buy BTC"), ticker names are allowed in the verdict because the user expects them. Raw prediction decimals still stay out of the normal answer.

**Verdict layer (the main report):**
- Default: use translated signal names ("AI infrastructure momentum," "cloud computing giants") instead of tickers
- Exception: ticker names permitted when the question is about that specific ticker/asset
- Never: raw prediction decimals (+0.0013) or node IDs (NVDA.price) in the verdict — always translate to directional language
- For life decisions: no exception applies. Read like expert advice, not financial analysis.


## Label Before Narrative

Before writing the verdict layer:

- shortlist the nodes, bridges, or drivers that materially shape the answer
- run `extensions.abel.node_description` on that shortlist
- translate raw anchors into semantic labels before drafting
- rewrite the visible answer using company names, industries, products, or economic roles instead of raw tickers or node ids
- run `scripts/render_guard.py` on the visible layer before finalizing
- do not print rendering scratch work unless the user explicitly asks for trace, debug, or evidence details

Rendering rules:

- Default: translate tickers into semantic labels in the verdict and body
- Explicit ticker exception: if the user explicitly asked about a ticker or named investment asset, you may keep that named ticker in the verdict, but the surrounding mechanism should still be rendered semantically where possible
- Life-decision rule: proxy-routed life decisions stay ticker-free in the visible answer
- Never leave raw node ids such as `NVDA.price` or raw prediction decimals in the verdict layer
- For proxy-routed or broad-macro questions, visible raw tickers are a failed render pass, not a soft preference

## ASDF Experience Standard

Every Abel report must pass four tests: **Authentic, Sharp, Deep, Fun.**

**Authentic** — every claim traceable to a specific probe or source. Tier annotation enforces this. If you can't name how you know it, don't say it. Web grounding requires TWO types of search: (1) "what's happening now" — latest policy decisions, current rates, recent earnings, this week's data (2) "how to" — rules, strategies, frameworks. Both are mandatory. Name specific events, numbers, dates. **Claim-strength honesty:** For life decisions, Abel provides "causal-graph-grounded decision advice" — not "causal proof." Don't imply stronger causal claims than the evidence supports. If L0-only details are exposed because the user explicitly asked for evidence, label them with anti-guarantees: "no statistical test, not reproducible, may vary."

**Sharp** — the verdict is ≤3 sentences. Sentence 1: position. Sentence 2: why (the mechanism, one line). Sentence 3: what to do (action + trigger). If you can't tweet the verdict, it's too long. Everything else goes in the body, not in a default appendix.

**Deep** — at least one insight the user couldn't have gotten from ChatGPT or common sense. The insight must be QUESTION-SPECIFIC — not a repetition of a general graph property (like "blankets are financial" which is true for all nodes). If the blanket finding is the same as last time, dig one layer deeper: what does THIS node's specific blanket composition tell us about THIS question? Deep is not long. Deep = "I didn't know that."

**Fun** — the verdict should make the user want to share it. Self-test after writing: would the user screenshot this and send to a friend? If no, rewrite.

## Story Arc (the source of Fun)

Every report should have a **plot twist** — a moment where the graph overturns the user's intuition. Structure the narrative as:

- **Act 1:** "You'd think..." (L0 common sense — what everyone assumes)
- **Act 2:** "But the graph says..." (L0.5 structural discovery — the twist)
- **Act 3:** "So the real answer is..." (fusion verdict — new understanding + action)

When no twist exists (graph confirms L0), the adversarial search is Act 2: "We looked for reasons you're wrong — here's what we found (or didn't)."

## Interleaving Rule (graph × web × action)

NEVER separate graph findings and web evidence into two blocks. Every graph insight must be immediately followed by its web grounding — supporting or contradicting — in the same breath. Then land the action.

**Bad:**
```
图谱发现：网安被内容企业驱动...（一大段图谱）
正在发生的事：网安岗位 480 万空缺...（一大段 web）
```

**Good:**
```
网安被内容/SaaS 企业的数字资产保护需求驱动（图谱 Layer 2: Disney + Dropbox 在安全龙头的因果链上游）— 印证这一点的是，41% 的网安岗位现在要求 AI/ML 技能（StationX 2026），CrowdStrike 正在往 AI 安全方向 pivot。图谱的结构指向和市场的实际招聘在同一个方向。所以：学网安 + AI 交叉是当前最抗替代的组合。
```

Every paragraph: graph says → web confirms/challenges → so you should. One flow, not three blocks.

L0.5 is the center of the experience. L1/L2 amplify its credibility. L0 web search provides the texture. But the story arc comes from the graph's structural surprise.

## Output Rules

- **Verdict: ≤3 sentences.** Position + mechanism + action. Everything else is body.
- **Graph voice first, web voice second.** The verdict must lead with what the GRAPH uniquely discovered — not with web facts anyone could find. Web facts support the graph insight, not the other way around. If your verdict could be written without the graph, you haven't used Abel. The graph's contribution must be FELT in the first sentence.
- **Insight → action translation is mandatory.** Every insight must end with a specific recommendation, timing trigger, or threshold. If an insight does not change action, cut it from the normal answer.
- The full report body follows the verdict for those who want depth. Keep it structured but concise.
- Analysis process (which probes ran, what surprised what) stays internal unless the user explicitly asks for trace, debug, or evidence details.
- Only collapse to a short answer when the user explicitly asks for brevity or the task is genuinely trivial.
- Explicit markdown section headings are often helpful, but they are optional.
- Natural longform prose is acceptable as long as the needed content is covered clearly.
- Match the user's language. Technical terms in English, explanations in user's language.
- For proxy-routed questions, state clearly: "Abel reads economic environment, not personal circumstances."
- **L2-First Rule:** Graph findings (L2) take precedence over web narratives (L0). Exception: graph-sparse dimensions where capillary search is exhausted — web is primary for those, mark as lower confidence.
- Separate `graph_fact`, `searched_mechanism`, and `inference`. Don't blur graph and web into one narrative.
- Include challenge section (untested assumption, counter-evidence, weakest link) for non-trivial analyses.
- Keep command/OAuth/script details out of the main report.
- Do not emit headings such as `Render map`, `Observations`, `Parents`, `Connectivity`, or `Provenance` in the normal answer.

Even in compact form, the report should still cover these contract fields in substance:

- `intent_read`
- `graph_mapping`
- `surface_used`
- `finding`
- `web_evidence`
- `challenge`
- `meaning`
- `caveat`
- `provenance`

## Coverage Areas

### 1. Original Question

State the user's real cause-effect question in one or two lines.

Optional but recommended field:

- `intent_read`: what the user is actually trying to obtain from this analysis

Prompt for the generator:

```text
What is the user actually trying to understand, decide, or explain?
```

### 2. Question To Graph Mapping

Explain how the original question maps onto graph nodes.

Required fields:

- `question_focus`: the real-world issue the user cares about
- `core_nodes`: the main graph nodes used for analysis
- `supporting_nodes`: bridge or comparison nodes if needed
- `mapping_type`: `direct_graph` or `proxy_routed`
- `mapping_reason`: why these nodes are relevant to the question

Compact contract name:

- `graph_mapping`: a concise rendering of the mapping fields above

Generator guidance:

- If the graph contains direct nodes for the topic, say that this is a direct graph read.
- If the graph does not contain direct nodes for the topic, explain which proxy dimensions are being used and why.
- When proxy routing is used, describe nodes by economic role first and ticker second.
- For life decisions (career, housing, education, entrepreneurship), explain the proxy bridge explicitly: the graph has financial/macro signals, not "should I quit my job" nodes. Name the specific proxy dimensions and why they carry signal for the user's real question. Example: "Your career-switch question maps to: tech labor demand (proxied via HIRING_INDEX), startup funding health (proxied via VC_DEAL_FLOW), and opportunity cost of staying (proxied via BIG_TECH_COMP_INDEX). These don't model your personal situation directly — they model the economic environment your decision lives in."

### 3. Verb Findings

You do not need a literal per-verb section every time, but the write-up should make clear:

- `result`: what the graph returned
- `meaning`: what that result contributes to the original question

When search or external evidence is part of the same section, add:

- `graph_fact`: the structural fact from CAP
- `searched_mechanism`: the mechanism evidence gathered outside the graph
- `inference`: the conclusion that combines both without blurring them

Before or around the findings, include:

- `surface_used`: the minimum sufficient capability set selected for the user's intent
- `finding`: a compact statement of the most decision-relevant graph result when a short answer is needed
- `provenance`: a compact note on which parts are graph-backed, search-backed, or still inferential

When a verb materially shapes the answer, these are the useful things to render:

#### `neighbors` / `traverse-parents` / `traverse-children`

- `result`: which nearby drivers, children, or local influences appear around the node
- `meaning`: what this says about immediate pressure, exposure, or influence direction

#### `markov_blanket` / `abel-markov-blanket`

- `result`: which surrounding nodes best localize the node's informational neighborhood
- `meaning`: what this says about the node's most relevant local causal context

#### `paths` / `validate-connectivity`

- `result`: whether a connection exists, through which intermediaries, and whether it looks direct or indirect
- `meaning`: what this says about transmission, mediation, or whether the proposed relationship is structurally plausible

#### `extensions.abel.observe_predict_resolved_time`

- `result`: what the resolved-time observational surface currently predicts
- `meaning`: what the current regime suggests, without overstating it as intervention effect

#### `extensions.abel.intervene_time_lag`

- `result`: what changes when the treatment node is stressed and how that stress rolls out across the requested horizon
- `meaning`: what this says about how robust or fragile the current verdict is

### 4. Web-Grounded Evidence

Summarize the focused web evidence gathered after the graph shortlist was clear.

Required fields:

- `search_target`: the edge, node, sector, or proxy dimension being clarified
- `search_result`: the most relevant current fact or mechanism found
- `why_it_matters`: how that evidence changes, confirms, or constrains the graph reading

Guidance:

- Use ordinary web or news search for this phase, not image search.
- Keep each search target narrow and graph-grounded.
- If a searched financial transmission node turned out to be low-signal, say that and explain the cleaner anchor you switched to.
- Do not inflate weak web evidence into a firm mechanism claim.

Compact contract name:

- `web_evidence`: the single most decision-relevant external grounding point

### 5. Challenges

Run a brief red-team pass against the working conclusion.

Required fields:

- `untested_assumption`: the key assumption not directly established by graph or web evidence
- `counter_evidence`: the strongest alternative explanation or contrary signal found
- `weakest_link`: the graph edge, bridge node, or proxy mapping most likely to fail

Guidance:

- Keep this evidence-based and brief.
- For non-trivial proxy-routed decisions, do one falsification-oriented search when search is available.
- If the challenge pass materially weakens the thesis, lower certainty or make the verdict conditional.
- Do not write generic balance language. Name the specific failure mode.

Compact contract name:

- `challenge`: the single most important reason the conclusion could be wrong

### 6. Pressure Test

Use this content by default for non-trivial comparative or high-stakes reads. It does not need to be a literal standalone section if the report flows better another way. Omit it only when no meaningful live intervention surface or stress target exists.

Required fields:

- `stress_target`: the node, bridge, or proxy dimension being stressed
- `stress_outcome`: the node, path, or proxy comparison most affected
- `stress_result`: whether the verdict held, weakened, or flipped

Guidance:

- Prefer one strong pressure test over multiple weak ones.
- Prefer a real graph-lever stress test over a user workflow suggestion.
- If a live intervention is not worth running, name the cleanest fallback graph lever instead of giving a generic execution plan.
- Keep this short and decision-oriented.

### 7. Integrated Interpretation

Synthesize the verb findings back into the original question.

Prompt for the generator:

```text
Given the node mapping, graph findings, web-grounded evidence, and challenge pass, what is the best plain-language answer to the user's original question?
```

Required: **Causal chain statement** — Every non-trivial report must include one explicit mechanism chain in the form: `A → (mechanism) → B → (mechanism) → C`. This is the backbone of the interpretation. The chain should:

- Name the cause, the intermediate transmission, and the outcome
- Label each arrow with the mechanism
- Distinguish direct effects from mediated effects

  **Good chain:** Names cause, intermediate transmission, outcome. Labels each arrow with mechanism. Flags confounders by name.
  **Bad chain:** "X affects Y through various mechanisms." (No mechanism named, no confounder identified.)
- Flag where the chain relies on proxy rather than direct observation

Guidance:

- Do not merely repeat the verb outputs.
- Explain how the structural and effect findings combine.
- Prioritize the user's decision or explanation need over graph-internal jargon.
- If a search loop was used, say which part of the interpretation comes from graph structure versus mechanism evidence.
- If the causal chain has a confounder or fork, name it explicitly rather than treating the path as unconditionally causal.
- End the interpretation with a concrete **"So what"** statement: what the user should do, watch, or reconsider given these findings. If the question is investment-related, name the position implication. If it's a life decision (career, real estate, education, starting a company), name the specific timing signal or condition that should trigger action. If operational, name the lever to pull. If exploratory, name the most valuable next question.

### 8. Boundaries And Caveats

State the limits that materially change interpretation.

Always check for these caveats:

- observational result versus intervention result
- direct graph signal versus proxy-routed signal
- direct path versus indirect path
- preview-only or approximate surface
- missing graph support or weak structural evidence
- searched mechanism that is plausible but not yet structurally re-grounded
- repeated anchor pattern that may still reflect a bridge rather than a true hub
- **life decision gap**: the graph models economic conditions, not personal fit, risk tolerance, relationships, or non-financial values. Always name what the graph cannot see when the question is about a life choice.

Prompt for the generator:

```text
What should the user not over-interpret from these graph findings?
```

Compact contract name:

- `caveat`: the highest-priority limit that changes interpretation


## Quality Check

Before finalizing a report, verify that:

- the original question appears before any graph mechanics
- the user's intent is explicit when ambiguity would otherwise change the result
- each chosen node is explained, not just listed
- the surface used is the smallest honest capability set, not an exhaustive dump
- each verb section has both a result and a meaning
- the web-grounded evidence section explains at least one current mechanism when the task is proxy-routed or current-state dependent
- the challenge section names a concrete way the answer could be wrong instead of generic hedging
- the pressure-test section either sharpens the verdict or gives useful next probes instead of acting like a method dump
- the integrated interpretation answers the user's question directly
- the interpretation includes an explicit causal chain (A → mechanism → B → mechanism → C)
- the interpretation ends with a concrete "So what" — what to do, watch, or reconsider
- for life decisions: the proxy bridge is named explicitly, the personal-vs-economic boundary is stated, and the "So what" gives a timing signal or condition, not just "it depends"
- the question archetype was identified and the answer shape matches it (survival→decompose skills, ROI→breakeven, timing→trigger, allocation→ratio, macro→dimensions, graph-sparse→honest handoff)
- the two-layer rendering rule was followed: verdict layer is ticker-free for life decisions, and raw data stayed internal unless the user explicitly asked for it
- a label pass was done before writing: `node_description` informed the final wording and the visible answer uses company, industry, product, or role labels instead of raw ticker-heavy phrasing
- the visible layer passed `scripts/render_guard.py`; if the question was proxy-routed, no raw ticker survived in the normal answer
- signal aggregation was applied: no individual ticker predictions in the verdict, only directional signals
- each significant claim is annotated with its epistemological tier (L2/L0.5/L0)
- the report ends with an epistemological composition summary
- caveats are strong enough to prevent overclaiming
- provenance is clear whenever search evidence or proxy reasoning materially shapes the answer
