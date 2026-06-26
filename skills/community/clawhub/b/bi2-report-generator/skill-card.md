## Description: <br>
Generates BI2 business analysis reports as HTML from PPTX screenshot data and can save and share the report through Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard052317](https://clawhub.ai/user/richard052317) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts and operations teams use this skill to turn PPTX screenshots of BI2 sales, margin, expense, customer, product, inventory, accounts receivable, and forecast data into a structured HTML operating report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds Feishu credentials. <br>
Mitigation: Rotate the exposed Feishu secret before use and replace hardcoded credentials with user-scoped configuration. <br>
Risk: The skill can upload local files with limited user control. <br>
Mitigation: Require confirmation of the exact file path and Feishu recipient before every send. <br>
Risk: Generated reports may contain sensitive business data. <br>
Mitigation: Run only in controlled workspaces and share reports only with approved recipients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richard052317/bi2-report-generator) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Report generator script](artifact/generator.py) <br>
- [HTML report template](artifact/report_template.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated HTML report files and Python execution steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local report paths and Feishu sharing actions when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
