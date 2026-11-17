## Description:

Chinese web search helper that aggregates free public search engines through web fetching, with coverage for general Chinese search, WeChat public-account content, finance, technical, academic, and encyclopedia queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c595390153-a11y](https://clawhub.ai/user/c595390153-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to compose web_fetch calls for Chinese-oriented and multilingual search across public search engines without API keys. It is suited to retrieving current public web information, public-account articles, finance/investment pages, technical community results, and encyclopedia entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to external public search engines.

Mitigation: Do not use the skill with secrets, credentials, private customer data, or sensitive personal information.

Risk: Public search results can be incomplete, stale, biased, or inconsistent across engines.

Mitigation: Cross-check important findings against authoritative sources before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/c595390153-a11y/skills/cn-web-search-custom)
- [Publisher profile](https://clawhub.ai/user/c595390153-a11y)
- [Repository declared in artifact metadata](https://github.com/joansongjr/cn-web-search)
- [Author URL declared in artifact metadata](https://github.com/joansongjr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with web_fetch URL examples and engine-selection tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search terms are embedded in public search-engine URLs; examples use extractMode and maxChars parameters for web_fetch.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact frontmatter and _meta.json report 2.3.0, package.json reports 0.9.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
