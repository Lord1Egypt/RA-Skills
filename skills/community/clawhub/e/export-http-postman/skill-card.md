## Description:

Export an HTTP API endpoint from the current work project into a Postman-importable collection JSON file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extraskittles](https://clawhub.ai/user/extraskittles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to locate an HTTP endpoint in a project and export a Postman Collection v2.1 JSON file with inferred method, URL, query parameters, path variables, headers, and example body placeholders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided domain values may be persisted into an agent-readable domain mapping file without validation or escaping.

Mitigation: Validate domains before saving them, review references/domains.md before use, and avoid persisting values from untrusted users.

Risk: Generated Postman collections could include incorrect endpoint details if the matching route or service domain is ambiguous.

Mitigation: Ask a concise clarification question when multiple endpoints or domains are plausible and report the selected endpoint, base URL, and assumptions.

Risk: Local project configuration may contain secrets that should not be copied into generated collections.

Mitigation: Use placeholders for tokens, cookies, IDs, timestamps, and other sensitive or environment-specific values.

## Reference(s):

- [Stored Service Domains](references/domains.md)
- [Postman Collection v2.1 schema](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Postman Collection v2.1 JSON file plus a concise Markdown summary of the chosen endpoint, base URL, and assumptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses placeholders for environment-specific or sensitive values and validates generated JSON before finishing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
