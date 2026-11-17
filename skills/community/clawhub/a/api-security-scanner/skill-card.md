## Description:

Reviews REST API endpoints, API documentation, and gateway or framework configurations against OWASP API Security Top 10-style checks, then produces a structured security report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caingao](https://clawhub.ai/user/caingao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and API teams use this skill to review REST API designs, endpoint lists, API documentation, gateway settings, and framework configurations before deployment or during lightweight security audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided API documentation or configuration may include real tokens, passwords, customer data, or other sensitive production details.

Mitigation: Provide sanitized API documentation, configurations, or examples unless the execution environment is approved for that data.

Risk: The skill provides checklist-based security review guidance and may miss context-specific vulnerabilities or produce findings that need validation.

Mitigation: Have qualified reviewers verify findings and remediation steps before using the report for production risk decisions.

## Reference(s):

- [API Security Scan Rules](artifact/scan-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/caingao/skills/api-security-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown security report with severity-ranked findings and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Critical, High, Medium, Low, and Passed result categories.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
