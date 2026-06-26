## Description: <br>
Guides agents through a confirmed OpenClaw agent deletion workflow that lists agents, asks for confirmation, moves selected agent data to local trash, and records deletion history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangyangupday](https://clawhub.ai/user/yangyangupday) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to delete one or more configured agents through a confirmation-gated flow with local trash backups and deletion history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user could confirm deletion for the wrong OpenClaw agent or workspace. <br>
Mitigation: Before confirming deletion, verify the selected agent IDs and workspace paths shown by the skill. <br>
Risk: The skill intentionally moves agent data and removes residual agent directories. <br>
Mitigation: Use the local trash paths and history records for recovery checks, and review complete script output before retrying or using manual fallback. <br>
Risk: Deleted agents may still have related channel bindings or gateway state that needs attention. <br>
Mitigation: After deletion, inspect OpenClaw bindings and restart the gateway when operationally required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangyangupday/agent-del) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands, numbered confirmation steps, and deletion status checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the OpenClaw CLI; deletion is gated by explicit user confirmation and local trash backup handling.] <br>

## Skill Version(s): <br>
1.10.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
