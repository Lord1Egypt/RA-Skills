## Description:

Checks whether AC Milan played yesterday and, when a match occurred, returns a Chinese-language Serie A result summary with score, YouTube highlights search, and up to three Google News links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paoloxiamn](https://clawhub.ai/user/paoloxiamn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation users, and AC Milan followers use this skill in scheduled agent runs to check yesterday's match status and forward a concise match notification only when a scheduled AC Milan match is found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scheduled Python script contacts ESPN and Google News and generates YouTube search links.

Mitigation: Install only where public sports and news network requests are acceptable, and review scheduled execution settings before deployment.

Risk: The security guidance notes under-documented behavior around Google News, YouTube search links, and the optional schedule update script.

Mitigation: Review the artifact scripts and update user-facing documentation before relying on the skill in routine automation.

Risk: The local schedule.json file controls whether the notifier checks a match and can become stale.

Mitigation: Maintain the schedule file or review the optional update script before depending on silence as a signal that no match occurred.

## Reference(s):

- [AC Milan Match Monitor ClawHub page](https://clawhub.ai/paoloxiamn/skills/acmilan-match-monitor)
- [Publisher profile](https://clawhub.ai/user/paoloxiamn)
- [ESPN AC Milan schedule API](https://site.api.espn.com/apis/site/v2/sports/soccer/ita.1/teams/103/schedule?limit=5)
- [Google News RSS search](https://news.google.com/rss/search)
- [YouTube search results](https://www.youtube.com/results)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions and Chinese-language plain-text notification output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Silent when no scheduled match is found; includes external highlights and news links when a result is available.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
