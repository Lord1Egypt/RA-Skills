## Description:

A real-time Chinese web search skill that uses 360 Search APIs for current web, news, AI search, and image search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonylwj](https://clawhub.ai/user/tonylwj)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users use this skill to retrieve current Chinese web, news, AI-search, and image-search results, especially for China-related companies, products, policy, market data, and other facts that need real-time verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to 360's third-party API.

Mitigation: Avoid sensitive or regulated content in queries and review outbound data handling expectations before deployment.

Risk: API key setup may store the key persistently in a shell startup file.

Mitigation: Prefer a credential manager or a scoped, quota-limited API key instead of long-lived plaintext shell configuration.

Risk: Search results can be current but still incomplete or misleading.

Mitigation: Review returned source URLs and timestamps before relying on results for decisions.

## Reference(s):

- [360 AI Open Platform](https://ai.360.com/platform)
- [ClawHub Skill Page](https://clawhub.ai/tonylwj/skills/360search)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown search summaries with source URLs and timestamps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should include source URLs, page timing when available, and official-site indicators when returned by the API.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
