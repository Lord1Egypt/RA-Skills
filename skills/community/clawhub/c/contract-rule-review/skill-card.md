## Description:

合同规则审阅助手 - 上传本地合同文件到 AnyShare 并调用规则审阅技能进行自动化审阅，支持保存结果和生成分享链接

This skill is ready for commercial/non-commercial use.

## Publisher:

[susan-meng](https://clawhub.ai/user/susan-meng)

### License/Terms of Use:

MIT-0

## Use Case:

Contract reviewers, legal operations teams, and business users use this skill to upload local contracts to AnyShare, apply built-in or user-provided review templates, run rule review, and save Markdown review reports with share links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive contract files and uploads them to AnyShare for review.

Mitigation: Use only contracts the user is authorized to upload, keep the AnyShare token least-privileged, and create or share report links only with approved recipients and clear retention expectations.

Risk: Server security evidence reports a verified filename-based code-injection flaw in the documented workflow.

Mitigation: Avoid processing files from untrusted sources or with untrusted filenames until the filename handling flaw is fixed and reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/susan-meng/skills/contract-rule-review)
- [Security Audit Checklist](SECURITY.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [General Contract Review Template](templates/通用合同审阅模板.md)
- [Service Contract Review Template](templates/服务合同审阅模板.md)
- [Procurement Contract Review Template](templates/采购合同审阅模板.md)
- [AnyShare MCP Service](https://anyshare.aishu.cn/asmcp/)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown review report, file uploads, saved report file, and share link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AnyShare access token, an AnyShare MCP service configuration, and authorized contract files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
