## Description:

Search web-indexed Douyin videos by topic and turn selected links into transcripts, on-screen text, key points, and engagement metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can find public Douyin videos by topic for content research, benchmarking, and competitor analysis. They can then read selected videos as transcripts and structured summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted links and share text are processed remotely, and digests may be shared by link.

Mitigation: Use public links, avoid including private information in share text, and review LinkDigest's privacy policy before use.

Risk: The API key grants access to the user's LinkDigest account.

Mitigation: Keep LINKDIGEST_API_KEY in the environment and do not paste it into chat or code.

Risk: Reading videos can consume paid credits.

Mitigation: Choose which videos to read and set --max-credits to limit per-video spending.

## Reference(s):

- [LinkDigest Douyin Search API](https://linkdigest.dev/zh/douyin-sousuo-api)
- [LinkDigest API key setup](https://linkdigest.dev/app/keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a spoken transcript, on-screen text, captions, key points, and engagement counts for selected videos.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
