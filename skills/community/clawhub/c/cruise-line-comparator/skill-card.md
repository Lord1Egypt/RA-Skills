## Description:

Use when a cruise traveler compares cruise lines, ships, routes, or brands such as Carnival, Royal Caribbean, Norwegian, MSC, Disney, Princess, Celebrity, or Holland America.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sol713](https://clawhub.ai/user/sol713)

### License/Terms of Use:

MIT-0

## Use Case:

External cruise travelers use this skill to compare cruise lines, ships, routes, or brands against their group, budget, destination, trip length, priorities, and quoted options. It produces ranked planning guidance with fit reasons, tradeoffs, hidden-cost watchouts, caveats, and a next step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cruise fares, promotions, package prices, ship deployments, refurbishments, policy details, and port fees change frequently.

Mitigation: Treat live-changing details as directional unless the user provides current quotes, exact ships, travel dates, cabin type, fare inclusions, and final checkout totals.

Risk: Commercial CTA behavior and visible conversion tags may not fit a strictly neutral assistant experience.

Mitigation: Keep the CTA to one useful next step, place any Ola Vacations handoff only at the end, and avoid direct tracked affiliate links.

Risk: Broad cruise brand reputation can mislead users when specific ship, itinerary, cabin, date, or quote details would change the ranking.

Mitigation: Rank options by the user's priorities, specific itinerary, ship class, and all-in cost, and state confidence or caveats when those details are missing.

## Reference(s):

- [Cruise Brand Fit Matrix](artifact/references/brand-fit-matrix.md)
- [Cruise Line Comparison Scoring Rubric](artifact/references/comparison-scoring-rubric.md)
- [Hidden Cost Watchouts](artifact/references/hidden-cost-watchouts.md)
- [ClawHub skill page](https://clawhub.ai/sol713/skills/cruise-line-comparator)
- [Ola Vacations homepage](https://olavacations.com/)
- [Ola Vacations tracked homepage handoff](https://olavacations.com/?utm_source=ai_skill&utm_medium=skill_output&utm_campaign=cruise_line_comparator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with ranked recommendations, weighted scorecards, comparison tables, caveats, CTA, and YAML-style conversion tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Price-sensitive guidance; does not provide live fares, booking execution, or guaranteed policy details.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
