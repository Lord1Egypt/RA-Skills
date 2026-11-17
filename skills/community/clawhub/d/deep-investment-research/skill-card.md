## Description:

Deep Investment Research provides an investment-research methodology and data-collection toolkit for macro, industry, policy, company, stock deep-dive, feasibility, risk, and investment-planning research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiaming88](https://clawhub.ai/user/wujiaming88)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use this skill to structure investment research, gather first-source market and policy data, and produce research reports with evidence, risks, and optional paths. It is scoped to research support and does not provide trading execution, live trading signals, or portfolio management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment topics, ticker symbols, and research queries may be sent to third-party data and search providers.

Mitigation: Use the skill only when that disclosure is acceptable; avoid confidential holdings, proprietary research themes, and other sensitive queries.

Risk: Subprocess handling can expose unrelated environment secrets to helper scripts.

Mitigation: Run the skill in an isolated environment containing only the specific API keys and environment variables needed for the research task.

Risk: Research reports and collected data are written to local output directories.

Mitigation: Configure RESEARCH_OUTPUT_DIR and RESEARCH_DATA_ROOT to non-sensitive locations and review generated files before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wujiaming88/skills/deep-investment-research)
- [README](README.md)
- [Skill instructions](SKILL.md)
- [Research core methodology](methodology/research-core.md)
- [Source registry](methodology/source-registry.md)
- [Content reading protocol](methodology/content-reading-protocol.md)
- [Risk analysis methodology](methodology/risk-analysis.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown reports, inline shell commands, Python helper scripts, and local data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research reports are written to RESEARCH_OUTPUT_DIR and collected data is written to RESEARCH_DATA_ROOT when those workflows are used.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
