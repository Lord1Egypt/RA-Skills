## Description:

Query the free countries.dev REST API for country, city, postal-code, IP geolocation, and distance data without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanookai](https://clawhub.ai/user/nanookai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and external users use this skill to answer geography-related requests by choosing the correct countries.dev endpoint and interpreting country, city, postal-code, IP geolocation, and distance responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IP geolocation endpoints can send the caller IP address or supplied IP addresses to countries.dev.

Mitigation: Use IP geolocation endpoints only when intentionally needed, and avoid submitting private, internal, or sensitive IP lists.

Risk: Some lookup endpoints use substring matching or endpoint-specific argument formats, which can lead to ambiguous or failed results.

Mitigation: Prefer ISO-code lookup when available, inspect search result arrays before choosing a match, and follow the endpoint reference for required path and query formats.

## Reference(s):

- [countries.dev API](https://countries.dev)
- [Complete Endpoint Reference](references/endpoints.md)
- [ClawHub Skill Page](https://clawhub.ai/nanookai/skills/countries-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline curl commands and JSON response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is required; countries.dev responses are JSON except some plain-text 404 errors.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
