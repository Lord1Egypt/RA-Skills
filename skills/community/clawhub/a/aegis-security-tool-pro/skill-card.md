## Description:

Helps DeFi teams and institutional users run blockchain security checks such as transaction simulation, batch address screening, token checks, multi-chain scanning, report export, and webhook alerting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External DeFi teams, institutional trading teams, security auditors, and developers use this skill to prepare API-driven checks before transactions, deployments, audits, and CI/CD gates. It guides agents through address and token risk checks, transaction simulation, batch screening, report export, and alert configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends blockchain addresses, token addresses, transaction simulation details, and optional webhook information to a configured external service.

Mitigation: Review the endpoint, credentials, and data sensitivity before use, especially for operational wallets or unreleased transactions.

Risk: The skill relies on shell commands and API calls for its core workflow.

Mitigation: Review commands before execution and run them only in an environment where network access, credentials, and output files are appropriate for the task.

Risk: Security scan results may influence deployment, trading, or CI/CD gate decisions.

Mitigation: Treat the results as decision support and review high-impact findings before blocking or approving operational activity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/aegis-security-tool-pro)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash, Python, YAML, JSON, and CSV examples; generated reports may be SARIF, HTML, or PDF.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces API-driven security check workflows and may write local result or report files when the user runs the provided commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
