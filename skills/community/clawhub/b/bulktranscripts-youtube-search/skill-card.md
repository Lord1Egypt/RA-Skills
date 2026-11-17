## Description:

Searches YouTube for videos, channels, or playlists through the BulkTranscripts API and retrieves transcripts for selected results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratie](https://clawhub.ai/user/pratie)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and agents use this skill to find relevant YouTube content, search within a creator's channel, and fetch transcripts for review, summarization, or comparison. It is useful when the task requires transcript-backed evidence from YouTube results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, video URLs or IDs, channel handles, and transcript requests are sent to BulkTranscripts.

Mitigation: Use the skill only when BulkTranscripts is approved for the user's data, and avoid confidential research topics unless that provider is approved for the use case.

Risk: The skill requires a BulkTranscripts API key.

Mitigation: Keep BULKTRANSCRIPTS_API_KEY private, avoid placing it in shared transcripts or logs, and rotate it if exposure is suspected.

Risk: Most search and transcript requests can consume account credits or encounter rate limits.

Mitigation: Check billing.remaining in responses, fetch only relevant transcripts, handle out_of_credits responses, and pace bulk requests according to the documented limits.

## Reference(s):

- [YouTube Search ClawHub listing](https://clawhub.ai/pratie/skills/bulktranscripts-youtube-search)
- [BulkTranscripts documentation](https://bulktranscripts.co/docs)
- [BulkTranscripts OpenAPI spec](https://bulktranscripts.co/openapi.json)
- [BulkTranscripts MCP server](https://bulktranscripts.co/youtube-mcp-server)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BULKTRANSCRIPTS_API_KEY and may consume BulkTranscripts credits for search, channel, playlist, and transcript requests.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
