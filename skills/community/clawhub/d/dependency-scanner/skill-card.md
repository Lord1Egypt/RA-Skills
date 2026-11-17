## Description:

Scan project dependencies for security vulnerabilities using npm audit. Use when checking for vulnerable packages, security audits, or dependency health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check a Node.js project's dependencies for known vulnerabilities during security audits, before deployment, while updating packages, or in periodic checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A scan may send dependency metadata to the configured npm registry.

Mitigation: Confirm the configured registry and that sharing this metadata is acceptable for the project before scanning.

Risk: The security evidence is incomplete: reported scan coverage was 66.7%, and static tool-misuse analysis was degraded.

Mitigation: Treat scan results as partial assurance and supplement them with checks that cover omitted components; rerun when full coverage is available.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/147258xuan/skills/dependency-scanner)

## Skill Output:

**Output Type(s):** [Text, Analysis, Structured data, Guidance]

**Output Format:** [Formatted plain-text report and structured scan-result object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes vulnerability counts by severity, affected package details, and recommendations when available.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
