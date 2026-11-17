## Description:

Free agent-commerce readiness checklist for x402/MCP/OpenAPI/payment-error/EVM safety launch reviews; routes full audits to the paid ClawMart Agent Commerce Readiness Pack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastiancoombs](https://clawhub.ai/user/sebastiancoombs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a quick launch-readiness review before an agent, MCP server, or paid API accepts autonomous buyer traffic. The checklist covers discovery, payment envelopes, payment-error handling, EVM signing safety, and buyer trust signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The preview may direct failed or uncertain audits toward a specific paid package.

Mitigation: Ask for concrete evidence and remediation steps before buying or installing the upgrade.

Risk: Agent-commerce reviews can involve sensitive wallet, credential, or payment context.

Mitigation: Use the preview as a checklist only; do not provide seed phrases, private keys, JWTs, API keys, raw wallet credentials, or payment submissions.

Risk: A service may appear discoverable while still having unsafe payment, signing, or buyer-trust behavior.

Mitigation: Require discovery, payment-envelope, error-handling, signing-safety, and buyer-trust checks before treating a launch as ready.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sebastiancoombs/skills/agent-commerce-readiness-preview)
- [Agent Commerce Readiness Pack listing](https://www.shopclawmart.com/listings/agent-commerce-readiness-pack-2081aec2)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown checklist guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces pass, warn, or fail readiness observations; it does not execute code, collect secrets, submit payments, or persist changes.]

## Skill Version(s):

1.0.0 (source: target metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
