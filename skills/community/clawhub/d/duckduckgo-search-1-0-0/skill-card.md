## Description:

Performs web searches using DuckDuckGo to retrieve real-time information from the internet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omprasad122007-rgb](https://clawhub.ai/user/omprasad122007-rgb)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search DuckDuckGo for current events, documentation, tutorials, news, images, videos, instant answers, suggestions, and map results when local context is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad Python execution and package-install authority beyond a narrow web-search workflow.

Mitigation: Review before installing, run it only in an isolated Python environment, and pin the DuckDuckGo search dependency version before use.

Risk: Generated commands may install packages or execute Python code.

Mitigation: Inspect proposed shell commands and Python snippets before execution, especially commands involving pip, uv, or local file writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omprasad122007-rgb/skills/duckduckgo-search-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python code snippets, shell commands, and optional JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search behavior can be configured with region, safesearch, timelimit, result count, proxy, and search type options.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
