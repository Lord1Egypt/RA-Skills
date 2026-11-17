## Description:

Delivery Verifier checks virtual goods delivery by confirming that a cloud-drive link is reachable, the Xianyu buyer message was sent, and the order status changed to shipped or completed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill after an automated virtual-goods delivery flow to verify link availability, buyer-message delivery, order status, and delivery-policy warnings before closing or reviewing an order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Python execution and access to Xianyu chat and order verification services.

Mitigation: Review the skill before trusted-environment installation and scope MCP access and credentials to the minimum services needed for delivery verification.

Risk: The verifier makes outbound requests to submitted delivery links.

Mitigation: Restrict link validation to approved cloud-drive domains and block unexpected external destinations.

Risk: The artifact includes chat inspection and an AI-declaration check that are under-disclosed by the public summary.

Mitigation: Document or remove the AI-declaration behavior, and limit chat-history inspection to the minimum messages needed for delivery evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/delivery-verifier)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Business rules](artifact/references/business_rules.md)
- [Error codes](artifact/references/error_codes.md)
- [Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Guidance]

**Output Format:** [JSON verification report printed to stdout or written to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports pass, fail, and warning checks for link access, chat message evidence, order status, and optional policy checks; the script exits nonzero when verification fails.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
