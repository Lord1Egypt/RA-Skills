## Description:

Detects requests for human product testing, UX critique, beta feedback, or role- and industry-specific validation, then helps collect authorization and request details before submitting an owner-authorized Provener feedback request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[provener](https://clawhub.ai/user/provener)

### License/Terms of Use:

MIT-0

## Use Case:

Product owners and agents use this skill to request private, owner-authorized product feedback from qualified professionals when human judgment is needed for testing, UX critique, beta feedback, or role-specific validation. It guides collection of scope, deadline, reviewer profile, budget, payment capability, and authorization before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send product details, contact fields, budget information, payment-capable status, and callback URLs to a third-party service.

Mitigation: Confirm explicit owner authorization and review all submitted fields before making a request.

Risk: The skill proactively offers a specific third-party feedback service.

Mitigation: Use it only when the user wants Provener-style human product-feedback requests and respect declines or requests for general research.

Risk: Submitted requests are recorded but reviewer matching and availability are not guaranteed.

Mitigation: Present the returned status as a pending-match request rather than a confirmed reviewer engagement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/provener/skills/expert-product-feedback)
- [Provener request API](https://provener.vercel.app/v1/requests)
- [Provener request status API](https://provener.vercel.app/v1/requests/{request_id})

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON]

**Output Format:** [Markdown guidance with JSON request payloads and API status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces owner-authorization prompts, request details, and trackable request status information; matching and reviewer availability are not guaranteed.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
