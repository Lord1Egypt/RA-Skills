## Description: <br>
Enables Feishu group chat robots to detect @mentions, extract tasks, request developer confirmation, remember approval preferences, and return task results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongjie888wang-commits](https://clawhub.ai/user/yongjie888wang-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate Feishu group-chat robot workflows where one robot can ask another robot to handle a task, seek developer approval when needed, and report the result back to the chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat-triggered tasks could run outside the intended developer control because sender checks and approval-memory logic are weak. <br>
Mitigation: Use only in trusted Feishu groups and low-risk workflows unless sender allowlisting, approval verification against FEISHU_DEVELOPER_ID, corrected confirmation memory handling, protected MEMORY_PATH storage, and sensitive-text minimization are added. <br>


## Reference(s): <br>
- [Feishu robot configuration guide](references/config.md) <br>
- [ClawHub skill page](https://clawhub.ai/yongjie888wang-commits/feishu-robot-interact) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and Python script output as JSON-compatible dictionaries or chat message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Feishu message payloads, environment variables, and a local JSON memory file for approval preferences.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
