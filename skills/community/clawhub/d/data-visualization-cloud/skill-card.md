## Description:

Generates interactive HTML dashboards from CSV or Excel data by analyzing tabular data characteristics and recommending suitable chart combinations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudcba](https://clawhub.ai/user/cloudcba)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this skill to turn tabular datasets into interactive dashboards with automatically selected charts for comparison, trend, distribution, relationship, and hierarchy analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted CSV or Excel content can be carried into executable HTML dashboards.

Mitigation: Use trusted or sanitized datasets and review generated dashboards before opening, publishing, or sharing them.

Risk: Generated dashboards may load Plotly from a CDN.

Mitigation: Use a trusted network path or modify the script to embed a reviewed local Plotly copy when external CDN loading is not acceptable.

Risk: User-selected output paths can write dashboards to unintended locations.

Mitigation: Choose explicit output paths in controlled directories and avoid overwriting important files.

## Reference(s):

- [Chart Types Guide](references/chart-types.md)
- [Data Format Specification](references/data-format.md)
- [ClawHub Skill Page](https://clawhub.ai/cloudcba/skills/data-visualization-cloud)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated HTML dashboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script writes a single responsive Plotly HTML dashboard and can include up to 15 recommended charts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
