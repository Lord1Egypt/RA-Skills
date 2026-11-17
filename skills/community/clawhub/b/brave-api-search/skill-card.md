## Description:

Search the web, suggest and correct queries, and generate grounded answers with citations through the Brave Search API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[broedkrummen](https://clawhub.ai/user/broedkrummen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to retrieve current web results, query suggestions, spelling corrections, and AI-grounded answers for research and information lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, questions, and optional search context are sent to Brave under the user's API account.

Mitigation: Do not submit secrets or sensitive personal data as queries; use only if Brave's data handling is acceptable.

Risk: API calls may consume quota or incur charges, especially for Answers and paid rich suggestions.

Mitigation: Keep API keys in environment variables or an uncommitted .env file, and monitor account quota and costs.

Risk: Citation and entity behavior outside streaming mode is ambiguously documented, and Answers uses English internally.

Mitigation: Use streaming when citations or entities matter and check the returned sources before relying on answers.

## Reference(s):

- [Brave Search API](https://brave.com/search/api/)
- [Brave Search API dashboard](https://api-dashboard.search.brave.com)
- [Brave API Search native plugin](https://clawhub.ai/plugins/brave-api-search-plugin)
- [Brave API Search skill release](https://clawhub.ai/broedkrummen/skills/brave-api-search)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown-formatted search results, suggestions, corrections, or answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers can include citations and usage/cost details; streaming is required for full citation, entity, and research features.]

## Skill Version(s):

4.2.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
