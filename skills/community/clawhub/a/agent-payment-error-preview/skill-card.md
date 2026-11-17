## Description:

Free triage preview for x402/AP2/ACP/MPP/MCP agent-payment failures; routes hard cases to the paid Agent Payment Error Diagnoser ClawMart skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastiancoombs](https://clawhub.ai/user/sebastiancoombs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for first-pass triage of agent-payment integration failures before deciding whether a paid structured diagnoser is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment logs may contain private keys, wallet seeds, bearer tokens, or unredacted authorization headers.

Mitigation: Redact payment logs before using the skill and avoid pasting secrets into the agent context.

Risk: Repeated payment retries can create duplicate attempts or mask permanent signature and scope errors.

Mitigation: Use a maximum retry counter and stop retries on permanent signature, scope, nonce, or idempotency failures.

Risk: The free preview promotes a separate paid ClawMart package for deeper diagnosis.

Mitigation: Install the paid package only when the separate listing is trusted and live corpus-backed diagnosis is needed.

## Reference(s):

- [Agent Payment Error Preview on ClawHub](https://clawhub.ai/sebastiancoombs/skills/agent-payment-error-preview)
- [Agent Payment Error Diagnoser on ClawMart](https://www.shopclawmart.com/listings/agent-payment-error-diagnoser-adda0b18)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with checklist-style triage steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No network calls, persistence, or secret access by itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
