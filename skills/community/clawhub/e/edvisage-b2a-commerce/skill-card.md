## Description:

Provides payment-safety guidance for OpenClaw agents using x402, including pre-transaction checks, spending limits, wallet-safety practices, transaction logging, and payment attack recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edvisage](https://clawhub.ai/user/edvisage)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to prepare payment-capable agents for safer business-to-agent transactions. It helps agents check service identity, payment scope, spending limits, wallet exposure, logs, and payment-specific attack patterns before committing funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment-safety guidance may be mistaken for a complete transaction implementation.

Mitigation: Treat it as guidance and independently validate wallet, payment, approval, and spending-limit logic before enabling real transactions.

Risk: A payment-capable agent could exceed intended spending or pay unapproved services.

Mitigation: Use internally consistent daily and per-transaction limits, human approval thresholds, and an approved-service whitelist before funding the wallet.

Risk: Wallet secrets or sensitive wallet material could be exposed through logs or agent-visible output.

Mitigation: Keep the wallet minimally funded and verify that logs, messages, API responses, and memory summaries never include private keys or sensitive wallet data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edvisage/skills/edvisage-b2a-commerce)
- [Edvisage publisher profile](https://clawhub.ai/user/edvisage)
- [Edvisage AI tools](https://edvisageglobal.com/ai-tools)
- [Pro version upgrade](https://edvisage.gumroad.com/l/ijjjud)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only safety guidance; does not provide a complete payment implementation.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
