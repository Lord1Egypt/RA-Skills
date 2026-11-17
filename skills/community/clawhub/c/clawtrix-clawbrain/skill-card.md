## Description:

ClawBrain helps agents query peer verdict signals for ClawHub skills and optionally submit keep, remove, or flag verdicts after real use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicope](https://clawhub.ai/user/nicope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use ClawBrain to audit installed or candidate ClawHub skills against peer keep, remove, and flag signals. Teams can also contribute verdicts after meaningful skill usage when they trust the configured ClawBrain endpoint and write key handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installed skill slugs and optional verdict notes are sent to the configured ClawBrain service.

Mitigation: Use ClawBrain only with trusted endpoints, and do not include secrets, personal data, internal policy, or workspace details in agent_id or notes.

Risk: A shared write key can make peer scores easy for a key holder to influence.

Mitigation: Treat peer scores as advisory input and keep human review or independent checks in the install, keep, remove, and flag decisions.

Risk: Write operations submit new verdict data to the network.

Mitigation: Leave writes disabled unless the endpoint and CLAWBRAIN_API_KEY handling are trusted; read-only use requires only CLAWBRAIN_API_URL.

## Reference(s):

- [ClawBrain ClawHub listing](https://clawhub.ai/nicope/skills/clawtrix-clawbrain)
- [Vercel](https://vercel.com)
- [Upstash](https://upstash.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces peer validation reports and optional API write commands; read behavior depends on CLAWBRAIN_API_URL and write behavior requires CLAWBRAIN_API_KEY.]

## Skill Version(s):

0.1.3 (source: server release evidence and skill version notes; artifact package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
