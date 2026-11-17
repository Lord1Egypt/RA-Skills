## Description:

Controls Apple's Find My app through local Peekaboo UI automation to locate people, devices, and items, capture location screenshots, and play sounds on AirTags without third-party APIs or credential sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loganprit](https://clawhub.ai/user/loganprit)

### License/Terms of Use:

MIT

## Use Case:

Mac users and agent developers use this skill to automate Apple's Find My app for locating people, devices, or AirTags and producing local screenshots or shell-command guidance for the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive Find My location data and local screenshots of people, devices, and items.

Mitigation: Install only when comfortable granting Screen Recording and Accessibility permissions, set FM_OUTPUT_DIR to a private directory, and delete screenshots after use.

Risk: Coordinate-based UI automation and broad clicks can select the wrong Find My item or trigger an unintended action.

Mitigation: Verify the selected tab and item before playing sounds or opening actions, and avoid arbitrary coordinate clicks.

Risk: The skill requires active control of the Mac UI while it runs.

Mitigation: Keep Find My visible and avoid interacting with the computer during automation to prevent click conflicts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loganprit/skills/apple-find-my-local)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands and local screenshot file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local PNG screenshots under FM_OUTPUT_DIR or /tmp.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
