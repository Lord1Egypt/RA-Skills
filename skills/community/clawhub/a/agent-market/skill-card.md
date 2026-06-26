## Description: <br>
Interact with the AgentMarket protocol on Base Sepolia to create, trade, provide liquidity, and resolve USDC-settled YES/NO prediction markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[humanjesse](https://clawhub.ai/user/humanjesse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to interact with a Base Sepolia prediction-market protocol, including market discovery, market creation, YES/NO trading, liquidity management, claims, and optimistic-oracle resolution actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign approvals and on-chain transactions for trades, liquidity, oracle bonds, disputes, finalization, arbitration, resets, emergency withdrawals, and claims. <br>
Mitigation: Require manual review before every wallet-signing action and use a dedicated low-balance Base Sepolia wallet. <br>
Risk: A reused private key, incorrect RPC endpoint, or incorrect contract address could expose funds or route actions to the wrong contracts. <br>
Mitigation: Do not use a primary private key; verify RPC_URL, AGENT_MARKET_FACTORY_ADDRESS, and USDC_ADDRESS before enabling the skill. <br>
Risk: Prediction-market and oracle actions can create financial loss or incorrect market resolution if the agent acts on weak or stale information. <br>
Mitigation: Review market questions, amounts, deadlines, proposed outcomes, and arbitration decisions outside the agent before execution. <br>


## Reference(s): <br>
- [Agent Market on ClawHub](https://clawhub.ai/humanjesse/agent-market) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and JSON strings with market data, status summaries, transaction hashes, configuration guidance, and operational instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some tools submit on-chain transactions and may return irreversible transaction status once signed by the configured wallet.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
