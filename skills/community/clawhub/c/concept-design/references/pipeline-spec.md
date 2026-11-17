# Data quality specification

Cross-concept coordination belongs in SYNCS.

```markdown
# pipeline: Name
## purpose
<consumer and required outcome>
## sources
<source, owner, grain, contract>
## stages
### Stage [tool: <actual tool>]
<input/schema → transform → output/schema>
<quality check and failure consequence>
## outputs
<artifact, schema, owner, consumer>
## invariants
<checkable rules and verification>
## triggers
<event, API, schedule, or manual entry>
## data boundary
<owners and permitted public reads/writes>
```

Backfill from commands, workflows, schemas, queries/joins, and checks.
Each source, stage, output, and invariant MUST resolve to code or an explicit intended contract.
A concept's SQL adapter does not grant pipelines cross-concept private access.
`score in [-1, 1]` is checkable; “clean data” is not.
Row-count limits require contract evidence.
New flows also specify append/refresh and idempotency behavior.
