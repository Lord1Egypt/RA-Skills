## Description:

Fetches YouTube video transcripts, searches YouTube, lists channel or playlist videos, runs background bulk transcript jobs, and tracks new uploads through the BulkTranscripts API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratie](https://clawhub.ai/user/pratie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve transcripts, search YouTube, inspect channel or playlist videos, and monitor recent uploads for summarization, analysis, quotation, and research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests share YouTube or TikTok URLs, search queries, and channel or playlist identifiers with BulkTranscripts.

Mitigation: Confirm the user is comfortable sending those identifiers to BulkTranscripts and avoid submitting sensitive or private material.

Risk: The skill requires a BulkTranscripts API key.

Mitigation: Keep BULKTRANSCRIPTS_API_KEY private, pass it as a bearer token, avoid logging it, and rotate the key if it is exposed.

Risk: Bulk jobs can continue server-side and consume transcript credits.

Mitigation: Confirm max_videos before starting a bulk job, monitor billing.remaining, and poll job status at the returned interval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pratie/skills/bulktranscripts-youtube)
- [BulkTranscripts documentation](https://bulktranscripts.co/docs)
- [BulkTranscripts OpenAPI specification](https://bulktranscripts.co/openapi.json)
- [BulkTranscripts YouTube MCP server](https://bulktranscripts.co/youtube-mcp-server)
- [BulkTranscripts API key setup](https://bulktranscripts.co/app?tab=mcp)
- [BulkTranscripts pricing](https://bulktranscripts.co/#pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with curl examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BULKTRANSCRIPTS_API_KEY; responses can include billing.remaining and long transcript text or paragraph data.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
