## Description:

Search the x402 bazaar for paid API services, browse marketplace resources, and inspect x402 payment requirements without making a payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find paid API services in the x402 bazaar, browse marketplace listings, and inspect endpoint payment requirements before selecting a service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned third-party npm CLI at invocation time.

Mitigation: Prefer a version pinned to a reviewed Agnic release before installation or operational use.

Risk: The details command can send requests to user-supplied URLs from the agent network environment.

Mitigation: Restrict use to explicit x402 marketplace inspection and confirm or limit arbitrary URL checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agnicpay-prog/skills/agnicpay-search-for-service)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return marketplace listings, service details, payment requirements, prices, accepted payment schemes, networks, and schemas.]

## Skill Version(s):

2.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
