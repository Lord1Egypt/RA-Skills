## Description:

Use shell commands to view and manage Evite events, guest lists, RSVPs, and messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Evite users can use shell commands to review events and guest responses, manage invitations, update RSVPs, and communicate with guests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious because scanners report undisclosed template discovery and photo-gallery publishing, and analysis of the referenced material was incomplete.

Mitigation: Review whether these capabilities are needed and acceptable before installing or using the skill; do not proceed if the behavior or incomplete analysis is not acceptable.

Risk: The skill uses Evite credentials and a session cookie jar, and its write operations can change RSVPs or events, send messages or invitations, email guest groups, and upload photos.

Mitigation: Review each write and its recipients before running it, protect the cookie jar, and test sending behavior only with a throwaway event and blackholed example.com guests.

## Reference(s):

- [Evite endpoint reference](artifact/references/endpoints.md)
- [Evite](https://www.evite.com/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read account data and perform changes or send communications through Evite.]

## Skill Version(s):

1.5.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
