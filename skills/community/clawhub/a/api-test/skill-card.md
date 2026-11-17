## Description:

Helps draft REST API documentation and includes a generic API request tool for GET and POST calls to user-supplied URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2367961075](https://clawhub.ai/user/2367961075)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API maintainers can use this skill to draft REST API documentation and, when intentionally configured, make GET or POST API calls during documentation or integration work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package can send GET or POST requests to arbitrary user-supplied URLs with custom headers, query parameters, and JSON bodies.

Mitigation: Install only when a generic HTTP request tool is intended, and constrain network access, allowed destinations, and runtime permissions externally.

Risk: The package presents itself as an API documentation helper while executable behavior performs external API requests.

Mitigation: Review behavior before installation and ensure users understand both the documentation-writing and HTTP request capabilities.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2367961075/skills/api-test)

## Skill Output:

**Output Type(s):** [text, markdown, code, API response data, guidance]

**Output Format:** [Markdown documentation guidance and JSON-like API call results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [HTTP call results can include status code, URL, method, parsed response data, or up to 1000 characters of non-JSON response text.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
