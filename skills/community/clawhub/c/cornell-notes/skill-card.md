## Description:

Manage Cornell Method notes as Markdown files using the bundled cornell.py CLI script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, and other note takers use this skill to create, list, view, search, edit, and delete Cornell-style Markdown notes with a local CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guidance includes an optional predictable /tmp/cornell.py workflow, which can add local code-execution risk.

Mitigation: Run the bundled scripts/cornell.py directly from the skill directory and avoid copying or executing the script from /tmp.

Risk: The CLI can launch an editor selected from $EDITOR or $VISUAL.

Mitigation: Set $EDITOR or $VISUAL to a trusted local editor before using create or edit commands.

Risk: Notes are stored persistently under ~/cornell-notes.

Mitigation: Use the skill only when local persistent storage of note content is acceptable, and review stored notes before sharing or deleting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/cornell-notes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown files and terminal text, with shell commands for CLI operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists notes under ~/cornell-notes and may launch the user's configured local editor.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
