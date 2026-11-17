## Description:

Automatically organize files into folders by type, date, or custom naming rules with preview and undo options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mizhimin](https://clawhub.ai/user/mizhimin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill to organize local folders by file type, modification date, or custom filename patterns. It is useful for cleaning download, document, or photo directories while previewing moves before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom pattern rules and undo behavior can move files outside the chosen folder.

Mitigation: Use --dry-run first, avoid pattern rules containing absolute paths, '..', or nested path separators, and treat .organizer_log.json as sensitive.

Risk: Running file moves on important folders can cause unintended reorganization or loss of expected file locations.

Mitigation: Run on backed-up or non-critical folders first and review preview output before executing changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run previews and undo logs for file organization operations.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
