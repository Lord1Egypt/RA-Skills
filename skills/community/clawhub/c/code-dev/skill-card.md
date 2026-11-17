## Description:

Provides a structured Git development workflow for branch management, repository analysis, implementation, code review, and pull request creation while preventing direct pushes to main.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luciuscao](https://clawhub.ai/user/luciuscao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to manage larger feature and bug-fix work through a develop-branch workflow, including codebase review, implementation, tests, automated review, branch push, and pull request creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can modify repository files, create branches, push to GitHub, and open pull requests when used with git, gh, and GitHub authentication.

Mitigation: Run it only in the intended project repository, review generated changes before pushing, and use a GitHub token with the minimum permissions needed for PR creation.

Risk: The workflow assumes a develop-branch PR model, which may not match every repository.

Mitigation: Confirm that the repository uses develop as the integration branch before applying the workflow or adapt the branch target during review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luciuscao/skills/code-dev)
- [Source Repository](https://github.com/LuciusCao/openclaw-skills/tree/main/code-dev)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell, JavaScript, and pull request template blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose branch names, git and GitHub CLI commands, review prompts, and PR body content.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
