## Description:

Check a YouTube channel's newest uploads for free via the BulkTranscripts API and fetch transcripts only for videos that are new.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratie](https://clawhub.ai/user/pratie)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to monitor YouTube channels for recent uploads, identify videos that are new since the last check, and fetch transcripts only when needed for alerts, digests, or competitor tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses BULKTRANSCRIPTS_API_KEY to authenticate with a third-party transcript API.

Mitigation: Keep the key private, store it in the environment, and avoid placing it in logs, shared chats, screenshots, or committed files.

Risk: Transcript, account, and channel requests are sent to bulktranscripts.co and some requests can consume credits.

Mitigation: Use the free channel/latest endpoint for monitoring, check billing.remaining in responses, and fetch transcripts only for videos that are new and relevant.

Risk: Bulk polling can hit service rate limits.

Mitigation: Respect Retry-After responses and pace bulk requests below the documented per-minute limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pratie/skills/bulktranscripts-upload-monitor)
- [BulkTranscripts documentation](https://bulktranscripts.co/docs)
- [BulkTranscripts OpenAPI spec](https://bulktranscripts.co/openapi.json)
- [BulkTranscripts MCP server](https://bulktranscripts.co/youtube-mcp-server)
- [BulkTranscripts API key page](https://bulktranscripts.co/app?tab=mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON API response references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include YouTube video metadata, transcript text, transcript summaries, billing status, and error-handling guidance depending on the user's request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
