## Description: <br>
Use when a user provides CSV data and asks to generate, plot, graph, or visualize it as a chart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, developers, and analysts use this skill to turn CSV data into suitable visualizations, including bar, line, scatter, pie, histogram, heatmap, or radar charts. The skill can recommend a chart type or produce runnable chart code with axis labels, titles, legends, and missing-value handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chart code may misrepresent data if column types, missing values, or chart suitability are handled incorrectly. <br>
Mitigation: Review the selected chart type, axis mappings, missing-value treatment, and rendered output before using the visualization for decisions. <br>
Risk: Generated code can execute in the user's local environment and may depend on charting libraries. <br>
Mitigation: Run generated code in a trusted workspace and inspect dependencies, file paths, and data handling before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangjipeng977/csv-to-chart) <br>
- [Publisher Profile](https://clawhub.ai/user/wangjipeng977) <br>
- [Declared Metadata Source](https://github.com/MiniMax-AI/skills) <br>
- [Reference Index](references/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with chart rationale and runnable Python, JavaScript, or Mermaid code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include chart type recommendations, axis mappings, dependency notes, missing-value treatment, and warnings for unsuitable chart choices or large inputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
