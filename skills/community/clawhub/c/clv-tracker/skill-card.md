## Description: <br>
Track Closing Line Value by logging placement odds, fetching closing lines, computing CLV, and generating betting performance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to track sports betting performance by comparing placement odds with closing lines. It helps log bets, compute Closing Line Value, export history, and report whether results indicate a betting edge or variance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores betting history locally in ~/.openclaw/data/clv.db, which may contain sensitive personal betting data. <br>
Mitigation: Treat the SQLite database as sensitive, restrict local access, and avoid sharing or uploading the file unless the user explicitly intends to export that data. <br>
Risk: The skill requires an ODDS_API_KEY for The Odds API. <br>
Mitigation: Provide the API key through the local environment, keep it out of committed files and transcripts, and rotate it if exposure is suspected. <br>
Risk: The skill proposes commands that write real bet details into a local database and may use external odds data. <br>
Mitigation: Review commands and placeholder substitutions before running them with real bet details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rsquaredsolutions2026/clv-tracker) <br>
- [The Odds API](https://the-odds-api.com/) <br>
- [AgentBets](https://agentbets.ai) <br>
- [OpenClaw CLV Tracker Skill Guide](https://agentbets.ai/guides/openclaw-clv-tracker-skill/) <br>
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, Files, Markdown] <br>
**Output Format:** [Markdown with inline bash and SQL commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ODDS_API_KEY and stores betting history locally in ~/.openclaw/data/clv.db.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
