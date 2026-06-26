## Description: <br>
AutoMD-Viz generates publication-quality molecular dynamics visualizations, including structures, data plots, trajectory projections, and full reports with journal-specific styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billwanttobetop](https://clawhub.ai/user/billwanttobetop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and computational biology teams use this skill to create journal-ready molecular dynamics figures from structure files, time-series data, trajectory projections, and analysis outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided paths and visualization options are passed into generated plotting scripts. <br>
Mitigation: Use trusted input files and filenames, and run the skill in a normal project directory or virtual environment. <br>
Risk: The skill relies on local scientific visualization dependencies that may be installed separately. <br>
Mitigation: Install dependencies from trusted package sources and keep the environment scoped to the project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billwanttobetop/automd-viz) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [publication-viz-errors.md](artifact/publication-viz-errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, markdown, files] <br>
**Output Format:** [Markdown guidance and shell commands; when executed, the bundled script can generate PNG, SVG, PDF, EPS, PyMOL session, and Markdown report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on local visualization tools and supplied molecular dynamics inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
