## Description:

Organize the Downloads folder into a clean, searchable command center by file type, project, date, and action state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan and preview organization of a Downloads folder by file type, project, date, and action state before optionally moving files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional apply mode can move local files and has insufficient path and overwrite safeguards.

Mitigation: Use preview output first, avoid broad or sensitive directories, check destination collisions and unexpected paths, and run apply mode only after explicit user confirmation.

Risk: Untrusted rules files could produce unexpected organization targets.

Mitigation: Use only trusted rules files and inspect the generated move plan before any file operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/downloads-command-center)
- [README](artifact/README.md)
- [Helper script](artifact/scripts/organize_downloads.py)
- [Sample rules](artifact/resources/rules.sample.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON preview output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview-first workflow; apply mode can move files only after explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.1.0 and artifact CHANGELOG says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
