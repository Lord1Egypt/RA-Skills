## Description:

Search the web using Cloudsways SmartSearch API. Returns highly relevant results with dynamic summaries, snippets, and optional full-text content. Use when you need up-to-date information, news, or deep research data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prismheart](https://clawhub.ai/user/prismheart)

### License/Terms of Use:


## Use Case:

Developers, researchers, and agents use this skill to run web searches through the Cloudsways SmartSearch API and retrieve snippets, dynamic summaries, or optional full-page content for current information gathering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key can be sent to a host selected through environment configuration.

Mitigation: Review the configured Cloudsways base path before use and only use a trusted official hostname.

Risk: Search queries and optional full-page content may expose sensitive information to the search provider.

Mitigation: Avoid sensitive queries unless sharing them with the provider is intended, and prefer snippet-only searches unless full content is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prismheart/skills/cloudsway-search-tob-test)
- [Cloudsways SmartSearch MCP endpoint example](https://searchmcp.cloudsway.net/search/{YOUR_SMARTSEARCH_ENDPOINT}/smart)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON search results and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include page titles, URLs, snippets, dynamic mainText fragments, optional full content, and publication dates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
