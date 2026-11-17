## Description:

Uploads Excel and CSV files to Volcengine DataAgent and converts them into structured Markdown reports with table-aware formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and workflow agents use this skill to analyze Excel or CSV files and turn spreadsheet content into Markdown documents or reports. It is suitable when tabular data needs to be uploaded to DataAgent for structured document generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet contents are uploaded to Volcengine DataAgent for processing.

Mitigation: Use the skill only with files approved for that service and avoid sending sensitive spreadsheets unless the deployment policy permits it.

Risk: The skill requires Volcengine access keys and can also accept credentials as command-line arguments.

Mitigation: Provide narrowly scoped credentials through protected environment variables and avoid pasting long-lived AK/SK values into chat or shell history.

Risk: A configurable API endpoint can redirect processing away from the intended service if PUBLIC_INSIGHT_API_URL is changed.

Mitigation: Keep PUBLIC_INSIGHT_API_URL unset or locked to the intended HTTPS Volcengine endpoint before execution.

Risk: The artifact suppresses detailed setup and error output during normal runs.

Mitigation: Review installation, dependency, and runtime behavior before deployment and monitor executions through approved operational logging.

## Reference(s):

- [Volcengine DataAgent](https://www.volcengine.com/product/DataAgent)
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-data-deepresearch-structured2markdown)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report written to a local file, with concise user-facing status or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts Excel (.xls, .xlsx) and CSV (.csv) file paths and requires Volcengine access credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
