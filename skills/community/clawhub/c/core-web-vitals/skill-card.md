## Description:

Guides agents in assessing and improving Core Web Vitals issues for LCP, INP, CLS, and related page performance concerns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kostja94](https://clawhub.ai/user/kostja94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO practitioners, and site performance engineers use this skill to diagnose Core Web Vitals failures and prioritize remediation for loading performance, responsiveness, and visual stability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad page speed or page performance requests beyond explicit Core Web Vitals issues.

Mitigation: Confirm that the user's request concerns Core Web Vitals or related page experience metrics before applying its recommendations.

Risk: Performance recommendations can be incorrect if applied without validating the affected metric, page type, and current field or lab data.

Mitigation: Review proposed changes against GSC, PageSpeed Insights, Chrome DevTools, or project-specific performance data before deployment.

## Reference(s):

- [Google Page Experience](https://developers.google.com/search/docs/appearance/page-experience)
- [Web Vitals](https://web.dev/vitals/)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with prioritized fixes, references, and optional inline code or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no executable artifact files are included.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
