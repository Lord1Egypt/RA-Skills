## Description:

Guides users through setting up and running Karpathy's autoresearch experiments, writing program.md instructions, interpreting training results, and tuning configurations for different GPU sizes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tommot2](https://clawhub.ai/user/tommot2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for advisory help with autoresearch setup, experiment planning, program.md drafting, result interpretation, and small-GPU configuration choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following the skill's setup guidance can lead users to run training jobs that consume GPU compute.

Mitigation: Review the external autoresearch repository and estimate compute cost before running experiments.

Risk: Allowing an agent to modify train.py can change project behavior or overwrite local experiment work.

Mitigation: Use version control or a disposable branch and review proposed changes before letting an agent continue experiments.

Risk: The skill provides experiment guidance rather than executing or validating commands itself.

Mitigation: Treat commands and configuration suggestions as advisory and verify them in the target environment before use.

## Reference(s):

- [Autoresearch GitHub repository](https://github.com/karpathy/autoresearch)
- [Autoresearch Pilot ClawHub page](https://clawhub.ai/tommot2/skills/autoresearch-pilot)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with explanatory text, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output only; the skill says not to run training commands or modify files directly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
