## Description:

Help install, inspect, run, troubleshoot, and adapt the DeepPurpose molecular modeling library for drug-target interaction prediction, compound property prediction, DDI, PPI, protein function prediction, drug repurposing, and virtual screening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoeprior](https://clawhub.ai/user/zoeprior)

### License/Terms of Use:

BSD-3-Clause

## Use Case:

Developers and researchers use this skill to get grounded guidance for installing DeepPurpose, selecting the correct task module, preparing molecular or protein datasets, loading pretrained models, and adapting DeepPurpose demos into agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guidance includes an unpinned Git dependency example.

Mitigation: Install in an isolated environment and pin the Git dependency to a reviewed commit before production use.

Risk: Dataset helpers and pretrained model helpers may download remote files.

Mitigation: Review download sources, keep writable paths explicit, and prefer local pretrained directories or local inputs when network downloads are not desired.

Risk: DeepPurpose has older Python and scientific package expectations that may not match current default runtimes.

Mitigation: Check the interpreter and dependency set before promising runtime execution; use static validation when a full dependency environment is unavailable.

## Reference(s):

- [Data And Pretrained Models](references/data-and-pretrained.md)
- [Install And Dependencies](references/install-and-dependencies.md)
- [Tasks And Entrypoints](references/tasks-and-entrypoints.md)
- [ClawHub Skill Page](https://clawhub.ai/zoeprior/skills/deeppurpose)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include warnings for dependency setup, remote downloads, dataset format pitfalls, and pretrained model behavior.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
