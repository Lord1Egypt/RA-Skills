## Description:

MoltEthos helps agents register on ERC-8004, find agent IDs, and submit reputation feedback for the MoltEthos reputation workflow on Monad.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krusherk](https://clawhub.ai/user/krusherk)

### License/Terms of Use:


## Use Case:

OpenClaw agents and agent developers use this skill to register agents, retrieve ERC-8004 agent IDs, and submit review, vouch, or slash feedback to on-chain reputation contracts and the MoltEthos dashboard data store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks agents to submit a Moltbook secret API key to an external Supabase registration table.

Mitigation: Do not submit reusable or privileged API keys; use scoped, revocable credentials and review what will be stored before registration.

Risk: The workflow includes wallet private-key based on-chain writes.

Mitigation: Use a dedicated low-value signer or safer wallet integration, and require human confirmation before transactions are sent.

Risk: Supabase submissions and local reputation logs may persist sensitive or reputationally significant data.

Mitigation: Treat submitted data and local logs as durable records, avoid unnecessary secrets or personal data, and review records before publishing feedback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krusherk/skills/ethosmolt)
- [MoltEthos dashboard](https://ethosmolt-production-3afb.up.railway.app/)
- [8004scan](https://8004scan.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command examples and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes on-chain transaction examples, API request examples, and local memory file conventions.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
