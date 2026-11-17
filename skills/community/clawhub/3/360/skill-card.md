## Description:

360-web-search, also known as 360智搜 or 360Aiso, helps agents retrieve current Chinese web, news, AI search, and image search results through 360 search APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonylwj](https://clawhub.ai/user/tonylwj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill when they need timely Chinese or China-related web, news, market, policy, product, or image-search information with source URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if users place them directly in shell history or broad profile files.

Mitigation: Prefer a secret manager or app-scoped environment variable for SEARCH_360_API_KEY, and avoid pasting paid keys into shared shell history.

Risk: Search terms, session IDs, and image-search inputs may be sent to api.360.cn.

Mitigation: Use the skill only for queries appropriate for 360's search APIs and avoid sensitive personal or confidential inputs.

Risk: Search results may be current but still incomplete, stale, or unsuitable without source review.

Mitigation: Review returned source URLs, timestamps, and official-site indicators before relying on results for decisions.

## Reference(s):

- [360 AI Open Platform](https://ai.360.com/platform)
- [ClawHub Skill Page](https://clawhub.ai/tonylwj/skills/360)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown search summaries with source URLs, timestamps when available, and setup commands when credentials are missing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SEARCH_360_API_KEY and curl; sends search terms, session IDs, and image-search inputs to api.360.cn.]

## Skill Version(s):

1.3.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
