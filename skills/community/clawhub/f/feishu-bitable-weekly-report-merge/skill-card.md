## Description: <br>
飞书多维表格周报权限检查与合并一体化工具，用户输入一个飞书多维表格 URL 后，它提取「链接地址」列、检查飞书文档阅读权限，并在用户确认后将可访问文档按章节合并为新文档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ganguagua](https://clawhub.ai/user/ganguagua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and team coordinators who collect weekly reports in Feishu Bitable use this skill to check which linked report documents are readable, review accessible and inaccessible lists, and merge accessible reports into a consolidated Feishu document after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Readable weekly-report content may be copied into a newly created Feishu document during the merge step. <br>
Mitigation: Review the accessible document list before confirming the merge, and proceed only when the listed documents are intended to be combined. <br>
Risk: Documents without current Feishu read permission should not be included in the merged output. <br>
Mitigation: Use the permission-check result as the merge boundary and include only documents reported as accessible. <br>


## Reference(s): <br>
- [Merge Rules Reference](references/merge_rules.md) <br>
- [Permission Rules Reference](references/permission_rules.md) <br>
- [ClawHub release page](https://clawhub.ai/ganguagua/feishu-bitable-weekly-report-merge) <br>
- [Publisher profile](https://clawhub.ai/user/ganguagua) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown status report with accessible and inaccessible document lists, a confirmation prompt, and a final Feishu document link when a merge is completed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a merged Feishu document only after the user confirms the merge step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
