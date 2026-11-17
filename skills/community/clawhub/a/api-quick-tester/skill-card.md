## Description:

Api Quick Tester helps developers send single HTTP API requests and generate simple mock JSON data from Node.js command-line scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to quickly exercise API endpoints from the command line, inspect status codes and response bodies, and create sample mock payloads during API development. Review the shipped files before relying on advertised batch, GraphQL, or report-generation behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises batch testing, GraphQL testing, and report features that are not fully represented by the shipped artifact files.

Mitigation: Verify the installed files and rely only on documented behavior that is present in the package, or update the package before using those features.

Risk: API credentials passed on the command line can be exposed through shell history, process listings, logs, or copied reports.

Mitigation: Use only test credentials, avoid placing real secrets directly in commands, and redact sensitive headers and response data before sharing output.

Risk: User-supplied endpoints and unpinned installer commands can create network and supply-chain exposure.

Mitigation: Prefer HTTPS test endpoints, restrict testing to systems you are authorized to call, and pin and verify installer versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/api-quick-tester)
- [Publisher profile](https://clawhub.ai/user/yang1002378395-cmyk)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Markdown, Guidance]

**Output Format:** [Command-line text, JSON payloads, and Markdown-style API test reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include outbound HTTP responses, status details, timing data, generated mock data, and authentication headers supplied by the user.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
