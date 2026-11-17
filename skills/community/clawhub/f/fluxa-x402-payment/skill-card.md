## Description:

A FluxA Agent Wallet skill that enables agents to request budgets, sign x402 payments, and call paid endpoints autonomously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cpppppp7](https://clawhub.ai/user/cpppppp7)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to request an approved FluxA wallet budget, generate x402 payment headers, and call paid API endpoints within that budget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled wallet CLI includes payment authority beyond x402 paid API calls.

Mitigation: Review or remove payout commands and require explicit user approval for each payment or transfer before use.

Risk: Wallet credentials may be stored in ways users should review carefully.

Mitigation: Protect or avoid plaintext stored credentials and restrict access to the runtime environment.

Risk: API endpoint overrides can redirect wallet or agent identity requests.

Mitigation: Restrict API endpoint overrides to trusted FluxA endpoints before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cpppppp7/skills/fluxa-x402-payment)
- [Skill instructions](artifact/SKILL.md)
- [FluxA CLI error handling](artifact/error-handle.md)
- [Initialize Agent ID](artifact/initialize-agent-id.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before requesting wallet mandates or payments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
