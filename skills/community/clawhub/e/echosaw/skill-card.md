## Description:

Analyze video, audio, and image files using AI, producing structured intelligence reports with transcripts, content moderation signals, sentiment analysis, visual object labels, geographic metadata, and LLM-generated summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echosaw](https://clawhub.ai/user/echosaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit audio, video, and image media to Echosaw, monitor analysis jobs, retrieve structured media intelligence reports, search analyzed media, and inspect account details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media files or media URLs are sent to Echosaw for analysis.

Mitigation: Only submit media you are authorized to process, and avoid private, regulated, or third-party media unless retention, deletion, and access controls are understood.

Risk: Deprecated local setup can require a long-lived Echosaw API key.

Mitigation: Prefer the recommended remote MCP server with OAuth, and use API keys only when intentionally choosing the deprecated local setup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/echosaw/skills/echosaw)
- [Echosaw MCP Integration Guide](https://echosaw.com/developers/mcp-integration)
- [Echosaw API Reference](https://echosaw.com/developers/api-reference)
- [Echosaw Pricing](https://echosaw.com/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool names, JSON response envelopes, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides asynchronous media analysis workflows and references structured JSON responses from Echosaw MCP tools.]

## Skill Version(s):

1.3.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
