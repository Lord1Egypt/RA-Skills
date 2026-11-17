## Description:

Fetch every transcript on a YouTube channel, up to 1,000 videos, as one background bulk job through the BulkTranscripts API; list channel videos; or search within one channel for a topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratie](https://clawhub.ai/user/pratie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to collect YouTube channel transcripts for creator research, knowledge-base construction, RAG corpus creation, and targeted channel search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a BulkTranscripts API key to call the service.

Mitigation: Confirm the user is comfortable providing a BulkTranscripts key and keep it in the BULKTRANSCRIPTS_API_KEY environment variable rather than embedding it in shared output.

Risk: Whole-channel jobs can process many videos, consume credits for newly fetched transcripts, and store transcripts in the user's BulkTranscripts library.

Mitigation: Confirm max_videos, expected credit use, and billing.remaining before starting large jobs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pratie/skills/bulktranscripts-channel-transcripts)
- [BulkTranscripts Documentation](https://bulktranscripts.co/docs)
- [BulkTranscripts OpenAPI Specification](https://bulktranscripts.co/openapi.json)
- [BulkTranscripts MCP Server](https://bulktranscripts.co/youtube-mcp-server)
- [BulkTranscripts API Key](https://bulktranscripts.co/app?tab=mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash code blocks and JSON API response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BULKTRANSCRIPTS_API_KEY; bulk jobs may consume account credits and should respect API polling and rate-limit guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
