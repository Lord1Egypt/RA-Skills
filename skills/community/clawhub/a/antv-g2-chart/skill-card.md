## Description:

Generate G2 v5 chart code. Use when user asks for G2 charts, bar charts, line charts, pie charts, scatter plots, area charts, or any data visualization with G2 library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxfu1](https://clawhub.ai/user/lxfu1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data visualization practitioners use this skill to generate and revise AntV G2 v5 chart code for common charts while following documented v5 spec-mode constraints and reference patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated chart code may be copied into contexts with private data or untrusted tooltip values.

Mitigation: Review generated code before use and escape or sanitize data displayed in tooltips, labels, and annotations.

Risk: Generated examples may reference third-party URLs or fetched data sources that are not appropriate for the deployment environment.

Mitigation: Allowlist trusted endpoints, proxy remote data where needed, and remove unapproved external URLs before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lxfu1/skills/antv-g2-chart)
- [G2 core chart initialization](references/core/g2-core-chart-init.md)
- [G2 encode channel reference](references/core/g2-core-encode-channel.md)
- [G2 view composition reference](references/core/g2-core-view-composition.md)
- [G2 chart selection guide](references/concepts/g2-concept-chart-selection.md)
- [G2 v4 to v5 migration patterns](references/patterns/g2-pattern-v4-to-v5.md)
- [G2 responsive patterns](references/patterns/g2-pattern-responsive.md)
- [G2 performance patterns](references/patterns/g2-pattern-performance.md)

## Skill Output:

**Output Type(s):** [code, markdown, configuration, guidance]

**Output Format:** [Markdown responses with JavaScript or TypeScript G2 v5 code blocks and concise implementation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated chart code should be reviewed before production use, especially with private data, untrusted tooltip content, or third-party URLs.]

## Skill Version(s):

1.0.2 (source: server release evidence, created 2026-04-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
