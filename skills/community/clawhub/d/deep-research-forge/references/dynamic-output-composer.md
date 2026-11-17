# Dynamic Output Composer

Use this file to convert a method stack into a dynamic output skeleton.

The existing templates remain useful, but they are bases. The method stack decides which blocks to add, remove, or emphasize.

## Composition Steps

1. Pick the base artifact from `output-routing-index.md`.
2. Pick method blocks from `assets/output-blocks/`.
3. Drop blocks that do not change the answer.
4. Order blocks by the user's need: answer first, evidence second, analysis third, action last.
5. Add confidence, gaps, and reversal conditions when judgment is involved.

## Base Artifact Defaults

| Base artifact | Always include | Optional method-driven blocks |
| --- | --- | --- |
| `research-brief` | research question, one-line answer, evidence base, next step | timeline, JTBD, dissent, monitoring |
| `deep-research-report` | executive judgment, evidence base, time / snapshot / mechanism axes, scenarios | literature thread, ecosystem map, benchmark caveats |
| `competitive-map` | category definition, competitor set, user choice logic | JTBD, user signals, ecosystem map, benchmark caveats |
| `decision-brief` | decision question, verdict, evidence, risk, reversal conditions | competitive matrix, monitoring, red team |
| `concept-lineage-timeline` | scope, evidence ledger, deep timeline, schools / disputes, mechanism shifts | productization, governance, adoption waves |
| `research-asset-pack` | evidence ledger, source map, timeline notes, gaps, monitoring | any block needed for reuse |

## Block Selection

| Method | Blocks to add |
| --- | --- |
| `evidence-triangulation` | `evidence-ledger-block.md`, `source-map-block.md`, `conflict-table-block.md` |
| `claim-citation-audit` | `claim-citation-map-block.md`, `evidence-ledger-block.md` |
| `historical-lineage` | `deep-timeline-block.md`, `mechanism-shifts-block.md` |
| `paradigm-analysis` | `schools-disputes-block.md`, `concept-current-snapshot-block.md` |
| `competitive-analysis` | `competitive-matrix-block.md`, `user-choice-logic-block.md` |
| `jtbd-user-choice` | `jtbd-analysis-block.md`, `user-signal-summary-block.md` |
| `ecosystem-mapping` | `ecosystem-map-block.md`, `power-dependency-map-block.md` |
| `literature-review` | `literature-thread-block.md`, `benchmark-caveats-block.md` |
| `osint-due-diligence` | `entity-dossier-block.md`, `risk-register-block.md` |
| `user-signal-analysis` | `user-signal-summary-block.md`, `channel-bias-note-block.md` |
| `causal-mechanism-analysis` | `causal-chain-block.md`, `mechanism-shifts-block.md` |
| `red-team-dissent` | `dissent-review-block.md`, `reversal-conditions-block.md` |
| `scenario-planning` | `future-scenarios-block.md`, `monitoring-list-block.md` |
| `decision-analysis` | `decision-matrix-block.md`, `next-actions-block.md` |
| `monitoring-design` | `monitoring-list-block.md`, `recheck-plan-block.md` |
| `benchmark-analysis` | `benchmark-caveats-block.md`, `comparison-table-block.md` |
| `policy-and-standard-tracking` | `official-source-priority-block.md`, `formal-adoption-status-block.md`, `claim-citation-map-block.md`, `policy-timeline-block.md`, `stakeholder-impact-block.md`, `monitoring-list-block.md` |
| `formal-status-analysis` | `formal-adoption-status-block.md`, `claim-citation-map-block.md`, `recheck-plan-block.md` |
| `exam-standard-analysis` | `official-source-priority-block.md`, `formal-adoption-status-block.md`, `claim-citation-map-block.md`, `policy-timeline-block.md`, `stakeholder-impact-block.md`, `comparison-table-block.md`, `recheck-plan-block.md` |
| `research-quality-audit` | `research-retrospective-block.md`, `report-quality-scorecard-block.md`, `recheck-plan-block.md` |
| `report-quality-scoring` | `report-quality-scorecard-block.md` |

## Ordering Rules

- For decision work: verdict -> evidence -> risks -> alternatives -> next actions -> monitoring.
- For lineage work: thesis -> evidence -> periodized timeline -> schools / disputes -> mechanism shifts -> current snapshot.
- For competitive work: category -> user jobs -> options -> comparison -> user signals -> risks.
- For source packs: evidence ledger -> source map -> reusable notes -> gaps -> follow-up queries.
- For policy / standard work: answer current official status first -> formal adoption status -> claim citation map -> source priority -> timeline -> stakeholder impact -> gaps -> monitoring.
- For exam / certification work: current test status -> formal adoption status -> claim citation map -> standard / syllabus / test-date distinction -> candidate impact -> institution-specific caveats -> recheck plan.
- For post-run evaluation: overall score -> report quality scorecard -> root causes -> next fixes -> whether the skill needs a rule, asset, eval, or only better execution.
- For parallel synthesis: integrated judgment -> parallel merge audit -> conflicts -> final confidence adjustment.

## Compact Mode

If the user wants a short answer:

- Use at most three blocks.
- Keep evidence ledger to 3-5 entries.
- Replace full tables with bullets when tables would overwhelm.
- Name the deeper method stack as an optional next step.
