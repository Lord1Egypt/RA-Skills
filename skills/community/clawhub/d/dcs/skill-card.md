## Description:

Dcs is presented as a distributed control system manager, but server security review characterizes it as a local note and configuration data manager.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this third-party skill to run shell commands for recording, listing, searching, exporting, and configuring local DCS-labeled entries. It should be reviewed carefully before operational use because server security evidence says the implementation does not match the industrial control claim.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence says the skill is presented as an industrial distributed control system manager but behaves as a persistent local data tracker.

Mitigation: Validate the actual behavior in a controlled environment and do not rely on it for industrial control decisions.

Risk: Server security evidence reports a command-execution risk in the config command.

Mitigation: Avoid the config command with untrusted keys or values until configuration serialization and command construction are fixed.

Risk: Server guidance warns against using config and CSV export features until serialization is made safe.

Mitigation: Review generated configuration and exported files before reuse, and avoid exporting untrusted or sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/dcs)
- [Publisher profile](https://clawhub.ai/user/bytesagain3)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Structured stdout text and local JSONL or export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local data under ~/.dcs by default unless DCS_DIR is set.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
