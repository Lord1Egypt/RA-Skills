## Description:

1688-88syt helps agents manage 1688 88 Shengyitong purchase-order workflows, including account checks, order creation, signing, receipt confirmation, invalidation, and refund requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[next-1688](https://clawhub.ai/user/next-1688)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 buyers, sellers, and their agents use this skill to query account and purchase-order status and to carry out 88 Shengyitong purchase-order actions through natural-language requests. It supports business workflows that can change transaction state, so write operations require explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a powerful 1688 access key for transaction-management actions.

Mitigation: Install only from a trusted publisher, store the AK in a platform secret store where possible, avoid sharing it in chat or command lines, and restrict permissions on ~/.openclaw/openclaw.json.

Risk: Create, sign, receipt-confirmation, invalidation, and refund commands can change real business or financial state.

Mitigation: Require explicit user intent before write actions and a second confirmation before operations involving funds or transaction-state changes.

Risk: Gateway misconfiguration could send signed requests through an unintended endpoint.

Mitigation: Verify OPENCLAW_GATEWAY_URL points only to the trusted local gateway before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/next-1688/skills/1688-88syt)
- [88 Shengyitong buyer page](https://syt.1688.com/page/SYT/buyer?tracelog=88sytskill)
- [Skill instructions](SKILL.md)
- [README](README.md)
- [Common operating rules](references/common/common-rules.md)
- [Error handling](references/common/error-handling.md)
- [Product overview FAQ](references/faq/product-overview.md)
- [Create order capability](references/capabilities/create-order.md)
- [Sign order capability](references/capabilities/sign-order.md)
- [Confirm receipt capability](references/capabilities/confirm-receipt.md)
- [Refund apply capability](references/capabilities/refund-apply.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [JSON command results with human-facing Markdown summaries and agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return success, markdown, and data fields; user-facing responses should preserve the markdown field before any additional analysis.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
