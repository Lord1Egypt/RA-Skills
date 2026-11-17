## Description:

Generate SOC2 evidence collection checklists, automate evidence gathering scripts, and produce audit-ready evidence packages across the SOC2 Trust Service Criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afrexai-cto](https://clawhub.ai/user/afrexai-cto)

### License/Terms of Use:

MIT-0

## Use Case:

Engineering, compliance, and audit teams use this skill to prepare SOC2 Type I and Type II evidence packages, generate collection scripts, identify gaps, and plan recurring evidence collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated evidence packages may contain sensitive security, identity, infrastructure, or audit data.

Mitigation: Store evidence output securely, use least-privilege read-only credentials for collection, and redact sensitive values before sharing with auditors or vendors.

Risk: Generated scripts can query production cloud, source control, or identity systems.

Mitigation: Review scripts before execution and run them only in approved environments with scoped credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afrexai-cto/skills/afrexai-soc2-evidence-collector)
- [AfrexAI](https://afrexai.com)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell script and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include evidence matrices, gap analyses, collection schedules, and generated scripts for cloud, source control, and identity platforms.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
