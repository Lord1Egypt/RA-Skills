## Description:

Automatically visualizes CSV, Excel, and JSON data files by analyzing tabular structure, selecting chart types, and generating PNG, SVG, HTML, or PDF outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaosusu](https://clawhub.ai/user/zaosusu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to turn local CSV, Excel, or JSON files into static or interactive charts and to inspect basic data structure without writing plotting code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Interactive HTML chart files may contain source data needed for browser-based interaction.

Mitigation: Treat generated HTML outputs with the same confidentiality controls as the input dataset.

Risk: The dependency ranges for pandas, plotly, and openpyxl are not pinned to exact reviewed versions.

Mitigation: Install and run the skill in a locked environment with reviewed dependency versions.

Risk: The skill reads user-selected local data files and writes chart outputs to local paths.

Mitigation: Review input and output paths before execution, especially when working with confidential or regulated data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaosusu/skills/autoplot-skill)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated chart files in PNG, SVG, HTML, or PDF.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against user-specified CSV, Excel, or JSON files; interactive HTML outputs may include the data needed for browser-based interaction.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
