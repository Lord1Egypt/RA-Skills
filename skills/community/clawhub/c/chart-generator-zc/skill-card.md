## Description: <br>
Data visualization tool producing SVG charts and terminal-friendly chart outputs for bar charts, line charts, pie charts, tables, sparklines, gauges, dashboards, heatmaps, and progress views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users can use this skill to generate quick data visualizations from command-line data inputs. It is suited for producing ASCII charts for terminals and SVG or HTML chart files for sharing or embedding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Bash/Python scripts that can write chart files and limited local history. <br>
Mitigation: Run it only in an environment where local script execution is acceptable, choose output paths deliberately, and avoid sensitive chart titles or labels when using history-enabled commands. <br>
Risk: Chart titles and labels are embedded into generated SVG or HTML outputs. <br>
Mitigation: Use trusted, non-sensitive labels and review generated files before sharing or publishing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lean-zhouchao/chart-generator-zc) <br>
- [Data visualization best practices](artifact/tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated ASCII, SVG, or HTML chart outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write chart files to caller-selected paths and limited local chart history when using the history-enabled script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
