## Description:

Control Apple TV via pyatv for playback, navigation, volume, app launching, power control, and checking what is playing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucakaufmann](https://clawhub.ai/user/lucakaufmann)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to operate a paired Apple TV from an agent by issuing local pyatv commands for media status, playback, navigation, volume, app launching, discovery, and power control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers such as "TV" may cause unintended Apple TV control.

Mitigation: Narrow or remove broad triggers and consider requiring confirmation for power and app-launch commands.

Risk: Pairing credentials stored in local configuration may be exposed through local files or process command lines.

Mitigation: Protect the Apple TV configuration file, avoid logging command lines that include credentials, and rotate pairing credentials if exposure is suspected.

Risk: Unpinned pyatv installation can change behavior across dependency updates.

Mitigation: Pin the pyatv version during installation and review updates before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Apple TV pairing configuration and pyatv on Python 3.13 or earlier.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
