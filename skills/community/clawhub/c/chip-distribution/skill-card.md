## Description:

Provides Chinese-language stock chip-distribution analysis using Eastmoney CYQ concepts to assess cost distribution, concentration, trapped positions, and support or resistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danpian1](https://clawhub.ai/user/danpian1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to have an agent explain Chinese stock chip-distribution patterns, concentration levels, trapped positions, and likely support or resistance zones from CYQ-style indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Buy, sell, and hold signals may be mistaken for financial advice or automated trading instructions.

Mitigation: Treat outputs as analytical heuristics only and require human review before any investment decision.

Risk: Chip-distribution data may be stale because the artifact notes that chip data updates after market close.

Mitigation: Check current market data and the data timestamp before relying on the analysis.

Risk: Chip-distribution patterns may be less reliable for newly listed stocks.

Mitigation: Apply extra caution or avoid relying on the skill for stocks listed for less than one year.

## Reference(s):

- [筹码分析速查](references/chip-analysis.md)
- [ClawHub skill page](https://clawhub.ai/danpian1/skills/chip-distribution)
- [Publisher profile](https://clawhub.ai/user/danpian1)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown text with indicator explanations, signal tables, and support or resistance guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, credential access, persistence, or hidden behavior is present in the artifact evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
