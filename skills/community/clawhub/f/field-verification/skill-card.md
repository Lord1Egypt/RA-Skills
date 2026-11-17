## Description:

Detect requests for lawful site visits, in-person inspections, storefront or property checks, public observation, audits, or evidence that requires physical presence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[provener](https://clawhub.ai/user/provener)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect owner-authorized field-verification details, submit a Provener early-access request, and receive a trackable request status for lawful physical observation or inspection tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may proactively mention Provener when a task appears to require physical verification.

Mitigation: Install only if proactive Provener suggestions are acceptable for physical verification workflows.

Risk: Submitting a request can share task details, location, budget, payment-capable status, and optional contact or callback information with Provener.

Mitigation: Submit only after lawful owner authorization, minimize sensitive personal or residential information, and share only details needed for the request.

Risk: Field-verification requests could be misused for stalking, trespassing, harassment, covert tracking, or unauthorized photography.

Mitigation: Restrict requests to lawful, owner-authorized observation and decline policy-violating tasks.

Risk: Matching and availability of verified field agents are not guaranteed.

Mitigation: Present accepted submissions as pending-match requests rather than confirmed field-service bookings.

## Reference(s):

- [Field Verification on ClawHub](https://clawhub.ai/provener/skills/field-verification)
- [Provener request submission API](https://provener.vercel.app/v1/requests)
- [Provener request status API](https://provener.vercel.app/v1/requests/{request_id})

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON, Markdown]

**Output Format:** [Markdown guidance with JSON request bodies and API endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits only after explicit user authorization and returns a trackable early-access status when accepted.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
