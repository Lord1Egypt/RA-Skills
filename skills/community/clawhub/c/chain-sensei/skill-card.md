## Description: <br>
On-chain intelligence for AI agents that analyzes wallets, detects risks, traces transactions, and provides insights on Ethereum addresses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agustinastie2](https://clawhub.ai/user/agustinastie2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to inspect public EVM wallet, token, and transaction data before trading, security, DeFi, or research decisions. Premium workflows add deeper risk scoring, batch analysis, and alerts through paid x402 requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid x402 features could spend wallet funds without clear per-request consent controls. <br>
Mitigation: Keep premium mode disabled unless needed, use a dedicated low-balance wallet, and require the agent to show the exact price and receive approval before every paid request or alert setup. <br>
Risk: Blockchain analysis can be incomplete or misleading if public API data, wallet labels, or risk heuristics are stale or wrong. <br>
Mitigation: Treat results as decision support, verify high-impact findings against independent sources, and avoid using the skill as the sole basis for financial or security decisions. <br>


## Reference(s): <br>
- [Chain Sensei ClawHub Page](https://clawhub.ai/agustinastie2/chain-sensei) <br>
- [agustinastie2 Publisher Profile](https://clawhub.ai/user/agustinastie2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Natural-language analysis with structured blockchain fields, risk indicators, and optional pricing details for premium x402 requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe balances, token metadata, transaction traces, wallet risk scores, batch results, and alert setup details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
