## Description: <br>
医生工作台助手。整理患者基本信息、关键时间线、检验趋势、待办事项并生成随访任务草稿。当用户以医生身份查询患者情况或需要随访建议时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergenceronearth](https://clawhub.ai/user/emergenceronearth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Doctors and clinical workflow users use this skill to organize a local demo patient record into patient context, timeline, lab trends, to-do items, and follow-up task drafts for clinician review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads patient-related demo data and may surface sensitive patient information. <br>
Mitigation: Install only where the referenced demo patient JSON is authorized for use, treat generated patient-related output as sensitive, and verify that no real patient identifiers are exposed unintentionally. <br>
Risk: Generated follow-up tasks could be mistaken for clinical direction. <br>
Mitigation: Have a clinician review generated follow-up tasks before acting on them. <br>
Risk: The skill posts progress updates to a localhost reporting endpoint. <br>
Mitigation: Install only where the localhost reporting endpoint is expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emergenceronearth/agentic-doctor-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/emergenceronearth) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs patient summaries, event timelines, lab trend notes, prioritized to-do items, and follow-up task drafts.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
