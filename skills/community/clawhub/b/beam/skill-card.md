## Description:

Beam helps agents coordinate verified bucket transfers and fan-out across supported storage providers, and use Rooms to exchange messages, streams, and files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beam-network](https://clawhub.ai/user/beam-network)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Beam to copy large objects between supported storage services, deliver one object to multiple destinations, and coordinate agents through Rooms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transfers can incur charges or overwrite destination objects without an enforced approval gate.

Mitigation: Review the source, all destinations, overwrite risk, and estimated credits; obtain user approval before starting a transfer.

Risk: The agent can use Beam and storage credentials to move remote data or cancel transfers.

Mitigation: Use least-privilege, bucket-scoped and revocable credentials; monitor activity and revoke access after use.

## Reference(s):

- [Beam skill on ClawHub](https://clawhub.ai/beam-network/skills/beam)
- [Beam documentation](https://docs.b1m.ai)
- [Choosing a Beam workflow](artifact/references/choosing.md)
- [Beam transfer reference](artifact/references/transfers.md)
- [Beam Rooms reference](artifact/references/rooms.md)
- [Beam Studio transfer reference](artifact/references/studio.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance and shell commands; transfer and Room status as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transfer IDs and status can be reported to the user.]

## Skill Version(s):

0.2.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
