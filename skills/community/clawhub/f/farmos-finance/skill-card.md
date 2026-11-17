## Description:

Queries farm financial data for cash flow projections, cost tracking, and breakeven analysis, with admin-only access for highly sensitive data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianppetty](https://clawhub.ai/user/brianppetty)

### License/Terms of Use:


## Use Case:

Authorized farm owners and admins use this skill to review operating costs, monthly cash flow, cost categories, and crop breakeven metrics. It helps an agent answer finance questions while requiring totals, error disclosure, and admin-only access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive farm financial data could be exposed if integration endpoints bypass admin authorization.

Mitigation: Require server-side admin authorization on every finance endpoint before use, and restrict responses to verified farm owners or admins.

Risk: Bearer tokens and financial data could be exposed over plaintext HTTP.

Mitigation: Use HTTPS or another authenticated encrypted transport for all finance API requests.

Risk: Partial finance results could mislead users when revenue data or an endpoint fails.

Mitigation: State totals, disclose revenue-side failures, and report endpoint errors instead of presenting incomplete data as complete analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brianppetty/skills/farmos-finance)
- [Publisher profile](https://clawhub.ai/user/brianppetty)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with endpoint references and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires crop_year and admin authorization when accessing sensitive financial data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
