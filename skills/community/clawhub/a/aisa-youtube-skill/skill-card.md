## Description:

YouTube SERP Scout for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and content teams use this skill to research YouTube search results, discover trends, monitor competitors, and inspect regional or language-specific video rankings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated API requests may expose the AIsa API key if redirects leave the intended API domain.

Mitigation: Review before installing, use a limited-scope or low-credit API key, avoid sensitive search terms, and prefer a version that rejects cross-origin redirects or strips Authorization on redirect.

## Reference(s):

- [OpenClaw](https://openclaw.ai)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [ClawHub Skill Page](https://clawhub.ai/bowen-dotcom/skills/aisa-youtube-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl or python3 and an AISA_API_KEY environment variable.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
