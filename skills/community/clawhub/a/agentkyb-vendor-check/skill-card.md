## Description:

Helps agents review vendor risk before payment using an optional paid AgentKYB preflight check or a free local payment consistency guard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy229651](https://clawhub.ai/user/andy229651)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to request vendor preflight evidence before payment or to check payment details locally before signing. Paid verification requires separate authorization, a configured signer, and spending limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unapproved or altered payment challenge could send funds to the wrong recipient or exceed the intended price.

Mitigation: Require independent payment authorization and spend limits; verify the pinned recipient, endpoint, Base network, and 0.05 USDC price before each payment, and never provide wallet private keys to the skill or service.

Risk: A vendor preflight result could be mistaken for proof of vendor safety or regulatory clearance.

Mitigation: Treat results as decision support, stop automatic payments on review or block, and do not present an allow result as compliance approval.

## Reference(s):

- [AgentKYB service homepage](https://agentkyb.andy229651.workers.dev)
- [AgentKYB tool descriptions](https://agentkyb.andy229651.workers.dev/tools)
- [AgentKYB x402 service metadata](https://agentkyb.andy229651.workers.dev/.well-known/x402)
- [AgentKYB API specification](https://agentkyb.andy229651.workers.dev/openapi.json)
- [Payment Guard SDK source](https://github.com/Andy229651/agentkyb-agent-tools)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Vendor decision and supporting reasons when a paid check is executed; otherwise, clearly states that no verification was performed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
