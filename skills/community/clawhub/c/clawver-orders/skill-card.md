## Description:

Manage Clawver orders. List orders, track status, process refunds, generate download links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nwang783](https://clawhub.ai/user/nwang783)

### License/Terms of Use:


## Use Case:

Store operators, support staff, and developers use this skill to inspect Clawver customer orders, track fulfillment, process refund requests, manage download links, and configure order webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refund examples can initiate monetary changes when executed with a privileged CLAW_API_KEY.

Mitigation: Require explicit human approval before refunds, verify order identity and customer intent, and limit CLAW_API_KEY permissions to the minimum store permissions available.

Risk: Webhook creation can send order events to an untrusted or incorrect endpoint.

Mitigation: Require explicit human approval before webhook creation and register only trusted endpoints controlled by the store operator.

Risk: Download and order-status links can expose customer order access when shared with the wrong recipient.

Mitigation: Share tokenized download and status links only with verified customers through approved support channels.

Risk: The security verdict is suspicious because refund and webhook guidance needs stronger scoping and confirmation controls.

Mitigation: Review and scan the skill before deployment, and apply the scanner guidance before operational use.

## Reference(s):

- [Orders API Examples](references/api-examples.md)
- [Clawver Store](https://clawver.store)
- [ClawHub Skill Page](https://clawhub.ai/nwang783/skills/clawver-orders)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl commands, Python examples, tables, and short operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CLAW_API_KEY environment variable and an active Clawver store with orders.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
