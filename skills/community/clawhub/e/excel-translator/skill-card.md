## Description:

Translates Excel files (.xlsx) from English to Chinese while preserving formatting, images, and charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilove323](https://clawhub.ai/user/ilove323)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to translate English text in provided Excel workbooks into Chinese while preserving workbook layout and returning a translated .xlsx file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workbook text cells are sent to the configured OpenAI-compatible API endpoint.

Mitigation: Use only with spreadsheets whose data is approved for that external service; avoid confidential, regulated, financial, or personal spreadsheets unless policy permits it.

Risk: The script reads API credentials from local secret files or environment variables and honors OPENAI_BASE_URL.

Mitigation: Verify OPENAI_BASE_URL and credential source before running, and scope credentials to the intended translation service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ilove323/skills/excel-translator)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and a generated .xlsx workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes .xlsx workbooks and writes Chinese translations below the original text in each translated cell when successful.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
