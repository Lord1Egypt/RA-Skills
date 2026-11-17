## Description:

Query Apple Find My device and family-device locations through the pyicloud iCloud CLI, using a locally stored Apple ID username in a deterministic state file instead of hardcoding it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rolandkakonyi](https://clawhub.ai/user/rolandkakonyi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents with authorized Apple account access use this skill to retrieve current location, battery, and device details for their own Apple devices or family-shared devices through a CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Apple device and family-device location data, including precise coordinates.

Mitigation: Use only with Apple accounts and family devices the user is authorized to locate, and avoid exposing coordinates in logs or chat history.

Risk: The stored account.env username file is sourced as shell code, so tampering with that state file could execute commands.

Mitigation: Parse the state file as data instead of sourcing it, and restrict permissions on the state directory and files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rolandkakonyi/skills/findmy-icloud-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live device location fields such as latitude, longitude, timestamp, horizontal accuracy, battery level, and battery status.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
