## Description:

AUSUB helps an agent fetch Tushare gold ETF market data and generate bounded, risk-disclosed gold dollar-cost-averaging suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juryory](https://clawhub.ai/user/juryory)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to produce disciplined gold ETF dollar-cost-averaging reports from Tushare daily market data, optional local configuration, and optional user plan settings. It is intended as an informational investment aid, not a guarantee of returns or individualized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Tushare token and queries external market-data APIs.

Mitigation: Set TUSHARE_TOKEN only in the runtime environment, prefer a pinned or locked tushare dependency, and review network access before installation.

Risk: Local configuration and user-plan files may contain sensitive financial planning details.

Mitigation: Avoid storing income, expenses, deposits, or similar sensitive financial details in persistent memory files; use those details transiently in conversation when needed.

Risk: Generated recommendations could be mistaken for guaranteed investment advice.

Mitigation: Treat outputs as informational decision support, preserve the included risk notices, and require user confirmation before writing personal plan settings.

## Reference(s):

- [AUSUB ClawHub skill page](https://clawhub.ai/juryory/skills/ausub)
- [juryory publisher profile](https://clawhub.ai/user/juryory)
- [Gold long-term return reference](artifact/references/gold-long-term-return.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-producing Python script outputs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include market summary, indicator table, recommendation multiplier, suggested amount, trigger rationale, account guidance, and risk notice.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
