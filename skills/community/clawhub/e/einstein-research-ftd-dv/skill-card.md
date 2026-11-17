## Description:

Detects Follow-Through Day (FTD) signals for market bottom confirmation using William O'Neil's methodology, with dual-index tracking, rally-attempt state management, FTD qualification, and post-FTD health monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-analysis developers use this skill to evaluate broad-market re-entry signals after corrections and generate FTD status, quality scores, exposure guidance, and watch levels for S&P 500/SPY and NASDAQ/QQQ.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides concrete market exposure guidance that could be mistaken for financial advice.

Mitigation: Treat outputs as informational market-analysis only and require human review before trading or allocation decisions.

Risk: The security review notes under-disclosed data-source and credential handling, especially for users expecting a Yahoo-only workflow.

Mitigation: Review data-source requirements before installation and provide FMP_API_KEY through the environment instead of passing secrets on the command line.

Risk: The security verdict is suspicious because the release combines market-analysis behavior with investment exposure recommendations.

Mitigation: Review the skill before deployment, keep position-sizing decisions outside automated execution, and apply normal risk-management controls.

## Reference(s):

- [Follow-Through Day (FTD) Methodology](references/ftd_methodology.md)
- [Post-FTD Monitoring Guide](references/post_ftd_guide.md)
- [Financial Modeling Prep API](https://financialmodelingprep.com/api/v3)
- [ClawHub Skill Page](https://clawhub.ai/clawdiri-ai/skills/einstein-research-ftd-dv)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Files, Guidance]

**Output Format:** [Natural-language analysis plus JSON and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Financial Modeling Prep using FMP_API_KEY and writes timestamped report files to the selected output directory.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
