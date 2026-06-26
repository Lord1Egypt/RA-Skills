## Description: <br>
Integrates agents with the Brek Partner Core Chat API for hotel search, booking session management, anti-abuse call controls, and payment-safe confirmation flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo9](https://clawhub.ai/user/leo9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect agents to Brek hotel-booking chat sessions, enforce call controls, and route booking, cancellation, price-change, and payment actions through explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can assist with real hotel booking, cancellation, price-change, and payment-confirmation workflows. <br>
Mitigation: Require explicit human confirmation before booking, cancellation, price-change, or payment-confirmation actions, and reuse deterministic idempotency keys for write-like events. <br>
Risk: The integration depends on BREK_PARTNER_API_KEY and outbound calls to BREK_BASE_URL. <br>
Mitigation: Store the API key in a secret manager, stop calls when it is missing or invalid, and restrict BREK_BASE_URL to the official Brek endpoint. <br>
Risk: Usage logs, request identifiers, actor IDs, and billing records may need retention and access controls. <br>
Mitigation: Define retention, access, and reconciliation controls for usage logs and keep immutable metering events scoped to operational and billing needs. <br>


## Reference(s): <br>
- [API Templates](references/api-templates.md) <br>
- [Call Control and Anti-Abuse](references/call-control.md) <br>
- [Payment and Billing](references/payment-and-billing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration plus JSON and TypeScript API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Brek base URL and partner API key, stable actor and tenant identifiers, idempotency keys for write-like actions, and durable stores for dedupe, budgets, and usage metering.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
