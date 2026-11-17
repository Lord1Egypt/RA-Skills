## Description:

MoltGuard helps protect OpenClaw agents and users from prompt injection, data exfiltration, and malicious command risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaslwang](https://clawhub.ai/user/thomaslwang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install and operate MoltGuard protections for OpenClaw agents, including status checks, account linking, dashboard access, updates, and enterprise Core enrollment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and activates an external cloud-backed plugin.

Mitigation: Install only after explicit user approval and confirm the package and version are the intended trusted release.

Risk: API keys and agent credentials may be displayed or handled during status and account-linking flows.

Mitigation: Treat generated API keys as secrets and avoid exposing them in shared transcripts, screenshots, or logs.

Risk: Core service data handling, retention, redaction, and credential-storage protections are not established in the provided evidence.

Mitigation: Avoid use with sensitive or regulated data until those controls are reviewed and accepted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thomaslwang/skills/antivirus)
- [MoltGuard homepage](https://github.com/openguardrails/openguardrails/tree/main/moltguard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational commands for plugin installation, status checks, account linking, dashboard access, enterprise enrollment, updates, and uninstall.]

## Skill Version(s):

6.8.20 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
