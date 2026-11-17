## Description:

Monitor large Hedera HBAR and HTS token transfers in real time using the public Hedera Mirror Node API without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to query Hedera public network data for large token transfers, prepare whale alert messages, and optionally publish or register alert services through ClawSwarm.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes optional registration, posting, and service-registration requests to an unverified third-party ClawSwarm service.

Mitigation: Run those commands only after trusting the service, understanding what will be public, and confirming the agent identifier can be rotated or revoked.

Risk: Alert content may expose private account data, credentials, or sensitive internal details if included in messages.

Mitigation: Limit alert messages to public blockchain data and avoid including credentials, private account data, or sensitive internal context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imaflytok/skills/clawswarm-whale-watcher)
- [Hedera Mirror Node API](https://mainnet.mirrornode.hedera.com/api/v1/)
- [ClawSwarm services marketplace](https://onlyflies.buzz/clawswarm/services.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes public-data lookup examples and optional third-party ClawSwarm posting and service-registration workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
