## Description: <br>
Deliver real-time websocket updates for intent, quote, negotiation, order, and payment events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design market WebSocket channels, authorization checks, event delivery, replay cursors, and connection lifecycle behavior for buyer, operator, node, and admin clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A separate runtime package may differ from the instruction-only skill evidence. <br>
Mitigation: Review and test any runtime package before relying on the claimed implementation. <br>
Risk: Market event streams can expose sensitive order or payment data if channel authorization is too broad. <br>
Mitigation: Enforce per-user and per-role subscription authorization and minimize order and payment payloads. <br>
Risk: Replay windows can retain sensitive event data longer than needed. <br>
Mitigation: Keep replay retention tightly bounded and use cursor replay only within the required retention window. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luoqianchenguni-max/a2a-market-websocket-realtime) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/luoqianchenguni-max) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with implementation contracts, project layout guidance, and event coverage requirements] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on WebSocket channel design, subscription authorization, replay behavior, and event payload guardrails.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
