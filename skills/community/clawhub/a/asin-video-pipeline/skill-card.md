## Description: <br>
ASIN营销视频全自动流水线 helps agents guide setup of an n8n, Topview AI, Apify, and Google Sheets workflow for turning ASIN lists into Amazon product marketing videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkk402373342](https://clawhub.ai/user/kkk402373342) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and automation engineers use this skill to configure and validate a workflow that reads ASINs from Google Sheets, retrieves product data, generates preview videos, supports review, and exports final marketing videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends ASIN and product data from Google Sheets to Apify and Topview AI. <br>
Mitigation: Use least-privilege API keys, share the service account only with the intended spreadsheet, and avoid placing sensitive internal notes in processed columns. <br>
Risk: Automated scheduling can consume third-party quotas or incur costs before behavior is confirmed. <br>
Mitigation: Test on a copy of the sheet first and enable scheduling only after confirming cost, quota, and update behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kkk402373342/asin-video-pipeline) <br>
- [Workflow setup guide](references/WORKFLOW_SETUP.md) <br>
- [n8n preview workflow](references/n8n-workflow-preview.json) <br>
- [n8n export workflow](references/n8n-workflow-export.json) <br>
- [Topview AI](https://www.topview.ai) <br>
- [Apify](https://apify.com) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON workflow files and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions, validation guidance, n8n workflow imports, and configuration commands for external services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
