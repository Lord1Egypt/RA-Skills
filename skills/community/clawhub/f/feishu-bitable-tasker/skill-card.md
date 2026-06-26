## Description: <br>
Helps an agent manage tasks in Feishu knowledge-base Bitable and document workflows, including task creation, linked document creation, status updates, and task summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KwokKwok](https://clawhub.ai/user/KwokKwok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure a dedicated Feishu app and run task-management commands against an authorized knowledge-base Bitable. It is intended for creating task records, generating linked task documents, updating status, and checking task statistics from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Feishu App ID and App Secret credentials and can write to Feishu Bitable, wiki, and document resources. <br>
Mitigation: Use a dedicated Feishu app, store credentials outside shared or synced folders with strict permissions, and do not paste real App Secrets into chat. <br>
Risk: Commands can create, update, validate, and potentially delete Feishu data in the configured workspace. <br>
Mitigation: Start with a test or isolated workspace, verify each app_token and table_id before running destructive or cleanup commands, and treat validation as a real write test. <br>
Risk: Overbroad Feishu permissions can expand the blast radius if credentials are misused. <br>
Mitigation: Grant the app only to the intended knowledge-base Bitable resource and confirm the required permission level before use. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Feishu task records and wiki documents when commands are executed with valid credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
