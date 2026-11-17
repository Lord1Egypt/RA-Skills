## Description:

Turns supported video links into transcripts, on-screen text, summaries, and available video metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing public video content can submit a supported video link or share text to receive a transcript, on-screen text, key points, and available video metadata. The skill documents Douyin and other supported video sources, subject to platform access limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted links and resulting text may be processed by LinkDigest and third-party model services; digests may be cached and shared with other users of the same public link.

Mitigation: Submit only public links and text you are comfortable sharing, and review the LinkDigest privacy policy. Backend privacy claims cannot be verified from the client code.

Risk: Requests can consume account credits, and the optional mcp-remote bridge adds a third-party dependency.

Mitigation: Protect LINKDIGEST_API_KEY and set --max-credits or a key spending limit. Prefer the bundled client or native HTTP integration; review and pin mcp-remote if you use it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jackchew7143/skills/douyin-video-to-text)
- [LinkDigest documentation](https://linkdigest.dev/zh/docs?ref=skill-douyin-video-to-text)
- [LinkDigest privacy policy](https://linkdigest.dev/privacy)
- [LinkDigest OpenAPI specification](https://linkdigest.dev/openapi.json)
- [LinkDigest MCP client repository](https://github.com/jcaiagent7143-ui/linkdigest-mcp)

## Skill Output:

**Output Type(s):** [text, Markdown, JSON]

**Output Format:** [A video digest with transcript, on-screen text, key points, and available metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript timestamps are segment-level; results may be partial. Full transcripts require an API key and credits, and engagement counts are snapshots.]

## Skill Version(s):

1.0.3 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
