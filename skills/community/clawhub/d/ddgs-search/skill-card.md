## Description:

Free multi-engine web search via ddgs CLI (DuckDuckGo, Google, Bing, Brave, Yandex, Yahoo, Wikipedia) + arXiv API search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camopel](https://clawhub.ai/user/camopel)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to run no-key web searches across supported search providers and to discover arXiv papers. It can also serve as a search backend for workflows that expect web-search-plus compatible JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to third-party search providers and arXiv.

Mitigation: Do not submit secrets, proprietary text, personal data, or other sensitive queries through this skill.

Risk: Installation performs user-level Python package installation for the ddgs dependency.

Mitigation: Use a reviewed and pinned ddgs version when reproducible or controlled deployments are required.

## Reference(s):

- [ddgs-search ClawHub release](https://clawhub.ai/camopel/skills/ddgs-search)
- [arXiv API endpoint](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON search results and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include provider metadata plus titles, URLs, snippets, publication dates, and arXiv-specific paper fields when available.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
