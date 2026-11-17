## Description:

Generate SOC2 evidence collection checklists, automate evidence gathering scripts, and produce audit-ready evidence packages covering all 5 Trust Service Criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shark1973](https://clawhub.ai/user/shark1973)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, engineering teams, and compliance managers use this skill to prepare SOC2 Type I or Type II evidence packages, build collection scripts, identify gaps, and schedule recurring evidence refreshes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated evidence collection scripts can operate as sensitive administrative tooling.

Mitigation: Run generated scripts only with authorized, least-privilege AWS, GitHub, or IdP credentials and review commands before execution.

Risk: Collected SOC2 evidence may contain sensitive security, access, infrastructure, or audit data.

Mitigation: Store evidence directories securely and redact sensitive values before sharing with auditors or third parties.

Risk: Evidence packages may be incomplete or misaligned if the audit scope is wrong.

Mitigation: Confirm the audit type, Trust Service Criteria, cloud providers, tech stack, team size, and audit boundary before generating or relying on the package.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shark1973/skills/afrexai-soc2-evidence-collector-skip)
- [AfrexAI](https://afrexai.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured tables, evidence-package outlines, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audit materials should be reviewed, authorized, securely stored, and redacted before auditor or third-party sharing.]

## Skill Version(s):

1.0.0 (source: frontmatter, server evidence, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
