## Description:

Quantifies market breadth health using TraderMonty's public CSV data and generates a 0-100 composite score across six components.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to assess end-of-day S&P 500 market breadth, participation, and rally quality from public TraderMonty CSV data. It supports market-health summaries, component breakdowns, and cautionary breadth context, but it is not a substitute for comprehensive investment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses outbound network access and accepts custom CSV URLs.

Mitigation: Run it in an isolated workspace, prefer the default TraderMonty URLs, and avoid untrusted custom data sources.

Risk: The skill writes reports and score history to the local output directory.

Mitigation: Choose an output directory with appropriate write permissions and review generated files before sharing or reusing them.

Risk: The reports include fairly prescriptive equity exposure guidance.

Mitigation: Treat outputs as informational market context and review them with other analysis before making financial decisions.

## Reference(s):

- [Market Breadth Analysis Methodology](references/breadth_analysis_methodology.md)
- [TraderMonty Market Breadth Dashboard](https://tradermonty.github.io/market-breadth-analysis/)
- [TraderMonty Detail CSV](https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv)
- [TraderMonty Summary CSV](https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv)
- [ClawHub Skill Page](https://clawhub.ai/clawdiri-ai/skills/einstein-research-breadth-dv)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Natural-language market breadth summary with generated JSON and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include a composite score, health zone, component scores, freshness warnings, equity exposure guidance, and rolling local history.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
