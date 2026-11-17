## Description:

Track AI agent usage and costs with Drip metered billing. Use when you need to record aggregate LLM usage, tool calls, agent runs, or other metered usage for billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucas-309](https://clawhub.ai/user/lucas-309)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to add Drip metered billing telemetry to AI agents, LLM calls, tool invocations, and customer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent billing and customer-operation authority.

Mitigation: Use pk_test_ for testing or a least-privileged pk_live_ key for production, avoid sk_ keys unless admin operations are required, and require human approval for billing or customer-changing actions.

Risk: The skill documents npm/npx package execution with an API key.

Mitigation: Pin package versions instead of using unversioned npm/npx commands and verify the package source before installation.

Risk: Telemetry metadata may contain sensitive data if callers pass raw user or system content.

Mitigation: Use a strict metadata allowlist and redaction policy; do not send PII, secrets, raw prompts, model outputs, request bodies, file contents, or source code.

## Reference(s):

- [Drip SDK API Reference](references/API.md)
- [Drip SDK npm package](https://www.npmjs.com/package/@drip-sdk/node)
- [ClawHub skill page](https://clawhub.ai/lucas-309/skills/drip-billing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, JSON, TypeScript, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DRIP_API_KEY and a trusted DRIP_BASE_URL; guidance emphasizes sanitized metadata and least-privileged keys.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
