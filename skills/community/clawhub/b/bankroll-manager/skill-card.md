## Description: <br>
Track bankroll across sportsbooks and prediction markets. Log bets, record results, calculate ROI, generate P&L reports, and enforce risk limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to maintain a local betting or prediction-market bankroll ledger, log bets and results, review P&L and ROI, and check stake sizes against risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write bankroll and betting records to a local SQLite database. <br>
Mitigation: Review sqlite3 write commands before execution and keep local bankroll data at ~/.openclaw/data/bankroll.db protected according to the user's privacy needs. <br>
Risk: Free-text notes and unusual characters may affect the intended sqlite3 command. <br>
Mitigation: Inspect user-provided note fields, especially quotes or unusual characters, before running generated sqlite3 writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rsquaredsolutions2026/bankroll-manager) <br>
- [AgentBets bankroll manager guide](https://agentbets.ai/guides/openclaw-bankroll-manager-skill/) <br>
- [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with SQLite command examples and concise bankroll summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write user-requested bet records to a local SQLite database at ~/.openclaw/data/bankroll.db.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
