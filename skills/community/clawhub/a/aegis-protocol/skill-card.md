## Description:

Self-healing stability monitor for AI agents with core and extended checks, auto-recovery, and health scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankechenlab-node](https://clawhub.ai/user/ankechenlab-node)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and AI agent maintainers use this skill to monitor OpenClaw host and session health, generate health summaries, and perform local recovery actions such as restarting services, killing stuck sessions, or compacting context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run shell diagnostics and unattended recovery actions on the host.

Mitigation: Install only when host-level OpenClaw watchdog behavior is intended, and review the heal path before production use.

Risk: Automatic recovery can disrupt active work by killing sessions or restarting services.

Mitigation: Tune thresholds, cooldowns, and whitelists before scheduled use; run with the least privileges practical.

Risk: The server security verdict is suspicious because the skill can run shell commands and may perform external network checks.

Mitigation: Review the source, security evidence, and scanner guidance before installing; constrain or disable network checks where they are not required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ankechenlab-node/skills/aegis-protocol)
- [README](artifact/README.md)
- [Security Information](artifact/SECURITY.md)
- [Security Audit](artifact/SECURITY_AUDIT.md)
- [Changelog](artifact/CHANGELOG.md)
- [VirusTotal Report](https://www.virustotal.com/gui/file/1a7561a744e840a167c5f70d9ff5e455d5a86cd77250b6b566c0e946413a8d59)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI-oriented text with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local configuration files, health summaries, logs, and recovery guidance depending on the invoked command.]

## Skill Version(s):

0.12.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
