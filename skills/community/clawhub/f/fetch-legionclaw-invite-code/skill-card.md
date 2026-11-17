## Description:

Fetches Tongfudun LegionClaw usage-permission invite codes by deriving userId from a LegionClaw session handle, calling the invite-code API, and returning one or more codes in chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legionspace-hackathon](https://clawhub.ai/user/legionspace-hackathon)

### License/Terms of Use:

MIT-0

## Use Case:

LegionClaw-hosted agents use this skill when a user asks for Tongfudun LegionClaw invite codes, including single or multiple codes. It uses host session context to derive the agent identifier, requests invite codes, and returns copyable Markdown responses with friendly failure handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses LegionClaw runtime or session identity to request and disclose permission invite codes without a clear user-side authorization boundary.

Mitigation: Install only for trusted LegionClaw-hosted agents, confirm the backend enforces claim authorization and issuance limits, and review generated codes before broad deployment.

Risk: Invite codes are returned directly in chat by default.

Mitigation: Use the skill only in conversations where the recipient is authorized to receive the codes, and avoid logging or forwarding chat transcripts that contain active codes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/legionspace-hackathon/skills/fetch-legionclaw-invite-code)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with optional shell command execution and JSON response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns invite codes inline by default; file output is only used when explicitly requested by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
