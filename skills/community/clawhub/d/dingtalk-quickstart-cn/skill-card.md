## Description:

钉钉快速集成配置 helps OpenClaw users connect DingTalk for robot messages, approval workflows, and intelligent office automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and enterprise users use this skill to configure OpenClaw with DingTalk webhooks, signing secrets, message templates, and troubleshooting steps for workplace messaging and approval automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DingTalk webhook tokens and signing secrets can grant message-sending access if exposed.

Mitigation: Keep webhook credentials out of source control, logs, screenshots, and shared chats; restrict config file permissions and rotate exposed webhooks.

Risk: Automated DingTalk messages may include sensitive customer, employee, approval, or incident details.

Mitigation: Send business data only to approved DingTalk groups and review message templates before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/skills/dingtalk-quickstart-cn)
- [DingTalk Developer Documentation](https://open.dingtalk.com/document)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with YAML, JSON, shell command, and text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and DingTalk webhook credentials supplied by the user.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
