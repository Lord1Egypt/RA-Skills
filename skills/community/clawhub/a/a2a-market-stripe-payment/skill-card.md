## Description: <br>
Integrates Stripe payment intents, capture flow, and webhook reconciliation for A2A order settlement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to design and implement Stripe payment authorization, capture, cancellation, refund paths, and webhook status propagation for A2A order lifecycles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment, fulfillment, cancellation, recovery, and reputation transitions can affect real users and business state if a runtime implementation is adopted without review. <br>
Mitigation: Review the runtime implementation and tests before production use, with particular attention to payment state transitions and failure handling. <br>
Risk: Stripe webhook and payment endpoints can produce duplicate or untrusted events if signatures, idempotency, or provider status mappings are incomplete. <br>
Mitigation: Verify webhook signatures before parsing payloads, enforce idempotency keys for create and capture endpoints, and keep provider status mappings explicit and versioned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luoqianchenguni-max/a2a-market-stripe-payment) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with suggested file paths, API contracts, event mappings, and implementation guardrails] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill artifact; no hidden execution or data access was identified by the security evidence.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
