## Description: <br>
将研究变量映射到院内数据字典，评估 Cohort 可行性（候选样本量、缺失率、风险提示），并生成纳排标准草案。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergenceronearth](https://clawhub.ai/user/emergenceronearth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, clinical data analysts, and agent workflows use this skill to map study variables to an institutional data dictionary, evaluate cohort feasibility, and draft inclusion and exclusion criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a fixed demo cohort data path that could contain sensitive patient data if repurposed. <br>
Mitigation: Confirm the file is intended for this workflow and does not contain sensitive real patient data before use. <br>
Risk: The skill posts progress messages to a localhost reporting endpoint. <br>
Mitigation: Use it only when the local report service is expected, and avoid including sensitive data in status messages. <br>
Risk: Generated cohort feasibility findings and draft criteria may be incomplete or unsuitable for a study protocol without expert review. <br>
Mitigation: Review variable mappings, missingness, risk notes, and inclusion or exclusion criteria with qualified domain reviewers before relying on them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis] <br>
**Output Format:** [Markdown tables and lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes variable mapping tables, cohort overview metrics, risk notes, draft inclusion and exclusion criteria, and optional group-preview counts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
