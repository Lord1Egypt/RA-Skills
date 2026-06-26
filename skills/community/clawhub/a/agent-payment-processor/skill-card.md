## Description: <br>
Use Paegents through the published SDK and API surface to register services, create usage agreements, activate bilateral escrow, route metered usage, and settle with the recommended execution mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markmcdaniels](https://clawhub.ai/user/markmcdaniels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and buyer or seller agents use this skill to integrate Paegents payments through the public SDK and API. It helps register services, create and activate bilateral escrow agreements, route metered usage, and choose settlement actions from current agreement state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide payment, escrow activation, and settlement workflows that may move or lock real funds. <br>
Mitigation: Use sandbox or testnet flows first, verify agreement amounts and state from live responses, and require explicit review before activating escrow or initiating settlement. <br>
Risk: Paegents API keys, seller API keys, wallet private keys, and other credentials could be exposed during setup or troubleshooting. <br>
Mitigation: Use least-privilege scoped keys stored in the environment or a secret manager, and keep secrets out of chat, logs, repositories, and shell history. <br>
Risk: Service registration, proxy traffic, webhooks, auto-accept behavior, and seller credentials can authorize external actions beyond a simple read-only integration. <br>
Mitigation: Review endpoint URLs, webhook creation, seller credentials, auto-accept settings, and approval policy before enabling them in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/markmcdaniels/agent-payment-processor) <br>
- [Publisher profile](https://clawhub.ai/user/markmcdaniels) <br>
- [Paegents homepage](https://paegents.com) <br>
- [Skill metadata repository](https://github.com/MarkMcDaniels/paegents-pay-skill) <br>
- [Quick Start](references/QUICK_START.md) <br>
- [Payment Flows](references/PAYMENT_FLOWS.md) <br>
- [SDK Usage](references/SDK_USAGE.md) <br>
- [API Reference](references/API_REFERENCE.md) <br>
- [Error Codes](references/ERROR_CODES.md) <br>
- [Rate Limits](references/RATE_LIMITS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with SDK examples, API references, shell commands, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Paegents environment variables and supervised handling of payment and wallet credentials.] <br>

## Skill Version(s): <br>
2.9.1 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
