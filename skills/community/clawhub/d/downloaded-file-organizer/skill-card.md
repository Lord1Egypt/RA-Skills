## Description:

Organize files from the Downloads folder into appropriate local directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuxinyuan2019](https://clawhub.ai/user/xuxinyuan2019)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to scan a Downloads folder, present a dry-run move plan, ask for confirmation, and then organize files into local target directories. It also supports configurable rules, logs, an index, and optional watch mode for newly arriving files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move files based on plan paths, and edited or untrusted plan JSON may send files to unintended locations.

Mitigation: Use narrow Downloads and target directories, review the dry-run plan before confirming, avoid passing edited or untrusted plan JSON to --execute, and add path containment checks before relying on automation.

Risk: The skill stores a persistent index of the target directory tree, which may expose local filenames beyond the immediate Downloads cleanup task.

Mitigation: Keep the target directory narrow, review the generated index location, and make indexing explicitly opt-in or narrower before broad use.

Risk: Watch mode automatically organizes new files as they arrive.

Mitigation: Enable watch mode only for controlled folders when automatic moves are intended, and stop it when unattended automation is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuxinyuan2019/skills/downloaded-file-organizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, dry-run tables, and JSON scan or execution payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script can move local files, write logs, update an index, and optionally watch for new downloads.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
