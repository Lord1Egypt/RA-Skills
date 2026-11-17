## Description:

Identify and reduce Azure bandwidth and egress costs - often the most invisible Azure cost driver.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers, cloud engineers, and FinOps teams use this skill to analyze user-provided Azure cost exports and network inventory, then identify egress cost drivers, optimization opportunities, ROI estimates, and infrastructure snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Azure cost exports and network inventory may contain sensitive operational details or accidentally pasted secrets.

Mitigation: Review data before sharing it with the agent and remove credentials, access keys, secret keys, or other sensitive values.

Risk: Optimization recommendations and Bicep/ARM snippets may be incomplete for the user's environment.

Mitigation: Have Azure engineering or FinOps reviewers validate proposed changes and infrastructure snippets before applying them.

## Reference(s):

- [Bandwidth Optimizer on ClawHub](https://clawhub.ai/anmolnagpal/skills/bandwidth-optimizer)
- [anmolnagpal ClawHub profile](https://clawhub.ai/user/anmolnagpal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with cost breakdowns, heatmaps, ROI tables, and Bicep/ARM snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only analysis based on user-provided Azure cost and network data; no credentials are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
