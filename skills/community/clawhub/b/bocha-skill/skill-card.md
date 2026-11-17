## Description:

Search the web using Bocha AI Search API, a Chinese search engine optimized for Chinese content, with support for web pages, images, news, and AI-generated summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ypw757](https://clawhub.ai/user/ypw757)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to route Chinese or English search requests through the Bocha AI Search API and receive summarized web, image, and news results. It is especially oriented toward Chinese-language and domestic Chinese content search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Bocha's API when the skill runs.

Mitigation: Install only when that data flow is intended, and provide a user-owned BOCHA_API_KEY through the environment or OpenClaw configuration.

Risk: The release evidence reports an API-key-shaped secret in PUBLISH.md.

Mitigation: Do not use or copy that key; the publisher should rotate it if it was ever valid.

Risk: Publishing helper commands may install a global npm CLI or perform account-level ClawHub actions.

Mitigation: Review publish.sh and any delete or publish commands before running them in a local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ypw757/skills/bocha-skill)
- [Bocha AI Open Platform](https://open.bocha.cn/)
- [Bocha API documentation](https://bocha-ai.feishu.cn/wiki/RXEOw02rFiwzGSkd9mUcqoeAnNK)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown search results with an embedded raw JSON block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and BOCHA_API_KEY; accepts query, count, freshness, and summary parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
