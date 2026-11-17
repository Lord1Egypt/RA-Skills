## Description:

Add API keys, per-customer rate limits, quotas and usage metering to a Node.js or Python API server with the UsageRail SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supertj](https://clawhub.ai/user/supertj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Node.js or Python API servers use this skill to add UsageRail customer authentication, per-customer rate limits and quotas, and usage metering for billing through their own Stripe account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom consumer that trusts caller-controlled identity data can attribute requests to the wrong customer.

Mitigation: Derive the consumer identity from authentication verified by the API, and place UsageRail after that authentication in the framework's middleware order.

Risk: An app key committed to source code or shared in chat could be exposed.

Mitigation: Read USAGERAIL_APP_KEY from the environment; do not write the key into source code or ask the user to paste it into chat.

Risk: Usage counts that have not yet been sent can be lost after abrupt termination or without framework-specific shutdown handling.

Mitigation: Use the documented shutdown handling, including the Django ASGI wrapper and Hono flushOnExit where applicable, and account for the documented five-second Express shutdown limit.

## Reference(s):

- [UsageRail documentation](https://usagerail.com/docs)
- [UsageRail app console](https://app.usagerail.com)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with framework-specific code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Framework-specific setup instructions and examples.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
