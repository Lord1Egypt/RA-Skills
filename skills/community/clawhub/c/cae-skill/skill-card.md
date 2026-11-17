## Description:

Control local CAE applications on Windows including launching apps, opening files, checking status, closing apps, detecting active and running apps, detecting common executable paths, and saving user-provided executable paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doudou459](https://clawhub.ai/user/doudou459)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage supported Windows CAE workstation applications, including launching tools, opening CAE files, checking running status, closing applications, and saving trusted executable paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch local CAE executables and open CAE files on a Windows workstation.

Mitigation: Use it only in trusted local CAE workflows with trusted executable paths and trusted config.json files.

Risk: Abaqus .py and .jnl files may execute when opened through the skill.

Mitigation: Open those file types only when the user intends to execute them and has reviewed the file source.

Risk: The close_app action can force-close supported CAE applications.

Mitigation: Require explicit user confirmation before force-closing applications, especially when unsaved work may be present.

Risk: Saving a new executable path changes which local binary the skill launches.

Mitigation: Confirm the path with the user and accept only trusted, user-provided executable locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/doudou459/skills/cae-skill)
- [Publisher profile](https://clawhub.ai/user/doudou459)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON status objects and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include success flags, messages, app names, executable paths, commands, process IDs, running application lists, and error details.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
