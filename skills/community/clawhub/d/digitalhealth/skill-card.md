## Description: <br>
Implements USDC x402 payments via PayAI and DHM x402 payments via EVVM native signed pay for the ClawHub/NHS EVVM app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arunnadarasa](https://clawhub.ai/user/arunnadarasa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add or debug x402 payment flows for USDC through PayAI Echo, DHM through EVVM pay(), and agent-to-agent payments with Privy server wallets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-signing guidance could be applied with incorrect token, amount, recipient, chain, nonce, or expiry values. <br>
Mitigation: Validate token, amount, recipient, chain, nonce, and expiry before production signing. <br>
Risk: Agent-payment flows can spend funds autonomously if wallet controls are too broad. <br>
Mitigation: Use testnet or strict spend limits first and review Privy server-wallet policies before enabling production agent payments. <br>
Risk: Payment integrations may expose sensitive wallet or executor credentials if copied into source control or logs. <br>
Mitigation: Keep secrets out of source control and logs, and review required environment variables before deployment. <br>


## Reference(s): <br>
- [Digital Health ClawHub listing](https://clawhub.ai/arunnadarasa/digitalhealth) <br>
- [Publisher profile](https://clawhub.ai/user/arunnadarasa) <br>
- [PayAI Echo Base Sepolia paid content endpoint](https://x402.payai.network/api/base-sepolia/paid-content) <br>
- [DHM x402 EVVM server](https://evvm-x402-dhm.fly.dev) <br>
- [Privy agentic wallets skill](https://github.com/privy-io/privy-agentic-wallets-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript type snippets, shell commands, endpoint references, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for payment signing flows, request payloads, environment variables, and debugging checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
