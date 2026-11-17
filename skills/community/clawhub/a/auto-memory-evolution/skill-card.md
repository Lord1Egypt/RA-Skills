## Description:

Automatically summarize daily discussions and update memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-11even](https://clawhub.ai/user/mr-11even)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to organize daily conversation notes into dated memory files and long-term memory summaries. It is intended for recurring local automation through scheduled daily evolution and heartbeat checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled execution can continue updating memory files after installation.

Mitigation: Enable cron jobs only after explicit opt-in, document how to disable them, and review the scheduled commands before deployment.

Risk: Conversation-derived summaries are written into long-term local memory.

Mitigation: Provide controls for review, deletion, and disabling automatic saves before using the skill with sensitive conversations.

Risk: Heartbeat handlers can run unrelated mutable workspace scripts.

Mitigation: Remove or constrain unrelated event handlers before enabling heartbeat automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mr-11even/skills/auto-memory-evolution)
- [Publisher profile](https://clawhub.ai/user/mr-11even)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration]

**Output Format:** [Markdown memory summaries with cron and command-line configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes conversation-derived summaries to local OpenClaw memory files and generates local JSON evolution reports.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
