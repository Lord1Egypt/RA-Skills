## Description:

Organize messy folders by moving files into subfolders grouped by extension, date, or category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwzhjt](https://clawhub.ai/user/dwzhjt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preview and organize messy local folders, such as downloads or project directories, into subfolders by file type, extension, or modification month.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect and move files in folders the user provides, which may break shortcuts, scripts, configurations, or application references that depend on the old paths.

Mitigation: Run the organizer with --dry-run first, review the proposed move list carefully, and execute only after the user confirms the target folder and plan.

Risk: Extension-based grouping can put files with missing or misleading extensions into unexpected folders.

Mitigation: Prefer smaller batches for important directories and review the dry-run output for unusual destinations before moving files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dwzhjt/skills/file-organize-test)
- [Publisher Profile](https://clawhub.ai/user/dwzhjt)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text move summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill reports one planned or completed file move per line plus a summary line.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
