## Description:

No-code cross-platform automation for ClawHub with WeChat, DingTalk, Feishu, WPS, Tencent Docs, and Aliyun Drive integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create, configure, and monitor no-code automation workflows across messaging, office, document, and cloud-drive platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive cross-platform data movement may expose account data or files before authorization and approval controls are hardened.

Mitigation: Review OAuth handling, enforce least-privilege scopes and workflow approvals, and use test accounts before connecting real accounts or sensitive files.

Risk: Workflow execution and export features can move logs or files to unintended destinations if paths and confirmations are not constrained.

Mitigation: Require confirmation prompts, safe export directories, audit logging review, and dependency pinning before production deployment.

## Reference(s):

- [ClawHub Automation Release Page](https://clawhub.ai/kaiyuelv/skills/clawhub-automation)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workflow definitions, connector configuration guidance, monitoring steps, and permission review guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
