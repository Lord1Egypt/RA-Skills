## Description:

Web search using Tavily's LLM-optimized API. Returns relevant results with content snippets, scores, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tavily web searches with configurable result count, depth, topic, time range, domain filters, and optional raw JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that this release publishes a real-looking Tavily API key in documentation and metadata.

Mitigation: Do not install this version as-is; revoke and replace the exposed key, require TAVILY_API_KEY, and use placeholders in examples.

Risk: Searches and raw-content requests are sent to Tavily.

Mitigation: Add a clear notice before use and avoid submitting confidential queries or content.

## Reference(s):

- [Tavily](https://tavily.com)
- [ClawHub skill page](https://clawhub.ai/cs995279497-byte/skills/chen-tavily-search)
- [Publisher profile](https://clawhub.ai/user/cs995279497-byte)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown source summaries by default, or formatted JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search requests are sent to Tavily and may include raw page content when enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
