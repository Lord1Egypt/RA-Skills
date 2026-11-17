## Description:

Helps developers implement, extend, or repair archived-session browsing, search, restore, resume, and cleanup behavior in OpenClaw Control UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers working on OpenClaw use this skill to diagnose and fix archived-session UX across the Control UI, gateway handlers, transcript storage, session history database, and live session store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Archived-session work may touch transcripts, session_history, sessions.json, or deleteArchived paths.

Mitigation: Review those changes before applying them, especially before deleting archived transcripts or running one-off reconciliation.

## Reference(s):

- [Archived Session Management on ClawHub](https://clawhub.ai/maverick-software/skills/archived-session-management)
- [Implementation Map](artifact/references/implementation-map.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with file references, implementation steps, and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
