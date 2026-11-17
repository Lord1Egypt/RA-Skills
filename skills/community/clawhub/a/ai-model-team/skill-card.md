## Description:

AI Model Team is a multi-model prediction skill for OKX crypto markets and US stocks using Kronos, Chronos-2, TimesFM, and VADER-based sentiment signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erongcao](https://clawhub.ai/user/erongcao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading analysts use this skill to run multi-model market prediction for OKX crypto instruments and US equities, review fused signals, risk-gate status, and optional sentiment context before making their own trading decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports risky runtime and install behavior.

Mitigation: Review before installing, use an isolated virtual environment, and do not run post_install.py until the package-rewrite approach is removed or justified.

Risk: Unreviewed symbol or timeframe inputs can produce misleading trading analysis.

Mitigation: Restrict inputs to expected asset and timeframe formats and treat every output as analytical context, not investment advice.

Risk: Model downloads can change behavior when Hugging Face revisions are not pinned to reviewed versions.

Mitigation: Pin model identifiers to reviewed revisions before production use.

Risk: Default note writing can target a personal Obsidian vault path.

Mitigation: Explicitly control output paths with environment configuration or avoid run_team.py when file writes are not desired.

## Reference(s):

- [ClawHub AI Model Team Skill Page](https://clawhub.ai/erongcao/skills/ai-model-team)
- [Kronos-Base Model Card](docs/KRONOS_MODEL_CARD.md)
- [Google TimesFM source dependency](https://github.com/google-research/timesfm.git@f085b90)
- [Amazon Chronos forecasting source dependency](https://github.com/amazon-science/chronos-forecasting.git@6d68ed7c4ed2805d122d77b4660765b4089de5ca)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Terminal report, compact signal summary, or JSON prediction output with model signals and risk-gate fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include market signal, confidence, forecast movement, model votes, and risk-gate decision fields; run_team.py can append Markdown notes to a configured Obsidian vault path.]

## Skill Version(s):

2.9.2 (source: server release metadata and README; SKILL.md frontmatter reports 2.9.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
