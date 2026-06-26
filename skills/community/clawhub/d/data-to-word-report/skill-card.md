## Description: <br>
Automatically generate a professional Word analysis report from user-provided data files, including data overview, key metric statistics and trend analysis, key findings and conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to turn uploaded CSV, JSON, Excel, or TXT data into a structured Word analysis report with overview metrics, trend notes, and findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording could activate the skill for generic report requests. <br>
Mitigation: Confirm that the user actually wants structured data analysis and Word .docx output before invoking the report workflow. <br>
Risk: The skill processes user-provided datasets, which may contain sensitive information. <br>
Mitigation: Avoid sending sensitive datasets unless the user is comfortable with local agent processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/data-to-word-report) <br>
- [Publisher profile](https://clawhub.ai/user/openlark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance plus a generated .docx report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a JSON report structure with title, sections, paragraphs, and optional tables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
