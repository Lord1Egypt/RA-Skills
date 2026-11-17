## Description:

Research TikTok and Facebook ads plus Meta Ad Library results in one combined cross-platform PipiAds skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyanggod](https://clawhub.ai/user/fanyanggod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research TikTok ads, Facebook ads, and Meta Ad Library data in one workflow. It supports comparing ad trends, validating advertiser or product presence across platforms, and drilling into ads, products, advertisers, or stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The globally installed third-party MCP server receives the user's PipiAds API key.

Mitigation: Install only if the pipiads-mcp-server package is trusted, prefer a limited API key, and isolate the global npm install in sensitive environments.

Risk: Broad ad research queries can consume PipiAds account credits.

Mitigation: Clarify whether adspy data, ad library data, or both are needed before running broad searches, and monitor account credit usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanyanggod/skills/adspy-ad-library-tiktok-facebook)
- [PipiAds homepage](https://www.pipiads.com)
- [PipiSpy API key and billing](https://www.pipispy.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text research summaries with tool-specific findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PIPIADS_API_KEY; API calls consume PipiAds account credits.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
