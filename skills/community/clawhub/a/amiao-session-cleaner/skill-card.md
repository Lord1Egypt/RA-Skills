## Description:

Helps OpenClaw users review and clean obsolete session records, expired session files, and cluttered session lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macofee](https://clawhub.ai/user/macofee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to identify stale OpenClaw sessions, preserve active and main sessions, propose deletions, and clean session indexes and transcript files after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete OpenClaw session history and rewrite session indexes using broad cleanup rules.

Mitigation: Back up each affected sessions.json and related session files before cleanup, review the proposed deletion set, and avoid broad confirmations unless the deletion scope is clear.

Risk: Changing session indexes while OpenClaw Gateway is active can leave the UI or session state inconsistent.

Mitigation: Stop or quiesce the Gateway before modifying session indexes, then restart it after cleanup and verify the session list.

## Reference(s):

- [Session Cleaner README](README.md)
- [ClawHub skill page](https://clawhub.ai/macofee/skills/amiao-session-cleaner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before deletion; may modify sessions.json and remove session-related files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
