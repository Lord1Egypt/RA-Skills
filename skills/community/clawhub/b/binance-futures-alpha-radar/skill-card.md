## Description:

Analyze Binance USDT-margined perpetual futures symbols with public futures market data only and return a structured market analysis report with a clear BUY, SELL, or HOLD recommendation without placing orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wqyblue3316](https://clawhub.ai/user/wqyblue3316)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Binance USDT-margined perpetual futures setups from public market data and receive structured BUY, SELL, or HOLD strategy commentary. It is analysis-only and does not execute trades or use private exchange APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on parent-directory strategy files that are outside this package and can change the effective analysis rules after review.

Mitigation: Install only with trusted repository context, and review or scan the external strategy files before relying on the skill.

Risk: If users provide balances or positions, the output can become personalized high-risk trading commentary.

Mitigation: Do not provide exchange credentials, API keys, or sensitive account details; treat outputs as analysis-only commentary, not automated trading actions.

## Reference(s):

- [Analysis Mode](references/analysis-mode.md)
- [System Prompt Coverage](references/system-prompt-coverage.md)
- [Binance Futures Public API](https://fapi.binance.com)
- [ClawHub Skill Page](https://clawhub.ai/wqyblue3316/skills/binance-futures-alpha-radar)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Structured Chinese Markdown report by default; canonical JSON array when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One report or decision object per requested symbol; uses public Binance futures data and default account assumptions unless the user supplies account context.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
