## Description: <br>
Use this for Dota 2 and OpenDota questions about players, Steam64 or account IDs, match IDs, heroes, hero matchups, pro matches, teams, leagues, live games, ranks, and win rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssunk](https://clawhub.ai/user/ssunk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to answer Dota 2 statistics questions by running a local Python CLI that queries OpenDota for player, match, hero, team, league, live game, rank, and win-rate data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Dota player names, account IDs, match IDs, hero IDs, and query filters to OpenDota. <br>
Mitigation: Use it for intended Dota 2 lookup data and avoid including unrelated sensitive information in queries. <br>
Risk: The bundled Python script runs locally and requires network access to OpenDota. <br>
Mitigation: Review the command before execution and allow network access only when OpenDota lookups are needed. <br>
Risk: The refresh command asks OpenDota to refresh player data instead of only reading cached results. <br>
Mitigation: Run refresh deliberately for the intended account ID and prefer read-only lookup commands for routine queries. <br>


## Reference(s): <br>
- [Dota2-Stats-Skill on ClawHub](https://clawhub.ai/ssunk/dota2-stats-skill) <br>
- [OpenDota API Documentation](https://docs.opendota.com/) <br>
- [OpenDota API Endpoint](https://api.opendota.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and text output from OpenDota queries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English output; default script output is Chinese unless --lang en is used.] <br>

## Skill Version(s): <br>
1.0.5 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
