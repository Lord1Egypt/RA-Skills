## Description: <br>
Autonomous Wallet helps AI agents operate a local crypto wallet through natural-language intents, transaction execution, self-healing retries, and guardian-based recovery workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to configure wallet credentials, check balances, execute transfers or DeFi intents, simulate transactions, and manage social recovery for EVM-chain wallets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may initiate irreversible transfers, swaps, approvals, staking, or recovery actions with real funds. <br>
Mitigation: Use a dedicated low-balance wallet, test on testnets first, require simulation and explicit human confirmation before mainnet actions, and configure daily limits. <br>
Risk: Private keys or seed phrases may be exposed if entered into chat, shell history, or persistent environment files. <br>
Mitigation: Prefer hardware wallets or secure signers, avoid pasting seed phrases or private keys into prompts or shell commands, and keep credentials out of persistent files where possible. <br>
Risk: Automated retry and gas adjustment behavior can increase cost or repeat unintended transactions. <br>
Mitigation: Set maximum gas and spending limits, inspect dry-run output, and keep transaction simulation enabled before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ZhenStaff/autonomous-wallet) <br>
- [Publisher profile](https://clawhub.ai/user/ZhenStaff) <br>
- [Source repository](https://github.com/ZhenRobotics/openclaw-autonomous-wallet) <br>
- [npm package](https://www.npmjs.com/package/openclaw-autonomous-wallet) <br>
- [Documentation](https://docs.openclaw.ai/wallet) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, configuration examples, TypeScript snippets, and JSON transaction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that initialize wallets, import credentials, execute blockchain intents, simulate transactions, and configure spending or recovery controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
