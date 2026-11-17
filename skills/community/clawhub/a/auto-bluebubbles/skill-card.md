## Description:

Send and manage iMessages via BlueBubbles self-hosted macOS server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and automation operators use this skill to send and manage iMessage conversations through a configured self-hosted BlueBubbles macOS server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sample configuration uses HTTP for a password-protected BlueBubbles server.

Mitigation: Use HTTPS or a trusted TLS reverse proxy before connecting the skill to the server.

Risk: A wildcard sender allowlist can expose messaging actions to overly broad sender access.

Mitigation: Avoid wildcard allowed_senders and restrict sender handles to trusted contacts.

Risk: Attachments sent through the skill may leave the local workspace and reach external recipients.

Mitigation: Review attachment paths and content before sending, and treat attachments as sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/auto-bluebubbles)
- [BlueBubbles](https://bluebubbles.app)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, Guidance, Text, Files]

**Output Format:** [Markdown with JSON examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces messaging tool-call guidance for text messages, attachments, reactions, edits, unsend actions, and iMessage effects.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
