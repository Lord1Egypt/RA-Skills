## Description:

Use when a Codex thread or local session is slow because prior turns contain heavy image, screenshot, or base64 payloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vyctorbrzezowski](https://clawhub.ai/user/vyctorbrzezowski)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Codex users use this skill to identify an oversized local Codex session, dry-run removal of embedded image or base64 payloads, create a backup, and validate the cleaned JSONL file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite sensitive Codex session history.

Mitigation: Only run it on an explicitly selected session, review the dry-run output before using --write, and keep the backup.

Risk: This version may remove some non-image data from selected session records when arrays named images contain an image string.

Mitigation: Inspect dry-run statistics and retain the backup so the original session can be restored if important data was removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vyctorbrzezowski/skills/codex-session-image-scrubber)
- [Server-resolved source repository](https://github.com/vyctorbrzezowski/skills)
- [Server-resolved source path at commit](https://github.com/vyctorbrzezowski/skills/tree/77599bd9e42c26fdb415595865e09c5136d59a72/skills/codex/codex-session-image-scrubber)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON scrubber statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run is the default; write mode rewrites the selected session JSONL and creates a backup.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
