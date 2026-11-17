## Description:

Provides financial analysis of listed companies, including valuation ratios, profitability metrics, financial health indicators, and DCF-based valuation models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gbabyzs](https://clawhub.ai/user/gbabyzs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to calculate valuation ratios, profitability metrics, financial health scores, and DCF estimates for listed companies from public market data. Results should be treated as informational analysis rather than professional financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces valuation outputs and buy, hold, or sell labels that may be mistaken for professional financial advice.

Mitigation: Treat outputs as informational calculations and review assumptions, data freshness, and context before using them in investment decisions.

Risk: The skill fetches public market data through Python dependencies, and unpinned dependencies can change behavior over time.

Mitigation: Install the skill in an isolated Python environment and pin dependency versions before operational use.

Risk: Some documentation and output labels are in Chinese, which may cause misunderstandings for non-Chinese readers.

Mitigation: Review or translate the documentation and labels before deployment in workflows where readers may not understand Chinese.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gbabyzs/skills/gbabyzs-financial-analysis)
- [ClawHub publisher profile](https://clawhub.ai/user/gbabyzs)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Python functions returning dictionaries, plus Markdown and inline shell commands for setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Financial outputs include timestamps, ratios, scores, valuation assumptions, and informational recommendation labels.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
