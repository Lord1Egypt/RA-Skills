## Description: <br>
Pay for MCP tool calls on Hedera using x402 micropayments, discover AI agents via on-chain registry, check reputation before transacting, and submit ratings after tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EmadQureshiKhi](https://clawhub.ai/user/EmadQureshiKhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to handle paid MCP tool calls, discover Hedera-hosted agent services, check reputation before payment, and submit ratings after tool use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blockchain private keys may be exposed if passed through command-line flags or logged during setup and use. <br>
Mitigation: Use SDK modes that read credentials from environment variables or a secret manager, and use only a dedicated Hedera testnet wallet or a wallet with minimal funds. <br>
Risk: Mainnet use grants real spending authority and can create irreversible payment activity. <br>
Mitigation: Keep workflows on Hedera testnet by default, confirm any mainnet switch explicitly, and maintain strict per-call spending caps. <br>


## Reference(s): <br>
- [x402 Payment Flow on Hedera](references/x402-flow.md) <br>
- [ClawPay-Hedera source](https://github.com/aspect-build/clawpay-hedera) <br>
- [ClawPay agent dashboard](https://clawpay-hedera.vercel.app/agents) <br>
- [Hedera testnet registry contract](https://hashscan.io/testnet/contract/0x411278256411dA9018e3c880Df21e54271F2502b) <br>
- [Hedera testnet reputation topic](https://hashscan.io/testnet/topic/0.0.8107518) <br>
- [ClawHub skill page](https://clawhub.ai/EmadQureshiKhi/clawpay-hedera) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npx, and HEDERA_PRIVATE_KEY for payment workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
