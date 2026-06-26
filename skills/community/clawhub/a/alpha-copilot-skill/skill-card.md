## Description: <br>
Generate a daily priority leaderboard for 5 crypto tokens, with per-token fundamentals, liquidity, and risk summaries plus ready-to-publish drafts for X posts, group updates, and quick briefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2663629531](https://clawhub.ai/user/2663629531) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External crypto research operators use this skill to generate a daily top-token watchlist from Binance Web3 market signals, with fundamentals, liquidity, risk summaries, and publish-ready drafts. It supports JSON or Markdown output and includes a SkillPay billing hook for successful ranking runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Successful rank runs may trigger the disclosed SkillPay billing hook. <br>
Mitigation: Use --skip-billing or SKILLPAY_BILLING_MODE=noop for testing, and provide SKILLPAY_APIKEY only for intended paid runs. <br>
Risk: Proxy-check output can include proxy configuration details that may expose sensitive network information. <br>
Mitigation: Do not share proxy-check output externally unless proxy URLs and related network details have been removed. <br>
Risk: Crypto rankings and generated drafts could be misread as investment advice. <br>
Mitigation: Keep the report disclaimer, review generated content before publication, and do not use the skill for automated trading decisions. <br>
Risk: Upstream market, metadata, or audit enrichment can be unavailable or incomplete. <br>
Mitigation: Run proxy-check when connectivity fails and review unavailable audit or metadata fields before relying on the report. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/2663629531/alpha-copilot-skill) <br>
- [Publisher profile](https://clawhub.ai/user/2663629531) <br>
- [Binance Web3 market data source](https://web3.binance.com) <br>
- [SkillPay billing endpoint base](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON or Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs a top-token leaderboard, per-token summaries, publish-ready draft copy, UTC generation time, and billing status for rank runs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
