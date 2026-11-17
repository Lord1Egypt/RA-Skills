## Description:

DuIvyTools Skills helps agents use the DuIvyTools (dit) CLI to analyze and visualize GROMACS molecular dynamics outputs, including XVG, XPM, NDX, statistics, Ramachandran plots, and CSV/DAT conversions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charleshahn](https://clawhub.ai/user/charleshahn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill when they need command guidance for DuIvyTools molecular dynamics analysis workflows, including plotting, statistical summaries, index operations, file conversion, and generated command examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running DuIvyTools from an untrusted package source could execute unreviewed third-party code.

Mitigation: Install only from a trusted source, preferably in a virtual environment, and pin a reviewed version.

Risk: Generated plots, CSV/DAT/XPM files, MDP templates, and style files may be written into the working directory.

Mitigation: Run commands in the intended project directory and review output paths before execution.

Risk: DuIvyTools command options may change over time.

Mitigation: Run dit <command> -h before use and verify parameters against the installed version.

## Reference(s):

- [DuIvyTools command reference](references/commands-reference.md)
- [DuIvyTools usage examples](references/examples.md)
- [DuIvyTools documentation](https://duivytools.readthedocs.io/)
- [DuIvyTools GitHub project](https://github.com/CharlesHahn/DuIvyTools)
- [DuIvyTools DOI](https://doi.org/10.5281/zenodo.6339993)
- [ClawHub skill page](https://clawhub.ai/charleshahn/skills/duivytools-skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and file-format notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend installing DuIvyTools, running dit subcommands, and writing analysis outputs in the working directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
