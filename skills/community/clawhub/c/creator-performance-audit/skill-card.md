## Description:

Audit creator/influencer performance for commerce teams - score creators on reach quality, engagement authenticity, conversion contribution, and cost efficiency, then output a keep/scale/renegotiate/drop decision with evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Commerce teams, creator marketers, and marketing operators use this skill to audit creator campaign history, compare creators on a common performance scorecard, and decide whether to keep, scale, renegotiate, or drop each creator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive creator contracts, full costs, revenue, margins, attribution data, and campaign performance details.

Mitigation: Use only data the operator is comfortable sharing with the agent, minimize unnecessary sensitive fields, and follow the organization's data-handling rules.

Risk: Creator renewal, rate, or drop recommendations could be over-applied as automatic business actions.

Mitigation: Treat outputs as decision support, review the evidence and confidence notes, and require human approval before contractual, budget, or relationship changes.

Risk: Thin samples, mixed attribution methods, or incomplete full-cost inputs can produce misleading creator comparisons.

Mitigation: State attribution method, sample window, and cost basis; flag data gaps; and run the pre-delivery checklist before relying on verdicts.

## Reference(s):

- [Four-Axis Scoring, Authenticity Checks, and Verdict Thresholds](artifact/references/audit-framework.md)
- [Scorecard Metrics, Formulas, and Cost Checklist](artifact/references/metrics-benchmarks.md)
- [Creator Audit Report Template](artifact/references/output-template.md)
- [Creator Audit Pre-Delivery Checklist](artifact/assets/audit-checklist.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Structured Markdown audit report with scorecard tables, per-creator verdicts, evidence, confidence notes, and action plans.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses supplied campaign, cost, attribution, and business-context inputs; does not execute code or request credentials.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
