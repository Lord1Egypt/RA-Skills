## Description:

Multi-source sports betting research tool. Aggregates odds, team form, head-to-head history, weather conditions, and injury data to identify value betting opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stigg86](https://clawhub.ai/user/stigg86)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to research sports matches or teams by aggregating form, fixtures, head-to-head history, weather, odds, and injury or lineup signals for betting analysis. It is intended to support data-driven decisions, not to provide guaranteed winners or inside information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads API keys from local plaintext config files for API-Football and The Odds API.

Mitigation: Use low-privilege keys and prefer environment or platform secret storage over plaintext files.

Risk: The skill may automatically run a separate local search-x Node.js script for lineup and injury searches when that script is present.

Mitigation: Verify or disable the search-x dependency before installation and execution.

Risk: Sports, odds, lineup, injury, and social signals can be incomplete, stale, rate-limited, or unavailable.

Mitigation: Treat outputs as research inputs, check source freshness, and confirm material betting decisions against primary sources.

Risk: Betting analysis can be mistaken for guaranteed wagering advice.

Mitigation: Present findings as patterns and value indicators only, preserving the artifact's warning that it does not provide guaranteed winners, tips, or inside information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stigg86/skills/betting-research)
- [Data Sources Reference](references/data-sources.md)
- [TheSportsDB](https://www.thesportsdb.com/)
- [API-Football](https://www.api-football.com/)
- [Open-Meteo](https://open-meteo.com/)
- [The Odds API](https://the-odds-api.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-oriented text with command examples and betting research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live or cached sports, weather, odds, lineup, injury, fatigue, and motivation signals depending on available API keys and rate limits.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
