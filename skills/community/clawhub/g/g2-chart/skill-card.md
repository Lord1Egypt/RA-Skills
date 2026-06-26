## Description: <br>
Generate G2 v5 chart code for bar charts, line charts, pie charts, scatter plots, area charts, and other AntV G2 visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxfu1](https://clawhub.ai/user/lxfu1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate runnable AntV G2 v5 chart code and to avoid common API mistakes when building data visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chart code may include custom tooltip HTML that could be unsafe if copied into an application without review. <br>
Mitigation: Review and sanitize tooltip HTML and dynamic content before production use. <br>
Risk: Generated examples may fetch remote data or suggest saving edited chart data to a backend. <br>
Mitigation: Validate data sources, request handling, and backend writes against the application security model before deployment. <br>
Risk: Generated visualization code can be incorrect or misleading if the chart type, encodings, or transforms do not match the data semantics. <br>
Mitigation: Review generated code and chart output with domain data before relying on it in user-facing workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lxfu1/g2-chart) <br>
- [G2 core chart initialization](artifact/references/core/g2-core-chart-init.md) <br>
- [G2 chart selection](artifact/references/concepts/g2-concept-chart-selection.md) <br>
- [G2 v4 to v5 migration patterns](artifact/references/patterns/g2-pattern-v4-to-v5.md) <br>
- [G2 tooltip configuration](artifact/references/components/g2-comp-tooltip-config.md) <br>
- [G2 data fetch transform](artifact/references/data/g2-data-fetch.md) <br>
- [G2 responsive patterns](artifact/references/patterns/g2-pattern-responsive.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JavaScript or TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces chart implementation guidance and G2 v5 spec-mode code; generated code should be reviewed before production use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
