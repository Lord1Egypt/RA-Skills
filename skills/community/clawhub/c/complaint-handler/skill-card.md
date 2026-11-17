## Description:

Retail complaint and after-sales handler for digital employees that classifies complaints, generates empathetic responses, routes escalations, and manages return, exchange, and refund requests according to configured policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangwei-frank](https://clawhub.ai/user/fangwei-frank)

### License/Terms of Use:

MIT-0

## Use Case:

Retail support teams and digital employees use this skill to classify customer complaints, generate empathetic policy-bound replies, and route refund, exchange, service, abuse, or escalation cases to the right permission level.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refund, exchange, or return guidance may exceed the organization's approval policy if permission thresholds are not configured.

Mitigation: Configure strict refund and exchange permissions, approval thresholds, and staff confirmation requirements before deployment.

Risk: Complaint handling may require contact, address, purchase, or order details from customers.

Mitigation: Add privacy wording before collecting personal details and collect only the missing details needed to resolve or escalate the case.

Risk: High-severity complaints may be delayed or routed incorrectly if escalation destinations are not approved.

Mitigation: Configure approved ticketing and escalation destinations for L2 and L3 cases before production use.

## Reference(s):

- [Complaint Classification Guide](references/classification-guide.md)
- [Complaint Response Templates](references/response-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with response templates and escalation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured policy_entries knowledge base and permissions_config for refund, exchange, ticketing, and escalation decisions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
