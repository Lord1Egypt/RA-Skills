## Description:

Dota2-Stats-Skill helps agents query OpenDota for Dota 2 player, match, hero, team, league, pro match, live game, rank, and win-rate information through a Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssunk](https://clawhub.ai/user/ssunk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer Dota 2 statistics questions by having an agent run focused OpenDota queries for players, matches, heroes, teams, leagues, live games, ranks, and win rates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send Dota 2 player names, account IDs, Steam64 IDs, match IDs, and filters to OpenDota.

Mitigation: Use the skill only when sharing those query values with OpenDota is acceptable.

Risk: The refresh command asks OpenDota to refresh a player record rather than only reading cached data.

Mitigation: Run refresh only when an explicit player record refresh is intended.

Risk: OpenDota availability, rate limits, or player privacy settings can delay, fail, or limit results.

Mitigation: Prefer known account IDs when available, expect slow player-name searches, and treat missing private-player data as an API limitation.

## Reference(s):

- [OpenDota API Documentation](https://docs.opendota.com/)
- [OpenDota API Endpoint](https://api.opendota.com/api)
- [ClawHub Skill Page](https://clawhub.ai/ssunk/skills/dota2-stats-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with inline shell commands and tabular query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is Chinese; English output is available with --lang en.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
