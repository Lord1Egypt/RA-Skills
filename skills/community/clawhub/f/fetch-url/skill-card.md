## Description:

Fetch raw HTTP response bodies from one or more URLs with optional custom headers and timeout, supporting JSON, XML, RSS, CSV, plain text, and files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roaycl](https://clawhub.ai/user/roaycl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to retrieve raw non-HTML HTTP responses from APIs, feeds, files, and other machine-readable URLs. It is useful when the agent needs the response body directly rather than converted webpage markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make unrestricted network requests with caller-supplied headers.

Mitigation: Install only when broad raw network fetch capability is intended, and avoid localhost, private-network, cloud metadata, or untrusted redirecting URLs unless that access is explicitly intended.

Risk: Sensitive headers could be sent to external or unintended endpoints.

Mitigation: Do not pass Authorization, Cookie, API keys, session tokens, or internal routing headers through this skill.

## Reference(s):

- [Fetch Url ClawHub listing](https://clawhub.ai/roaycl/skills/fetch-url)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [Raw HTTP response body text for single URLs; JSON array of result objects for multiple URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports one or more URLs, optional per-URL headers, and configurable request timeout.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
