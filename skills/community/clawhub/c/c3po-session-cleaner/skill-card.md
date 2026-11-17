## Description:

Clean up old OpenClaw session files and keep only active sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccc-3po](https://clawhub.ai/user/ccc-3po)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can invoke this skill to remove .jsonl session files older than three days from the main agent sessions directory and report the remaining session count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill permanently deletes local session files without preview or confirmation.

Mitigation: Review the files matched for deletion before execution, require explicit confirmation, and consider archiving or quarantining files before permanent removal.

Risk: Unsafe path handling could delete files from an unintended location if the target sessions directory is missing or the directory change fails.

Mitigation: Check that changing into the intended sessions directory succeeds before running deletion commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccc-3po/skills/c3po-session-cleaner)

## Skill Output:

**Output Type(s):** [shell commands, text]

**Output Format:** [Markdown with an inline bash command block and brief status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deletes matching local .jsonl session files older than three days.]

## Skill Version(s):

1.0.5 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
