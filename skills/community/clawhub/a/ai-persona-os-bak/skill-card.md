## Description:

AI Persona OS helps OpenClaw agents set up and maintain a persistent persona workspace with guided onboarding, persona presets, memory files, heartbeat checks, context protection, escalation patterns, and optional automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-xiaolin](https://clawhub.ai/user/wu-xiaolin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create a persona-centered workspace, initialize core memory and operating files, choose or build assistant personalities, and maintain continuity through heartbeat and checkpoint routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps persistent workspace memory under ~/workspace and reads it at session start.

Mitigation: Install only when persistent local memory is acceptable, keep sensitive content out of workspace memory files, and review the generated workspace files before relying on them.

Risk: Optional cron briefings or announcements can expose workspace information to unintended destinations or channels.

Mitigation: Enable cron or announcements only after reviewing the destination, channel access, schedule, and removal path.

Risk: The security audit may print credential-like values found in workspace files.

Mitigation: Treat audit output as sensitive and rotate any real credential that has already appeared in chat, logs, or audit output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wu-xiaolin/skills/ai-persona-os-bak)
- [AI Persona OS Changelog](artifact/CHANGELOG.md)
- [Security Note](artifact/SECURITY_NOTE.md)
- [Security Patterns](artifact/references/security-patterns.md)
- [Heartbeat Automation Guide](artifact/references/heartbeat-automation.md)
- [SOUL.md Maker](artifact/references/soul-md-maker.md)
- [Author Website](https://jeffjhunter.com)
- [AI Persona Method](https://aipersonamethod.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Core setup writes local Markdown workspace files under ~/workspace; optional OpenClaw cron and gateway configuration require explicit user request.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version is 1.6.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
