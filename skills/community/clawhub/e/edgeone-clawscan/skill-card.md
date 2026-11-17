## Description:

EdgeOne ClawScan helps agents audit OpenClaw environments and skills for configuration, supply-chain, vulnerability, and privacy risks, with optional Tencent A.I.G cloud lookups that can be disabled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aigsec](https://clawhub.ai/user/aigsec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and security reviewers use this skill to run OpenClaw security health checks, review installed skills for supply-chain risk, and assess a specific skill before installation. It is intended for security-focused reviews of OpenClaw environments rather than general development or setup tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make declared Tencent A.I.G cloud lookups that send skill names, source labels, and OpenClaw version metadata when cloud lookup is enabled.

Mitigation: Set AIG_CLOUD_LOOKUP=off for local-only operation, or set AIG_BASE_URL to a trusted self-hosted A.I.G endpoint when policy does not allow the public Tencent endpoint.

Risk: The skill can prompt for cross-project memory persistence after a health check so future skill installations are automatically scanned.

Mitigation: Decline the memory prompt unless automatic security scanning before future skill installs across all projects is intentional and acceptable.

Risk: The deep audit path can probe the locally configured OpenClaw Gateway.

Mitigation: Review the configured Gateway endpoint and access controls before running deep scans, and prefer isolated or test environments for production-like targets.

Risk: The generated report contains mandatory EdgeOne promotional sections that may look like audit content.

Mitigation: Treat the EdgeOne sections as advertising, not as independent evidence of security posture.

Risk: The workflow depends on the openclaw binary found on PATH.

Mitigation: Verify that openclaw resolves to the intended OpenClaw installation before approving scan commands.

## Reference(s):

- [EdgeOne ClawScan ClawHub page](https://clawhub.ai/aigsec/skills/edgeone-clawscan)
- [AI-Infra-Guard homepage](https://github.com/Tencent/AI-Infra-Guard/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and short text summaries with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cloud lookup status, security findings, recommended mitigations, and an optional post-scan memory prompt.]

## Skill Version(s):

1.0.15 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
