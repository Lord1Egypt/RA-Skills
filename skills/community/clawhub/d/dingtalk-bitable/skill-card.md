## Description: <br>
DingTalk Bitable API integration for table management and record CRUD operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cxwos](https://clawhub.ai/user/cxwos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect DingTalk Bitable tables and manage records, fields, and table metadata through a configured DingTalk app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, and change schema for DingTalk Bitable data when invoked with valid credentials. <br>
Mitigation: Use least-privilege DingTalk app permissions and explicitly confirm table, record, and field targets before write or schema-changing actions. <br>
Risk: Configured DingTalk app credentials allow the agent to access Bitable data within the app's granted scope. <br>
Mitigation: Store credentials only in the intended environment or OpenClaw configuration and rotate them if access scope changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cxwos/dingtalk-bitable) <br>
- [DingTalk Tables documentation](https://open.dingtalk.com/document/orgapp/overview-of-dingtalk-tables) <br>
- [DingTalk Open Platform API reference](https://open.dingtalk.com/document/orgapp) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Text, Configuration guidance] <br>
**Output Format:** [JSON responses and concise text status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DingTalk app credentials and permissions for the targeted Bitable workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
