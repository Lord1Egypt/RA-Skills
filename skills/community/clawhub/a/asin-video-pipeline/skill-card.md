## Description:

Helps agents guide setup of an n8n workflow that turns Amazon ASIN rows into marketing video previews and approved final exports using Apify, Topview AI, and Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkk402373342](https://clawhub.ai/user/kkk402373342)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation builders, and ecommerce operators use this skill to configure a pipeline that reads ASINs from Google Sheets, retrieves product data, submits video generation tasks, tracks review status, and writes resulting video links back to the sheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends ASINs, product images, titles, descriptions, and generated video metadata to third-party services including Apify, Topview AI, and Google Sheets.

Mitigation: Review data-sharing requirements before use and only process product data that may be shared with those services.

Risk: The workflow depends on API keys and service account credentials for Topview AI, Apify, and Google Sheets.

Mitigation: Use least-privilege keys, restrict the Google service account to the target spreadsheet, and keep secrets out of repositories and screenshots.

Risk: Unpinned n8n runtime images or changing third-party APIs can alter workflow behavior.

Mitigation: Pin the n8n Docker image for production use and re-run setup validation after dependency or API changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kkk402373342/skills/asin-video-pipeline)
- [WORKFLOW_SETUP.md](references/WORKFLOW_SETUP.md)
- [n8n preview workflow](references/n8n-workflow-preview.json)
- [n8n export workflow](references/n8n-workflow-export.json)
- [Topview AI](https://www.topview.ai)
- [Apify](https://apify.com)
- [Google Cloud Console](https://console.cloud.google.com)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON workflow files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup steps, credential guidance, n8n workflow import commands, and validation commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
