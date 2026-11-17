## Description:

Free web search using DuckDuckGo with web, news, image, suggestion, and instant-answer modes without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eternal0404](https://clawhub.ai/user/eternal0404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run DuckDuckGo searches for web results, recent news, images, suggestions, and instant answers. It is useful when a workflow needs current public information without configuring a paid search API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to DuckDuckGo through the ddgs client, which may expose sensitive terms to an external service.

Mitigation: Avoid credentials, private data, and confidential business details in search queries.

Risk: Search results and instant answers may be incomplete, stale, or misleading.

Mitigation: Review returned sources before relying on the information in decisions or downstream outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eternal0404/skills/eternal-free-search)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text search results or JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count, region, and time filter can be configured by command-line options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
