## Description:

Research and compare competitors, products, pricing, customer feedback, hiring signals, positioning, or a market landscape using current public evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product teams, sales teams, and analysts use this skill to turn multi-source public evidence into competitor snapshots, product comparisons, pricing intelligence, review analysis, hiring signals, market landscapes, and battlecards with cited findings and prioritized recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security verdict is suspicious because resume and report scripts trust saved run state in ways that could run unintended local code or ingest local files.

Mitigation: Review before installing, use only run directories you created and trust, avoid resuming third-party or edited state.json files, and run the skill in a restricted workspace where possible.

Risk: The skill uses a DATAIFY_API_TOKEN for collection actions, so an over-scoped token could expose more account access than needed.

Mitigation: Keep DATAIFY_API_TOKEN scoped to the minimum needed account and never place the token in chat, command arguments, reports, or committed project files.

Risk: Autonomous or high-volume research plans can spend collection capacity or produce misleading reports if evidence is incomplete or weak.

Mitigation: Prefer dry-run and checkpoint modes for unfamiliar plans, confirm deep or credit-sensitive scopes, inspect generated evidence, and verify reports before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-competitive-intelligence)
- [Data Source Routing](artifact/references/data-source-routing.md)
- [Analysis Frameworks](artifact/references/analysis-frameworks.md)
- [Evidence and Finding Contract](artifact/references/evidence-schema.md)
- [Scope and Cost Control](artifact/references/cost-control.md)
- [Failure Recovery](artifact/references/failure-recovery.md)
- [Output Templates](artifact/references/output-templates.md)
- [Delivery Verification](artifact/references/verification-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Guidance]

**Output Format:** [Markdown reports with adjacent citations, structured JSON evidence and report files, CSV evidence indexes, and concise shell commands for bounded collection and verification workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should distinguish facts, inferences, recommendations, unknowns, confidence, source dates, evidence gaps, and failures.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
