## Description:

Exclusive morning and evening briefing skill for listed company chairmen that produces executive-level market briefings covering stock movements, policy updates, competitor intelligence, market sentiment, and regulatory announcement alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buxibuxi](https://clawhub.ai/user/buxibuxi)

### License/Terms of Use:

MIT

## Use Case:

Listed-company executives and their support teams use this skill to generate morning pre-market and evening post-market briefings for monitored companies, competitors, market conditions, policy developments, and strategic risk alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated financial briefings may include realistic mock data that can be mistaken for verified live market intelligence.

Mitigation: Use the reports only for testing or draft workflows until data retrieval is connected to verified live sources and failures are clearly shown to users.

Risk: Scheduled morning or evening reports could circulate unverified market analysis to decision makers.

Mitigation: Review generated briefings before executive, trading, financing, investor-relations, or strategy use, especially when the skill is configured for automated delivery.

## Reference(s):

- [QVeris](https://qveris.ai)
- [Chairman Daily Brief on ClawHub](https://clawhub.ai/buxibuxi/skills/chairman-daily-brief)
- [Tool Chain Routing Configuration](artifact/references/tool-chains.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Markdown briefings or JSON, with shell commands for setup and watchlist management]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QVERIS_API_KEY; can write watchlist configuration within the skill directory.]

## Skill Version(s):

1.3.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
