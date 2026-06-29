## Description: <br>
高考志愿填报AI参谋，支持AI初筛、数据查询、风险评估和志愿建议，覆盖全国31省市录取数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjfl888](https://clawhub.ai/user/hjfl888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External students and parents use this skill to plan Chinese gaokao applications by collecting profile details, comparing scores or rank against historical admissions data, and producing school, major, probability, and risk guidance. It is intended as an AI-assisted first pass, with final choices checked against official admissions materials and human judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist sensitive student, ranking, location, and family-income details in memory files. <br>
Mitigation: Collect only needed details, obtain clear user consent before storing them, and clear or disable stored profile and search-history data when counseling is finished. <br>
Risk: Admissions probabilities and recommendations can be wrong or outdated because score lines, rankings, plans, and policies change each year. <br>
Mitigation: Verify every recommendation against current provincial exam-authority materials, official university admissions documents, and one-score-one-rank tables before making decisions. <br>
Risk: Embedded consulting-service referrals may create perceived bias in guidance. <br>
Mitigation: Keep recommendations data-based, clearly separate optional paid consulting from admissions analysis, and avoid presenting referral offers as required next steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hjfl888/gaokao-gaowei-counselor) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/hjfl888) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with structured recommendation sections and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for and persist student profile and search-history details in memory files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
