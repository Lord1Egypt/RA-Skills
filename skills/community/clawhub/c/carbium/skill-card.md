## Description: <br>
Guides agents through using Carbium Solana infrastructure for RPC, WebSocket subscriptions, gRPC block streaming, DEX swap quotes and execution, gasless swaps, MEV-protected bundles, and migration from other providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ukkometa](https://clawhub.ai/user/ukkometa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate Solana applications, wallets, trading bots, and migration workflows with Carbium RPC, WebSocket, gRPC, and Swap API surfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples can sign and broadcast real Solana transactions. <br>
Mitigation: Use burner wallets or devnet where possible, cap trade amounts and slippage, and require human review before signing or submitting transactions. <br>
Risk: Server-generated swap transactions may move funds if signed without inspection. <br>
Mitigation: Decode or simulate any generated transaction before signing and verify route, token mints, amounts, fees, and recipient accounts. <br>
Risk: API keys, signed transactions, or wallet material may be exposed in logs or client-side code. <br>
Mitigation: Keep credentials server-side in environment variables, avoid logging URLs or transaction payloads containing secrets, and rotate exposed keys immediately. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ukkometa/carbium) <br>
- [Carbium Documentation](https://docs.carbium.io) <br>
- [Ecosystem Overview](https://docs.carbium.io/docs/the-carbium-ecosystem) <br>
- [RPC Quick Start](https://docs.carbium.io/docs/quick-start-rpc) <br>
- [Swap API Quick Start](https://docs.carbium.io/docs/quick-start-dex-api) <br>
- [gRPC / Streaming](https://docs.carbium.io/docs/solana-grpc) <br>
- [CQ1 Engine](https://docs.carbium.io/docs/cq1-engine-overview) <br>
- [Endpoints, Authentication & Pricing](resources/endpoints-and-auth.md) <br>
- [Swap API Reference](resources/swap-api-reference.md) <br>
- [gRPC Reference](resources/grpc-reference.md) <br>
- [WebSocket Reference](resources/websocket-reference.md) <br>
- [Trading Bot Architecture](docs/trading-bots.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline TypeScript, Python, Rust, JSON, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation guidance and examples that may include API calls, environment variables, transaction signing flows, and operational checks.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
