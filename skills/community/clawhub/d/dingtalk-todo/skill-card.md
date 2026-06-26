## Description: <br>
Dingtalk Todo helps agents manage DingTalk todo tasks, including creating, listing, updating, completing, assigning, and deleting tasks through DingTalk APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breath57](https://clawhub.ai/user/breath57) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to operate DingTalk todo workflows from an agent, including personal task management and collaboration tasks that involve other users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores DingTalk credentials and bearer tokens in a local configuration file. <br>
Mitigation: Use a least-privileged DingTalk app and protect ~/.dingtalk-skills/config as sensitive data. <br>
Risk: The skill can create, update, complete, assign, and delete real business tasks, and broad triggers could invoke it unexpectedly. <br>
Mitigation: Require explicit confirmation before any task-changing action, especially when the request does not clearly specify DingTalk. <br>


## Reference(s): <br>
- [DingTalk Todo API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/breath57/dingtalk-todo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and API response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist DingTalk credentials and access tokens locally while executing requested task operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
