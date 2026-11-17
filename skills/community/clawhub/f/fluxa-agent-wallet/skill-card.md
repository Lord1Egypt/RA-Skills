## Description:

FluxA Agent Wallet lets AI agents use a linked user wallet, within approved scope, for x402 payments, USDC transfers, payment links, prepaid cards, agent identity credentials, and payment-enabled services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cpppppp7](https://clawhub.ai/user/cpppppp7)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an AI agent set up a FluxA wallet identity, request user-approved spending mandates, make or receive payments, and integrate FluxA payment flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is payment-related and can link an agent to a user wallet.

Mitigation: Install only when the user accepts wallet linkage, and require confirmation before transfers, paid API calls, reward claims, social actions, or card-detail display.

Risk: Reusable spending mandates can authorize repeated payments within an approved scope.

Mitigation: Use narrow mandate purpose, amount, and duration limits, verify remaining budget before reuse, and review or delete stored mandates when they are no longer needed.

Risk: The scheduled wallet check creates recurring wallet access and received-payment inspection.

Mitigation: Enable the scheduled task only after explicit user opt-in and make clear that it runs twice daily.

Risk: Unpinned or latest CLI usage can change behavior after installation.

Mitigation: Pin CLI versions where possible and review release notes or fetched skill updates before relying on changed commands.

Risk: Wallet records and prepaid card details may expose sensitive financial information.

Mitigation: Ask for confirmation before displaying received-payment records or full card details, and avoid retaining sensitive output beyond the active task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cpppppp7/skills/fluxa-agent-wallet)
- [SKILL.md](artifact/SKILL.md)
- [Mandate Planning Policy](artifact/MANDATE-PLANNING.md)
- [x402 Payment Reference](artifact/X402-PAYMENT.md)
- [Payout CLI Reference](artifact/PAYOUT.md)
- [Payment Link CLI Reference](artifact/PAYMENT-LINK.md)
- [Transfer to Agent](artifact/TRANSFER-TO-AGENT.md)
- [Agent Verifiable Credential CLI Reference](artifact/VC-ISSUE.md)
- [FluxA Wallet Daily Check Scheduled Task Setup](artifact/SCHEDULED-CHECKIN.md)
- [Agent ID Integration Guide](artifact/INTEGRATION-GUIDE-AGENTID.md)
- [Pay to Agent Integration Guide](artifact/INTEGRATION-GUIDE-PAY-TO-AGENT.md)
- [Charge Agent Integration Guide](artifact/INTEGRATION-GUIDE-CHARGE-AGENT.md)
- [Payout Integration Guide](artifact/INTEGRATION-GUIDE-PAYOUT.md)
- [ClawPI Reference](artifact/CLAWPI.md)
- [Oneshot API Trial Guide](artifact/TRY-ONESHOT-API.md)
- [x402 Services Reference](artifact/x402-SERVICES.md)
- [FluxA Agent ID JWT Verification Documentation](https://docs.fluxapay.xyz/wallet/agent-guide-jwt-verification.html)
- [FluxA Skill Source](https://fluxapay.xyz/skill.md)
- [FluxA Oneshot API Discovery](https://monetize.fluxapay.xyz/api/discover?type=api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands, JSON examples, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to install and run the FluxA CLI, create local wallet and mandate state, open user authorization URLs, and call external FluxA services.]

## Skill Version(s):

1.4.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
