## Description:

Detects spelling issues in documentation files and can apply common typo fixes for Markdown, plain text, MDX, and reStructuredText files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT

## Use Case:

Developers and documentation maintainers use this skill to check project documentation for spelling errors, preview changes, and apply common typo corrections before commits or CI checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the bundled script can automatically install aspell with Homebrew or sudo apt-get without an explicit opt-in.

Mitigation: Pre-install aspell through an approved package-management process and avoid running the script with passwordless sudo or elevated privileges.

Risk: Fix mode edits documentation files in place and temporary-file handling is not documented as hardened.

Mitigation: Use dry-run or check mode first, run fix mode only on trusted directories, and review version-control diffs before committing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linux2010/skills/doc-spellcheck)
- [Publisher profile](https://clawhub.ai/user/linux2010)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report spelling findings, file counts, dry-run diffs, and applied typo fixes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
