## Description:

Provides A-share real-time quote lookup, intraday volume distribution analysis, main-fund activity signals, limit-up or limit-down indicators, and local portfolio profit-and-loss analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanchanghua](https://clawhub.ai/user/zhanchanghua)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Shanghai, Shenzhen, and Beijing A-share market data, inspect intraday volume patterns, and manage locally stored portfolio holdings with command-line tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio holdings are stored in a local JSON file under the user's home directory.

Mitigation: Restrict permissions on ~/.clawdbot/skills/a-stock-analysis/portfolio.json on shared machines and back it up before update or remove operations.

Risk: Stock symbols are sent to Sina market-data endpoints when quote or minute-level analysis is requested.

Mitigation: Use the skill only when sending requested stock symbols to Sina is acceptable for the user's privacy and compliance needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhanchanghua/skills/a-stock-analysis-1-0-0)
- [Sina Finance](https://finance.sina.com.cn)
- [Sina quote endpoint](https://hq.sinajs.cn)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, analysis, configuration]

**Output Format:** [Plain text reports or JSON emitted by command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Portfolio commands read and write a local JSON file at ~/.clawdbot/skills/a-stock-analysis/portfolio.json.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
