## Description: <br>
Manage Clawver orders by listing orders, tracking status, processing refunds, and generating download links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nwang783](https://clawhub.ai/user/nwang783) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Clawver store operators and support agents use this skill to inspect customer order history, check fulfillment status, resend digital download links, process refunds, and configure order webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Refund actions can move money or change order outcomes if an agent follows an incorrect request. <br>
Mitigation: Require explicit confirmation before refunds and use the least-privileged API key available. <br>
Risk: API keys, receipt tokens, download tokens, and order status tokens can expose store or customer order access. <br>
Mitigation: Treat all tokens as secrets, avoid sharing them in untrusted contexts, and rotate credentials if exposed. <br>
Risk: Webhook configuration can send order events to endpoints outside the operator's control. <br>
Mitigation: Create webhooks only for controlled endpoints with strong secrets, minimal event scopes, signature verification, and periodic audits. <br>


## Reference(s): <br>
- [Clawver Store](https://clawver.store) <br>
- [ClawHub Skill Page](https://clawhub.ai/nwang783/clawver-orders) <br>
- [Orders API Examples](references/api-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with curl commands, JSON payload examples, and Python or JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAW_API_KEY and review before refund or webhook operations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
