## Description:

Exports Git and SVN commit history for selected authors, time ranges, revision ranges, and project paths to Markdown, CSV, JSON, or detailed reports with changed files and commit messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wallaceliang](https://clawhub.ai/user/wallaceliang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to retrieve, filter, and export Git or SVN commit records for audits, contribution reviews, release notes, and project history analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SVN passwords may be exposed when supplied directly on the command line.

Mitigation: Use SVN credential cache or an interactive/protected secret flow instead of passing passwords as command arguments.

Risk: Exported reports may contain sensitive repository history, including names, emails, commit messages, file paths, and repository URLs.

Mitigation: Treat generated reports as sensitive artifacts and apply appropriate storage, sharing, and retention controls.

Risk: The shipped shell scripts use unsafe command construction and need review before installation.

Mitigation: Review and preferably fix the scripts before deployment; run them only with trusted inputs and in intended repositories.

## Reference(s):

- [Git commit command reference](references/git_commands.md)
- [SVN commit command reference](references/svn_commands.md)
- [SVN working copy database query guide](references/svn_database_query.md)
- [ClawHub skill page](https://clawhub.ai/wallaceliang/skills/commit-history-exporter)
- [SlikSVN download](https://sliksvn.com/download/)
- [VisualSVN downloads](https://www.visualsvn.com/downloads/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, CSV, JSON, detailed text reports, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report content may include author names, email addresses, commit messages, changed file paths, repository paths, and repository URLs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
