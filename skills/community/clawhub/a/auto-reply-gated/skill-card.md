## Description:

Create a clean human-approved Instagram DM reply skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to draft Instagram DM replies that require explicit human approval before export for manual sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft recipient and message text are stored locally in JSON files.

Mitigation: Use the skill only with message contents suitable for local storage and remove draft files when they are no longer needed.

Risk: Approving or exporting an unrelated draft file could expose or prepare the wrong message payload.

Mitigation: Review the exact recipient and message before approval and pass only the intended draft file to approve or export commands.

Risk: Incoming DM text may contain prompt injection or unsafe instructions.

Mitigation: Treat incoming messages as untrusted input and screen them before creating a reply draft.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/auto-reply-gated)
- [Publisher profile](https://clawhub.ai/user/mupengi-bot)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON draft or export payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft files store recipient and message text locally and require explicit human approval before export.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
