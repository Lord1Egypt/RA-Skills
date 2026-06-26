## Description: <br>
智慧餐饮 enables restaurant guests to use natural-language chat to look up restaurant information and menus, place dine-in or delivery orders, reserve tables, take queue numbers, check member benefits, and submit feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dawangda](https://clawhub.ai/user/dawangda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External restaurant guests and restaurant staff use this skill through chat channels such as Feishu, WeChat, QQ, and Telegram to complete food ordering, delivery, table reservation, queue, order-status, member-service, and feedback workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill sends personal and transaction data to a raw-IP MCP endpoint that conflicts with the stated domain. <br>
Mitigation: Before using real customer data, verify that the publisher controls the MCP endpoint and require the disclosed domain with valid TLS instead of the raw IP address. <br>
Risk: The security review notes inconsistent privacy-retention disclosures for member data and conversation logs. <br>
Mitigation: Clarify and document retention for user IDs, phone numbers, delivery addresses, orders, member data, and conversation logs before production deployment. <br>
Risk: The skill can initiate customer-impacting actions such as orders, reservations, cancellations, delivery requests, queue numbers, and feedback submissions. <br>
Mitigation: Require explicit user confirmation of items, amounts, contact details, delivery addresses, times, party sizes, cancellation intent, and feedback content before approving tool calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dawangda/ai-restaurant) <br>


## Skill Output: <br>
**Output Type(s):** [text, API Calls, configuration, guidance] <br>
**Output Format:** [Natural-language chat responses with MCP JSON-RPC tool calls and structured order, reservation, queue, and member-service results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool calls may create or cancel orders, create delivery requests, reserve tables, take queue numbers, and submit feedback; the skill instructs the agent to confirm user details before transactional actions.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
