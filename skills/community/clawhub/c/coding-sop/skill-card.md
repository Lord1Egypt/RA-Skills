## Description:

Coding SOP guides an agent through a seven-stage software development workflow for requirements review, branch creation, design, review, implementation, testing, and Git commit and push steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckystarry](https://clawhub.ai/user/luckystarry)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill to follow a structured SOP for feature work, bug fixes, and refactoring. It helps plan changes, review designs, run tests, maintain project SOP documentation, and manage Git branch, commit, and push steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may stage all repository changes and push them to a remote repository, which can expose unrelated local files or secrets.

Mitigation: Require review of git status, the full staged diff, and the exact file list before any commit or push; keep secrets and unrelated local changes outside the repository.

Risk: Pushes and merges can alter shared branches or publish incomplete work.

Mitigation: Require explicit approval for each push or merge, and confirm the target branch and test/build status before running Git commands.

## Reference(s):

- [Server-resolved GitHub repository](https://github.com/LuckyStarry/coding-sop)
- [ClawHub skill page](https://clawhub.ai/luckystarry/skills/coding-sop)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and structured reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SOP documents under .sop/ and Git commands for branch, commit, merge, and push workflows.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
