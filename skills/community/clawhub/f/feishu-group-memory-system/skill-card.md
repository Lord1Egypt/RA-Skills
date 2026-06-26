## Description: <br>
Persists Feishu group chat context by saving and loading structured local memory summaries, while routing private-chat requests to the appropriate archive or other action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzlqxbms](https://clawhub.ai/user/zzlqxbms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams using OpenClaw in Feishu group chats use this skill to preserve conversation context across sessions by saving, loading, and summarizing group memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Group-chat content can gain lasting influence through local memory and daily diary files. <br>
Mitigation: Install only when all Feishu group participants are comfortable with storage, and define consent, redaction, retention, review, and deletion rules before use. <br>
Risk: The skill describes broad [SYSTEM] text-command handling that could trigger unsafe actions. <br>
Mitigation: Remove or tightly restrict [SYSTEM] command handling before deployment. <br>
Risk: Heartbeat auto-save can persist discussions without an explicit user save request. <br>
Mitigation: Disable heartbeat auto-save unless explicitly needed and make any automatic save policy visible to participants. <br>


## Reference(s): <br>
- [Known Feishu Group IDs Reference](references/group-ids.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zzlqxbms/feishu-group-memory-system) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands and memory-file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local Feishu group memory and daily diary Markdown files when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
