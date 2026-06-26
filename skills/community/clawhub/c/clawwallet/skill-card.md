## Description: <br>
Clawwallet lets agents manage multi-chain wallets, DeFi operations, multi-signature transactions, ENS registration, policy checks, agent identity, and wallet event workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vibes-me](https://clawhub.ai/user/vibes-me) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect an AI agent to wallet infrastructure for creating wallets, checking balances, sending funds, using DeFi services, managing policies, and monitoring wallet activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent direct authority over private keys, payments, swaps, staking, bridge transfers, and other fund-moving wallet actions. <br>
Mitigation: Install only when the publisher and configured CLAW_WALLET_URL backend are trusted; start with testnet or low-value wallets and require human approval, spend limits, destination allowlists, and transaction previews before fund-moving calls. <br>
Risk: Wallet service credentials and webhook secrets may expose sensitive wallet workflows if configured carelessly. <br>
Mitigation: Limit access to CLAW_WALLET_API_KEY and webhook secrets, use a controlled backend, and avoid importing valuable private keys unless that service is intended to control them. <br>


## Reference(s): <br>
- [Clawwallet on ClawHub](https://clawhub.ai/vibes-me/clawwallet) <br>
- [CLAWwallet documentation](https://clawwallet.pages.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Code, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [JavaScript module with JSON-like method responses from the configured wallet service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CLAW_WALLET_URL, CLAW_WALLET_API_KEY, and CLAW_WALLET_CHAIN configuration; methods can request wallet, transaction, DeFi, policy, identity, webhook, history, and diagnostic operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
