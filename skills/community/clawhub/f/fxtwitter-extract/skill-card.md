## Description:

Extracts X (Twitter) posts, threads, and user profiles through the FxTwitter API without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicoxia](https://clawhub.ai/user/nicoxia)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to look up public X/Twitter post content, threads, media metadata, polls, and user profile data for summarization, analysis, or workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries disclose X/Twitter post IDs, URLs, or handles to the third-party FxTwitter service.

Mitigation: Use only when that third-party disclosure is acceptable, and avoid sensitive investigations or private workflows.

Risk: Returned post content and media URLs are untrusted external data.

Mitigation: Review outputs before reuse, avoid executing or automatically trusting returned links, and apply downstream content validation where needed.

Risk: FxTwitter availability, rate limits, and API behavior can change outside the skill owner's control.

Mitigation: Handle network errors and failed lookups gracefully, and verify critical results against primary sources when reliability matters.

## Reference(s):

- [FxTwitter API](https://api.fxtwitter.com)
- [FxTwitter Documentation](https://docs.fxtwitter.com/)
- [FxTwitter GitHub](https://github.com/FxEmbed/FxTwitter)
- [FxEmbed GitHub](https://github.com/FxEmbed/FxEmbed)
- [FxTwitter Status](https://status.fxtwitter.com)
- [ClawHub Skill Page](https://clawhub.ai/nicoxia/skills/fxtwitter-extract)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or structured JSON returned from command-line usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external content, media URLs, profile fields, engagement counts, error messages, and FxTwitter API response data.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
