## Description: <br>
Bybit AI Trading Skill helps agents trade on Bybit using natural language across spot, derivatives, earn, and related exchange workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[victorwu-bybit](https://clawhub.ai/user/victorwu-bybit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to configure Bybit credentials, inspect market and account state, and prepare or execute exchange actions through an AI assistant. It is intended for broad trading workflows, including spot, derivatives, earn, fiat, copy trading, trading bots, strategy orders, and account management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad financial actions on a real Bybit account, including trades and product interactions. <br>
Mitigation: Use a dedicated limited-balance sub-account, start with testnet or read-only access, require confirmation for mainnet write actions, and never enable withdrawals for AI use. <br>
Risk: The skill requires sensitive exchange credentials and may be used from hosted AI services. <br>
Mitigation: Prefer local environment variables or a self-hosted secret store; avoid pasting real API secrets into hosted AI sessions. <br>
Risk: The skill includes automatic remote self-updating behavior that can replace local skill files. <br>
Mitigation: Review updates before installation where possible and rely on the documented checksum and path validation controls before using updated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/victorwu-bybit/bybit-exchange-trading-skill) <br>
- [Bybit website](https://www.bybit.com) <br>
- [Bybit API management](https://www.bybit.com/app/user/api-management) <br>
- [Bybit API base URL](https://api.bybit.com) <br>
- [Bybit testnet API base URL](https://api-testnet.bybit.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-style API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading confirmations, simulated examples when live execution is unavailable, and credential setup guidance.] <br>

## Skill Version(s): <br>
1.4.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
