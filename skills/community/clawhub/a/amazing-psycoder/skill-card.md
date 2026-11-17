## Description:

Amazing PsyCoder routes psychology experiment and data-analysis requests through mandatory design, coding, and review chains for PsychoPy, jsPsych, Psychtoolbox, R, and Python workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soupandpsy](https://clawhub.ai/user/soupandpsy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research assistants use this skill to design psychological experiments, generate experiment or analysis code, and require structured review before data collection or publication use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled raw experiment demos contain unsafe code patterns and data-upload behavior.

Mitigation: Do not run or copy raw demos directly; use the specification, checklist, and reviewer workflow before data collection, and disclose upload behavior to participants and researchers.

Risk: Manual installation may overwrite existing skill directories with the same names.

Mitigation: Inspect the target skill directory first, keep backups of existing skills, and test installation in a disposable workspace when possible.

Risk: Experiment or analysis outputs can be misused before methodological or implementation review.

Mitigation: Require the mandatory reviewer step and resolve Critical and Major findings before data collection or publication use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/soupandpsy/skills/amazing-psycoder)
- [Agent Skills Open Standard](https://agentskills.io)
- [Platform Compatibility](artifact/PLATFORMS.md)
- [Experiment Config Schema](artifact/psy-exp-designer/references/config-schema.md)
- [Experiment Timing Guidance](artifact/psy-exp-designer/references/timing.md)
- [Experiment Data Recording Guidance](artifact/psy-exp-designer/references/data-recording.md)
- [PsychoPy Code Specification](artifact/psy-exp-coder/psychopy/spec/README.md)
- [jsPsych Code Specification](artifact/psy-exp-coder/jspsych/spec/README.md)
- [Psychtoolbox Code Specification](artifact/psy-exp-coder/psychtoolbox/spec/README.md)
- [Python Analysis Code Specification](artifact/psy-ana-coder/python/spec/README.md)
- [R Analysis Code Specification](artifact/psy-ana-coder/r/spec/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated code, configuration snippets, shell commands, and review reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are gated by mandatory design and reviewer steps before experiment collection or analysis publication use.]

## Skill Version(s):

1.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
