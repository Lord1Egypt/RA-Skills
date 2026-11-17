## Description:

将研究变量映射到院内数据字典，评估 Cohort 可行性（候选样本量、缺失率、风险提示），并生成纳排标准草案。当用户需要做数据映射或队列可行性分析时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergenceronearth](https://clawhub.ai/user/emergenceronearth)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and clinical analytics teams use this skill to map study variables to an internal data dictionary, assess cohort feasibility, review missingness and risk notes, and draft inclusion and exclusion criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reports run status and aggregate cohort counts to a localhost endpoint.

Mitigation: Run it only in environments where http://localhost:5001/api/report is expected and aggregate cohort counts are acceptable to send there.

Risk: The skill reads a fixed local cohort data file.

Mitigation: Confirm that the configured cohort file path and data classification are approved for the intended analysis environment before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emergenceronearth/skills/agentic-cohort-analyst)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables and concise status text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads the configured local cohort JSON file and reports run status to the configured localhost endpoint.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
