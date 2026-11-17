## Description:

Say 'lint my docs' to scan your markdown KB for broken links, orphan pages, and missing metadata, then auto-fix them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[singggggyee](https://clawhub.ai/user/singggggyee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to scan Markdown knowledge bases, docs, wikis, notes, and Claude Code memory files for broken links, orphan pages, missing frontmatter, thin articles, filename issues, and inconsistent metadata. The skill can summarize issues, propose fixes, and help apply reviewed changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs or runs the external `kb-lint` CLI without a pinned package version.

Mitigation: Review and pin the package source or version before installation in managed environments.

Risk: Memory mode can inspect files under `~/.claude/`, which may contain sensitive user or project context.

Mitigation: Use memory mode only after reviewing the target files and limiting the scan scope to intended paths.

Risk: Auto-fix behavior may rename files, edit frontmatter, or rewrite references.

Mitigation: Require a preview or diff and explicit user confirmation before applying file changes.

## Reference(s):

- [kb-lint GitHub repository](https://github.com/SingggggYee/kb-lint)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell commands, issue summaries, and proposed file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include before/after lint scores, proposed renames, frontmatter edits, and reference rewrites.]

## Skill Version(s):

4.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
