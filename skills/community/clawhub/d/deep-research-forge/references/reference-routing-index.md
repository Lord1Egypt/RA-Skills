# Reference Routing Index

Use only the references needed for the current route.

## Token Budget Guide

Each route lists an estimated token load for its required references. Use this to decide whether to load all files at once or selectively.

| Load level | Estimated tokens | Strategy |
| --- | --- | --- |
| Light | < 8k | Safe to load all listed files. |
| Medium | 8k–20k | Load core files first; load assets on demand. |
| Heavy | > 20k | Load routing index + protocol first; fetch other references as the method stack requires. |

If the context window is tight, prioritize in this order: routing index → research-protocol → methodology atlas → source-strategy → quality-gates → everything else.

For any route that produces a polished report, brief, executive summary, or research update, load `report-expression-gate.md` after the route's evidence and methodology work is complete. It is a final expression pass, not a substitute for evidence or mechanism repair.

## `research-orientation` — Load: Medium (~8k)

Use when the user has a broad topic but no clear research question.

Read:

- `research-protocol.md`
- `research-methodology-atlas.md`
- `methodology-routing-index.md`
- `dynamic-output-composer.md`
- `source-strategy.md`
- `output-routing-index.md`
- `quality-gates.md`

> If parallel execution may be needed, also load `multi-agent-protocol.md` (+~4k tokens).

Output:

- research question
- scope boundary
- recommended output shape
- evidence plan

## `evidence-first-deep-dive` — Load: Medium (~12k)

Use when the user asks for a full deep research pass.

Read:

- `research-protocol.md`
- `research-methodology-atlas.md`
- `methodology-routing-index.md`
- `dynamic-output-composer.md`
- `source-strategy.md`
- `evidence-ledger.schema.json`
- `output-routing-index.md`
- `quality-gates.md`

Assets:

- `assets/output-blocks/`
- `assets/research-brief-template.md`
- `assets/deep-research-report-template.md`
- `assets/evidence-ledger-template.json`
- `assets/research-asset-pack-template.md`

> If parallel execution may be needed, also load `multi-agent-protocol.md` (+~4k tokens) and `assets/parallel-research-plan-template.md`.

## `competitive-snapshot` — Load: Light (~8k)

Use when the main question is competition, substitutes, alternatives, or ecosystem position.

Read:

- `research-protocol.md`
- `research-methodology-atlas.md`
- `methodology-routing-index.md`
- `dynamic-output-composer.md`
- `source-strategy.md`
- `output-routing-index.md`
- `quality-gates.md`

Assets:

- `assets/competitive-map-template.md`

## `decision-brief` — Load: Light (~9k)

Use when the user wants an action recommendation: buy, learn, invest, copy, adopt, avoid, wait, or monitor.

Read:

- `research-protocol.md`
- `research-methodology-atlas.md`
- `methodology-routing-index.md`
- `dynamic-output-composer.md`
- `source-strategy.md`
- `decision-rubric.md`
- `output-routing-index.md`
- `quality-gates.md`

Assets:

- `assets/decision-brief-template.md`

## `concept-lineage` — Load: Medium (~10k)

Use when the object is a concept, technical paradigm, theory, discourse, or cultural phenomenon.

Read:

- `research-protocol.md`
- `research-methodology-atlas.md`
- `methodology-routing-index.md`
- `dynamic-output-composer.md`
- `source-strategy.md`
- `output-routing-index.md`
- `quality-gates.md`

Assets:

- `assets/output-blocks/`
- `assets/concept-lineage-timeline-template.md`

Focus:

- origin and naming
- early disputes
- competing definitions
- adoption waves
- method / mechanism shifts
- data, compute, algorithm, product, institution, and governance inflection points
- adjacent concepts
- current usage drift

## `research-update` — Load: Light (~8k)

Use when an existing report or older analysis needs revision.

Read:

- `research-methodology-atlas.md`
- `methodology-routing-index.md`
- `dynamic-output-composer.md`
- `source-strategy.md`
- `quality-gates.md`
- `evidence-ledger.schema.json`
- `output-routing-index.md`

Output:

- what changed
- what judgment changed
- what judgment stayed stable
- what still needs monitoring

## `research-asset-pack` — Load: Medium (~12k)

Use when the user wants reusable notes, a source pack, an evidence ledger, or material for later writing / delegation.

Read:

- `research-protocol.md`
- `research-methodology-atlas.md`
- `methodology-routing-index.md`
- `dynamic-output-composer.md`
- `source-strategy.md`
- `evidence-ledger.schema.json`
- `output-routing-index.md`
- `quality-gates.md`

Assets:

- `assets/output-blocks/`
- `assets/research-asset-pack-template.md`
- `assets/evidence-ledger-template.json`
- `assets/agent-dispatch-cards.md`

## `parallel-research-sprint` — Load: Heavy (~20k)

Use when the user explicitly requests multi-agent / parallel research or when independent lanes materially improve source coverage, contradiction handling, or speed.

Read:

- `research-methodology-atlas.md`
- `methodology-routing-index.md`
- `dynamic-output-composer.md`
- `multi-agent-protocol.md`
- `research-protocol.md`
- `source-strategy.md`
- `evidence-ledger.schema.json`
- `quality-gates.md`

Assets:

- `assets/parallel-research-plan-template.md`
- `assets/agent-dispatch-cards.md`
- `assets/sample-parallel-research-sprint.md`
- whichever final output template matches the user's target

Output:

- parallel research plan
- specialist lane contracts
- parallel execution summary
- one synthesized final artifact

## `research-retrospective` — Load: Light (~6k)

Use when the user asks how a real research run performed or what should be improved next.

Read:

- `research-retrospective-protocol.md`
- `report-quality-rubric.json`
- `quality-gates.md`

Assets:

- `assets/output-blocks/research-retrospective-block.md`
- `assets/output-blocks/report-quality-scorecard-block.md`

Output:

- overall score with reason
- scorecard across 8 dimensions
- root cause diagnosis
- next highest-leverage fix
- ship / revise / rerun decision
