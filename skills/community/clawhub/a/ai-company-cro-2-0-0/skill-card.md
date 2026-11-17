## Description:

AI company Chief Risk Officer skill package for enterprise risk governance, compliance audit, crisis response, circuit-breaker handling, NIST AI RMF workflows, and FAIR-based risk quantification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agent operators use this skill to assess AI company risks, coordinate compliance and crisis response, prepare mitigation plans, and summarize board-level risk reporting. It is suited to governance workflows that expect quantitative risk analysis, cross-agent escalation, and explicit oversight of high-impact recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes high-impact operational actions, including halt, rollback, isolation, permission restriction, cross-agent escalation, agent provisioning, and persistent audit writes.

Mitigation: Require explicit approval before carrying out those actions, and deploy only where cross-agent escalation and circuit-breaker recommendations are expected.

Risk: Long-term audit logging and cross-agent routing can expose sensitive operational or financial risk information if access and retention are unclear.

Mitigation: Clarify where logs are stored, who can read them, and what retention and review controls apply before enabling persistent audit workflows.

## Reference(s):

- [ClawHub skill homepage](https://clawhub.com/skills/ai-company-cro)
- [ClawHub release page](https://clawhub.ai/johnsmithfan/skills/ai-company-cro-2-0-0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown or structured text containing risk assessments, mitigation plans, board-report summaries, circuit-breaker recommendations, and FAIR risk metrics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity levels, escalation paths, audit-log summaries, and quantitative LEF, LM, and risk exposure values.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact/SKILL.md frontmatter lists 2.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
