## Description:

FlowBridge helps users create no-code automation workflows across WeChat, DingTalk, Feishu, WPS, Tencent Docs, and Aliyun Drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use FlowBridge to generate, configure, execute, and monitor cross-platform automation workflows for chat, document, approval, file-sync, and notification scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages sensitive cross-platform workflows involving chat, files, approvals, and cloud storage while evidence.security says the advertised controls are not strong enough.

Mitigation: Review before installing in a real workspace and require explicit admin approval plus workflow execution authorization before connecting live platform credentials.

Risk: Connector behavior involves OAuth-style authorization and broad read/write workflow actions across WeChat, DingTalk, Feishu, WPS, Tencent Docs, and Aliyun Drive.

Mitigation: Do not connect real credentials until platform scopes are reviewed, dependencies are pinned, and least-privilege access is enforced.

Risk: Execution and audit logs can be exported and may contain workflow, chat, file, approval, or user activity details.

Mitigation: Require audit-export permissions, safe export paths, and privacy warnings for templates or workflows that handle chat, file, approval, or user data.

## Reference(s):

- [FlowBridge ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/flowbridge)
- [FlowBridge README](artifact/README.md)
- [FlowBridge skill definition](artifact/SKILL.md)
- [Connector configuration](artifact/config/connectors.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; workflow objects and JSON/CSV logs when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate workflow configurations, connector setup guidance, execution reports, audit records, and exportable logs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
