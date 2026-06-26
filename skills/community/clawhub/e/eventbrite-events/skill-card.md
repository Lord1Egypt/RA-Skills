## Description: <br>
Manage Eventbrite events, attendees, organizations, venues, orders, and ticketing data - powered by ClawLink. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an Eventbrite account through ClawLink, then manage events, ticketing, attendees, orders, venues, organizers, discounts, webhooks, and reports from chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires ClawLink OAuth access to an Eventbrite account. <br>
Mitigation: Install only when the user is comfortable granting Eventbrite access, and review the Eventbrite permissions during OAuth before approving the connection. <br>
Risk: Event, ticketing, discount, webhook, and buyer-setting actions can publish, cancel, delete, or otherwise modify live Eventbrite resources. <br>
Mitigation: Confirm destructive or public-facing actions with the user before execution and prefer previewing affected event, ticket, order, or webhook details first. <br>
Risk: Attendee, order, sales, organization-member, and user tools can expose sensitive account or customer data. <br>
Mitigation: Limit requests to the minimum needed scope and avoid sharing retrieved attendee or order data outside the active task. <br>


## Reference(s): <br>
- [ClawHub Eventbrite Skill](https://clawhub.ai/hith3sh/eventbrite-events) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=eventbrite-events) <br>
- [ClawLink Eventbrite Connection](https://claw-link.dev/dashboard?add=eventbrite) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with shell commands and JavaScript tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ClawLink pairing and Eventbrite OAuth; tool calls operate on the user's connected Eventbrite account.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
