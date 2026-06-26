## Description: <br>
企业用车服务助手，支持即时用车、预约用车、接送机、包车等企业差旅用车场景，并提供车型选择、费用预估和订单管理 guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fbt](https://clawhub.ai/user/fbt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business travel assistants use this skill to plan or manage company car service requests, including immediate rides, scheduled rides, airport transfers, charters, cost estimates, cancellations, and invoice-related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can present simulated rides, drivers, prices, and cancellations as if they were real bookings. <br>
Mitigation: Require an authenticated provider integration and clearly label simulated responses before using the skill for transportation, invoices, driver details, or cancellations. <br>
Risk: A user may believe a ride has been booked or cancelled without a real provider confirmation. <br>
Mitigation: Add an explicit user confirmation step and return provider-confirmed order status before representing a booking or cancellation as final. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fbt/business-ride) <br>
- [Publisher profile](https://clawhub.ai/user/fbt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with JSON-shaped booking, pricing, order, and cancellation outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; outputs should be treated as simulated unless backed by an authenticated transportation provider integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
