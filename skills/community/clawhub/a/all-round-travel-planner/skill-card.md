## Description:

A Chinese-oriented travel planning skill that gathers trip details and current web information to produce structured itineraries covering food, lodging, attractions, transportation, budgets, weather, practical tips, and backup options for domestic and international destinations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nameused](https://clawhub.ai/user/nameused)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create practical domestic or international travel plans from their departure city, destination, dates, group type, budget, preferences, and special needs. It is especially suited for Chinese-language itinerary planning that compares transportation options and organizes attractions, food, lodging, budget, weather, local transport, tips, and fallback plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel recommendations, prices, schedules, weather, and availability can change after web research is summarized.

Mitigation: Verify time-sensitive details with current carrier, booking, venue, weather, and destination sources before purchase or travel.

Risk: Generated HTML may contain user-provided or web-sourced names, links, and other dynamic values.

Mitigation: Treat those values as untrusted, escape them before generating HTML, and review links before opening or sharing generated files.

Risk: Optional HTML output can load Chart.js from the jsDelivr CDN.

Mitigation: Remove or pin the CDN dependency when third-party script loading is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nameused/skills/all-round-travel-planner)
- [Destination information templates and transport query guide](artifact/references/destination_templates.md)
- [HTML output template](artifact/references/html_template.md)
- [Chart.js CDN](https://cdn.jsdelivr.net/npm/chart.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, guidance]

**Output Format:** [Markdown travel plans by default; optional HTML, tables, document, presentation, or visualization-ready output when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use current web search for destination facts, flight fares, weather, lodging, dining, and local transport; optional HTML can include Chart.js from jsDelivr.]

## Skill Version(s):

1.0.0 (source: release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
