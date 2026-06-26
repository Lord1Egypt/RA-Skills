## Description: <br>
Uploads Excel and CSV files to Volcengine DataAgent and converts the cloud-generated analysis into structured Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and business users use this skill to upload spreadsheet data for remote analysis and receive a formatted Markdown report for documentation, reporting, or downstream agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected spreadsheets are sent to Volcengine DataAgent for remote analysis and report generation. <br>
Mitigation: Install and run only when the user is comfortable sending those files to Volcengine DataAgent. <br>
Risk: The skill requires Volcengine cloud credentials and may expose risk if long-lived keys are pasted into chat or reused broadly. <br>
Mitigation: Use least-privilege or temporary credentials through environment variables or a secret manager, and clear them after use. <br>
Risk: A custom PUBLIC_INSIGHT_API_URL can redirect processing to a destination the user may not fully trust. <br>
Mitigation: Avoid setting PUBLIC_INSIGHT_API_URL unless the destination is explicitly trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-data-deepresearch-structured2markdown) <br>
- [Volcengine DataAgent product page](https://www.volcengine.com/product/DataAgent) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown file generated from cloud-processed spreadsheet analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Excel or CSV file paths and Volcengine credentials; selected files are uploaded to Volcengine DataAgent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
