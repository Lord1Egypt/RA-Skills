## Description:

Removes dates, hashes, UUIDs, and extra symbols from filenames to create clean, readable file names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill to preview and apply cleaner filenames by removing common clutter such as date stamps, hashes, UUIDs, and repeated separators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apply mode can rename files in place without collision checks, which may overwrite or lose expected filenames.

Mitigation: Use preview mode first, avoid running apply mode on important folders without backups, and add collision detection that refuses existing destination names by default.

## Reference(s):

- [Fileclean ClawHub release page](https://clawhub.ai/albionaiinc-del/skills/fileclean)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text rename previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview mode lists planned filename changes; apply mode renames files on disk.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
