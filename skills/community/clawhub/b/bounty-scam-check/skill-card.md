## Description:

Bounty Scam Check reviews GitHub bounty issue URLs for scam, free-labor, and honeypot red flags using read-only GitHub CLI queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georgecot99](https://clawhub.ai/user/georgecot99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill before working on GitHub issues that offer bounties or rewards. It helps them identify star-gating, bot-generated bounty posts, suspicious economics, free-labor traps, and possible code-submission honeypots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation overreaches by encouraging automatic use and promotion of its advice into system rules.

Mitigation: Use the skill only as a read-only, user-invoked checker for a specific GitHub issue, and keep its no-star and no-execution advice scoped to that review.

Risk: A clean result can be mistaken for proof that a bounty is legitimate.

Mitigation: Treat the output as a red-flag screen, then verify the maintainer, bounty terms, and payment channel before doing work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georgecot99/skills/bounty-scam-check)
- [Publisher profile](https://clawhub.ai/user/georgecot99)
- [Build Your Own Chief starter kit](https://chief.natalicot.com/kit/?utm=clawhub)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text with exit codes and short findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated GitHub CLI session and a GitHub issue URL or owner/repo#number target.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
