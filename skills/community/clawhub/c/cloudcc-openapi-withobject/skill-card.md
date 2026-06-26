## Description: <br>
Provides CloudCC OpenAPI guidance and helper shell scripts for authentication, CRM object metadata lookup, data operations, file services, messaging, Chatter, approval workflows, and API logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[androidxhm](https://clawhub.ai/user/androidxhm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to configure CloudCC credentials, retrieve access tokens, inspect object and field metadata, and run authenticated CRM API calls for data, files, messaging, Chatter, and approvals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence identifies exposed CloudCC credential material and an access token in the packaged configuration. <br>
Mitigation: Rotate or remove the exposed credentials and token, replace config.json with a template, and require users to provide their own credentials during setup. <br>
Risk: The skill can perform broad CRM-changing actions, including data mutation, outbound messaging, file operations, Chatter actions, and approval workflow actions. <br>
Mitigation: Use a least-privileged CloudCC app and require explicit user confirmation before destructive, outbound, file, Chatter, or approval operations. <br>
Risk: Configuration and API logs may contain sensitive CloudCC organization, object, response, or authentication details. <br>
Mitigation: Restrict permissions on configuration and log files, keep log retention short, and review logs before sharing or publishing artifacts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/androidxhm/cloudcc-openapi-withobject) <br>
- [CloudCC OpenAPI overview](https://help.cloudcc.cn/product03/apigai-lan/) <br>
- [CloudCC help documentation](https://help.cloudcc.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts can update local CloudCC configuration, write API logs, and send authenticated outbound CloudCC requests when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact files mention 2.0.0 and 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
