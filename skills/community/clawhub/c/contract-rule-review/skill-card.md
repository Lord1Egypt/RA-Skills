## Description: <br>
合同规则审阅助手 - 上传本地合同文件到 AnyShare 并调用规则审阅技能进行自动化审阅，支持保存结果和生成分享链接 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[susan-meng](https://clawhub.ai/user/susan-meng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, legal operations teams, and contract reviewers use this skill to upload local contracts to AnyShare, apply rule-review templates, generate an automated review report, and save the result in a structured document library location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads sensitive contract files to AnyShare and processes them through review and indexing services. <br>
Mitigation: Run it only where organizational policy permits this processing, confirm the file and destination folder before execution, and use a least-privileged token. <br>
Risk: The skill can generate a share link for the review report. <br>
Mitigation: Create or retain share links only when sharing is explicitly required, and revoke links that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/susan-meng/contract-rule-review) <br>
- [Publisher Profile](https://clawhub.ai/user/susan-meng) <br>
- [Security Audit Checklist](artifact/SECURITY.md) <br>
- [Troubleshooting Guide](artifact/references/troubleshooting.md) <br>
- [AnyShare MCP Endpoint](https://anyshare.aishu.cn/asmcp/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review reports with setup guidance and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured AnyShare access token and personal document library GNS; generated reports may include share links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
