## Description:

Security and compliance auditing tool for AI agents. Scans code for vulnerabilities, checks GDPR/CCPA compliance, generates risk reports with remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agent-compliance-org](https://clawhub.ai/user/agent-compliance-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and compliance teams use this skill to audit AI agent or skill code before deployment, identify common vulnerability patterns, and generate risk reports with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include proprietary code snippets, secrets, or sensitive security findings.

Mitigation: Run the skill in controlled environments and share reports only through approved destinations.

Risk: Static, pattern-based checks may produce false positives or miss context-specific vulnerabilities.

Mitigation: Have qualified reviewers validate findings before using them to approve or block a release.

Risk: GDPR and CCPA checks are generalized compliance guidance, not legal advice.

Mitigation: Use legal and privacy review for decisions involving regulatory obligations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agent-compliance-org/skills/compliance-audit-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Guidance]

**Output Format:** [Text, JSON, or HTML audit reports with risk scores, findings, summaries, and remediation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static analysis only; pattern-based findings may include false positives, and compliance checks are not legal advice.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
