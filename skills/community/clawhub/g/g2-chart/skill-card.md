## Description:

Generate G2 v5 chart code for G2 charts, bar charts, line charts, pie charts, scatter plots, area charts, and other data visualizations with the G2 library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxfu1](https://clawhub.ai/user/lxfu1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to generate runnable AntV G2 v5 chart code for common data visualization requests. It helps agents choose G2 marks, encodings, interactions, themes, and layout patterns while avoiding known v4-to-v5 API mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated chart code may contain mistakes or omit project-specific production requirements.

Mitigation: Review generated code before production use and test it with representative data and target browser environments.

Risk: Charts that fetch external data or image URLs can depend on untrusted or cross-origin resources.

Mitigation: Prefer trusted or same-origin data and image URLs, and validate fetched data before rendering.

Risk: Custom raw HTML tooltip renderers can expose unsafe labels or values when chart data is untrusted.

Mitigation: Avoid raw HTML tooltip renderers with untrusted data unless labels and values are sanitized first.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lxfu1/skills/g2-chart)
- [G2 v5 Chart Code Generator](artifact/SKILL.md)
- [G2 Chart Initialization](artifact/references/core/g2-core-chart-init.md)
- [G2 Encode Channels](artifact/references/core/g2-core-encode-channel.md)
- [G2 View Composition](artifact/references/core/g2-core-view-composition.md)
- [G2 Chart Selection Guide](artifact/references/concepts/g2-concept-chart-selection.md)
- [G2 v4 to v5 Migration](artifact/references/patterns/g2-pattern-v4-to-v5.md)
- [G2 Performance Patterns](artifact/references/patterns/g2-pattern-performance.md)
- [G2 Responsive Patterns](artifact/references/patterns/g2-pattern-responsive.md)
- [AntV G2 Core Chart Documentation](https://g2.antv.antgroup.com/manual/core/chart)
- [AntV G2 Encode Documentation](https://g2.antv.antgroup.com/manual/core/encode)

## Skill Output:

**Output Type(s):** [Code, Markdown, Guidance]

**Output Format:** [Markdown with JavaScript code blocks and concise implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated chart code should be reviewed before production use, especially when it fetches external data or renders custom tooltip HTML.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
