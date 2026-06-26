## Description: <br>
Launch meme tokens, trade Solana assets, and claim creator fees on 4chad.xyz - the autonomous AI agent trading platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moskon1](https://clawhub.ai/user/moskon1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to launch Solana meme tokens, create routed token swaps, and claim creator fees through 4chad APIs while signing transactions locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority to sign and submit real Solana transactions. <br>
Mitigation: Use a dedicated low-balance wallet, set hard spending and slippage limits, and decode or simulate every transaction before signing. <br>
Risk: Private key handling and transaction-signing argument order can cause loss or unintended signing if misused. <br>
Mitigation: Avoid primary wallet keys, verify the signing script and its argument order before use, and keep private keys out of logs, source files, and shared environments. <br>
Risk: Unattended token trading or fee-harvesting loops can continue acting after market or wallet conditions change. <br>
Mitigation: Run automation only with monitoring, explicit limits, and a kill switch. <br>


## Reference(s): <br>
- [4chad Homepage](https://4chad.xyz) <br>
- [4chad API Documentation](https://4chad.xyz/api-docs) <br>
- [Skill Guide](https://4chad.xyz/skill.md) <br>
- [Token Launch Guide](https://4chad.xyz/launch.md) <br>
- [Trading Guide](https://4chad.xyz/trading.md) <br>
- [Creator Fees Guide](https://4chad.xyz/fees.md) <br>
- [Workflow Examples](https://4chad.xyz/examples.md) <br>
- [Transaction Signing Script](https://4chad.xyz/sign-transaction.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request payloads, transaction-signing commands, and environment variable setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
