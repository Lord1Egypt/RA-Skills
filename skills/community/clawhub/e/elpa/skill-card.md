## Description:

Orchestrate real ELPA-style ensemble forecasting workflows by triggering external sub-model training jobs (for example PyTorch/Prophet/TiDE/transformers), then computing ELPA online/offline weights from validation errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anonymouscodemaker](https://clawhub.ai/user/anonymouscodemaker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan or execute external forecasting model training jobs, then produce ELPA online and offline ensemble policy weights from validation errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Training configs can become unrestricted local shell commands with broad environment access.

Mitigation: Review every train_cmd and placeholder before using --execute, run only trusted configs, avoid sensitive API keys in the environment, and use an isolated workspace or container.

## Reference(s):

- [ELPA Config Schema](references/config-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/anonymouscodemaker/skills/elpa)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration files; scripts can emit JSON manifests and ELPA policy JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run planning records commands without training; execution requires trusted configuration, local ML dependencies, and suitable hardware.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
