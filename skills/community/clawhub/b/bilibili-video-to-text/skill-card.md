## Description:

Turns Bilibili video links or shared text into timestamped transcripts, on-screen text, summaries, metadata, and engagement statistics through LinkDigest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

External users can turn Bilibili video links or copied share text into transcripts, notes, or summaries. Results can include on-screen text, video details, key points, and engagement statistics when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The entire supplied share message is forwarded to LinkDigest, and public-link digests may be cached or shared under the provider's policy.

Mitigation: Submit only the public video URL when possible, remove sensitive text from share messages, and review LinkDigest's privacy policy.

Risk: Video processing consumes API credits, with cost varying by video length and options.

Mitigation: Use a dedicated API key with a credit cap and set --max-credits for individual requests.

Risk: Some Bilibili error wording in the client may be outdated.

Mitigation: Treat client error wording as potentially stale and consult current LinkDigest guidance when a request fails.

## Reference(s):

- [LinkDigest platform information](https://linkdigest.dev/platforms?ref=skill-bilibili-video-to-text)
- [LinkDigest privacy policy](https://linkdigest.dev/privacy)
- [LinkDigest MCP endpoint](https://linkdigest.dev/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown or JSON; transcripts are segmented with timestamps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include on-screen text, video metadata, key points, engagement statistics, and optional translation or breakdowns. Recognition may misspell names and numbers.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
