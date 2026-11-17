## Description:

Emotional processing layer for AI agents. Persistent emotional states that influence behavior and responses. Part of the AI Brain series.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to add persistent emotional state tracking, decay, visualization, and session context for OpenClaw-style agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cross-session emotional profiles may retain sensitive conversation-derived signals.

Mitigation: Install only after confirming storage location, retention expectations, and delete or reset controls.

Risk: Cron-based decay or automatic encoding creates recurring local execution.

Mitigation: Leave cron disabled unless the user explicitly accepts scheduled execution and can audit or remove the jobs.

Risk: Automatic encoding may send conversation history or derived emotional signals to external processing.

Mitigation: Require opt-in, payload preview, redaction, or a local-only path before processing private conversations.

Risk: The artifact describes script behavior without bundling the scripts for review.

Mitigation: Review the actual installed scripts before deployment and prefer releases that include auditable implementation files.

## Reference(s):

- [Amygdala Memory ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvis2-amygdala-memory)
- [alvisdunlop ClawHub publisher profile](https://clawhub.ai/user/alvisdunlop)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes persistent emotional state files, optional cron schedules, and dashboard generation behavior.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
