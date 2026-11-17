## Description:

MoltGuard helps OpenClaw agents protect users from prompt injection, data exfiltration, and malicious commands hidden in files and web content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaslwang](https://clawhub.ai/user/thomaslwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, test, configure, update, and remove MoltGuard protection for agent security checks. The skill focuses on guardrails for prompt injection, data exfiltration, risky commands, and sensitive-data exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs executable code from an external package.

Mitigation: Review the skill before installing and prefer a pinned, audited plugin version.

Risk: Sensitive prompts, files, commands, or secrets may be routed to Core for detection.

Mitigation: Confirm Core data-handling terms and avoid sending content that violates user or organizational data policies.

Risk: Local credentials are persisted and some commands can display API keys.

Mitigation: Protect local credential storage and avoid sharing transcripts or logs containing /og_status or /og_claim output.

## Reference(s):

- [MoltGuard homepage](https://github.com/openguardrails/openguardrails/tree/main/moltguard)
- [ClawHub skill page](https://clawhub.ai/thomaslwang/skills/flaw0)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, status, onboarding, enterprise enrollment, update, and uninstall guidance.]

## Skill Version(s):

6.8.20 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
