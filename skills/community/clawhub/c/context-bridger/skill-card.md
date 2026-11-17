## Description:

Context Bridge maintains and transfers OpenClaw context across sessions, models, and time so users do not have to restate prior work after a new session or model switch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loudmouthedmedia](https://clawhub.ai/user/loudmouthedmedia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to preserve session startup context, installed skill registries, cron and agent awareness, and model handoff notes across sessions. It is intended for continuity workflows where agents need a concise memory bridge after `/new` or model changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently collects and auto-loads broad OpenClaw metadata, including registries and model handoff notes.

Mitigation: Review and minimize the contents of the generated ~/.openclaw registry and handoff files before relying on them in future sessions.

Risk: The setup script writes multiple files under ~/.openclaw and may include cron payloads, agent workspace paths, and recent project context.

Mitigation: Run setup only after reviewing the files it will create or update, then restrict file permissions for any sensitive local context.

Risk: Direct archive installation commands can install code from a remote release without local inspection.

Mitigation: Prefer a reviewed source checkout or verify the release source and checksum before using direct archive commands.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/loudmouthedmedia/skills/context-bridger)
- [Artifact README](artifact/README.md)
- [ClawHub metadata](artifact/clawhub.json)
- [Project homepage](https://github.com/loudmouthedmedia/context-bridge)
- [Support issues](https://github.com/loudmouthedmedia/context-bridge/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on OpenClaw registry files, model handoff notes, setup steps, and session startup configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
