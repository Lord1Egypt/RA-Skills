## Description:

Provides guidance for using the GitHub CLI (`gh`) to manage GitHub issues, pull requests, workflow runs, and API queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuangyinbot-boop](https://clawhub.ai/user/chuangyinbot-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare or run GitHub CLI workflows for pull requests, issues, CI runs, repository queries, and structured `gh api` calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub CLI commands can create, merge, close, comment, rerun CI, or call the GitHub API using the user's account permissions.

Mitigation: Review repository-changing commands before execution and confirm the intended repository, account, and permission scope.

Risk: The skill depends on a configured `gh` CLI session.

Mitigation: Install the GitHub CLI through the listed package-manager option and verify authentication with `gh auth status` before use.

Risk: Repeated or broad GitHub API queries can hit rate limits or return more repository data than needed.

Mitigation: Use targeted fields and filters, and apply `gh api --cache` for repeated read-only queries when appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chuangyinbot-boop/skills/cool-github-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and GitHub CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that use the active GitHub CLI authentication session and repository permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
