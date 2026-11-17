## Description:

Career Counselor helps Chinese university graduates plan career paths, compare offers, choose cities, prepare job-search materials, and manage career uncertainty using structured counseling protocols and current labor-market research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuizhang1988-cmyk](https://clawhub.ai/user/kuizhang1988-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially Chinese undergraduate and master's graduates, use this skill to explore job directions, validate career choices, compare offers, choose cities, and plan 3-5 year fallback-aware career paths.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill asks for personal career context, including family constraints, which may be sensitive for users.

Mitigation: Collect only the context needed for the current counseling task and avoid retaining or sharing unnecessary personal details.

Risk: The skill uses live web searches for labor-market data, so search-result errors or outdated sources could affect career advice.

Mitigation: Cross-check important claims against multiple reliable sources and clearly mark uncertain or fallback-based findings.

Risk: The security evidence notes behavior that may persist web-derived updates into reference files.

Mitigation: Run packaged skill files read-only or require review and approval before any reference-file updates are retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kuizhang1988-cmyk/skills/career-counselor)
- [Server-resolved GitHub provenance](https://github.com/kuizhang1988-cmyk/career-counselor)
- [Industry Employment Data Baseline](references/industry-data.md)
- [City Selection Decision Framework](references/city-selection.md)
- [Online Analysis and Forecasting Framework](references/trend-forecast.md)
- [Emerging Roles and Tracks 2025-2026](references/emerging-roles.md)
- [Safety Guardrails and Evolution Mechanism](references/safety-and-evolution.md)
- [Offer Comparison Decision Protocol](references/offer-comparison.md)
- [Job Hunt Toolkit](references/job-hunt-toolkit.md)
- [Output Format Templates](references/output-format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown counseling responses with structured recommendations, comparisons, checklists, and contingency plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for personal career context and may use live web search for current labor-market evidence.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
