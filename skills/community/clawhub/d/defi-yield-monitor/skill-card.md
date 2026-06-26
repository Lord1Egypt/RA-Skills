## Description: <br>
Monitor DeFi lending and savings positions across Aave v3, SparkLend, Spark Savings, and Kamino with balances, APYs, health factors, and yield tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reed1898](https://clawhub.ai/user/reed1898) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to monitor wallet-linked DeFi lending and savings positions, review APYs and health factors, and produce daily or yield-summary reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow installs and runs mutable code from an external repository. <br>
Mitigation: Install only after reviewing and trusting the external repository, and prefer a release pinned to a reviewed commit or bundled runtime code. <br>
Risk: The skill processes wallet-linked financial data in generated reports. <br>
Mitigation: Configure only wallet addresses intended for monitoring and review reports before sharing them. <br>
Risk: Automated cron delivery to Telegram or Discord can send financial position data outside the local environment. <br>
Mitigation: Enable automated delivery only after confirming exactly what data will be sent and who can access the destination channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reed1898/defi-yield-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Text, Markdown-style reports, JSON output, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include wallet-linked positions, balances, APYs, health factors, realized yield summaries, and risk alerts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
