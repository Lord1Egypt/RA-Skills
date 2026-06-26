## Description: <br>
Guides an agent in using the DuIvyTools command-line interface for GROMACS molecular dynamics analysis, including XVG and XPM visualization, NDX index operations, statistics, Ramachandran plots, and CSV/DAT conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CharlesHahn](https://clawhub.ai/user/CharlesHahn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and computational scientists use this skill when they need concise DuIvyTools command guidance for molecular dynamics analysis workflows. It helps agents propose installation, help, visualization, statistical analysis, file conversion, and index-file commands while preserving the tool's data-handling conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to install or invoke the external DuIvyTools Python package. <br>
Mitigation: Verify the external package and source before installation, and install it only for molecular dynamics analysis use cases. <br>
Risk: Local file-processing, conversion, batch, or overwrite-style commands may read or write analysis files unexpectedly. <br>
Mitigation: Review generated commands, input files, and output paths before execution; use command help such as dit <command> -h before running unfamiliar commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/CharlesHahn/duivytools-skills) <br>
- [commands-reference.md](references/commands-reference.md) <br>
- [examples.md](references/examples.md) <br>
- [DuIvyTools GitHub Repository](https://github.com/CharlesHahn/DuIvyTools) <br>
- [DuIvyTools Documentation](https://duivytools.readthedocs.io/) <br>
- [DuIvyTools Zenodo Record](https://doi.org/10.5281/zenodo.6339993) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no hidden or abusive behavior found in security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
