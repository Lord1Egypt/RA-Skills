## Description:

Alphagbm Tepper Signal helps an agent evaluate whether market conditions match a Tepper-style panic-buy signal using VIX, FearScore, and large-cap quality gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-oriented agents use this skill to check whether current or supplied market signals meet a high-conviction panic-buy framework. Its output should support research and review, not automated trading or personalized portfolio decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake market signal output for personalized financial advice.

Mitigation: Present outputs as informational research and require separate human or advisory review before acting on them.

Risk: An agent could over-apply the signal language to trading or portfolio decisions.

Mitigation: Do not grant the skill authority to place trades, rebalance portfolios, or execute financial transactions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-tepper-signal)
- [AlphaGBM](https://alphagbm.com)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown text with signal diagnostics, ETF recommendations, and natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference ticker-specific inputs and signal levels such as armed, watch, near, or cold.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
