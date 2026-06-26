## Description: <br>
DingTalk API helps agents query DingTalk users and departments, send robot messages, and manage OA approval workflows through DingTalk Open Platform scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ogenes](https://clawhub.ai/user/ogenes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operations teams use this skill to automate DingTalk directory lookups, department queries, robot messaging, resigned or inactive employee checks, and OA approval workflow actions with app credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read employee and workflow data when supplied DingTalk app credentials. <br>
Mitigation: Use a dedicated DingTalk app with least-privilege scopes and install only where the operator controls the credentials. <br>
Risk: Approval and messaging commands can modify workflows or send messages on behalf of a DingTalk app. <br>
Mitigation: Require human confirmation before approval-write operations or message sends, and avoid enabling approval-write permissions unless they are required. <br>
Risk: Debug output may expose employee or workflow data in shared logs. <br>
Mitigation: Avoid --debug in shared environments and treat command output as sensitive operational data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ogenes/dingtalk-api) <br>
- [Publisher profile](https://clawhub.ai/user/ogenes) <br>
- [DingTalk Open Platform](https://open.dingtalk.com/) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs TypeScript scripts with DingTalk app credentials and returns structured success or error JSON.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
