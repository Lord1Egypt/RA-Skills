## Description:

Coordinates specialized AI agents to propose and rank drug candidates using synthesis planning, inventory checks, ADMET and toxicity proxies, pharmacology scoring, patent scouting, and visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminem](https://clawhub.ai/user/cheminem)

### License/Terms of Use:

MIT-0

## Use Case:

Drug-discovery practitioners and research developers use this skill to coordinate early-stage molecule ideation, synthesis feasibility review, inventory-aware cost checks, ADMET and toxicity proxy scoring, and patent novelty screening for a target or indication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent scouting may send molecule and target search terms to Google Patents.

Mitigation: Avoid confidential targets or structures unless network disclosure is acceptable, or disable patent scouting for sensitive work.

Risk: The stock-check path can create fake persistent inventory data when the expected inventory file is missing.

Mitigation: Run only in an isolated workspace with verified non-production inventory data, and ensure the inventory file exists before execution.

Risk: Broad trigger phrases may start the workflow unexpectedly.

Mitigation: Use explicit invocation or narrow triggers and require confirmation before running in shared or lab-adjacent environments.

Risk: ADMET, toxicity, pharmacology, and novelty scores are proxy outputs.

Mitigation: Treat results as preliminary screening guidance and require qualified expert review before research, procurement, synthesis, or lab decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cheminem/skills/drug-team)
- [Google Patents](https://patents.google.com/)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain text report with generated molecule visualization files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks top candidates by molecular, feasibility, inventory, cost, and novelty scores.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
