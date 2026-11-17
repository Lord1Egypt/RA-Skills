## Description:

Research German amateur-football clubs, teams, competitions, local fixtures, results, tables, and player match records through FUSSBALL.DE. Use for grassroots and regional football, not professional scouting or player outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

External users researching grassroots and regional German football can request source-attributed briefs on clubs, fixtures, competition standings, results, and player match records from FUSSBALL.DE. Results retain season and competition context so readers can interpret the records accurately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookups send search terms to Crawlora and may consume API credits; public player records may include birth dates and youth-team history.

Mitigation: Keep the API key private, avoid putting private information in searches, and include only player details needed for the requested research, especially for youth records and birth dates.

## Reference(s):

- [FUSSBALL.DE](https://www.fussball.de/)
- [Endpoint reference](reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/german-amateur-football-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown source-attributed brief, list, or table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes season and competition context where available; identifies truncated match-calendar results and missing data.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
