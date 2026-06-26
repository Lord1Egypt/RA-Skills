## Description: <br>
Manages Feishu-sourced to-dos by detecting task requests, storing task records, listing and updating items, handling links, reminders, and optional Feishu calendar synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyu68](https://clawhub.ai/user/zhangyu68) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams or individual Feishu users can use this skill to turn messages and /todo commands into managed task lists, reminders, links, and calendar entries. It is intended for environments where local task storage and Feishu API integration are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message-derived tasks and private links may be saved locally and sent or synchronized through Feishu. <br>
Mitigation: Use only with data suitable for local task storage and Feishu transmission; review stored todo records and avoid sensitive task content or private links. <br>
Risk: Broad automatic triggers, reminders, cron scheduling, and calendar synchronization can act on task-like messages without enough user intent. <br>
Mitigation: Make reminders, cron setup, and calendar sync explicit opt-in actions and confirm task details before syncing or notifying. <br>
Risk: Hard-coded Feishu recipient identifiers can route reminders or calendar attendees to the wrong account. <br>
Mitigation: Replace hard-coded Feishu user IDs with per-user configuration before installation or production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyu68/feishu-omni-todo) <br>
- [Feishu Open Platform APIs](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown-style Feishu replies, local JSON todo records, and command/script invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores tasks in ~/.openclaw/workspace/todo.json and may send reminders or create Feishu calendar events when configured.] <br>

## Skill Version(s): <br>
v1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
