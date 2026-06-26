## Description: <br>
Interprets physical exam reports from uploaded images, PDFs, or pasted text by explaining indicators, identifying abnormal values, and giving plain-language health suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marson2016](https://clawhub.ai/user/marson2016) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to understand body check and lab report values, compare results against report-provided or bundled reference ranges, and identify which abnormal results may warrant follow-up. It is educational guidance and not a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive health information from medical reports. <br>
Mitigation: Redact unnecessary identifiers before use and avoid sharing report content beyond the intended agent session. <br>
Risk: The output could be mistaken for a diagnosis. <br>
Mitigation: Treat interpretations as educational guidance and consult a clinician for serious, persistent, or clearly abnormal results. <br>
Risk: Reference ranges vary by hospital and testing method. <br>
Mitigation: Prefer the reference ranges printed on the uploaded report before using the bundled common ranges. <br>


## Reference(s): <br>
- [Common Physical Exam Indicator Reference Ranges](references/ranges.md) <br>
- [ClawHub Release Page](https://clawhub.ai/marson2016/body-report-interpreter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with tables, abnormal-value explanations, and follow-up suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses report-provided reference ranges first, then bundled common ranges; avoids diagnosis and recommends clinician follow-up for clearly abnormal results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
