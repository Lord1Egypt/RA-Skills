## Description:

ETF and fund portfolio manager with price alerts, profit/loss tracking, and position management for Chinese A-shares through Tencent Finance and US securities through Yahoo Finance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[popwho](https://clawhub.ai/user/popwho)

### License/Terms of Use:

MIT License

## Use Case:

External users and developers can use this skill to track ETF and fund positions, calculate portfolio gains and losses, query current prices, and manage local price alerts. It is suited for personal portfolio monitoring rather than regulated investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and dependency setup can alter the local Python environment.

Mitigation: Review the installer before execution and install yfinance in a dedicated virtual environment with pinned versions.

Risk: Local portfolio and alert files can reveal private financial information.

Mitigation: Restrict permissions on ~/.clawdbot/etf_investor/ and avoid storing sensitive portfolio data on shared systems.

Risk: Uninstall removes the local portfolio and alert data directory after confirmation.

Mitigation: Back up positions.json and alerts.json before uninstalling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/popwho/skills/etf-finance)
- [Publisher profile](https://clawhub.ai/user/popwho)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command-line examples and plain-text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local JSON files for positions, alerts, and cached prices under ~/.clawdbot/etf_investor/.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
