## Description:

豆包 WebSearch helps agents submit web search queries through the RedFox API, poll for Doubao search results, and return structured JSON for real-time information retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need current web search results from Doubao via RedFox, including asynchronous submission, polling, error handling, and structured result presentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to RedFox/Doubao using an API key.

Mitigation: Avoid sending secrets, credentials, regulated data, or confidential business text in search queries.

Risk: The skill depends on external service availability and a Python requests dependency.

Mitigation: Use an isolated environment with pinned dependencies and handle API errors or timeouts before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/doubao-websearch)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox Doubao Search API endpoint](https://redfox.hk/story/api/doubaoSearch)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration]

**Output Format:** [JSON from the search script, with agent-facing Markdown summaries and citations derived from the returned content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may emit progress messages to stderr while polling for results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
