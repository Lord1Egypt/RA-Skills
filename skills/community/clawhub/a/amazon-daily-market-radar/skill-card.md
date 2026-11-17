## Description:

Automated daily Amazon market digest that monitors opted-in ASINs and competitors for price, BSR, entrant, review, and stockout changes and returns a RED/YELLOW/GREEN briefing against the previous snapshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiclaw](https://clawhub.ai/user/apiclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and marketplace operators use this skill to set up explicit, opted-in daily monitoring for their own ASINs, competitors, and surrounding category. It produces day-over-day market change briefings with prioritized alerts, KPI snapshots, competitor movement, market shifts, action items, data provenance, and API usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key and endpoint handling can expose sensitive access if the user overrides the service endpoint incorrectly.

Mitigation: Use only the default HTTPS ZooData endpoint, do not set ZOODATA_BASE_URL to an http:// or untrusted value, and confirm the ZOODATA_API_KEY source before execution.

Risk: The README install command is mutable and may resolve different content over time.

Mitigation: Prefer a pinned or otherwise verified installer before installing or updating the skill.

Risk: Recurring runs send tracked ASINs, keywords, categories, filters, and marketplace/date values to ZooData, consume API credits, and retain local baseline files.

Mitigation: Require explicit opt-in for setup and recurring execution, review expected credit use before broad scans, and delete the skill data folder to reset retained watchlists and baselines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apiclaw/skills/amazon-daily-market-radar)
- [Project homepage from metadata](https://github.com/SerendipityOneInc/ZooData-Skills)
- [ZooData API Field Reference](artifact/references/reference.md)
- [ZooData CLI Contract](artifact/references/cli-contract.md)
- [ZooData API key setup](https://zoodata.ai/en/api-keys)
- [ZooData pricing](https://zoodata.ai/en/pricing)
- [ZooData homepage](https://zoodata.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefing with tables, alert sections, inline shell commands, and JSON-derived provenance and API usage summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports match the user's language while API field names and endpoint names remain in English; scheduled monitoring requires explicit opt-in and stores watchlist and baseline JSON in the skill data folder.]

## Skill Version(s):

1.0.9 (source: release evidence and SKILL.md frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
