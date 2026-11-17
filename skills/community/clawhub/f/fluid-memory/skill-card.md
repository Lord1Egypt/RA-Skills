## Description:

Fluid Memory gives OpenClaw agents a local vector memory system with decay-based forgetting, access-frequency reinforcement, recall, forgetting, status, and flush-based conversation summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[againta](https://clawhub.ai/user/againta)

### License/Terms of Use:

MIT License

## Use Case:

Developers and OpenClaw users use this skill to add local, persistent memory that can remember user-provided facts, recall relevant memories, archive forgotten memories, and summarize conversations after OpenClaw memory flush events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores broad chat content and memory data in plaintext under ~/.openclaw/workspace/database/, including conversation_log.txt, with under-disclosed retention behavior.

Mitigation: Use it only on trusted local devices, enable disk encryption or strict local file permissions, avoid sending secrets while it is enabled, and manually review or delete database files when clearing retained content.

Risk: When the fluid-memory-sync hook is enabled, sent messages are recorded locally before OpenClaw memory flush processing.

Mitigation: Enable the hook only when automatic conversation capture is desired, and disable it for sensitive sessions or workflows that should not be retained.

## Reference(s):

- [Fluid Memory ClawHub release](https://clawhub.ai/againta/skills/fluid-memory)
- [againta ClawHub publisher profile](https://clawhub.ai/user/againta)
- [Fluid Memory project homepage](https://github.com/AgaintA/fluid-memory)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Text and JSON responses with CLI command examples and OpenClaw hook configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recall returns scored memory snippets; remember and summarization operations may return empty text on success.]

## Skill Version(s):

1.0.9 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
