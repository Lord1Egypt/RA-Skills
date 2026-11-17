## Description:

Fetches transcripts for every video in a YouTube playlist through BulkTranscripts, either as a background bulk job or by listing the playlist and fetching videos one by one.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratie](https://clawhub.ai/user/pratie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when a user provides a YouTube playlist and wants transcripts turned into study notes, course summaries, or reusable text. It guides API-key setup, playlist listing, background bulk jobs, transcript retrieval, balance checks, and common error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Playlist or video links, transcript requests, and the API key are sent to the BulkTranscripts service.

Mitigation: Use the skill only when the user is comfortable sharing those links and requests with BulkTranscripts, and avoid submitting private or sensitive playlists.

Risk: Changing a private playlist to unlisted can expose it to anyone with the link.

Mitigation: Explain the visibility change before asking the user to retry a private playlist, and use only playlists the user is comfortable making accessible by link.

Risk: Transcript, search, channel, and playlist requests can consume account credits or hit rate limits.

Mitigation: Check billing metadata in responses, prefer bulk jobs for larger playlists, and respect retry guidance for rate-limited requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pratie/skills/bulktranscripts-playlist-transcripts)
- [BulkTranscripts documentation](https://bulktranscripts.co/docs)
- [BulkTranscripts OpenAPI specification](https://bulktranscripts.co/openapi.json)
- [BulkTranscripts MCP server](https://bulktranscripts.co/youtube-mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BULKTRANSCRIPTS_API_KEY; transcript responses may include text, paragraphs, timestamped segments, and billing metadata.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
