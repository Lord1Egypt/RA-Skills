## Description:

60s API 综合技能，提供每日新闻、AI资讯、热搜榜单、天气查询、数据查询、娱乐内容、媒体信息和实用工具。

This skill is ready for commercial/non-commercial use.

## Publisher:

[awsl1414](https://clawhub.ai/user/awsl1414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Chinese-language public information and utility APIs, including news, trending topics, weather, exchange rates, media rankings, translation, IP lookup, QR codes, hashes, and password tools. It helps an agent choose the right 60s API endpoint, issue curl requests, and summarize results concisely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and submitted content can be sent to the external 60s API service.

Mitigation: Install only when external submission to 60s API is acceptable, and avoid sending confidential text, URLs, API keys, tokens, or other secrets.

Risk: The password-check endpoint can send real passwords to an outside service.

Mitigation: Do not use the password-check endpoint with real passwords; prefer local password-strength checks.

Risk: Translation, hash, QR, and OG URL features submit provided text or URLs to an external service.

Mitigation: Use these features only for public or low-sensitivity inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awsl1414/skills/60s-api)
- [Publisher profile](https://clawhub.ai/user/awsl1414)
- [60s API base endpoint](https://60s.viki.moe/v2)
- [60s API documentation](https://docs.60s-api.viki.moe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise text or Markdown with curl commands and summarized API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses may include JSON, Markdown, plain text, images, audio, or downloaded files depending on the endpoint.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
