## Description:

Track football teams and return last match, next match, kickoff time, broadcasters, standings, and recent news in a compact emoji-formatted summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geison-paitra](https://clawhub.ai/user/geison-paitra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and sports fans use this skill to track football clubs and FIFA World Cup 2026 national teams. It returns match status, kickoff details, venue, broadcasters, standings, group tables when available, and recent football news in English or Portuguese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores football-data.org API keys locally in plaintext and the artifact includes a populated user_config.json.

Mitigation: Revoke or rotate the bundled key before release, remove user_config.json from the shipped artifact, and store user secrets outside the skill package.

Risk: The skill depends on external sports and news services for club lookups, broadcasters, standings, and recent news.

Mitigation: Review returned sports and news data before relying on it, and prefer the internal World Cup 2026 schedule only for the tournament structure it explicitly covers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geison-paitra/skills/football-tracker)
- [FIFA World Cup 2026 schedule source](http://digitalhub.fifa.com/asset/4b5d4417-3343-4732-9cdf-14b6662af407/FWC26-Match-Schedule_English.pdf)
- [football-data.org API v4](https://api.football-data.org/v4)
- [Google News RSS search](https://news.google.com/rss/search?q=)
- [English output pack](references/locales/en.md)
- [Portuguese output pack](references/locales/pt-br.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Compact Markdown-style football summaries with emoji labels and localized English or Portuguese text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup guidance for a football-data.org API key, N/A placeholders for unavailable match data, and beta/version notices.]

## Skill Version(s):

1.2.0 (source: server release metadata and config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
