## Description:

Build on Solana with Carbium infrastructure for RPC, WebSocket pubsub, gRPC full-block streaming, DEX aggregation, gasless swaps, and MEV-protected execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ukkometa](https://clawhub.ai/user/ukkometa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate Carbium RPC, WebSocket, gRPC streaming, Swap API, gasless swaps, and MEV-protected execution into Solana applications and trading systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live wallet signing and transaction submission can move funds or create unintended trades.

Mitigation: Never let an agent sign or submit transactions automatically; inspect and validate every transaction before signing.

Risk: Carbium API keys or wallet keys can be exposed if examples are copied into client-side or shared environments.

Mitigation: Keep Carbium keys and wallet keys server-side, prefer header authentication when supported, and rotate exposed keys immediately.

Risk: Trading, MEV-protected execution, and token-sniping flows can cause financial loss on mainnet.

Mitigation: Use the skill only for deliberate Solana infrastructure or trading work and test with unfunded or small-balance wallets before mainnet use.

Risk: Retries or low-validation transaction flows can submit incorrect, failed, or duplicate transactions.

Mitigation: Check transaction status before retrying, avoid automatic repeated submission, and review simulation or quote failures before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ukkometa/skills/carbium)
- [Carbium documentation](https://docs.carbium.io)
- [Ecosystem Overview](https://docs.carbium.io/docs/the-carbium-ecosystem)
- [RPC Quick Start](https://docs.carbium.io/docs/quick-start-rpc)
- [Swap API Quick Start](https://docs.carbium.io/docs/quick-start-dex-api)
- [gRPC / Streaming](https://docs.carbium.io/docs/solana-grpc)
- [CQ1 Engine](https://docs.carbium.io/docs/cq1-engine-overview)
- [API Recipes](https://docs.carbium.io/recipes)
- [Full AI Context](https://carbium.io/llms-ctx.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript, Python, Rust, Bash, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoints, authentication patterns, examples, and operational safety guidance.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
