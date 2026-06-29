## Description: <br>
AIOS (Aiden Investment Operating System) helps users run pre-trade checks, calculate position size, record trade logs, and conduct monthly reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jchcvfsf4n-cmd](https://clawhub.ai/user/jchcvfsf4n-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to apply a structured trading-discipline workflow before stock, fund, or ETF trades, including risk checks, position sizing, journaling, and periodic review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading plans and account-related details may be stored in local cleartext files under the workspace logs directory. <br>
Mitigation: Install and run the skill only in workspaces where local logs are acceptable, and avoid shared, public, or automatically synced folders unless that exposure is intended. <br>


## Reference(s): <br>
- [Aiden Investment Operating System (AIOS) Manual](references/AIOS-Manual.md) <br>
- [Trade Journal Template](references/trade-journal-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local JSON files in a workspace logs directory for configuration, positions, and trade history.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence; artifact metadata version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
