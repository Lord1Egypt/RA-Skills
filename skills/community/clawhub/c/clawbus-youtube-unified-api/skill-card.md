## Description:

YouTube API helps agents use MyBrandMetrics to search YouTube, retrieve video and channel data, browse playlists and comments, check live broadcasts, query YouTube Analytics, and work with YouTube Reporting jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawbus](https://clawhub.ai/user/clawbus)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to choose YouTube Data API, YouTube Analytics API, and YouTube Reporting API endpoints and build MyBrandMetrics Discovery API requests for connected YouTube accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide account-changing YouTube operations, including upload, update, delete, moderation, subscription, playlist, live-stream, and reporting-job actions.

Mitigation: Require explicit confirmation of the connected account, endpoint, target resource ID, request parameters, and intended result before running any account-changing request.

Risk: A MyBrandMetrics API key may carry YouTube read, write, upload, analytics, or reporting authority for connected accounts.

Mitigation: Use only a key whose granted YouTube permissions are acceptable for the task, never expose keys in files or chat, and reconnect YouTube with narrower permissions when appropriate.

Risk: Changing the API base URL could route credentialed requests away from the intended MyBrandMetrics host.

Mitigation: Keep MYBRANDMETRICS_API_BASE_URL fixed to https://api.mybrandmetrics.com unless the publisher provides a verified replacement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawbus/skills/clawbus-youtube-unified-api)
- [ClawHub publisher profile](https://clawhub.ai/user/clawbus)
- [MyBrandMetrics](https://mybrandmetrics.com/)
- [clawbus](https://www.clawbus.com/)
- [YouTube Unified API References](artifact/references/index.md)
- [Curl Usage](artifact/references/curl.md)
- [MyBrandMetrics Discovery API](artifact/references/mybrandmetrics-api.md)
- [YouTube Data API v3 endpoint reference](artifact/references/services/youtube-data-v3.md)
- [YouTube Analytics API v2 endpoint reference](artifact/references/services/youtube-analytics-v2.md)
- [YouTube Reporting API v1 endpoint reference](artifact/references/services/youtube-reporting-v1.md)
- [Endpoint catalog](artifact/references/catalog.json)
- [YouTube Data API v3 discovery document](https://youtube.googleapis.com/$discovery/rest?version=v3)
- [YouTube Analytics API v2 discovery document](https://youtubeanalytics.googleapis.com/$discovery/rest?version=v2)
- [YouTube Reporting API v1 discovery document](https://youtubereporting.googleapis.com/$discovery/rest?version=v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with curl command examples, API endpoint paths, query parameters, and JSON request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MyBrandMetrics account selectors, request bodies, upload/download notes, and error-handling guidance; does not provide YouTube transcripts.]

## Skill Version(s):

1.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
