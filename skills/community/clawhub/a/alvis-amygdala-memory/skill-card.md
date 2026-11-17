## Description:

Emotional processing layer for AI agents with persistent emotional states that can influence behavior and responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent emotional-state tracking, decay, visualization, and conversation-derived emotional encoding to OpenClaw-style agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent emotional state can influence future agent sessions.

Mitigation: Review generated state files and confirm there is a clear way to inspect, disable, reset, and delete persistent state before use.

Risk: Conversation-derived data may be processed by an external SkillBoss API.

Mitigation: Avoid sending sensitive details in free-form triggers or conversation history, and review privacy expectations before enabling automatic encoding.

Risk: Optional cron jobs can run recurring background updates.

Mitigation: Do not enable cron until the scheduled scripts and generated cron entries have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvis-amygdala-memory)
- [Metadata repository link](https://github.com/ImpKind/amygdala-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent JSON and Markdown state files, HTML dashboard output, cron entries, and external API requests when installed and configured.]

## Skill Version(s):

1.0.5 (source: server release metadata and auto changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
