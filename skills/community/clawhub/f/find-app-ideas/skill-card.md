## Description:

Finds underserved App Store / Google Play niches with live AppGoat data - search demand (keyword popularity) against weak supply (low ratings, abandoned incumbents, few strong apps) - and returns a ranked shortlist of app ideas with evidence and user pain points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafalzawadzki](https://clawhub.ai/user/rafalzawadzki)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and aspiring app builders use this skill to discover or validate app niches by comparing search demand, incumbent quality, competition, and user review pain points. It helps them shape a focused MVP and launch keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AppGoat receives submitted search terms and charges credits for research.

Mitigation: Generalize confidential ideas before submitting them, and monitor the credit usage shown by AppGoat.

Risk: Automated reports may expose research in a GitHub issue.

Mitigation: Check repository visibility before enabling issue publishing.

Risk: A monthly automation schedule can continue running after it is no longer needed.

Mitigation: Disable the schedule when finished.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/rafalzawadzki/skills/find-app-ideas)
- [REST API fallback](reference/api.md)
- [AppGoat API](https://api.appgoat.ai/v1)

## Skill Output:

**Output Type(s):** [Analysis, Recommendations, Markdown]

**Output Format:** [Markdown report with a ranked shortlist, supporting market evidence, user pain points, MVP suggestions, and launch keywords]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Niche, app store, and country can be specified; findings use live market data.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
