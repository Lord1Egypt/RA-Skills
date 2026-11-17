## Description:

Runs a Spanish competitive product benchmark for a chosen niche, researching public competitor pages, ads, reviews, and social profiles to produce a self-contained HTML report, scoring matrix, executive summary, competitor briefs, opportunities, and a 30/60/90 plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to compare competitors in a market niche, identify pricing, offer, positioning, proof, channel, and product patterns, and turn the findings into actionable product and positioning recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be used to request credentials or scrape private competitor communities.

Mitigation: Do not provide passwords or authorize private-community scraping unless rights and secure handling are confirmed; prefer public pages, public ads, public reviews, and public profiles.

Risk: The workflow can persist competitor research reports and raw data.

Mitigation: Confirm the intended report and raw-data storage locations before execution, and avoid storing sensitive or unauthorized material.

Risk: External research tools can incur usage costs and may produce incomplete results when sources block access.

Mitigation: Confirm Apify cost estimates before use, disclose unavailable sources, and mark partial findings instead of filling gaps with unsupported claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/benchmark-producto-formula100k)
- [10 Dimensiones de Analisis](references/dimensiones.md)
- [Template HTML Reporte Benchmark F100K](references/template-reporte-html.md)
- [Template del Reporte Final](references/template-reporte.md)
- [Fallbacks](references/fallbacks.md)
- [Apify Actors curados](references/apify-actors.md)
- [Voz y frases tipo F100K](references/voz-y-frases.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated HTML, Markdown, and CSV report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary deliverable is a self-contained HTML report; secondary outputs include a CSV scoring matrix, Markdown summaries, competitor files, opportunities, and raw research notes.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
