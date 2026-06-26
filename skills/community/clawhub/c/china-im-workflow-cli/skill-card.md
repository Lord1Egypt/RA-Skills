## Description: <br>
Orchestrates cross-platform IM workflows across Feishu CLI, DingTalk Workspace CLI, and WeCom CLI for reporting, task sync, notifications, marketing distribution, and meeting coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business operations teams use this skill to guide agents in composing Feishu, DingTalk, and WeCom CLI commands for multi-platform enterprise messaging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to send broadcasts, urgent messages, customer-group messages, calendar invites, task updates, and document writes across enterprise IM platforms. <br>
Mitigation: Require explicit confirmation of platform, authenticated tenant/account, recipients, audience size, and final message or item content before executing generated commands. <br>
Risk: Cross-platform workflow commands may create inconsistent state if one platform operation fails after others succeed. <br>
Mitigation: Preview planned operations, execute in a controlled sequence, and report per-platform success or failure so the user can reconcile partial completion. <br>


## Reference(s): <br>
- [China IM Workflow CLI release page](https://clawhub.ai/lm203688/china-im-workflow-cli) <br>
- [Feishu/Lark CLI](https://github.com/larksuite/cli) <br>
- [DingTalk Workspace CLI](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli) <br>
- [WeCom CLI](https://github.com/WecomTeam/wecom-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should be reviewed against authenticated account, tenant, recipient, audience size, and message content before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
