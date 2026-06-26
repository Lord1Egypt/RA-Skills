## Description: <br>
FineBI skill for OpenClaw that helps agents query BI datasets, export dashboards, analyze reports, and coordinate selected outputs into Feishu documents, cards, tasks, or Bitable workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zsmj1994](https://clawhub.ai/user/zsmj1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, analysts, and operations teams use this skill to retrieve FineBI data, export dashboards, generate business-analysis reports, send Feishu briefings, create follow-up tasks, and synchronize BI data into Feishu Bitable. It is intended for business-data automation where users can provide FineBI credentials and verify downstream Feishu destinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access FineBI business data and export dashboards or datasets. <br>
Mitigation: Use least-privileged FineBI credentials and avoid sensitive datasets until permissions, retention, and sharing rules are clear. <br>
Risk: The skill can move BI outputs into Feishu documents, groups, tasks, and Bitable destinations. <br>
Mitigation: Verify each Feishu document, group, task owner, webhook, or Bitable target before sending or synchronizing data. <br>
Risk: Overwrite, scheduled-job, and deletion workflows can affect existing collaboration records or recurring automation. <br>
Mitigation: Review overwrite operations, scheduled-job changes, and task deletions carefully, and require confirmation for destructive or recurring actions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zsmj1994/finebi-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zsmj1994) <br>
- [Primary skill instructions](artifact/SKILL.md) <br>
- [Report-to-doc subskill](artifact/bi-report-to-doc/SKILL.md) <br>
- [Briefing subskill](artifact/skill-bi-briefing/SKILL.md) <br>
- [Alert-to-task subskill](artifact/skill-bi-skill-alert-to-task/SKILL.md) <br>
- [BI-to-Bitable subskill](artifact/skill-bi-to-bitable/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or structured text with tool-call guidance and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local file paths for exported dashboards and Feishu destination links when the connected tools return them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter version is 0.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
