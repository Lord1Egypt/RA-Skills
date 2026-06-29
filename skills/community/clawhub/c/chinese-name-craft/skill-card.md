## Description: <br>
Chinese Name Craft guides an agent through a traditional Chinese naming workflow using Bazi, Wuxing, and name-study references to generate candidate names, analysis, JSON, and an optional Word report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruokkkkk](https://clawhub.ai/user/ruokkkkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect birth and naming preferences, perform traditional Chinese Bazi, Wuxing, and name-study analysis, generate candidate Chinese names, and prepare a local Word report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses birth date, birth time, and family naming details that may be sensitive. <br>
Mitigation: Use the skill only with informed user consent, avoid unnecessary retention, and review where generated reports are stored locally. <br>
Risk: The Word export path can install python-docx automatically if it is missing. <br>
Mitigation: Review the generated JSON first and prefer installing python-docx explicitly before running the export. <br>
Risk: Traditional naming, Bazi, Wuxing, and numerology analysis may be mistaken if treated as determinative advice. <br>
Mitigation: Treat the analysis as cultural and advisory, verify input birth details, and let user preference drive the final name choice. <br>


## Reference(s): <br>
- [Bazi and Wuxing Reference](references/bazi-wuxing.md) <br>
- [Name Study Numerology Reference](references/name-study.md) <br>
- [Output Template and JSON Schema](references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, JSON, shell commands, files] <br>
**Output Format:** [Markdown guidance with structured JSON data and optional DOCX file generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate a local Word document from user-provided birth and family naming details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
