## Description:

Detects unusual options activity and smart money signals by monitoring volume/OI ratio spikes, large block trades, unusual strike/expiry combinations, and net premium flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask for symbol-specific or market-wide options-flow analysis, including unusual trades, sentiment classification, net premium flow, and smart money scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic finance questions about volume or block trades may invoke this skill outside a focused options-flow task.

Mitigation: Use the skill for options-flow analysis prompts and review whether its output is relevant before relying on it.

Risk: Market-analysis output can be incomplete, outdated, or misleading if treated as financial advice.

Mitigation: Verify market data and assumptions against authoritative sources before making trading or investment decisions.

## Reference(s):

- [Alphagbm Unusual Activity on ClawHub](https://clawhub.ai/clementgu/skills/alphagbm-unusual-activity)
- [AlphaGBM](https://alphagbm.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis with structured trade fields and summary metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include unusual activity lists, sentiment summaries, net premium flow, smart money scores, and historical accuracy metrics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
