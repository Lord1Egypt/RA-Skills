## Description: <br>
Persistent context survival for OpenClaw that reads local memory notes and writes short, user-triggered anchors to memory/anchors/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tommot2](https://clawhub.ai/user/tommot2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preserve compact task context across long conversations, compaction, or later resume points. It helps record active state, decisions, pending work, and important paths without modifying MEMORY.md, HEARTBEAT.md, or daily logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory files can contain sensitive project context, and anchors persist after the conversation. <br>
Mitigation: Do not save secrets, rely on the skill's redaction rules, and periodically review or delete old files under memory/anchors/. <br>
Risk: Saved anchors can become stale as project decisions change. <br>
Mitigation: Review recent anchors when resuming work and replace outdated context with a new user-triggered anchor. <br>


## Reference(s): <br>
- [Context Brief on ClawHub](https://clawhub.ai/tommot2/context-brief) <br>
- [TommoT2 publisher profile](https://clawhub.ai/user/tommot2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown text and optional local anchor files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Anchor files are limited to concise context summaries and are written only after a user trigger or explicit consent.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
