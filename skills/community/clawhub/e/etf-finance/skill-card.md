## Description: <br>
ETF and fund portfolio manager with price alerts, profit/loss tracking, and position management, using Tencent Finance for Chinese A-shares and Yahoo Finance for US stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[popwho](https://clawhub.ai/user/popwho) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to track ETF and fund positions, calculate profit and loss, query prices, and manage local price alerts from command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio records can include holdings, purchase prices, quantities, and alerts stored in local JSON files. <br>
Mitigation: Run the skill only in a trusted local environment and avoid sharing or committing ~/.clawdbot/etf_investor data files. <br>
Risk: Ticker lookups query Yahoo/yfinance or Tencent Finance, which can expose the symbols being checked to those providers. <br>
Mitigation: Use the skill only when querying those external price services is acceptable for the symbols involved. <br>
Risk: The installer can fall back to pip's --break-system-packages option when installing yfinance. <br>
Mitigation: Prefer an isolated Python environment and review the installer before running it on a shared or managed system. <br>
Risk: The uninstall script removes the local ETF data directory after confirmation. <br>
Mitigation: Back up ~/.clawdbot/etf_investor before uninstalling if the positions or alerts should be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/popwho/etf-finance) <br>
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/q={market}) <br>
- [Publisher profile](https://clawhub.ai/user/popwho) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill manages local JSON files for positions and alerts.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
