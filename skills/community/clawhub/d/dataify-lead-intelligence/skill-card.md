## Description:

Discover and rank companies that match an ideal customer profile using public company, hiring, and market evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, go-to-market, and operations users use this skill to build evidence-backed company prospect lists for account research, territory planning, and lead qualification. The workflow qualifies organizations from public sources and excludes private personal contact enrichment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package bundles an unrelated Amazon review-scraping capability alongside lead intelligence.

Mitigation: Review installed capabilities before deployment and invoke only the lead intelligence workflow unless Amazon review collection is intended.

Risk: Dataify API token handling could expose secrets through URLs or logs.

Mitigation: Use a limited Dataify API token when possible, avoid persistent token setup unless needed, never paste tokens into chat, and rotate the token if exposure is suspected.

Risk: Automated company qualification can be incomplete or misleading when public evidence is sparse.

Mitigation: Use the generated missing fields, disqualifiers, source evidence, and human-verification queue before acting on prospect rankings.

## Reference(s):

- [Dataify Lead Intelligence on ClawHub](https://clawhub.ai/dataify-server/skills/dataify-lead-intelligence)
- [Dataify Token Setup](_dependencies/skills/dataify-task-operations/references/token-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON reports, and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Execution can produce report.md, report.json, state files, and retained raw evidence; lead scores and records require human verification before business decisions.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
