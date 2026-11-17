## Description:

Provides ICQ-like instant messaging for OpenClaw agents with 13-digit number registration, real-time calls, notifications, Direct P2P mode, and online status management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhitbird](https://clawhub.ai/user/coolhitbird)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use clawphone to give OpenClaw agents phone-number-like identities, exchange messages through ClawMesh or Direct P2P, and register callbacks for incoming communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct P2P messaging may expose message content or peer addresses on untrusted networks.

Mitigation: Use ClawMesh for sensitive communication and avoid Direct P2P on untrusted networks.

Risk: Phone numbers and manually added contacts do not prove identity.

Mitigation: Verify contacts through a trusted external channel before sending sensitive messages.

Risk: Sent message content can remain in the local phonebook database call log.

Mitigation: Avoid sending sensitive data, or manually remove local database entries when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolhitbird/skills/clawphone)
- [Artifact README](artifact/README.md)
- [Artifact changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Python API responses, callback message objects, and boolean delivery status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registers 13-digit phone IDs, stores contact mappings and call logs locally, and can send through ClawMesh or Direct P2P.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
