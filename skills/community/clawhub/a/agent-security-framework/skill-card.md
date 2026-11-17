## Description:

Agent Security Framework for OpenClaw provides Docker containerization, fake agent detection, security scanning, and security hardening guidance for AI agent deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffvsutherland](https://clawhub.ai/user/jeffvsutherland)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use this skill to assess, harden, and operate OpenClaw agent deployments with security audit, containerization, scanning, and policy guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included identity guidance can encourage autonomous task claiming, external script execution, status posting, and persistent memory updates without clear user control.

Mitigation: Remove or heavily constrain the SOUL.md workflow instructions before installation, and require explicit user approval for external actions, script execution, posting, and memory writes.

Risk: The Docker Compose example is illustrative and uses unpinned container images.

Mitigation: Pin image versions or digests and add normal deployment safeguards before production use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jeffvsutherland/skills/agent-security-framework)
- [Skill definition](artifact/SKILL.md)
- [Security hardening guide](artifact/SECURITY-HARDENING.md)
- [Agent identity and operating guidance](artifact/SOUL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Security and deployment guidance should be reviewed before execution in the target environment.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
