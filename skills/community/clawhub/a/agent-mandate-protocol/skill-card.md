## Description:

Use A-MAP (Agent Mandate Protocol) to verify incoming agent requests, sign outgoing requests, and delegate permissions to sub-agents with cryptographic authorization controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmyshuyulee](https://clawhub.ai/user/jimmyshuyulee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add A-MAP request verification, request signing, and constrained sub-agent delegation to agent-to-agent workflows. It is intended for services that need to prove human authorization, reject replayed or tampered requests, and preserve narrowed permissions across delegation chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on @agentmandateprotocol/core for signing, verification, and delegation behavior.

Mitigation: Verify that @agentmandateprotocol/core is the intended package before installation and deployment.

Risk: AMAP_PRIVATE_KEY is a signing secret that can authorize outgoing A-MAP requests.

Mitigation: Store AMAP_PRIVATE_KEY only in protected environment configuration, never hardcode it, and never log it.

Risk: Signed mandate headers authorize specific downstream requests and could be misdirected if sent to unintended services.

Mitigation: Send signed A-MAP headers only to services the operator means to authorize.

Risk: Using an in-memory nonce store in a multi-instance deployment can miss replay detection across instances.

Mitigation: Use a shared nonce store such as Redis or Cloudflare KV behind load balancers or other multi-instance deployments.

Risk: Proceeding after verification errors or ignoring effective constraints can allow unauthorized or over-scoped actions.

Mitigation: Reject requests whenever verifyRequest throws, log the audit ID on success, and check effective constraints before consequential actions.

## Reference(s):

- [A-MAP Protocol Reference](references/amap-protocol.md)
- [A-MAP Delegation Invariants](references/delegation-invariants.md)
- [A-MAP Error Codes](references/error-codes.md)
- [A-MAP Signed Request Header Format](references/signed-request-format.md)
- [A-MAP OpenClaw Homepage](https://github.com/Agent-Mandate-Protocol/a-map/tree/main/sdks/typescript/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/jimmyshuyulee/skills/agent-mandate-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes A-MAP header names, delegation constraints, error codes, environment variables, and implementation guardrails.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
