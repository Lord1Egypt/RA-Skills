## Description:

Validate .editorconfig syntax and check source files for EditorConfig compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate .editorconfig files, inspect effective EditorConfig settings, check source trees for formatting compliance, and optionally apply basic whitespace, newline, line-ending, and BOM fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fix mode can rewrite many files in a workspace.

Mitigation: Use validate, check, or show for routine review; run fix only on a clean, version-controlled checkout and limit it to narrow paths.

Risk: Unsafe file-handling issues may matter on untrusted repositories, especially when symlinks are present.

Mitigation: Avoid running this skill on untrusted repositories that may contain symlinks, and exclude sensitive or untracked files before running write-capable commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/editorconfig-linter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; the bundled CLI can emit text, JSON, or Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fix mode can modify workspace files; validate, check, and show modes are read-oriented.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
