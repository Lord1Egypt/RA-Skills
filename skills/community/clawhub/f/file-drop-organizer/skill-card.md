## Description:

File Drop Organizer helps review a downloads or temporary-materials directory, then drafts categories, naming suggestions, duplicate-risk notes, and a move plan before any action is taken.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to audit local downloads or temporary work folders and produce a reviewable organization plan before moving, renaming, or deleting anything.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Directory audits may include local directory names and Markdown headings in generated reports.

Mitigation: Review the input path before running the skill and avoid including sensitive folders unless the report destination is appropriate.

Risk: A proposed move or naming plan could be wrong when the input directory context is incomplete.

Mitigation: Use the default dry-run review workflow and manually confirm the plan before moving, renaming, or deleting files.

Risk: Using --output can create or overwrite a report file.

Mitigation: Set --output only to a report path that is intended for creation or replacement.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/file-drop-organizer)
- [Publisher Profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown report or JSON from a local dry-run directory audit]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; designed for read-only review workflows and manual confirmation before file changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
