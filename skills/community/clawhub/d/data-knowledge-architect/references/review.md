# Phase 2: Decision Review

Turn the inventory into atomic decisions and an HTML workbench. Every decision records ID, section,
question, current proposal, alternatives, evidence, risk, dependencies, status
(`pending|approved|rejected|blocked`), and optional user amendment.

## Decision Model

The ontology is explicit: an `object` owns each atomic `decision`; a decision offers an `option` set
and may declare a `relation` such as `depends_on`, conflict, or tradeoff. Global `constraint` values
apply across objects. Every recommendation records `evidence`, evidence `basis`, `confidence`,
`status`, impact, and `risk`. Relationships are bidirectional where required and dependency cycles
are invalid.

Collect in dependency order: facts and falsifiable grain; dimensions with kind, business key, source
operations, and attributes; measures with additivity, unit, currency/basis, and aggregation scope;
then routing and evidence boundaries.

## Fixed Guidance

- A fact records a repeatable business event or snapshot; grain states exactly what one row
  represents.
- A dimension answers who/what/where and needs a stable business key plus authoritative source.
- A measure must answer an analysis question and declare unit, money basis, and aggregation limits.
- Routing selects the smallest evidence path by fact, dimension, measure, time, and scope;
  boundaries state what the model cannot answer.
- YAGNI means defer an object with no current question, evidence, or consumer—not omit data needed
  for correctness.

Generate compact model JSON and inject it into `assets/review-template.html`. The report lets the
user approve, reject, select, correct, or request evidence. Treat every decision as pending
initially. Write feedback to `amendments.md`, apply it to the model, and regenerate; never patch
only the rendered HTML.

Guidance remains visible by focus/click as well as hover. Approval is user-owned, not agent-owned.
Stop after delivering the report. Exit only when the user returns `approved:true` and no
decision remains pending or blocked. A partial approval advances nothing that depends on an
unresolved decision.
