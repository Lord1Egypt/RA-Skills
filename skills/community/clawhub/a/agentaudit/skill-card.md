## Description:

Automatic security gate that checks packages against a vulnerability database before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starbuck100](https://clawhub.ai/user/starbuck100)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and agent operators use AgentAudit to check package, skill, and MCP server installs against a trust registry, run structured security audits for unknown packages, and submit findings for shared review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer path includes curl-to-bash setup.

Mitigation: Avoid the one-line installer; inspect the artifact first and install from a trusted local checkout or package manager path.

Risk: A bundled API key is present in the artifact credentials file.

Mitigation: Revoke or replace the bundled key before use, and prefer an environment-specific AGENTAUDIT_API_KEY or newly registered user credential.

Risk: Private-code audits may upload findings to the registry unless upload behavior is fixed and configured correctly.

Mitigation: Do not use the skill for private or proprietary code until upload behavior is reviewed; keep audits local when sensitive code is involved.

Risk: Registry PASS results are advisory because malformed registry responses can fail open.

Mitigation: Review unexpected registry responses manually, keep WARN/BLOCK handling in place, and combine checks with sandboxing or permission controls.

Risk: The security gate is cooperative and instruction-based rather than OS-enforced.

Mitigation: Use manual pre-checks and platform-level controls for installs that require stronger assurance.

## Reference(s):

- [AgentAudit ClawHub Skill Page](https://clawhub.ai/starbuck100/skills/agentaudit)
- [AgentAudit Homepage](https://agentaudit.dev)
- [API Reference](references/API-REFERENCE.md)
- [Audit Methodology](references/AUDIT-METHODOLOGY.md)
- [Detection Patterns](references/DETECTION-PATTERNS.md)
- [Report Format](references/REPORT-FORMAT.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [Trust Scoring](references/TRUST-SCORING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON gate results, shell commands, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires registry access for live checks; local audits may produce report JSON for upload or review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
