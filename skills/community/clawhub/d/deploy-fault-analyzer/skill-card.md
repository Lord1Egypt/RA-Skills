## Description: <br>
部署故障分析及解决助手 — 接收日志/报错文本，优先查询 MySQL 故障知识库；未命中时检索 /data/scripts/ 脚本库；支持交互式单条更新故障库并生成 Word 分析报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bounding-elk](https://clawhub.ai/user/bounding-elk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Deployment and operations engineers use this skill to analyze deployment logs or pasted error text, compare issues with a MySQL fault knowledge base, search deployment scripts when no matching case is found, and produce a troubleshooting summary and Word report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment logs, generated reports, Excel records, and MySQL inserts may preserve secrets, hostnames, customer data, credentials, tokens, or personal identifiers. <br>
Mitigation: Use the skill only in an approved environment, redact sensitive values before analysis or storage, and review or delete raw archives, reports, Excel records, and MySQL inserts after use. <br>
Risk: Troubleshooting findings or knowledge-base updates may republish inaccurate or sensitive operational details. <br>
Mitigation: Review the generated summary, Word report, JSON draft, and dry-run output before sharing or committing any new fault record. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bounding-elk/skills/deploy-fault-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/bounding-elk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown troubleshooting summary with generated DOCX reports, JSON drafts, Excel records, and shell command blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May preserve raw logs and produce Word reports, Excel knowledge-base rows, and MySQL insert drafts in the configured skill workspace.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
