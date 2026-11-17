## Description:

HSM-backed secret management for AI agents: store, retrieve, rotate, and share secrets via the 1Claw vault without exposing them in conversation context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kmjones1979](https://clawhub.ai/user/kmjones1979)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to let agents retrieve, store, rotate, and share vault-managed credentials at runtime. It also supports optional EVM transaction simulation and signing when explicitly enabled and governed by configured access policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may receive broad authority over vaults, secrets, policies, and shares.

Mitigation: Grant only the vault paths, permissions, and token lifetimes needed for the task, and avoid broad policy creation unless required.

Risk: Raw secrets and environment bundles returned by tools may become visible to the agent or model.

Mitigation: Fetch secrets only when needed, avoid summarizing or echoing secret values, and treat tool results as sensitive.

Risk: Optional transaction signing can authorize blockchain actions if enabled.

Mitigation: Enable transaction signing only when necessary and configure narrow transaction guardrails before use.

## Reference(s):

- [1Claw Skill on ClawHub](https://clawhub.ai/kmjones1979/skills/1claw)
- [1Claw Dashboard](https://1claw.xyz)
- [1Claw Documentation](https://docs.1claw.xyz)
- [1Claw MCP Server npm package](https://www.npmjs.com/package/@1claw/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, TypeScript, shell command, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe or invoke vault, secret, policy, sharing, and transaction-related operations when the agent has the required 1Claw credentials and permissions.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
