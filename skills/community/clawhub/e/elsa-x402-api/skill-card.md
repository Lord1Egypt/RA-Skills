## Description: <br>
DeFi tools for portfolio analysis, token search, and swap execution via Elsa API with x402 micropayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justjkk](https://clawhub.ai/user/justjkk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to query DeFi portfolio, token, wallet-risk, and pricing data and to run opt-in swap workflows through the Elsa API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use local private keys to spend funds and sign blockchain transactions supplied by an external API. <br>
Mitigation: Install with a dedicated low-balance payment wallet and a separate limited trading wallet; prefer external_signer mode and inspect every transaction before signing. <br>
Risk: Execution tools can perform real onchain transactions when enabled. <br>
Mitigation: Keep execution tools disabled unless prepared for real transactions, use the dry-run and confirmation flow, and avoid calling execution tools in loops. <br>
Risk: Advertised daily budget limits may not be a hard safety boundary if the host does not preserve budget state. <br>
Mitigation: Run the skill in a persistent process or add persistent budget enforcement before relying on daily budget limits. <br>
Risk: Debug logging or unsafe host configuration could expose sensitive transaction or wallet details. <br>
Mitigation: Avoid debug logging and keep payment and trading private keys scoped to low-value wallets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justjkk/elsa-x402-api) <br>
- [Elsa API](https://x402.heyelsa.ai) <br>
- [x402 Protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command inputs; tool calls return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PAYMENT_PRIVATE_KEY for x402 payments; execution tools require explicit opt-in and may use TRADE_PRIVATE_KEY for transaction signing.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
