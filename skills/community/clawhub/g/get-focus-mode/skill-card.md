## Description:

Get the current macOS Focus mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickchristensen](https://clawhub.ai/user/nickchristensen)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent report the active macOS Focus mode from the local machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local macOS Focus/Do Not Disturb database files to determine the active Focus mode.

Mitigation: Install and run it only on macOS systems where reading those local Focus configuration files is acceptable.

Risk: The skill depends on jq and macOS Do Not Disturb database paths being present.

Mitigation: Confirm jq is installed and the expected macOS database files exist before relying on the output.

## Reference(s):

- [Get Focus Mode on ClawHub](https://clawhub.ai/nickchristensen/skills/get-focus-mode)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text written to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the active Focus mode name or "No Focus"; requires macOS and jq.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
