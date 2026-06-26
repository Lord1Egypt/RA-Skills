## Description: <br>
Use when YouTube data is needed through MyBrandMetrics: search YouTube videos, get video metadata, inspect channel info, browse playlists, list comments, check live broadcasts, query YouTube Analytics, and work with YouTube Reporting jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawbus](https://clawhub.ai/user/clawbus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose YouTube Data, Analytics, and Reporting endpoints and prepare MyBrandMetrics Discovery API requests for connected YouTube accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare requests for connected YouTube accounts with write, upload, moderation, administration, live, branding, and account-linking capabilities. <br>
Mitigation: Require explicit confirmation of the connected account, target resource, request parameters, and intended result before any upload, update, delete, moderation, live, branding, account-linking, or reporting-job action. <br>
Risk: MyBrandMetrics API keys and connected YouTube account identifiers are sensitive credentials or account data. <br>
Mitigation: Keep API keys out of skill files, examples, logs, and chat replies; scope keys as narrowly as possible and show only non-sensitive account labels during account selection. <br>
Risk: Using the full skill for read-only analytics can expose high-impact endpoints that are unnecessary for that workflow. <br>
Mitigation: For read-only analytics use cases, disable or separate upload, write, delete, moderation, live, branding, and account-linking endpoints before installation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/clawbus/clawbus-youtube-unified-api) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/clawbus) <br>
- [YouTube Unified API References](references/index.md) <br>
- [Curl Usage](references/curl.md) <br>
- [MyBrandMetrics Discovery API](references/mybrandmetrics-api.md) <br>
- [YouTube Data API v3](references/services/youtube-data-v3.md) <br>
- [YouTube Analytics API v2](references/services/youtube-analytics-v2.md) <br>
- [YouTube Reporting API v1](references/services/youtube-reporting-v1.md) <br>
- [Endpoint catalog](references/catalog.json) <br>
- [MyBrandMetrics](https://mybrandmetrics.com/) <br>
- [Clawbus](https://www.clawbus.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline curl examples, endpoint routes, request parameters, and account-selection guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON request bodies, API routes, query parameters, and credential-handling guidance.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
