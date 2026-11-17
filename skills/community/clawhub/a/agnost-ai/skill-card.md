## Description:

Use when implementing data ingestion for Agnost AI analytics, including API reference, Python and TypeScript SDK guidance, and examples for tracking AI conversations, MCP server events, and user interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajmeraparth132](https://clawhub.ai/user/ajmeraparth132)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to integrate Agnost analytics ingestion into AI applications and MCP servers through SDKs or direct HTTP API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analytics examples may send raw prompts, responses, tool inputs, tool outputs, and user identifiers to a third-party service.

Mitigation: Disable raw input and output capture by default where possible, and redact prompts, responses, tool arguments, tool results, exceptions, emails, IPs, and identifiers before ingestion.

Risk: Analytics collection may require user or organizational consent and reviewed dependency versions.

Mitigation: Confirm applicable consent requirements before deployment and pin reviewed Agnost SDK versions.

## Reference(s):

- [Agnost API Reference](references/api-reference.md)
- [Python SDK Reference](references/python-sdk.md)
- [TypeScript SDK Reference](references/typescript-sdk.md)
- [Agnost Documentation](https://docs.agnost.ai)
- [Agnost Dashboard](https://app.agnost.ai)
- [ClawHub Skill Page](https://clawhub.ai/ajmeraparth132/skills/agnost-ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline Python, TypeScript, Go, HTTP, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SDK setup steps, API request examples, and privacy safeguards for analytics payloads.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
