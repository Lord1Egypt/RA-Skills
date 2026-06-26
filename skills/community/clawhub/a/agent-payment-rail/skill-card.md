## Description: <br>
Provides a unified API for AI agents to create, query, refund, and cancel multi-currency payments via Stripe and other providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add payment operations to AI agents, including creating payments, checking transaction status, issuing refunds, and canceling pending payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, refund, and cancel payments without documented approval or safety limits. <br>
Mitigation: Require explicit human approval for every create, refund, and cancel action; set transaction and refund limits before using live credentials. <br>
Risk: Payment provider credentials can authorize financial operations. <br>
Mitigation: Start with test or restricted provider keys, verify the external npm package and publisher, store credentials outside prompts, and enable audit logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ZhenStaff/agent-payment-rail) <br>
- [GitHub Repository](https://github.com/ZhenRobotics/openclaw-agent-payment-rail) <br>
- [npm Package](https://www.npmjs.com/package/openclaw-agent-payment-rail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration instructions, API calls] <br>
**Output Format:** [Markdown with JavaScript, TypeScript, and shell command examples; payment operation inputs and transaction responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires payment provider credentials and supports payment creation, transaction lookup, refunds, and cancellation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
