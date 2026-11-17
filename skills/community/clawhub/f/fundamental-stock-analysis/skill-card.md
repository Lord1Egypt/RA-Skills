## Description:

Fundamental equity analysis and peer ranking using a structured scoring playbook for quality, balance-sheet safety, cash flow, valuation, sector adjustments, and confidence modifiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickfiorani](https://clawhub.ai/user/nickfiorani)

### License/Terms of Use:


## Use Case:

External users and analysts use this skill to analyze one or more public equity tickers, compare peers, and produce a fundamentals-based verdict with confidence and data-quality caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock-analysis conclusions may be incomplete, stale, or unsuitable for a user's financial situation.

Mitigation: Treat outputs as educational analysis and verify important financial decisions independently, as stated in the security guidance.

Risk: Ticker ambiguity, missing metrics, or conflicting public data can distort scores and peer rankings.

Mitigation: Use the playbook's ticker disambiguation, source hierarchy, data quality scorecard, NA handling, and confidence caps before presenting a verdict.

Risk: The skill requires web research over financial sources, which can expose the agent to low-quality or irrelevant market commentary.

Mitigation: Restrict retrieval to ticker-relevant financial data, filings, reputable datasets, and relevant financial news, with source quality disclosed in the output.

## Reference(s):

- [Fundamental Stock Analysis Playbook](references/playbook.md)
- [ClawHub Skill Page](https://clawhub.ai/nickfiorani/skills/fundamental-stock-analysis)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown with sourced financial analysis, scores, peer ranking, risks, and confidence notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Educational analysis only; no machine-readable JSON block in user-facing output.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
