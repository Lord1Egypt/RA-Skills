## Description:

Looks up cake product names by order number using an internal order API and returns the product name or API message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echojiandong](https://clawhub.ai/user/echojiandong)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user asks to check a cake order or provides an order number and needs the corresponding cake product name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated order lookup can expose order-product information when numeric order IDs are guessable.

Mitigation: Use only in controlled test environments, or require authentication, authorization, rate limits, and non-enumerable identifiers before production use.

Risk: Raw API error messages may expose internal details or provide poor user-facing feedback.

Mitigation: Normalize error responses and avoid exposing raw backend messages to users.

Risk: Users may request lookups outside the intended merchant or order domain.

Mitigation: Require users to identify the specific merchant/order domain and verify they are allowed to access the order before lookup.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, API Calls]

**Output Format:** [Plain text response with a cake product name or an error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a numeric order ID and depends on the order lookup API being available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
