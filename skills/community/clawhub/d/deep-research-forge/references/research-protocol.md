# Research Protocol

Deep Research Forge turns an ambiguous topic into a decision-ready research asset.

## 0. Route And Depth

First choose the smallest route and output that can answer the user:

- orientation before full research when the object or decision is unclear.
- competitive snapshot when the user mainly compares choices.
- decision brief when the user needs action.
- research update when old conclusions may be stale.
- research asset pack when reuse matters more than polished prose.
- parallel research sprint when the user asks for multi-agent execution or independent lanes clearly improve coverage.

Use `research-methodology-atlas.md` and `methodology-routing-index.md` before choosing an output artifact. Use `output-routing-index.md` for artifact selection, `dynamic-output-composer.md` for output block composition, `source-strategy.md` for evidence depth, and `multi-agent-protocol.md` when work can be split without duplicating effort.

## 0.25 Method Stack Selection

Before choosing a template, select a method stack:

```text
Primary method:
Supporting methods:
Methods explicitly not used:
Why this stack fits:
Output blocks to compose:
```

Methods decide what analysis is needed. Templates are base containers. If the selected methods do not fit an existing full template, compose a dynamic output from `assets/output-blocks/`.

## 0.5 Parallel Execution Check

Before collecting sources, decide:

```text
Parallel mode:
Reason:
Roles needed:
Shared definitions:
Merge risk:
```

If parallel mode is active, the lead-integrator owns the final answer. Specialist lanes provide evidence and deltas; they do not each write separate mini reports unless the requested artifact is an asset pack.

## 1. Frame The Question

Before research, rewrite the user request as:

```text
Research object:
Object type:
Decision or curiosity:
Time boundary:
Geographic / market boundary:
Primary output:
Important uncertainty:
```

If the user does not give a boundary, choose a sensible default and state it.

## 2. Source Discipline

Prefer sources in this order:

1. Official primary material: company blog, docs, filings, release notes, repository, paper, speech transcript.
2. Direct public records: SEC filings, court records, patent records, standards documents, official statistics.
3. Original reporting from reputable media.
4. User evidence: GitHub issues, reviews, forums, Reddit, Zhihu, X posts, app store reviews.
5. Aggregators and summaries, only as pointers to better sources.

Never treat repeated secondary reports as independent confirmation when they all trace to one source.

Match the source mix to object type. A product study needs release notes and user signals; a concept lineage needs papers, early usage, and competing definitions; a decision brief needs evidence that can affect the verdict.

For volatile facts, state the evidence window and verify against current sources before making the claim.

## 3. Evidence Ledger

Track important claims as entries:

- claim
- source
- source type
- date published
- date accessed
- reliability
- status
- implication

Use `confirmed_fact` for hard facts, `reported_claim` for claims, `user_signal` for community evidence, `inference` for your own reasoning, and `gap` for missing or conflicting evidence.

## 4. Three-Axis Analysis

### Time Axis

Answer:

- Where did it come from?
- What problem, belief, or constraint created it?
- Which people or institutions mattered early?
- What were the stage changes?
- Which decisions became path dependencies?
- Which moments could have gone another way?

### Snapshot Axis

Answer:

- What is the current category?
- Who are the direct competitors, indirect competitors, and substitutes?
- What job does the user hire each option to do?
- Where is the object stronger, weaker, cheaper, riskier, or more trusted?
- What do users praise and complain about?

### Mechanism Axis

Answer:

- Which old choices explain today's advantage?
- Which old choices explain today's constraint?
- Which outside forces could change the next stage?
- What would prove the current judgment wrong?

## 5. Output Selection

Choose the smallest artifact that answers the user's actual need:

- `research-brief`: fast but sourced orientation.
- `deep-research-report`: full narrative and competitive analysis.
- `competitive-map`: comparison-focused output.
- `concept-lineage-timeline`: development history with schools, disputes, mechanism shifts, and current usage drift.
- `decision-brief`: action recommendation with confidence and risks.
- `research-asset-pack`: evidence ledger plus reusable notes.
- `parallel-research-plan`: task split and merge contract for multi-agent execution.

When the user asks for a decision, apply `decision-rubric.md` before writing the final recommendation.

## 6. Writing Standard

Write like a rigorous human analyst:

- Lead with the answer.
- Use concrete details before abstraction.
- Separate fact, inference, and judgment.
- Mark uncertainty plainly.
- Avoid corporate filler and empty trend language.
- Prefer a readable story over a lifeless chronology.
- Include the strongest opposing evidence when it changes confidence.
- Name what would make the conclusion wrong.
- When parallel execution was used, summarize role contributions and merge decisions without exposing unnecessary process chatter.

Do not hide weak evidence behind confident prose.
