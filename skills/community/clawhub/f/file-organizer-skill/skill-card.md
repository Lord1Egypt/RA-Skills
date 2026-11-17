## Description:

Organize files in directories by grouping them into folders based on their extensions or date. Includes Dry-Run, Recursive, and Undo capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1999azzar](https://clawhub.ai/user/1999azzar)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to organize a chosen local directory by file extension or modification date, preview file moves, run recursive organization, and undo prior organization runs from a history file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local organizer script moves files in the selected directory, and recursive mode can affect nested files.

Mitigation: Run dry-run first, target only directories you explicitly choose, and avoid recursive mode on broad or sensitive folders.

Risk: Undo mode can move arbitrary files when supplied with an untrusted history JSON file.

Mitigation: Use --undo only with an organize_history.json file that you created and inspected.

## Reference(s):

- [File Categories Reference](references/categories.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python script guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local file-move guidance and command examples; the bundled script can write organize_history.json for audit and undo.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
