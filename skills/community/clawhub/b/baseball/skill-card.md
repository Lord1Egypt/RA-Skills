## Description:

Fetch MLB game schedules, live game status, box scores, player search, and season statistics via the MLB Stats API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khaney64](https://clawhub.ai/user/khaney64)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer MLB schedule, score, live game, player lookup, and season statistics questions from public MLB API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs outbound network access for MLB lookups.

Mitigation: Allow only the MLB Stats API access required for schedule, score, live game, player, and stat queries.

Risk: The package does not declare a tight domain permission scope.

Mitigation: Review future updates for any expansion beyond public MLB data fetching before deployment.

Risk: Excessive live-game polling may cause the upstream API to block requests from the caller's IP address.

Mitigation: Follow the skill documentation's guidance to poll live games no more than once every 15 seconds.

## Reference(s):

- [ClawHub Baseball skill page](https://clawhub.ai/khaney64/skills/baseball)
- [MLB Stats API schedule endpoint](https://statsapi.mlb.com/api/v1/schedule/games)
- [MLB Stats API live game feed endpoint](https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live)
- [MLB Stats API player search endpoint](https://statsapi.mlb.com/api/v1/people/search)
- [MLB Stats API player stats endpoint](https://statsapi.mlb.com/api/v1/people/{player_id}/stats)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Plain text tables or JSON from Python CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and outbound network access to the public MLB Stats API; no API key is required.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
