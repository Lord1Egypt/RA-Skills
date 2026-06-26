## Description: <br>
Provides Fantasy Premier League squad, transfer, captaincy, lineup, chip, rules, and gameweek guidance using public FPL data and documented strategy references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongbinnie](https://clawhub.ai/user/dongbinnie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External FPL players and agents use this skill to analyze squads, plan transfers, select captains, order benches, understand FPL rules, and choose chip timing for a gameweek. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request or process a manager ID or squad details while helping with FPL analysis. <br>
Mitigation: Share only the FPL manager ID or squad details needed for analysis and do not provide FPL passwords, session tokens, or other credentials. <br>
Risk: Broad trigger phrases such as fantasy, captain, or transfer may activate the skill outside an FPL conversation. <br>
Mitigation: Narrow trigger phrases or confirm FPL intent when accidental activation would disrupt non-FPL conversations. <br>
Risk: Recommendations based on live public FPL data can become stale as fixtures, injuries, and prices change. <br>
Mitigation: Refresh the public FPL API data and review injury, rotation, and deadline context before acting on lineup, transfer, captaincy, or chip advice. <br>


## Reference(s): <br>
- [FPL API Reference](references/api.md) <br>
- [FPL Rules Reference](references/rules.md) <br>
- [FPL Player Selection Strategy](references/strategy.md) <br>
- [Fantasy Premier League Public API](https://fantasy.premierleague.com/api/) <br>
- [ClawHub Skill Page](https://clawhub.ai/dongbinnie/fpl-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured recommendations and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include starting XI, bench order, captain and vice-captain picks, transfer suggestions, chip recommendations, and supporting analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
