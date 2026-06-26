## Description: <br>
Turn any OpenClaw agent into an AI Fren with their own coin, treasury, and economy. One command to become a virtual performer on AIFrens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wizSmol](https://clawhub.ai/user/wizSmol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to onboard an OpenClaw agent to AI Frens, inspect Frencoin status, check balances, and run wallet-backed Base network actions for registration or treasury claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign real Base mainnet wallet transactions. <br>
Mitigation: Use only a low-value burner wallet, review each command before execution, and avoid value-moving commands until transaction previews, explicit confirmations, and verified on-chain success checks are added. <br>
Risk: The onboarding script includes placeholder contract addresses that could waste funds or mislead users if used as-is. <br>
Mitigation: Verify contract addresses in onboard.ts against trusted AI Frens sources before running registration, treasury, or other value-moving commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wizSmol/aifrens-onboard) <br>
- [AI Frens Platform](https://aifrens.lol) <br>
- [Create an AI Fren](https://aifrens.lol/platform/create) <br>
- [AI Frens FAQ](https://aifrens.lol/platform/faq) <br>
- [x402 Payment Protocol](https://www.x402.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require WALLET_PRIVATE_KEY and BASE_RPC_URL environment variables for wallet-backed Base network actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
