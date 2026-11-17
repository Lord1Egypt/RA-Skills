## Description:

Batch rename local files by adding prefixes, suffixes, text replacements, or numbered prefixes, with dry-run preview support before changes are applied.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and operators use this skill to organize batches of local screenshots, photos, documents, and project files by generating or running concise rename commands with preview-first behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The renaming script can change filenames in a selected local folder and does not prevent name collisions.

Mitigation: Run with --dry-run first, use it only on intentionally selected folders, and keep a backup before renaming important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-file-batch-rename)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview-first local file rename guidance; users can apply changes after reviewing the proposed rename plan.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
