## Description:

Automate and control Flashforge Adventurer 5M 3D printers for status checks, print jobs, temperature monitoring, homing, file management, slicing, and camera snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickbmerrill-collab](https://clawhub.ai/user/nickbmerrill-collab)

### License/Terms of Use:


## Use Case:

Developers, makers, and printer operators use this skill to automate Flashforge Adventurer 5M workflows, including checking printer status, slicing models, starting or stopping jobs, managing files, and capturing camera snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a real-looking printer check code and specific device network details.

Mitigation: Rotate the exposed check code if it belongs to an actual device and replace device identity, IP address, and credential values with local configuration or secrets before use.

Risk: Printer control commands can start, pause, stop, or otherwise affect a physical 3D printer.

Mitigation: Require explicit user confirmation before start, pause, stop, homing, slicing-and-printing, or similar high-impact operations.

Risk: Printer camera and control ports may expose operational or visual data if reachable by untrusted hosts.

Mitigation: Restrict camera and control ports to trusted hosts and networks before enabling camera snapshots or printer control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickbmerrill-collab/skills/3dprint)
- [Publisher profile](https://clawhub.ai/user/nickbmerrill-collab)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and printer configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include G-code commands, printer endpoint examples, material settings, and operational guidance.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
