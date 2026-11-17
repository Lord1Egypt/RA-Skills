## Description:

Controls ClashX through Peekaboo to test proxy latency and switch to the lowest-latency US node using menu bar automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shifengwang333-ai](https://clawhub.ai/user/shifengwang333-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate ClashX proxy node testing and select a US node with the lowest observed latency on a macOS menu bar setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full-screen screenshots saved to predictable temporary paths may capture unrelated private windows or notifications.

Mitigation: Hide unrelated windows and notifications before use, prefer capturing only the ClashX menu into a private temporary directory, and delete screenshots immediately.

Risk: Coordinate-based menu automation can select the wrong item when the display resolution, menu position, or ClashX state differs from the documented setup.

Mitigation: Confirm the ClashX menu position and visible node list before clicking, and adjust coordinates for the active display layout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shifengwang333-ai/skills/clashx-node-switcher)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates and node choices depend on the user's ClashX menu state and display layout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
