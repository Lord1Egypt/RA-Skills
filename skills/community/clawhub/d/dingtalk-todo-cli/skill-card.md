## Description: <br>
Manage DingTalk tasks and todos using the official dws CLI, including task creation, tracking, DING-based escalation, AI sheet updates, calendar scheduling, and cross-platform task sync guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, team leads, and agent operators use this skill to plan, assign, monitor, and escalate DingTalk todos through dws CLI workflows. It is intended for workplace task management patterns such as daily standups, delegation tracking, overdue escalation, sprint planning, and meeting action-item follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to operate live DingTalk workflows, including DING messages, escalations, deletes, bulk sheet updates, raw API calls, approval, drive, bot, and cross-platform sharing actions. <br>
Mitigation: Require explicit user approval before executing live workflow commands, especially DING messages, escalations, deletes, raw API calls, approval/drive/bot actions, and Feishu or WeCom sharing. <br>
Risk: Escalation examples may send intrusive or high-severity notifications to managers, directors, or HR. <br>
Mitigation: Confirm recipient lists, urgency, message content, and working-hour constraints before sending DING escalations; do not run the Level 3 escalation example as written. <br>
Risk: Cross-platform task sync can disclose workplace task information outside DingTalk. <br>
Mitigation: Verify the business need, destination platform, recipients, and data minimization requirements before sharing to Feishu or WeCom. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lm203688/dingtalk-todo-cli) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lm203688) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose live DingTalk workflow commands that require user approval before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
