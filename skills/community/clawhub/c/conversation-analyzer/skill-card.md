## Description: <br>
Intelligent conversation analysis, summarization, and conclusion recording. Analyzes user personality, tracks tasks, checks incomplete tasks, and writes to memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opendolph](https://clawhub.ai/user/opendolph) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to analyze conversations, maintain user and task memory, detect incomplete work, and generate reminder content for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation profiling and persistent memory can capture sensitive or inaccurate personal and work information. <br>
Mitigation: Enable the skill only when this analysis is intended, then regularly review USER.md, MEMORY.md, and HEARTBEAT.md and correct or delete sensitive or inaccurate entries. <br>
Risk: Task reminders may expose work details through Feishu notification content. <br>
Mitigation: Confirm recipients and message routing before enabling Feishu reminders, and review the notification content produced by the skill. <br>
Risk: Scheduled analysis can repeatedly process conversations without a fresh manual review. <br>
Mitigation: Use manual runs or a narrowly scoped cron schedule until retention, review, and deletion practices are clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/opendolph/conversation-analyzer) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, Markdown memory updates, cron commands, and notification text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or guides updates to USER.md, MEMORY.md, and HEARTBEAT.md; may generate Feishu reminder content.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
