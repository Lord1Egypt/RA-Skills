## Description:

Memory management system with automated tiered storage (hot/warm/gist/forgotten), time-decay organization, promotion engine, layer-search protocol, and session-injection plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slientrain-new](https://clawhub.ai/user/slientrain-new)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to manage local cross-session memory, refresh active sessions, search older checkpoint content by storage layer, and promote frequently reused memories into longer-term storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically persists local conversation memory and injects recent memory into prompts.

Mitigation: Install only when cross-session memory is intended, avoid storing secrets or credentials, and review ~/.openclaw/memory_fs regularly.

Risk: /refresh can reorganize, mark, reset, and eventually delete memory files.

Mitigation: Run /refresh only after confirming the local memory state and keep backups for memory that must not be lost.

## Reference(s):

- [Context Clear ClawHub Skill Page](https://clawhub.ai/slientrain-new/skills/context-clear)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration, and generated local memory reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepend recent local memory content to prompts and may generate promote_report.md during refresh.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and plugin/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
