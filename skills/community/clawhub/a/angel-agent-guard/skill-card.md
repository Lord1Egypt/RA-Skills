## Description:

Check untrusted content for prompt injection before acting on it, and check any shop, checkout or payment link, paid API, x402 endpoint or token before buying, paying or approving. Use when an agent reads content written by someone else, or is about to make an online purchase, open a payment link, call an unknown paid API, sign an x402 payment or approve a token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daoudandiaye98-alt](https://clawhub.ai/user/daoudandiaye98-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Agent developers and operators use this skill to screen external text before relying on it and to check shops, payment links, paid APIs, x402 requests, and tokens before an agent spends or approves funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted external text can contain instructions intended to steer the agent.

Mitigation: Scan external text before using it, treat it as data, and follow the returned action; drop hostile content or keep the step read-only when directed.

Risk: Package installation commands may run unpinned code.

Mitigation: Confirm the package identity and pin a trusted version before invoking it.

Risk: Hosted checks raise privacy concerns for submitted content.

Mitigation: Use the documented offline quick check for sensitive content and avoid sending it to hosted checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daoudandiaye98-alt/skills/angel-agent-guard)
- [Project homepage (metadata link)](https://github.com/daoudandiaye98-alt/angel-agent-guard)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions with shell commands and JSON check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns verdicts and risk signals with suggested next actions.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
