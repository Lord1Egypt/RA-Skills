## Description:

Conventional Commits v1.0.0 branch naming, worktree naming, and commit message standards for GitHub and GitLab projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external contributors use this skill to name branches and worktrees, write Conventional Commit messages, and prepare GitHub or GitLab commits that support changelog automation and issue closing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad GitHub CLI authority that is not clearly used or scoped.

Mitigation: Review requested permissions before installation and narrow or remove Bash(gh:*) unless authenticated GitHub CLI operations are intentionally needed.

Risk: The skill may guide branch names, commit messages, issue-closing footers, and squash-merge titles that affect repository history and automation.

Mitigation: Review generated names and commit text before applying them, especially release-affecting Conventional Commit markers and issue-closing references.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/conventional-git)
- [Publisher profile](https://clawhub.ai/user/samber)
- [Project homepage](https://github.com/samber/cc-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose with inline commit-message examples and bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git for command examples; GitHub CLI permissions should be reviewed before installation.]

## Skill Version(s):

1.3.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
