## Description:

Analyze competitor product listings, pricing strategies, and promotional tactics to identify ecommerce gaps and opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce operators, marketers, and marketplace sellers use this skill to turn public competitor listing observations and user-provided business inputs into structured competitive intelligence reports with prioritized actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process user-provided prices, margins, product URLs, and other business-sensitive competitive inputs.

Mitigation: Avoid providing confidential internal analytics unless those details are intended to be used in the analysis.

Risk: Competitor recommendations can be misleading if snapshot observations are treated as durable trends.

Mitigation: Timestamp data, flag information older than seven days, and label claims as observed, inferred, or estimated.

Risk: Marketplace data can be incomplete because private conversion rates, exact ad spend, backend search terms, and internal analytics are not publicly observable.

Mitigation: Base recommendations on public or user-provided evidence and explicitly state data limitations.

## Reference(s):

- [Output Template](artifact/references/output-template.md)
- [Analysis Frameworks Reference](artifact/references/analysis-frameworks.md)
- [Platform-Specific Reference](artifact/references/platform-specifics.md)
- [Quality Checklist](artifact/assets/quality-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown reports with structured tables, evidence labels, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should timestamp observations, flag data freshness, distinguish observed, inferred, and estimated claims, and avoid unsupported private analytics.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
