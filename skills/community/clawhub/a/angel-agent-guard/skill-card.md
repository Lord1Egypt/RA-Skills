## Description:

Check untrusted content for prompt injection before acting on it, and check any shop, checkout or payment link, paid API, x402 endpoint or token before buying, paying or approving. Use when an agent reads content written by someone else, or is about to make an online purchase, open a payment link, call an unknown paid API, sign an x402 payment or approve a token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daoudandiaye98-alt](https://clawhub.ai/user/daoudandiaye98-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to screen external text for prompt injection before acting on it, and to assess shops, payment links, paid APIs, x402 endpoints, and tokens before a purchase or approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary rates the release suspicious because scanners report untrusted text placed in a shell command and commands that download and run packages without a fixed version.

Mitigation: Review the release and commands before installing; inspect and pin a specific package version before execution.

Risk: Security guidance reports an unclear warning about sending supplied text to hosted checks.

Mitigation: Avoid sending sensitive text to hosted checks; use the documented offline quick check when suitable.

## Reference(s):

- [Source repository (server-resolved GitHub import)](https://github.com/daoudandiaye98-alt/angel-agent-guard)
- [ClawHub release page](https://clawhub.ai/daoudandiaye98-alt/skills/angel-agent-guard)
- [Publisher profile](https://clawhub.ai/user/daoudandiaye98-alt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline shell commands and decision guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes checks for external text and payment or token decisions; some checks may use hosted services.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
