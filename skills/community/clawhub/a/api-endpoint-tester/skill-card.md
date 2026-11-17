## Description:

CLI tool to test REST API endpoints with various HTTP methods, headers, and payloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to send single HTTP or HTTPS requests, inspect responses, validate status codes, and debug REST API integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad outbound HTTP or HTTPS requests.

Mitigation: Use it only against URLs you control or are explicitly authorized to test, and avoid private, internal, and metadata endpoints.

Risk: Headers and request bodies can contain sensitive credentials or payload data.

Mitigation: Do not paste live tokens, secrets, or sensitive data into command-line headers or bodies; use scoped test credentials when needed.

Risk: The optional output-file behavior writes response data to disk.

Mitigation: Avoid the output-file option until path containment and overwrite behavior have been reviewed and fixed.

Risk: The requests dependency is declared without a pinned version.

Mitigation: Pin the dependency version for reproducible installation and review updates before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/derick001/skills/api-endpoint-tester)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [JSON, Files]

**Output Format:** [JSON response object with status, headers, body, response time, URL, and method; optionally written to a JSON file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs one request at a time, supports common HTTP methods, and defaults to a 10-second timeout.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
