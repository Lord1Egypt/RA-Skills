## Description:

Analyzes App Store and Google Play listings against ASO best practices and produces prioritized recommendations for improving metadata, visuals, ratings, and conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[troatpopcorn](https://clawhub.ai/user/troatpopcorn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and app teams use this skill to audit Apple App Store or Google Play listings, compare competitors when provided, and produce a prioritized ASO action plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local product marketing context if present.

Mitigation: Review that context for sensitive material before using it in an audit and avoid including confidential details in shared outputs.

Risk: The skill may fetch public App Store or Google Play pages and screenshots, and store pages can be incomplete or rendered client-side.

Mitigation: Treat unavailable fields as gaps, ask the user for critical missing data, and separate observed evidence from recommendations.

## Reference(s):

- [Apple App Store Specs and Guidelines](references/apple-specs.md)
- [Google Play Store Specs and Guidelines](references/google-play-specs.md)
- [ASO Benchmarks and Conversion Data](references/benchmarks.md)
- [ASO Scoring Criteria](references/scoring-criteria.md)
- [ASO Audit Report Template](references/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report with scoring tables, findings, keyword suggestions, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include competitor comparison, platform-specific limitations, and requests for missing listing data when public store pages are incomplete.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
