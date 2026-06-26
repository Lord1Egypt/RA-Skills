## Description: <br>
Provides Decker trading assistance for signals, portfolio status, order requests, auto-order rules, news digest setup, Slack or Telegram integration, and exchange API key setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gigshow](https://clawhub.ai/user/gigshow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Decker users use this skill to ask an agent for trading signals, portfolio and position status, order and auto-order workflows, market news, and setup guidance for Slack, Telegram, Binance, Hyperliquid, and Polymarket. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat commands may initiate financially sensitive order, auto-order, portfolio, and credential workflows without consistently clear simulated versus live mode boundaries. <br>
Mitigation: Install only if you trust Decker as a trading service, start in simulated mode, verify whether each action is simulated or live, and review or disable active auto-order rules regularly. <br>
Risk: Exchange API keys or wallet credentials can expose trading accounts or on-chain funds if they are over-scoped or reused. <br>
Mitigation: Use limited-scope exchange keys with withdrawals disabled and dedicated wallets containing only trading funds for Hyperliquid or Polymarket. <br>


## Reference(s): <br>
- [Decker AI 트레이딩 on ClawHub](https://clawhub.ai/gigshow/decker) <br>
- [Decker](https://decker-ai.com) <br>
- [Decker Slack linking](https://decker-ai.com/decker-link) <br>
- [Decker Telegram linking](https://decker-ai.com/decker-link-telegram) <br>
- [User Guide](USER_GUIDE.md) <br>
- [API Quick Reference](references/API_QUICK.md) <br>
- [Questions List](references/QUESTIONS_LIST.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, configuration, API calls] <br>
**Output Format:** [Markdown or plain text agent responses with trading workflow guidance and service links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide financially sensitive trading workflows and uses a required OPENCLAW_SECRET credential for Decker integration.] <br>

## Skill Version(s): <br>
2.3.2 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
