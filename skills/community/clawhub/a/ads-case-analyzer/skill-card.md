## Description:

Analyzes content-ad campaign cases from campaign, advertiser, or brand-account identifiers by gathering post-delivery and bidding data, decomposing funnel and bidding signals, inferring root causes, and producing a structured Redoc analysis document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fiendark](https://clawhub.ai/user/fiendark)

### License/Terms of Use:

MIT-0

## Use Case:

Advertising analysts and operations engineers use this skill to troubleshoot campaign performance issues such as volume drops, high CPA, weak ROI, retention decline, bidding weakness, prediction gaps, and placement anomalies. It turns validated campaign identifiers and date ranges into SQL-backed diagnostics, root-cause analysis, and a Redoc report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive internal advertising data and uses broad SQL templates.

Mitigation: Install only for authorized analysts, require explicit account or campaign identifiers, validate dates and IDs, and use read-only scoped database roles.

Risk: Free-form predicates or over-broad queries could expose more data than needed.

Mitigation: Avoid free-form SQL predicates and keep queries constrained to the validated identifiers and analysis window.

Risk: Referenced privileged impersonation tooling could create access-control or audit risk.

Mitigation: Do not use impersonation tooling unless a separate approved and audited process requires it.

## Reference(s):

- [adtrace_funnel.md](references/adtrace_funnel.md)
- [constraint_type_mapping.md](references/constraint_type_mapping.md)
- [root_cause_prompt.md](references/root_cause_prompt.md)
- [sql_templates.md](references/sql_templates.md)
- [ClawHub Skill Page](https://clawhub.ai/fiendark/skills/ads-case-analyzer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, SQL, Shell commands, Guidance]

**Output Format:** [Markdown with SQL and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured Redoc campaign analysis report after the agent gathers approved query results.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
