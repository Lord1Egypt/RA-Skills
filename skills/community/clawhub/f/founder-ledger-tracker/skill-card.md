## Description:

A dependency-free Python tool that tracks a numeric goal (like a first revenue milestone) and a date-based budget guard, printing a one-line reminder and exiting with a branchable code for the calling agent or script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulscode](https://clawhub.ai/user/paulscode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to initialize and check a local goal and budget reminder state file, then branch workflows from the emitted one-line status and exit code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and updates a local JSON state file in the current directory by default, and --force can overwrite an existing tracker state file.

Mitigation: Run it in the intended workspace, set --state to an explicit path when needed, and use --force only after confirming the target state file may be replaced.

Risk: The local state file can contain goal, deadline, and spend-tracking values chosen by the caller.

Mitigation: Store the state file in an appropriate local project location and avoid entering sensitive financial or credential data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulscode/skills/founder-ledger-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/paulscode)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text reminders, numeric exit codes, and local JSON state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses exit codes 0, 1, and 2 for no trigger, soft trigger, and hard trigger; writes a local JSON state file when initialized or updated.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
