## Description: <br>
Operate DingTalk messaging APIs through UXC with a curated OpenAPI schema, app-token bearer auth, and robot/service-group guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to configure UXC authentication, inspect a curated DingTalk OpenAPI surface, look up DingTalk users, and send one-to-one, group, or service-group robot messages with explicit write-operation guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through DingTalk message-send operations. <br>
Mitigation: Require explicit user confirmation before every one-to-one, group, or service-group send operation. <br>
Risk: DingTalk app secrets and access tokens are required for authenticated API use. <br>
Mitigation: Store credentials in environment variables or UXC credential storage, avoid shared terminals for secrets, and use a least-privileged DingTalk app. <br>
Risk: The linked OpenAPI schema controls which DingTalk operations the generated CLI exposes. <br>
Mitigation: Review or pin the curated OpenAPI schema before linking the CLI in sensitive environments. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Curated DingTalk Messaging OpenAPI Schema](references/dingtalk-messaging.openapi.json) <br>
- [DingTalk Developer Docs](https://open.dingtalk.com/document/) <br>
- [ClawHub Skill Page](https://clawhub.ai/jolestar/dingtalk-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces UXC setup, authentication, schema-inspection, user lookup, and DingTalk message-send guidance; write operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
