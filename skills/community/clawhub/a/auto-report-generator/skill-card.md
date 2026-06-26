## Description: <br>
Auto Report Generator turns CSV or Excel files into formatted Excel reports with charts and optional AI-written analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiji0802](https://clawhub.ai/user/qiji0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data analysts, business operators, and developers use this skill to create recurring monthly, sales, financial, or comparison reports from spreadsheet data with less manual formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security review says the skill under-discloses external data and credential handling. <br>
Mitigation: Review or remove the geo-api.yk-global.com verification path before installation, and do not run it with sensitive OPENAI_API_KEY values unless that validation behavior is acceptable. <br>
Risk: Spreadsheet summaries can be sent to an OpenAI-compatible API when AI analysis is enabled. <br>
Mitigation: Use --no-ai for confidential spreadsheets or configure only an approved AI provider and endpoint for the data being processed. <br>
Risk: Artifact documentation includes cleanup commands that remove directories with rm -rf. <br>
Mitigation: Do not run the cleanup commands from SKILLHUB.md in a normal environment; inspect paths and use a disposable workspace for packaging cleanup. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qiji0802/auto-report-generator) <br>
- [README](artifact/README.md) <br>
- [ClawHub listing](artifact/CLAWHUB.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [Excel workbook (.xlsx), PNG chart images, and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AI analysis is optional and depends on configured provider credentials and quota settings.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
