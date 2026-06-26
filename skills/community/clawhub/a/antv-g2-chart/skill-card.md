## Description: <br>
Generate G2 v5 chart code for bar charts, line charts, pie charts, scatter plots, area charts, and other AntV G2 data visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxfu1](https://clawhub.ai/user/lxfu1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to produce AntV G2 v5 visualization code that follows Spec Mode, valid mark types, encoding rules, interactions, components, scales, coordinates, themes, palettes, animations, and responsive chart patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chart snippets may include unsafe raw HTML tooltip renderers when fed untrusted values. <br>
Mitigation: Review generated snippets and escape untrusted values before running or publishing them. <br>
Risk: Charts may reference remote data or image URLs that are untrusted or unavailable. <br>
Mitigation: Use trusted or proxied data sources and verify remote assets before deployment. <br>
Risk: Complex G2 chart requests can produce inaccurate or outdated chart options. <br>
Mitigation: Verify complex chart references against official G2 documentation before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lxfu1/antv-g2-chart) <br>
- [G2 v5 chart initialization](references/core/g2-core-chart-init.md) <br>
- [G2 encode channels](references/core/g2-core-encode-channel.md) <br>
- [G2 view composition](references/core/g2-core-view-composition.md) <br>
- [Chart selection guidance](references/concepts/g2-concept-chart-selection.md) <br>
- [G2 v4 to v5 migration patterns](references/patterns/g2-pattern-v4-to-v5.md) <br>
- [G2 performance patterns](references/patterns/g2-pattern-performance.md) <br>
- [G2 responsive patterns](references/patterns/g2-pattern-responsive.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with JavaScript or HTML code blocks and concise implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated snippets should be reviewed before execution, especially when they include raw HTML tooltip renderers or remote data and image URLs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
