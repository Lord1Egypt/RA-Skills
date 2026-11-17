## Description:

Web search without an API key using DuckDuckGo Lite via web_fetch, returning titles, URLs, and snippets for research queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakelin](https://clawhub.ai/user/jakelin)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run web searches through DuckDuckGo Lite when no search API key is configured, then select and fetch organic result pages for research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search query terms and fetched page URLs are sent to external web services.

Mitigation: Do not include secrets, credentials, private data, or confidential business details in search queries or fetched URLs.

Risk: Search results can include sponsored links, outdated pages, or incomplete coverage.

Mitigation: Skip sponsored entries, fetch primary sources where possible, and verify important claims against multiple relevant results.

## Reference(s):

- [DuckDuckGo Lite search endpoint](https://lite.duckduckgo.com/lite/?q=QUERY)
- [DuckDuckGo URL parameters](https://duckduckgo.com/params)
- [ClawHub skill page](https://clawhub.ai/jakelin/skills/ddg-web-search)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown with web_fetch URL examples and result-reading guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search queries are sent to DuckDuckGo Lite and selected result pages may be fetched separately; no API key or local dependencies are required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
