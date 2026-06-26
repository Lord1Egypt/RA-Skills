## Description: <br>
Help install, inspect, run, troubleshoot, and adapt the DeepPurpose molecular modeling library for drug-target interaction prediction, compound property prediction, DDI, PPI, protein function prediction, drug repurposing, and virtual screening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoeprior](https://clawhub.ai/user/zoeprior) <br>

### License/Terms of Use: <br>
BSD 3-Clause <br>


## Use Case: <br>
Developers and researchers use this skill to get practical guidance for installing DeepPurpose, selecting task modules, preparing molecular or protein datasets, using pretrained models, and adapting demos for drug discovery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DeepPurpose installation and runtime workflows can involve heavy scientific dependencies and shell commands. <br>
Mitigation: Use an isolated environment and review conda and pip commands before running them. <br>
Risk: Dataset helpers and pretrained model helpers may download remote assets and create local output files. <br>
Mitigation: Confirm download behavior and writable output paths before running workflows, especially in shared or production environments. <br>


## Reference(s): <br>
- [deeppurpose ClawHub page](https://clawhub.ai/zoeprior/deeppurpose) <br>
- [Install And Dependencies](references/install-and-dependencies.md) <br>
- [Tasks And Entrypoints](references/tasks-and-entrypoints.md) <br>
- [Data And Pretrained Models](references/data-and-pretrained.md) <br>
- [Descriptastorus dependency](https://github.com/bp-kelley/descriptastorus) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include warnings about dependency setup, remote downloads, local output files, and task-specific DeepPurpose APIs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
