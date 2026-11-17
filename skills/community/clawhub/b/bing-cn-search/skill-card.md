## Description:

Uses Bing CN search to retrieve current internet information for Chinese-language news, events, and explicit web-search requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evensix66](https://clawhub.ai/user/evensix66)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when an agent needs current Chinese-language web search results from Bing CN, especially for news, recent events, and user requests to search online.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs unpinned npm packages and registers a persistent MCP server.

Mitigation: Pin and review package versions before installation, avoid elevated privileges, and keep the MCP server registered only where it is needed.

Risk: Searches may be triggered on broad Chinese terms and the results come from third-party sites with possible Bing indexing delays.

Mitigation: Use the skill for explicit current-information searches, cite the listed sources, and verify time-sensitive or sensitive claims against authoritative sources.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown summary with source list and inline shell commands for setup or MCP calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search calls request up to 10 Bing CN results; source websites should be listed after the summary.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
