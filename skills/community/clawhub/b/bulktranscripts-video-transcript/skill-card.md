## Description:

Gets a single YouTube, YouTube Shorts, or TikTok video transcript as clean text, timestamped segments, SRT/VTT, or Markdown via the BulkTranscripts API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratie](https://clawhub.ai/user/pratie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they have a video link and need an agent to retrieve transcript text for summarization, quotation, translation, fact-checking, notes, or subtitle output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a BulkTranscripts API key, and exposing that key could allow unauthorized use of the account.

Mitigation: Set BULKTRANSCRIPTS_API_KEY only in a trusted environment, avoid pasting it into logs or shared chats, and rotate the key if exposed.

Risk: The skill sends video identifiers or URLs to a third-party transcript service.

Mitigation: Install and use the skill only when BulkTranscripts is acceptable for the intended video transcript retrieval workflow.

Risk: Transcript requests can consume account credits or encounter service rate limits.

Mitigation: Check billing.remaining in API responses, handle out_of_credits responses clearly, and respect Retry-After when rate limited.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pratie/skills/bulktranscripts-video-transcript)
- [BulkTranscripts documentation](https://bulktranscripts.co/docs)
- [BulkTranscripts OpenAPI spec](https://bulktranscripts.co/openapi.json)
- [BulkTranscripts MCP server](https://bulktranscripts.co/youtube-mcp-server)
- [BulkTranscripts API key setup](https://bulktranscripts.co/app?tab=mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples and transcript output formats including text, JSON, SRT, VTT, CSV, and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BULKTRANSCRIPTS_API_KEY; transcript calls may consume credits, and responses include billing.remaining.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
