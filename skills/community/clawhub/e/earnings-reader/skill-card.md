## Description:

Guides agents through Chinese A-share earnings analysis across income statements, balance sheets, cash flow, key ratios, valuation comparisons, and concise stock report summaries.

This skill is for research and development only.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to structure research-oriented analysis of Chinese A-share earnings reports, including financial statement trends, ratio health checks, valuation context, and concise Markdown summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial-report summaries and investment-view sections may be mistaken for investment advice.

Mitigation: Present outputs as research only, preserve the not-investment-advice framing, and have users independently verify financial data and conclusions before acting.

Risk: The skill relies on a separate AKShare finance script when used as written, so missing or stale external data can affect analysis quality.

Mitigation: Confirm the AKShare workflow is available and validate source data freshness before relying on generated earnings analysis.

## Reference(s):

- [Earnings Reader ClawHub listing](https://clawhub.ai/lanyasheng/skills/earnings-reader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Financial analysis guidance only; investment views are for reference and are not investment advice.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
