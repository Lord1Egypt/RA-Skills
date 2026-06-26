## Description: <br>
钉钉快速集成配置 - 5分钟连接 OpenClaw 与钉钉，解锁机器人消息、审批流程、智能办公。适合：企业用户、钉钉生态、国内企业。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and enterprise OpenClaw users use this skill to configure DingTalk bot messaging, alert notifications, daily briefs, and approval workflow integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook URLs and signing secrets can expose DingTalk bot access if committed, logged, or shared. <br>
Mitigation: Store webhook URLs and signing secrets securely, avoid committing or screenshotting configuration files, and use test webhooks for troubleshooting. <br>
Risk: Automatic approval-processing guidance is broad for a business workflow without clear user controls. <br>
Mitigation: Do not enable automatic approval processing unless actions are explicitly allowlisted, credentials are least-privilege, and a human confirms approve, reject, or modify decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yang1002378395-cmyk/dingtalk-quickstart-cn) <br>
- [DingTalk developer documentation](https://open.dingtalk.com/document) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code] <br>
**Output Format:** [Markdown with YAML, JSON, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl plus DingTalk webhook and optional signing-secret configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
