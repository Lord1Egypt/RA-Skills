## Description:

Manage ebook collections, track reading progress, and export highlights using bash and Python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ebook readers use this skill to maintain a local command-line ebook library, log reading sessions, capture highlights and reviews, view progress, and export library data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reading history, highlights, reviews, and notes in a local data file.

Mitigation: Review the contents of ~/.ebook/data.jsonl before sharing or backing up the file, and remove sensitive entries when they are no longer needed.

Risk: The delete command removes a book and related sessions, highlights, and reviews.

Mitigation: Confirm the target book ID and keep a backup of ~/.ebook/data.jsonl before deleting records.

Risk: The export command can overwrite the output path supplied by the user.

Mitigation: Use a new or disposable output path for exports, especially when writing JSON, CSV, or Markdown files.

## Reference(s):

- [Ebook ClawHub Skill](https://clawhub.ai/ckchzh/skills/ebook)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files]

**Output Format:** [Terminal text, JSON objects, formatted tables, and exported JSON, CSV, or Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores ebook records, sessions, highlights, and reviews locally in ~/.ebook/data.jsonl.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter and script report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
