## Description:

Apollo Endo helps an agent monitor its operating state and dynamically tune global work-mode parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to adjust an agent's global operating parameters, such as efficiency, context priority, creativity, confirmation level, and verbosity, based on explicit preference changes or detected system state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persistently influence global agent behavior across tasks.

Mitigation: Require explicit confirmation before persistent parameter changes and review or narrow the configured triggers before deployment.

Risk: The skill can inspect OpenClaw memory and cross-skill task activity when its helper script is run.

Mitigation: Run it only with the workspace access needed for the intended task and avoid exposing other skills' private state.

Risk: Broad triggers can cause parameter guidance to activate in more conversations than intended.

Mitigation: Limit triggers to explicit parameter, preference, and mode-change requests where possible.

## Reference(s):

- [Apollo Endo ClawHub skill page](https://clawhub.ai/nic-yuan/skills/apollo-endo)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text status reports with shell command output and JSON state data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script can write a local parameter-state report when executed.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
