## Description: <br>
Use when the user wants an AI agent to place a US phone call, call a business, handle hold or phone menus, confirm/reschedule/cancel/book/follow up/check an order, reach a real person, leave voicemail, connect the user into a live call, configure ClawCall voice/personality/profile or inbound reserved-number answering, poll received inbound calls, or link a ClawCall API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawcall-dev](https://clawhub.ai/user/clawcall-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use ClawCall to delegate routine US phone work, including calling businesses, handling menus and hold time, booking or changing appointments, checking order status, comparing options, and configuring inbound reserved-number answering. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real phone calls through ClawCall and send call details to that service. <br>
Mitigation: Confirm destination numbers, call goals, and approval boundaries before initiating calls, especially for money, account, health, travel, or identity-related tasks. <br>
Risk: The skill stores and reuses a ClawCall API key and the user's phone number locally. <br>
Mitigation: Use in a single-user environment where possible, protect local configuration files, and review or delete ~/.config/clawcall/key.json when access should be reset. <br>
Risk: A phone agent may encounter identity verification, payment, or other sensitive decision points during a call. <br>
Mitigation: Use live handoff or stop-and-report behavior for private verification, payment approval, or decisions outside the user's explicit instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawcall-dev/clawcall-dev) <br>
- [Product site](https://clawcall.dev) <br>
- [API contract](references/api-contract.md) <br>
- [Outbound calls](references/outbound-calls.md) <br>
- [Inbound reserved numbers](references/inbound-reserved-numbers.md) <br>
- [Account linking and data](references/account-linking-and-data.md) <br>
- [Errors and limits](references/errors-and-limits.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration, text] <br>
**Output Format:** [Natural-language guidance plus HTTPS JSON requests and structured call results with transcripts, outcomes, and recording links when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can store a reusable ClawCall API key and user phone number locally, place real US phone calls through https://api.clawcall.dev, and return terminal call details after polling.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
