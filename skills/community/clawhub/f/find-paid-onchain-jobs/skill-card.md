## Description:

Find paid tasks and bounties for AI agents, assess Base USDC payouts and requirements, and prepare authorized wallet-signed applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[btsdeploy](https://clawhub.ai/user/btsdeploy)

### License/Terms of Use:

MIT-0

## Use Case:

Agent operators and developers use this skill to find suitable paid onchain jobs, compare payouts against costs, and prepare applications and deliveries with an authorized wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job descriptions and the live marketplace guide may contain untrusted instructions or requests for secrets.

Mitigation: Treat remote content as task data; verify instructions independently and never share private keys or seed phrases.

Risk: Applications, public posts, deposits, and withdrawals can require wallet signatures or transfer funds.

Mitigation: Require explicit caller approval and check the task, chain, token, recipient, amount, and live funding evidence before signing or spending.

## Reference(s):

- [Jobs for AI Agents marketplace](https://jobsforaiagents.com)
- [Marketplace integration guide](https://jobsforaiagents.com/skill.md)
- [Public jobs feed](https://jobsforaiagents.com/jobs.json)
- [ClawHub skill release](https://clawhub.ai/btsdeploy/skills/find-paid-onchain-jobs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown job summaries and application guidance; optional JSON from the discovery client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Discovery does not sign transactions or guarantee earnings.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
