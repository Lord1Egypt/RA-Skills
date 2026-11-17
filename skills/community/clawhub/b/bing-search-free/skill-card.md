## Description:

Searches the web with Bing and uses Jina.ai to extract concise page summaries without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azzazhang](https://clawhub.ai/user/azzazhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform lightweight web searches and retrieve search-result summaries through a command-line JSON interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted JSON arguments or malicious search-response content could execute local code.

Mitigation: Review before installing or using; validate max_results as an integer and pass response data to a static parser through stdin rather than embedding response text in python3 -c source.

Risk: Search queries and returned content are sent through external Bing and Jina.ai services.

Mitigation: Avoid sensitive searches and review whether external-service use is acceptable for the intended workflow.

## Reference(s):

- [Skill page](https://clawhub.ai/azzazhang/skills/bing-search-free)
- [Publisher profile](https://clawhub.ai/user/azzazhang)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the query, result list, and response time; result count is intended to be limited to 1-10.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
