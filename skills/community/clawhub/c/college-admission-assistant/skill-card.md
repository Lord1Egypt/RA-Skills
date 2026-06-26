## Description: <br>
A Chinese Gaokao college-admissions planning assistant that helps students, families, and teachers with subject selection, volunteer application strategy, university and major lookup, score analysis, and admissions policy interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to plan Chinese college admissions decisions, including new-Gaokao subject combinations, application gradients, institution and major comparisons, score-band interpretation, and policy lookups. It supports offline reference-data use by default and optional API-backed commercial mode for current admissions data. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Admissions guidance can become outdated or differ by province and year. <br>
Mitigation: Label sources and years in responses, use official provincial education-exam sources for final decisions, and state when detailed provincial data is unavailable. <br>
Risk: Optional commercial/API mode can expose API keys or rely on an untrusted endpoint. <br>
Mitigation: Enable API mode only with a trusted endpoint and provider, keep COLLEGE_ADMISSION_API_KEY secret, and fall back to offline reference guidance when API calls fail. <br>
Risk: Personal admissions planning may involve sensitive identity, score, ranking, or contact details. <br>
Mitigation: Avoid collecting or repeating unnecessary personal information and do not output non-public admissions data. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/yezhaowang888-stack/college-admission-assistant) <br>
- [New Gaokao guide](references/xinkao-guide.md) <br>
- [University reference database](references/universities.md) <br>
- [Gaokao policy knowledge base](references/policies.md) <br>
- [Jiangsu province reference](references/provinces/jiangsu.md) <br>
- [Zhejiang province reference](references/provinces/zhejiang.md) <br>
- [Shandong province reference](references/provinces/shandong.md) <br>
- [Beijing reference](references/provinces/beijing.md) <br>
- [Shanghai reference](references/provinces/shanghai.md) <br>
- [Henan province reference](references/provinces/henan.md) <br>
- [Hebei province reference](references/provinces/hebei.md) <br>
- [Hubei province reference](references/provinces/hubei.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown guidance with optional JSON script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers should label data source and year, avoid unsupported estimates, protect personal data, and direct final decisions to official provincial education-exam sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
