## Description:

Search and play Netflix content on Android TV. When the user asks to play a specific Netflix title on TV, the agent looks up the title ID and executes ADB commands for precise playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiayun](https://clawhub.ai/user/jiayun)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to find Netflix title IDs, connect to an authorized Android TV over ADB, and start Netflix playback for requested titles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let a local machine control an Android TV over ADB.

Mitigation: Use a private local IP, authorize only trusted machines, and disable debugging or revoke authorization when remote playback control is no longer needed.

## Reference(s):

- [ADB Keycode Reference](references/adb-keycodes.md)
- [ClawHub Skill Page](https://clawhub.ai/jiayun/skills/androidtv-netflix)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires adb on macOS or Linux and an Android TV authorized for ADB control.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
