## Description: <br>
合同规则审阅助手 - 上传本地合同文件到 AnyShare 并调用规则审阅技能进行自动化审阅，支持保存结果和生成分享链接 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyshare-aishu](https://clawhub.ai/user/anyshare-aishu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Contract, legal operations, and business users can use this skill to upload a local contract to AnyShare, run an automated rule review with built-in or custom templates, save a Markdown review report, and generate a share link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contract uploads, stored review reports, generated share links, and AnyShare tokens are sensitive. <br>
Mitigation: Use a least-privilege token when available, keep mcporter configuration private, verify the AnyShare account and link permissions, and remove local or cloud copies that are no longer needed. <br>
Risk: Automated contract review results may be incomplete or unsuitable for direct legal reliance. <br>
Mitigation: Review the generated Markdown report with qualified legal or business stakeholders before acting on findings. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anyshare-aishu/as-contract-rule-review) <br>
- [Security Checklist](SECURITY.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command, JSON, and TOML snippets; the workflow saves a Markdown review report and share link in AnyShare.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AnyShare access token and a user-selected contract file; outputs should be reviewed before relying on them for legal or business decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
