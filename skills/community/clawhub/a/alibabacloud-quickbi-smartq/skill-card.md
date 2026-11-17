## Description: <br>
Quick BI-SmartQ routes user requests across Quick BI file and dataset Q&A, document parsing, dashboard skill generation, data insights, and data-report workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to route natural-language Quick BI requests into file Q&A, dataset Q&A, document extraction, dashboard skill generation, insight analysis, or report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload business files, dashboards, and datasets to Alibaba Cloud Quick BI services. <br>
Mitigation: Install only when Quick BI processing is intended and approved for the relevant files; avoid uploading sensitive or regulated documents unless organizational policy permits it. <br>
Risk: The skill uses sensitive Quick BI credentials and can create or persist identity data in workspace and global QBI configuration files. <br>
Mitigation: Use least-privilege Quick BI credentials, avoid global credential storage where possible, and review changes to ~/.qbi and workspace .qbi folders. <br>
Risk: Dashboard workflows can generate skills and may install or overwrite generated skill names. <br>
Mitigation: Require explicit confirmation before installing a generated skill or reusing an existing skill name. <br>
Risk: The report workflow may use online search behavior while producing reports. <br>
Mitigation: Use report generation only when online search is acceptable for the user's data and business context. <br>


## Reference(s): <br>
- [Quick BI-SmartQ Skill Definition](artifact/SKILL.md) <br>
- [Chat Module](artifact/references/chat/module-chat.md) <br>
- [Dashboard Skill Generator](artifact/references/dashboard/module-dashboard.md) <br>
- [Dashboard Generator Reference](artifact/references/dashboard/module-dashboard-reference.md) <br>
- [Document Parser](artifact/references/document/module-document-parser.md) <br>
- [Document Classification Fields](artifact/references/document/document_classification.md) <br>
- [Data Insight Module](artifact/references/insight/module-data-insight.md) <br>
- [Data Report Module](artifact/references/report/module-data-report.md) <br>
- [Quick BI Smart Product Page](https://www.aliyun.com/product/quickbi-smart?utm_content=g_1000411205) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with shell commands, API result summaries, generated file paths, chart or table references, and report links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce generated Quick BI query skills, structured Excel outputs, chart image paths, JSON data paths, trace IDs, or report replay links depending on the routed workflow.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata; artifact metadata version 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
