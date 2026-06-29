## Description: <br>
Bybit AI Trading Skill - Trade on Bybit using natural language. Covers spot, derivatives, earn, and more. Works with Claude, ChatGPT, OpenClaw, and any AI assistant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[victorwu-bybit](https://clawhub.ai/user/victorwu-bybit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an AI assistant prepare Bybit market queries, account checks, trading workflows, and configuration guidance from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate with Read+Trade credentials for a real Bybit account. <br>
Mitigation: Use a limited subaccount, start on Testnet, fund only a bounded amount, and never enable Withdraw permission. <br>
Risk: Hosted AI platforms may require users to paste API credentials into the chat session. <br>
Mitigation: Prefer local environment variables or a self-hosted environment; if hosted chat is unavoidable, use a limited subaccount and rotate keys after use. <br>
Risk: The skill includes a self-update path that can change local skill instructions. <br>
Mitigation: Disable or manually review self-updates where the agent platform allows it, and verify update integrity before accepting changed instructions. <br>
Risk: Mainnet trading can affect real funds if a user confirms a write operation. <br>
Mitigation: Require explicit human confirmation for each Mainnet write action and review order size, symbol, side, environment, and estimated value before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/victorwu-bybit/skills/bybit-exchange-trading-skill) <br>
- [Bybit AI Subaccount help article](https://www.bybit.com/en/help-center/article/Introduction-to-the-AI-Subaccount) <br>
- [Bybit API mainnet endpoint](https://api.bybit.com) <br>
- [Bybit API testnet endpoint](https://api-testnet.bybit.com) <br>
- [Bybit API management](https://www.bybit.com/app/user/api-management) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API call instructions] <br>
**Output Format:** [Markdown with inline shell commands, API request examples, confirmation cards, and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured trade confirmation cards and simulated examples when live execution is unavailable.] <br>

## Skill Version(s): <br>
1.4.5 (source: evidence release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
