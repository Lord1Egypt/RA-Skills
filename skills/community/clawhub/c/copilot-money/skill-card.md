## Description: <br>
Queries Copilot Money personal finance data, including accounts, transactions, net worth, holdings, asset allocation, and bank connection refresh workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayhickey](https://clawhub.ai/user/jayhickey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to ask an agent for Copilot Money account balances, recent transactions, net worth, holdings, asset allocation, and bank connection refresh commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive personal financial data from Copilot Money. <br>
Mitigation: Install and use it only when the user is comfortable giving the agent access to Copilot Money account, transaction, net worth, holdings, and allocation data. <br>
Risk: Authentication can read a Copilot Money session token from local browser storage on supported macOS browsers. <br>
Mitigation: Prefer manual token entry or an explicit browser source when broad browser scanning is not desired. <br>
Risk: Refresh commands can act on bank connections. <br>
Mitigation: Ask for explicit confirmation before running refresh actions against bank connections. <br>
Risk: The skill depends on the external copilot-money-cli package. <br>
Mitigation: Review the external package before installation or use. <br>


## Reference(s): <br>
- [Copilot Money](https://copilot.money) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local CLI authentication, queries, and refresh actions for Copilot Money data.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
