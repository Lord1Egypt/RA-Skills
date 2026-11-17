## Description:

Verify that a digital-product listing's buyer files and access instructions match its customer-facing claims before promotion, renewal, or publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiwi-phantomworks](https://clawhub.ai/user/kiwi-phantomworks)

### License/Terms of Use:

MIT-0

## Use Case:

Digital product sellers use this skill to compare buyer-facing delivery claims with attached files and authenticated access flows before promoting, renewing, or publishing a listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public response or attached file alone may give a false impression that a buyer can access or duplicate an external destination.

Mitigation: Verify the buyer-facing flow with authorized authenticated access; report BLOCKED when that proof is unavailable.

Risk: Inspecting purchaser data could expose private customer information.

Mitigation: Limit the audit to listing claims, attached buyer files, and access-flow evidence; do not inspect, copy, or expose purchaser data.

## Reference(s):

- [Buyer Delivery QA on ClawHub](https://clawhub.ai/kiwi-phantomworks/skills/buyer-delivery-qa)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Compact Markdown audit table or bullets with a per-listing verdict and go/no-go recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes customer promise, verified file evidence, external-flow status, verdict, and the smallest corrective action.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
