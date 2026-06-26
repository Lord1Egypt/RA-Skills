## Description: <br>
Interact with the Cal.com API v2 to manage scheduling, bookings, event types, availability, and calendars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PeerRich](https://clawhub.ai/user/PeerRich) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI agents use this skill to build Cal.com scheduling integrations that check availability, create and manage bookings, configure event types and schedules, manage calendars, and set up webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward real Cal.com actions such as creating, cancelling, rescheduling, deleting, or changing webhooks. <br>
Mitigation: Require user confirmation before mutating bookings, event types, schedules, calendars, or webhooks. <br>
Risk: The skill requires Cal.com API access and may involve API keys, OAuth client secrets, webhook secrets, and calendar or booking data. <br>
Mitigation: Use least-privilege credentials, keep secrets out of client-side code and logs, and redact sensitive values in generated examples or diagnostics. <br>
Risk: Webhook and calendar integrations can send scheduling data to external endpoints. <br>
Mitigation: Use only trusted HTTPS endpoints, verify webhook signatures, and avoid logging full webhook payloads. <br>


## Reference(s): <br>
- [Cal.com API v2 skill page](https://clawhub.ai/PeerRich/calcom) <br>
- [Cal.com API v2 documentation](https://cal.com/docs/api-reference/v2) <br>
- [Cal.com API v2 OpenAPI specification](https://api.cal.com/v2/docs) <br>
- [Authentication API Reference](references/authentication.md) <br>
- [Bookings API Reference](references/bookings.md) <br>
- [Calendars API Reference](references/calendars.md) <br>
- [Event Types API Reference](references/event-types.md) <br>
- [Schedules API Reference](references/schedules.md) <br>
- [Slots and Availability API Reference](references/slots-availability.md) <br>
- [Webhooks API Reference](references/webhooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with HTTP examples, JSON request and response bodies, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for Cal.com API v2 operations; agents may turn the guidance into authenticated API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
