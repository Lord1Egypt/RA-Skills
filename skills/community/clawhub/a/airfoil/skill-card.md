## Description:

Control AirPlay speakers via Airfoil from the command line. Connect, disconnect, set volume, and manage multi-room audio with simple CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asteinberger](https://clawhub.ai/user/asteinberger)

### License/Terms of Use:


## Use Case:

External users and developers on macOS use this skill to control Airfoil-managed AirPlay speakers from an agent or terminal, including listing speakers, connecting or disconnecting them, setting volume, and checking status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted or untrusted speaker names could be handled unsafely by the AppleScript command path.

Mitigation: Use only trusted speaker names until the script passes speaker names as AppleScript arguments and validates or escapes inputs.

Risk: Unvalidated volume values could cause unexpected command behavior.

Mitigation: Constrain volume input to numeric values from 0 to 100 before invoking the volume command.

## Reference(s):

- [ClawHub Airfoil Skill Page](https://clawhub.ai/asteinberger/skills/airfoil)
- [Airfoil for Mac](https://rogueamoeba.com/airfoil/mac/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text with shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, Airfoil, osascript, and trusted speaker names and volume values.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
