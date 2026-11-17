## Description:

Evo Memory provides a two-layer self-evolution memory system with persistent principles, topic-specific patterns, signal capture, and scheduled reflection for continuous agent improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiran71](https://clawhub.ai/user/weiran71)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an OpenClaw agent durable local memory across sessions, including principles, topic-specific patterns, user corrections, command-failure signals, and periodic reflection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and bootstrap hooks can influence later agent sessions beyond the current task.

Mitigation: Install only when always-on memory is desired, and periodically review or disable the self-evolution hook and workspace files.

Risk: User-derived prompts and tool-output signals may be stored locally with weak consent and review controls.

Mitigation: Review pending memory records before promotion, avoid storing sensitive content, and remove local memory files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weiran71/skills/evo-memory)
- [Skill instructions](artifact/SKILL.md)
- [Setup guide](artifact/setup.md)
- [Configuration](artifact/config.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with JSONL memory records, configuration files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local memory and signal records under the configured OpenClaw workspace path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
