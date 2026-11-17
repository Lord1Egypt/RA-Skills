## Description:

Converts tabular CSV data into visual charts and graphs by selecting appropriate chart types and generating runnable rendering code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with CSV data use this skill to choose a suitable chart type and generate code for visual charts. It is intended for requests where the user provides CSV data and explicitly asks to plot, graph, or visualize it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV inputs may contain sensitive data that the agent reads to build the chart.

Mitigation: Provide only CSV files or pasted rows that are intended for the agent to process.

Risk: Generated chart code may be incorrect, omit data, or rely on external plotting libraries.

Mitigation: Review the generated code, chart mappings, dependencies, and rendered output before running or sharing it.

## Reference(s):

- [ClawHub Csv To Chart skill page](https://clawhub.ai/wangjipeng977/skills/csv-to-chart)
- [Metadata source: MiniMax-AI skills](https://github.com/MiniMax-AI/skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown with runnable Python, JavaScript, or Mermaid code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include chart type rationale, axis labels, legends, and notes for missing values or large category counts.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata and changelog report 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
