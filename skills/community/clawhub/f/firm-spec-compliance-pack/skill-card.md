## Description:

MCP 2025-11-25 specification compliance audit pack that validates elicitation, tasks, resources/prompts, audio content, JSON Schema 2020-12, SSE transport, and icon metadata compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to audit MCP server configurations and implementations for compliance with the MCP 2025-11-25 specification. It focuses on protocol features including elicitation, durable tasks, resources and prompts, audio content, JSON Schema 2020-12, SSE resumption, and icon metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact documents audit workflows but does not include the implementation of the referenced audit tools.

Mitigation: Confirm that the required mcp-openclaw-extensions package and its audit tools are the intended trusted dependency before installing or relying on results.

Risk: Compliance findings may be incomplete or misleading if generated checks are accepted without review.

Mitigation: Review audit outputs against the relevant MCP 2025-11-25 requirements before using them for release or deployment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/skills/firm-spec-compliance-pack)
- [Publisher profile](https://clawhub.ai/user/romainsantoli-web)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with YAML configuration and audit command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents seven MCP compliance audit entry points; reviewed artifact does not include the audit tool implementations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
