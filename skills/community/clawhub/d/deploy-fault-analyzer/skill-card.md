## Description:

Analyzes deployment logs and error text, checks a MySQL fault knowledge base before drawing conclusions, falls back to deployment script search when needed, supports fault-record updates, and generates Word analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bounding-elk](https://clawhub.ai/user/bounding-elk)

### License/Terms of Use:

MIT-0

## Use Case:

Deployment engineers use this skill to triage deployment failures from JSON logs, log files, or pasted error text. It compares incidents with known fault records, searches deployment scripts when no high-confidence case is found, and prepares structured remediation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded database passwords could expose the fault knowledge base if copied into an uncontrolled environment.

Mitigation: Remove the embedded passwords, rotate any exposed credentials, and use environment-scoped secrets or controlled wrapper scripts before installation.

Risk: Raw logs and incident records may contain sensitive operational data that the skill stores in local files, Excel records, or MySQL.

Mitigation: Make retention explicit opt-in, redact secrets before storage, and define retention and access controls for raw logs and fault records.

Risk: Docker, database, and /data/scripts access can affect deployment infrastructure if granted too broadly.

Mitigation: Run the skill only in a controlled deployment-support environment with least-privilege access to Docker, MySQL, and deployment script paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bounding-elk/skills/deploy-fault-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown analysis with inline shell commands, generated DOCX reports, and optional Excel or MySQL fault-record updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist raw logs and incident records in the configured deployment-support environment.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
