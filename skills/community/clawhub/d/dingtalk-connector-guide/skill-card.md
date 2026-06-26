## Description: <br>
Guides users through connecting OpenClaw to a DingTalk bot for group message handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use this skill to configure a DingTalk internal app, bot webhook, permissions, and OpenClaw connection settings for workplace chat automation. <br>

### Deployment Geography for Use: <br>
Global, with practical focus on DingTalk enterprise deployments. <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags broad workplace data and secret access without enough privacy and scoping safeguards. <br>
Mitigation: Install only when authorized, obtain required consent, limit collection size and scope, and delete generated knowledge files when no longer needed. <br>
Risk: DingTalk app credentials and message or contact permissions can expose workplace data if over-scoped or shared in chat. <br>
Mitigation: Use a dedicated least-privilege DingTalk app, avoid pasting secrets into chat, and store tokens in a secure local secrets manager. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/dingtalk-connector-guide) <br>
- [DingTalk Open Platform](https://open.dingtalk.com) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential placeholders; users must supply their own DingTalk app values.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
