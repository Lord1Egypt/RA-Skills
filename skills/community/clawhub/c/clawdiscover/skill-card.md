## Description:

ClawDiscover helps agents discover new AI tools and services, with optional premium summaries and webhook notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x4v13r1120](https://clawhub.ai/user/x4v13r1120)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to query ClawDiscover service listings, filter services by category, receive updates about newly listed tools, and optionally use premium x402 endpoints for AI summaries or webhook subscriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to contact ClawDiscover for service listings and may encourage recurring third-party communication.

Mitigation: Install only when this external service discovery behavior is desired, and keep heartbeat or cron checks disabled unless explicitly approved.

Risk: Webhook subscriptions and paid x402 endpoints can create recurring communication, payment, or exposure risk.

Mitigation: Use a non-sensitive agent ID, a hardened public webhook endpoint, and explicit opt-in before enabling paid endpoints or subscriptions.

## Reference(s):

- [ClawDiscover Website and API Docs](https://clawdiscover.com)
- [ClawDiscover ClawHub Skill Page](https://clawhub.ai/x4v13r1120/skills/clawdiscover)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with JavaScript, bash, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional recurring heartbeat checks, webhook subscription guidance, and paid x402 endpoint examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
