## Description:

Chinese web search skill that aggregates 17 free search engines without API keys, using web page fetching for WeChat, finance, technical, academic, knowledge, Chinese, and English search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misonokisaki](https://clawhub.ai/user/misonokisaki)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent search Chinese, English, WeChat, finance, technical, and knowledge sources through free third-party search websites. It is intended for current-information lookup and source discovery where search terms can be safely shared with external search providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to third-party search engines and may reveal confidential names, credentials, unreleased business plans, or other sensitive intent.

Mitigation: Use only non-sensitive search terms unless the user is comfortable sharing them with external search providers.

Risk: Fetched search results can be incomplete, stale, promotional, or misleading.

Mitigation: Cross-check important claims across multiple sources and review source pages before acting on the results.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/misonokisaki/skills/cn-web-search-2-2-0)
- [Publisher profile](https://clawhub.ai/user/misonokisaki)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text search guidance with fetched web results and source-oriented summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search terms are sent to third-party search providers through web page fetches; no API key is required.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter and _meta.json; ClawHub release version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
