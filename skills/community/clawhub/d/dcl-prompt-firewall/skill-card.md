## Description:

DCL Prompt Firewall screens untrusted input for prompt injection, jailbreak, role-switch, and instruction-override attempts before the input reaches a model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daririnch](https://clawhub.ai/user/daririnch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to gate user-supplied messages, retrieved documents, web content, and tool results before forwarding them to an LLM. It supports either a paid DCL Trust Oracle MCP check or a local instruction-only checklist for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The live screening path sends raw input to a paid third-party MCP service.

Mitigation: Review before installing, avoid sending secrets, credentials, private documents, or regulated data, and apply local redaction before live checks when sensitive content may be present.

Risk: Paid live calls can trigger USDC-on-Base wallet payments.

Mitigation: Configure wallet spending limits and require explicit confirmation for paid calls before enabling the live MCP path.

Risk: The security verdict flags unclear data and spending controls.

Mitigation: Use the free checklist or add strict approval controls unless the operator accepts the live-service data flow and payment model.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daririnch/skills/dcl-prompt-firewall)
- [ClawHub publisher profile](https://clawhub.ai/user/daririnch)
- [DCL Trust Oracle MCP endpoint](https://mcp.fronesislabs.com/mcp)
- [DCL Security Suite](https://hub.fronesislabs.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live checks return a verdict, confidence score, reason, transaction hash, input hash, policy version, drift mode, and drift score.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
