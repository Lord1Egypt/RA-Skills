## Description: <br>
Foreseek AI helps agents parse natural-language predictions, find matching Kalshi prediction-market contracts, and execute or manage related orders through Foreseek. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HypeGamer007](https://clawhub.ai/user/HypeGamer007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent search prediction markets, parse event beliefs into candidate Kalshi contracts, inspect positions and balances, and place or manage orders through a Foreseek account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live Kalshi trades and expose financial account data. <br>
Mitigation: Install only when account access is intended, use the least-privilege API key available, start with demo or small limit orders, and require confirmation of ticker, side, order type, contract count, and estimated cost before live trades. <br>
Risk: The FORESEEK_API_KEY grants access to Foreseek operations and connected Kalshi account information. <br>
Mitigation: Store the key in an environment variable, avoid sharing it in prompts or logs, rotate it if exposed, and revoke keys that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/HypeGamer007/foreseekai) <br>
- [Foreseek Website](https://foreseek.ai) <br>
- [Foreseek Dashboard](https://foreseek.ai/dashboard) <br>
- [Foreseek Documentation](https://foreseek.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the FORESEEK_API_KEY environment variable and may return live account, market, order, balance, portfolio, and watchlist data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
