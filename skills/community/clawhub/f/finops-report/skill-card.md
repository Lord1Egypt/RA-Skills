## Description:

Generate executive-ready monthly AWS FinOps reports with team-level chargeback and savings opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Engineering, finance, and FinOps teams use this skill to turn AWS billing or cost-allocation data into monthly executive and team-level reports with chargeback, budget variance, savings opportunities, and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AWS billing and cost-allocation data may contain sensitive business or account information.

Mitigation: Use scoped billing exports or sanitized datasets instead of broad AWS credentials or unnecessary account details.

Risk: Budget variance, savings, and forecast recommendations may be misleading if source billing data is incomplete or stale.

Mitigation: Review the generated report against authoritative finance and billing records before using it for executive or team action.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown report with executive summary, cost tables, savings opportunities, finance summary, and team-level action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses billing or cost-allocation data supplied to the agent; no persistent access or account changes are requested by the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
