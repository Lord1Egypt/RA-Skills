## Description:

A stock-market quantitative analysis agent skill for A-share, Hong Kong, and U.S. equity analysis, including technical analysis, strategy generation, backtesting, and risk management.

This skill is for research and development only.

## Publisher:

[ganjiakoun16](https://clawhub.ai/user/ganjiakoun16)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users can use this skill to fetch market data, run quantitative stock analysis, generate strategy signals, perform backtests, and review risk controls. It is framed by the artifact as research and development support rather than ready-to-use financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broker or market-data credentials may be exposed or over-scoped if used directly in a shared or production environment.

Mitigation: Install in an isolated environment, use read-only and narrowly scoped API tokens, avoid Longport tokens with trading authority, and protect config.env permissions.

Risk: Local model loading can be unsafe when model files are untrusted because joblib relies on pickle-like deserialization behavior.

Mitigation: Do not load or keep model files unless their origin is trusted, and prefer safer model formats when adapting the skill.

Risk: Pinned or aging dependencies may carry security or operational risk in sensitive account workflows.

Mitigation: Review and update dependency pins before using the skill with sensitive accounts or production workflows.

Risk: Financial analysis outputs may be mistaken for investment advice.

Mitigation: Treat outputs as research support and require independent human review before any trading or portfolio decision.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ganjiakoun16/skills/beergaao)
- [Strategy Engine Reference](artifact/strategy-reference.md)
- [Factor System Reference](artifact/factor-reference.md)
- [Risk and Backtest Reference](artifact/risk-reference.md)
- [Tushare API](https://api.tushare.pro)
- [EastMoney API](https://push2.eastmoney.com)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, configuration, guidance]

**Output Format:** [Markdown and JSON-style tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock signals, market summaries, backtest metrics, risk checks, and configuration guidance.]

## Skill Version(s):

3.3.5 (source: ClawHub release metadata; artifact frontmatter 3.2.6 and pyproject/skill.json 3.3.1 differ)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
