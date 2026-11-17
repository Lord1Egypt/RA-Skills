## Description:

Multi-platform bounty automation system for GitHub, Opire, Algora, and OpenTask that scans, filters, claims, and submits pull requests for bounty tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkcash](https://clawhub.ai/user/mkcash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate scanning, filtering, claiming, implementation, and pull request submission for bounty tasks across GitHub, Opire, Algora, and OpenTask.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled jobs can repeatedly act with user credentials.

Mitigation: Install only when unattended bounty automation is intended, review the cron entries before enabling them, and avoid overwriting existing cron configuration.

Risk: Automation may bid, modify repositories, push code, create comments, and open pull requests with real account side effects.

Mitigation: Require manual approval before any bid, commit, push, comment, or pull request creation, and use narrowly scoped protected tokens.

Risk: Default QQ delivery and fixed payment or branding text may send output to the wrong recipient or publish incorrect payment details.

Mitigation: Remove the hard-coded QQ default and replace fixed payment or branding text before use.

## Reference(s):

- [Deployment Guide](references/DEPLOY_GUIDE.md)
- [ClawHub Skill Page](https://clawhub.ai/mkcash/skills/bounty-automation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, JSON configuration snippets, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce account-affecting automation instructions for scheduled scans, bids, repository changes, commits, pushes, comments, and pull requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
