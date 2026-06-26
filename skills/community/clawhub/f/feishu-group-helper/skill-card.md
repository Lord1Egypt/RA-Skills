## Description: <br>
Manage Feishu group records, track bot join and leave status, and help agents send messages to confirmed Feishu groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panmenglin](https://clawhub.ai/user/panmenglin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Feishu bot operators use this skill to maintain per-agent Feishu group records, confirm active groups, and send group messages through a Feishu bot when a user requests it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A fuzzy group-name match could select an unintended Feishu group. <br>
Mitigation: Confirm the exact target group and chat ID before sending messages or updating records. <br>
Risk: The skill can update stored Feishu group records and mark groups active or removed. <br>
Mitigation: Review requested add, remove, or sync operations before allowing the agent to persist changes. <br>
Risk: A drafted group message could be sent to a live Feishu chat. <br>
Mitigation: Confirm the message text and destination immediately before using Feishu bot send permissions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/panmenglin/feishu-group-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript snippets and operational steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update feishu-groups.json in the agent workspace and may send Feishu bot messages when directed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
