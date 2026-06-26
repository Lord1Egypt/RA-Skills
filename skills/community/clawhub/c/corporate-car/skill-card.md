## Description: <br>
企业用车服务助手，支持即时用车、预约用车、接送机、包车等多种用车场景，提供车型选择、费用预估、订单管理等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cs200809](https://clawhub.ai/user/cs200809) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and travel coordinators use this skill to estimate car-service costs, request immediate or scheduled rides, arrange airport transfers, and manage car-service orders for corporate travel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can present simulated ride bookings as successful real-world actions, which may mislead users about whether a vehicle was actually booked. <br>
Mitigation: Require explicit user confirmation and verified provider integration before reporting a booking as complete; clearly disclose when results are simulated. <br>
Risk: Booking and cancellation calls are exposed without an explicit confirmation gate. <br>
Mitigation: Ask for confirmation before booking or cancellation, then show the provider response, order identifier, and any applicable cancellation rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cs200809/corporate-car) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON function-call responses and formatted Chinese trip or order summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; supports price estimates, ride requests, scheduled rides, airport transfers, order cancellation, and order formatting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
