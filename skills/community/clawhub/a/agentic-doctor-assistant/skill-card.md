## Description:

医生工作台助手。整理患者基本信息、关键时间线、检验趋势、待办事项并生成随访任务草稿。当用户以医生身份查询患者情况或需要随访建议时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergenceronearth](https://clawhub.ai/user/emergenceronearth)

### License/Terms of Use:

MIT-0

## Use Case:

Doctors and clinical-demo users use this skill to summarize a demo patient record, review key events and lab trends, list open tasks, and draft follow-up task details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local reporting endpoint could log or forward sensitive patient content if future payloads include clinical details.

Mitigation: Confirm that http://localhost:5001/api/report is the intended local service and keep status payloads free of patient identifiers, notes, lab details, or clinical summaries unless explicit consent and controls are in place.

Risk: The skill reads from a fixed demo patient-data path.

Mitigation: Confirm the file contains demo or de-identified data before use and avoid repointing the workflow to identifiable patient records without appropriate governance.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary with inline shell commands for local status reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a fixed demo patient JSON file and posts limited running/completed status updates to a local reporting endpoint.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
