## Description:

Looks up digital movie and TV deals, current prices, charts, recommendations, and price history across CheapCharts-supported stores, with all-time-low flags where available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tracerman](https://clawhub.ai/user/tracerman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find digital movie and TV discounts, compare purchase or rental prices, check whether a title is at its tracked all-time low, and produce concise deal reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes public web requests to CheapCharts and may optionally use IMDb or CheapCharts web pages for compatibility or savings advice.

Mitigation: Use it only in environments where these public requests are acceptable and review any optional browsing before allowing the agent to proceed.

Risk: Digital prices, availability, and sale status can change or lag behind store data.

Mitigation: Treat reported prices as informational and verify price and availability in the linked store before purchasing.

Risk: Recurring monitoring could create unexpected scheduled activity if delegated without review.

Mitigation: Require the user or operator to explicitly configure any recurring checks or schedules.

Risk: Some CheapCharts endpoints have documented coverage limits or instability, especially the unofficial DetailData endpoint and non-iTunes batch deal lookups.

Mitigation: Prefer the bundled script for all-time-low and history workflows, check API status responses, and present endpoint limitations when results may be incomplete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tracerman/skills/cheapcharts)
- [Publisher profile](https://clawhub.ai/user/tracerman)
- [Server-resolved GitHub provenance](https://github.com/tracerman/cheapcharts-skill/tree/main/skills/cheapcharts)
- [CheapCharts AI documentation](https://www.cheapcharts.com/us/ai)
- [CheapCharts website](https://www.cheapcharts.com)
- [API reference](references/API.md)
- [API pitfalls](references/PITFALLS.md)
- [Recipes](RECIPES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, JSON, shell commands, and concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make public web requests to CheapCharts and optional related public pages; no API key is required.]

## Skill Version(s):

0.1.6 (source: server release evidence; artifact frontmatter reports 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
