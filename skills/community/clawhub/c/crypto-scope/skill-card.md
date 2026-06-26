## Description: <br>
Crypto Scope helps agents query cryptocurrency prices, calculate technical indicators, and generate trading signals for monitored coins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imgolye](https://clawhub.ai/user/imgolye) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, traders, and Web3 developers use this skill to request price checks, MA/RSI/MACD analysis, and BUY/SELL/HOLD signal summaries from CoinGecko-backed data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds payment credentials and can charge a supplied user through SkillPay without a separate confirmation step. <br>
Mitigation: Review before installing, replace exposed payment credentials with a secure secret, and only provide a real user ID when per-call SkillPay charges are intended. <br>
Risk: Generated BUY, SELL, and HOLD signals may be inaccurate or misleading for financial decisions. <br>
Mitigation: Treat outputs as informational analysis only, verify market data and assumptions independently, and do not rely on the skill as investment advice. <br>


## Reference(s): <br>
- [Crypto Scope on ClawHub](https://clawhub.ai/imgolye/crypto-scope) <br>
- [CoinGecko](https://coingecko.com) <br>
- [CoinGecko Coin List](https://coingecko.com/coins) <br>
- [SkillPay](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON or plain text CLI output, with Markdown setup guidance in the artifact documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid paths require a user ID and may charge 0.05 USDT per call after a balance check.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
