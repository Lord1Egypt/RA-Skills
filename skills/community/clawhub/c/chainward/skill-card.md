## Description: <br>
Monitor AI agent wallets on Base. Register wallets, check health scores, view transactions, manage alerts, and watch live feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saltxd](https://clawhub.ai/user/saltxd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use ChainWard to monitor AI agent wallets on Base, register and remove wallets, inspect balances and transactions, and configure alerts through the ChainWard CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ChainWard API key and uses the external @chainward/cli package. <br>
Mitigation: Install only when the ChainWard service and npm package are trusted, and use a dedicated API key where possible. <br>
Risk: Wallet activity data may be sent to Discord, Telegram, or webhook alert destinations. <br>
Mitigation: Configure alert channels only where the monitored wallet activity can be shared safely. <br>


## Reference(s): <br>
- [ChainWard homepage](https://chainward.ai) <br>
- [ClawHub ChainWard listing](https://clawhub.ai/saltxd/chainward) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the chainward CLI and CHAINWARD_API_KEY; supports Base-chain wallet monitoring and alert setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
