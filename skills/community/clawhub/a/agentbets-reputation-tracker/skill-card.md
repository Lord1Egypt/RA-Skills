## Description: <br>
Track and display an agent's betting reputation by computing win rate, ROI, volume, streaks, max drawdown, and a Sharpe proxy from local bet history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to compute betting performance metrics from a local SQLite bet log and prepare reputation summaries or Moltbook profile payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reputation profiles can reveal sensitive betting activity, including wager volume, profit/loss, ROI, platforms used, and activity dates. <br>
Mitigation: Review and redact generated summaries before sharing; publish only when the user intends to disclose those derived stats. <br>
Risk: Optional Moltbook publishing sends derived profile data to an external service when an API key is configured. <br>
Mitigation: Set MOLTBOOK_API_KEY only for intentional publishing, inspect the JSON payload first, and avoid publishing private betting logs or unnecessary details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rsquaredsolutions2026/agentbets-reputation-tracker) <br>
- [Moltbook](https://moltbook.com) <br>
- [AgentBets OpenClaw Agent Reputation Tracker guide](https://agentbets.ai/guides/openclaw-agent-reputation-tracker-skill/) <br>
- [AgentBets OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack guide](https://agentbets.ai/guides/agent-betting-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, Markdown, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local SQLite betting history and can optionally publish derived profile stats to Moltbook when MOLTBOOK_API_KEY is configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
