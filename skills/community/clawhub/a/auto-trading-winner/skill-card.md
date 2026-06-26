## Description: <br>
Cross-venue trading skill for ClawHub that supports both manual candidate selection and unattended auto mode, while filtering markets by price band and trading volume. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skybinjf](https://clawhub.ai/user/skybinjf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan Simmer, Kalshi, or Polymarket markets, review ranked candidates, and run dry-run or explicitly enabled live trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run on a 30-minute schedule and may place unattended trades when live and auto modes are enabled. <br>
Mitigation: Keep the skill in dry-run or manual mode until the strategy is reviewed, and disable or tightly control scheduled automation before enabling live execution. <br>
Risk: Live trading requires sensitive credentials and can expose real funds on connected venues or wallets. <br>
Mitigation: Use limited-scope credentials with limited funds, store secrets only in runtime environment variables, and set external account-level risk limits. <br>
Risk: The default strategy is a template based on volume ranking and a price-band filter, so its selections may not reflect a reliable trading edge. <br>
Mitigation: Review and adapt the strategy, sizing, and fair-value assumptions before relying on it for live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skybinjf/auto-trading-winner) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Publishing notes](artifact/PUBLISHING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console output and Markdown-style guidance with environment-variable configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May place live or paper trades when live mode and required credentials are explicitly configured; defaults to dry-run/manual mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
