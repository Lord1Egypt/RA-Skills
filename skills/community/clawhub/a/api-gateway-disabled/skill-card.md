## Description:

Connects agents to 100+ third-party APIs through Maton's managed OAuth gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyuechuimeng](https://clawhub.ai/user/xiyuechuimeng)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to make authenticated calls to supported third-party services and manage OAuth-backed connections through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent modify, delete, send, or administer data across many connected services.

Mitigation: Use least-privilege OAuth scopes, specify the intended connection when multiple exist, and require explicit human confirmation before deletes, sends, financial or admin changes, or public posts.

Risk: The Maton API key can be exposed if printed, pasted, or included in logs or transcripts.

Mitigation: Do not print or paste MATON_API_KEY, keep it in the environment or a secret store, and rotate it if it appears in logs or transcripts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/xiyuechuimeng/skills/api-gateway-disabled)
- [Maton homepage](https://maton.ai)
- [Maton API Reference](https://www.maton.ai/docs/api-reference)
- [API Gateway skill instructions](SKILL.md)
- [Supported service reference docs](references/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with endpoint patterns and Python, curl, and shell snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and user-authorized OAuth connections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
