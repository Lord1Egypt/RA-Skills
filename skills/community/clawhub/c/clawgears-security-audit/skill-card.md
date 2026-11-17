## Description:

Comprehensive OpenClaw security audit -- checks gateway binding, credential exposure, channel policies, tool sandboxing, network/IP leaks, and macOS system security (SIP, FileVault, TCC).

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunt23310-ops](https://clawhub.ai/user/sunt23310-ops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run local OpenClaw security checks for gateway exposure, credentials, channel policies, tool sandboxing, network leaks, and system hardening. It helps produce pass, warning, fail, or skip results and points users toward appropriate fixes when issues are found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs unpinned external Bash scripts that were not included in the reviewed artifact.

Mitigation: Review or pin the external repository content before running the audit commands.

Risk: Audit and fix scripts run as local code with access to OpenClaw configuration, credentials, network details, and user-writable files.

Mitigation: Run only after confirming trust in the source, and review each proposed fix before approving changes.

Risk: The network/IP leak check may send IP information to external services.

Mitigation: Confirm the check only when sharing that network information is acceptable.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sunt23310-ops/skills/clawgears-security-audit)
- [Project homepage](https://github.com/sunt23310-ops/openclaw-security-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and summarized audit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference HTML or JSON report generation through the external audit tool.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
