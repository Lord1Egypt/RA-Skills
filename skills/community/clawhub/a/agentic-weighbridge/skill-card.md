## Description:

Use when an agent is about to pay an unfamiliar x402 endpoint. Read-only weighing of the live endpoint (402 challenge, v2 shape, accepts[], discovery manifest, openapi) with a verdict per check, plus how to obtain a signed, offline-verifiable verdict document from the hosted weighbridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[33ai-wq](https://clawhub.ai/user/33ai-wq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect an unfamiliar x402 endpoint before deciding whether to pay, and to obtain and check a hosted verdict document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that endpoint checks may follow redirects to unintended destinations.

Mitigation: Follow the security guidance and avoid installation or use until the redirect-handling concern is addressed; review destination behavior before relying on results.

Risk: An offline signature check does not establish who issued the verdict.

Mitigation: Authenticate the signing key through a trusted channel and treat the signature as evidence of payload integrity and service production, not issuer identity.

Risk: The hosted-verdict workflow sends the target URL to a third-party service.

Mitigation: Use the hosted workflow only when the target URL is appropriate to share with that service.

Risk: The security scan was partial because two local references could not be resolved.

Mitigation: Treat the scan evidence as incomplete and review the skill before installation.

## Reference(s):

- [Agentic Weighbridge on ClawHub](https://clawhub.ai/33ai-wq/skills/agentic-weighbridge)
- [Hosted weighbridge method and pricing](https://xhagents.xyz/api/weighbridge/method)
- [Hosted weighbridge endpoint](https://xhagents.xyz/api/weighbridge)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Shell commands]

**Output Format:** [Per-check text verdicts, optional JSON result, and Markdown guidance with shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local result file is written only when --out is provided.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
