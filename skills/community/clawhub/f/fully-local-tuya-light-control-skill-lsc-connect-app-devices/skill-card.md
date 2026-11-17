## Description:

Controls locally configured LSC/Tuya lamps and lamp groups from a workspace registry, including on/off actions, brightness, colors, white modes, status checks, and onboarding after repair or network changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ooxtcoo](https://clawhub.ai/user/ooxtcoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent translate local lighting requests into Tuya lamp-control commands for a configured home or workspace setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run local executables from mutable project paths.

Mitigation: Verify the lampctl binary, Python scripts, and configured paths before enabling the skill.

Risk: The skill may refresh Tuya device keys and update local lamp configuration.

Mitigation: Keep real local keys only in local configuration, sanitize shared registry examples, and review configuration updates before applying them.

Risk: The skill asks agents to persistently edit the installed skill file for local path changes.

Mitigation: Prefer a separate local configuration file for site-specific paths and avoid automatic rewrites of the installed SKILL.md.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for local execution against user-configured Tuya device registries and controller binaries.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
