## Description:

BridgeNode provides OpenAI-compatible LLM inference and MCP access for agents with x402 pay-per-request Solana USDC payments, free models, and no API keys or registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bridgenode](https://clawhub.ai/user/bridgenode)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and external agent operators use this skill to give agents pay-per-request LLM inference through an OpenAI-compatible endpoint or MCP tool when they do not want to manage provider API keys or subscriptions. It is most relevant for agents that can use free models or sign x402 Solana USDC payment requests for paid models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid examples and MCP setup can automatically spend real USDC.

Mitigation: Start with free models, use a dedicated low-balance Solana wallet, and require independent per-call and daily spending limits before running paid calls.

Risk: A payment request may quote an unexpected amount, asset, or recipient.

Mitigation: Verify every 402 amount, USDC asset, recipient, and memo before signing a payment transaction.

Risk: Unpinned package installs or npx commands can introduce supply-chain drift.

Mitigation: Prefer pinned package versions and review dependency changes before running examples or MCP commands.

## Reference(s):

- [BridgeNode website](https://bridgenode.cc)
- [Models and pricing endpoint](https://bridgenode.cc/v1/models)
- [BridgeNode MCP endpoint](https://bridgenode.cc/mcp)
- [BridgeNode agent card](https://bridgenode.cc/.well-known/agent-card.json)
- [x402 documentation](https://docs.x402.org)
- [ClawHub skill page](https://clawhub.ai/bridgenode/skills/bridgenode)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request bodies, and Python, TypeScript, curl, and MCP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent calls can return OpenAI-compatible JSON chat completions, streaming responses, tool-call messages, MCP tool results, and x402 payment headers.]

## Skill Version(s):

1.0.36 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
