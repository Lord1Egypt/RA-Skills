## Description: <br>
Crypto Trading instructs an agent to run a recurring crypto trading decision loop that gathers market and account data, compares Dify AI and OpenClaw analyses, applies trading rules, records decisions, and executes market orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WuZiMaKi](https://clawhub.ai/user/WuZiMaKi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and trading automation operators use this skill to have an agent evaluate BTC, ETH, and BNB markets, compare independent AI analyses, apply rule checks, and record buy, sell, or hold decisions before trade execution. It should be reviewed carefully before use with live exchange accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring automatic market-order trading can create financial exposure if user controls, position limits, or loss limits are missing or misconfigured. <br>
Mitigation: Review carefully before live use, use trade-only keys with withdrawals disabled, and set strict position and loss limits. <br>
Risk: The skill depends on external AI analysis providers and does not define clear data-sharing boundaries. <br>
Mitigation: Confirm what market, account, and trading data is sent to external providers before enabling the workflow. <br>
Risk: The artifact describes automation and stored trading state without a clearly documented stop or cleanup path. <br>
Mitigation: Require an operator-visible stop mechanism and a process to remove stored trading state before deployment. <br>


## Reference(s): <br>
- [Crypto Trading Skill Source](artifact/SKILL.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/WuZiMaKi/crypto-trading) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions with structured trading decisions and state or log updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces buy, sell, or hold decisions, rule-check rationale, execution records, and trading memory updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
