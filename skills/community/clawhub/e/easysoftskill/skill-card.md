## Description: <br>
易软（EasySoft）数据查询 Skill，当用户询问易软系统内的数据报表时触发，覆盖报表、数据查询、收缴率、预收率、清欠率、欠费、应收、实收和月报等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xjwang2002](https://clawhub.ai/user/xjwang2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
物业管理公司的财务、运营和管理人员 use this skill to query EasySoft property-management reports through guided natural-language workflows. The current release focuses on arrears reporting and also documents report types for collection rate, receivables, receipts, and monthly summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles EasySoft company keys, usernames, passwords, and business report data. <br>
Mitigation: Use a least-privilege or read-only EasySoft account where possible, confirm local credential storage behavior before use, and avoid administrator credentials. <br>
Risk: Broad report-related triggers could activate the skill for generic reporting requests. <br>
Mitigation: Confirm the request is intended for EasySoft before entering credentials or running report queries. <br>
Risk: Several documented report types are marked as still in development. <br>
Mitigation: Rely on the listed online arrears report workflow for production use and treat unavailable report types as roadmap items. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xjwang2002/easysoftskill) <br>
- [Publisher profile](https://clawhub.ai/user/xjwang2002) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown tables and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides users through credential setup, report parameter selection, confirmation, and tabular report presentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
