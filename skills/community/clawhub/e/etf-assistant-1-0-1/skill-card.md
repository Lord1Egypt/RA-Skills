## Description:

ETF Investment Assistant helps agents query ETF prices, list and search common ETFs, compare ETF prices, summarize ETF categories, and estimate dollar-cost averaging returns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squally2k](https://clawhub.ai/user/squally2k)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to inspect common ETF codes, query Yahoo Finance quote data, compare two ETFs, and produce simple ETF investing summaries or DCA estimates. It is informational only and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports that calculator amount and year values are not strictly validated and may execute shell commands locally.

Mitigation: Review before installing, run only in a sandbox when possible, and use trusted numeric values for the calc command until strict validation is added.

Risk: Price and comparison commands send ETF codes to Yahoo Finance.

Mitigation: Avoid submitting sensitive or private identifiers, and disclose the external quote-data request path to users.

Risk: The skill provides ETF tips and simplified DCA estimates that could be mistaken for financial advice.

Mitigation: Keep outputs informational, preserve the investment-risk disclaimer, and require independent financial review before acting on results.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/squally2k/skills/etf-assistant-1-0-1)
- [Yahoo Finance chart endpoint used for quote data](https://query1.finance.yahoo.com/v8/finance/chart/510300.SS)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text output with ETF lists, quote summaries, comparisons, and calculator estimates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Yahoo Finance for quote lookups; calculator output uses a simplified assumed annual return.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
