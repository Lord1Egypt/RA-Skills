## Description: <br>
Cal.com API integration with managed OAuth for managing event types, bookings, schedules, availability, calendars, conferencing, webhooks, teams, verified resources, and user profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect and manage Cal.com scheduling resources through Maton's managed OAuth integration. It supports booking workflows, event type configuration, availability checks, calendar and conferencing lookup, webhook management, team lookup, verified email lookup, and profile updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Maton API key and managed OAuth access to a connected Cal.com account. <br>
Mitigation: Install it only when the operator trusts Maton for the connected account, set MATON_API_KEY deliberately, and remove or rotate credentials when access is no longer needed. <br>
Risk: Write operations can create, update, or delete scheduling resources, bookings, schedules, webhooks, and profile data. <br>
Mitigation: Require explicit user approval before every create, update, delete, cancel, or reserve action, including the target resource and expected effect. <br>
Risk: Webhooks can transmit attendee names, email addresses, and scheduling details to external subscriber URLs. <br>
Mitigation: Confirm the subscriber URL, triggers, active state, and purpose with the user before creating or updating any webhook. <br>
Risk: Booking and profile reads can expose personal data such as attendee identities, emails, and schedule details. <br>
Mitigation: Retrieve personal data only when the user requests it and limit queries to the needed booking, date range, or account context. <br>
Risk: Booking creation may fail or create an unintended appointment if the slot is unavailable or the wrong connection is used. <br>
Mitigation: Check available slots first and specify the Maton-Connection header when more than one Cal.com connection exists. <br>


## Reference(s): <br>
- [Cal.com skill page on ClawHub](https://clawhub.ai/byungkyu/cal-com) <br>
- [byungkyu publisher profile](https://clawhub.ai/user/byungkyu) <br>
- [Maton homepage](https://maton.ai) <br>
- [Cal.com API documentation](https://cal.com/docs/api-reference/v2/introduction) <br>
- [Cal.com API reference](https://cal.com/docs/api-reference/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline Python, JavaScript, shell commands, HTTP request examples, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Maton OAuth connection to Cal.com.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
