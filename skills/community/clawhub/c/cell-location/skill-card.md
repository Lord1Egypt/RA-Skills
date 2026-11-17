## Description:

This skill queries Juhe's 5G cell-tower location service with MCC, MNC, LAC/TAC, and CI values, then routes paid A2M HTTP 402 flows through an Alipay payment skill before returning location data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to resolve carrier cell-tower identifiers into static geographic location data for location checks, nearby-service support, or basic positioning after user-confirmed payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cell-tower identifiers may expose location-related information when sent to Juhe.

Mitigation: Submit only the identifiers needed for the lookup and avoid adding unrelated sensitive context.

Risk: The payment flow shares payment and order metadata with the Alipay payment skill.

Mitigation: Review product, amount, transaction number, and user order number before authorizing payment.

Risk: The documented install path uses a mutable `@latest` payment package.

Mitigation: Prefer a pinned, reviewed payment dependency and verify the package source and version before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/cell-location)
- [ClawHub publisher profile](https://clawhub.ai/user/juhemcp)
- [Juhe A2A query endpoint](https://apis.juhe.cn/a2a/query)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MCC, MNC, LAC/TAC, and CI values; payment processing may return an HTTP 402 response before location data is available.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
