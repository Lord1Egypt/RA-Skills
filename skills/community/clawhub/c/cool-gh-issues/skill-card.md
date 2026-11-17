## Description:

Fetch GitHub issues, spawn sub-agents to implement fixes and open PRs, then monitor and address PR review comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuangyinbot-boop](https://clawhub.ai/user/chuangyinbot-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to triage GitHub issues, delegate selected fixes to sub-agents, open pull requests, and respond to actionable pull request review comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make real changes to GitHub repositories and lets issue or review text influence privileged agents.

Mitigation: Use only with trusted repositories, review selected issues before processing, and avoid unattended --yes, --watch, or --cron modes on untrusted issue trackers.

Risk: The security evidence reports unsafe token handling, including token printing and token-bearing git remote configuration.

Mitigation: Use a narrowly scoped, revocable GitHub token and do not run until token printing, token-bearing git remotes, and global git credential configuration changes are removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chuangyinbot-boop/skills/cool-gh-issues)
- [Publisher profile](https://clawhub.ai/user/chuangyinbot-boop)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown status tables, command-oriented task prompts, pull request summaries, and review response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open or update pull requests, push git branches, call GitHub APIs, and send optional Telegram notifications when configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
