## Description:

A-share short-term trading decision skill for the 1-5 day horizon that uses AkShare market data to assess sentiment, sector rotation, strong stocks, capital flow, risk controls, prediction logs, and next-day comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-xiaolin](https://clawhub.ai/user/wu-xiaolin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent operators use this skill to generate CN A-share short-term market signals, daily reports, prediction logs, and next-day comparisons for research-supported trading decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated stock signals may be mistaken for financial advice or automated trading authority.

Mitigation: Treat outputs as research support only and require human review before any trading decision.

Risk: Market-data and dependency behavior depends on AkShare and pandas availability and version behavior.

Mitigation: Install in a dedicated virtual environment and pin or review AkShare and pandas versions before deployment.

Risk: Prediction snapshots are retained locally under data/decision_log.jsonl.

Mitigation: Manage local retention and avoid storing sensitive information in prediction logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-xiaolin/skills/a-share-short-decision-bak)
- [Publisher profile](https://clawhub.ai/user/wu-xiaolin)
- [Skill README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration, guidance]

**Output Format:** [Markdown and JSON-style command output, with optional local JSONL prediction logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses real market data when available, returns explicit no-trade messages when no candidate exists, and can store prediction snapshots under data/decision_log.jsonl.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
