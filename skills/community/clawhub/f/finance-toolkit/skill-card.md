## Description:

A China A-share quantitative analysis toolkit that helps agents fetch market data, run technical indicators and backtests, monitor scores, perform FFT analysis, and generate daily reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dnaxxx-hub](https://clawhub.ai/user/dnaxxx-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, finance analysts, and agent builders use this skill to guide Python-based A-share market analysis workflows, including market-data retrieval, technical analysis, strategy backtesting, monitoring, and report generation. Outputs should be reviewed as analytical support rather than financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts third-party market-data providers and queried stock symbols may be disclosed.

Mitigation: Use only when this disclosure is acceptable for the stocks being analyzed, and avoid querying sensitive watchlists in trusted or confidential environments.

Risk: The security review flagged under-disclosed automatic interpreter handoff behavior.

Mitigation: Review or remove the MSYS64 interpreter handoff before using the skill in a trusted agent environment.

Risk: The security review flagged optional external bridge behavior for alert synchronization.

Mitigation: Review or disable the optional system_bridge alert synchronization before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dnaxxx-hub/skills/finance-toolkit)
- [Publisher profile](https://clawhub.ai/user/dnaxxx-hub)
- [Artifact README](artifact/README.md)
- [Artifact skill file](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include finance-analysis outputs, strategy signals, backtest summaries, monitoring scores, FFT insights, and daily-report content for reviewer validation.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
