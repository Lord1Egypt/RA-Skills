## Description: <br>
Create data visualizations from the command line. Generate charts, graphs, and plots from CSV/JSON data without leaving the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianalloway](https://clawhub.ai/user/ianalloway) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create terminal charts, plots, sparklines, and tables from CSV, JSON, piped data, system metrics, and API responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends installing Ruby and Python packages for terminal visualization. <br>
Mitigation: Install YouPlot and termgraph only after reviewing the package sources and confirming they are acceptable for the target environment. <br>
Risk: Examples fetch remote data with curl, process local files, and can be run repeatedly with watch. <br>
Mitigation: Review commands before execution, use trusted data sources and local files, and avoid live-update loops unless the command and interval are appropriate. <br>


## Reference(s): <br>
- [Data Viz Skill Page](https://clawhub.ai/ianalloway/data-viz) <br>
- [Publisher Profile](https://clawhub.ai/user/ianalloway) <br>
- [YouPlot](https://github.com/red-data-tools/YouPlot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command examples for terminal data visualization tools; users run and adapt commands in their own shell environment.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
