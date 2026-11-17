## Description:

An overview of the python package for running the GaMMA earthquake phase association algorithm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and seismic data engineers use this skill to understand how GaMMA associates P/S phase picks with earthquake events and how to prepare pick, station, and configuration inputs for the core API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation command uses an unpinned mutable GitHub dependency, and the security evidence says the relationship between the installed wayneweiqiang/GaMMA repository and the artifact's stated AI4EPS/GaMMA derivative source is not explained.

Mitigation: Review and pin the GaMMA dependency before installation, prefer a trusted release or fully reviewed commit hash, install in an isolated virtual environment or container, and confirm the intended upstream repository before use.

## Reference(s):

- [GaMMA repository named in skill artifact](https://github.com/AI4EPS/GaMMA)
- [GaMMA install dependency named in skill artifact](https://github.com/wayneweiqiang/GaMMA.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API signatures, tables, and inline Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents expected DataFrame inputs, configuration keys, return values, and practical usage notes for GaMMA association workflows.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
