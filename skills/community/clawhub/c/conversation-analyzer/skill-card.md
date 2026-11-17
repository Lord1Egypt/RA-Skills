## Description:

Intelligent conversation analysis, summarization, and conclusion recording. Analyzes user personality, tracks tasks, checks incomplete tasks, and writes to memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opendolph](https://clawhub.ai/user/opendolph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to analyze conversation history, maintain user profile and memory notes, track requested work, and surface incomplete tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill analyzes private, work, customer, or personal conversation content and retains chat-derived profile and memory information.

Mitigation: Review the information captured in USER.md and MEMORY.md before enabling the skill, and establish clear review and deletion controls for retained records.

Risk: Scheduled execution can repeatedly analyze conversations without an explicit per-run prompt.

Mitigation: Keep cron or automatic triggers disabled until the intended scope, frequency, and retention behavior are approved.

Risk: Incomplete-task reminders may be sent externally through Feishu.

Mitigation: Configure notification recipients carefully and disable external notifications until recipient controls are verified.

## Reference(s):

- [Conversation Analyzer ClawHub listing](https://clawhub.ai/opendolph/skills/conversation-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown memory updates, console text, task-notification text, and Node.js command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates USER.md, MEMORY.md, and HEARTBEAT.md; may produce Feishu task notification content.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
