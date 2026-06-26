## Description: <br>
Inform users about Clawstin, an Austin OpenClaw meetup series, show upcoming events, and help with RSVP, mailing list signup, or organizer contact requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youens](https://clawhub.ai/user/youens) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and meetup participants use this skill to learn about Clawstin events in Austin, get current event details, and ask an agent to RSVP, subscribe to updates, or contact organizers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send a user's name, email, RSVP details, or contact message to Clawstin APIs. <br>
Mitigation: Confirm the user's intent and the exact personal details before submitting an RSVP, mailing list signup, or organizer contact request. <br>
Risk: Live event information may reference a purchase or checkout flow outside the skill. <br>
Mitigation: Require separate explicit user approval before treating any purchase or checkout action as authorized. <br>
Risk: Contact organizer requests are rate limited to 3 messages per hour per email or IP. <br>
Mitigation: Tell the user when repeated contact attempts may be rate limited and avoid retry loops. <br>


## Reference(s): <br>
- [Clawstin skill page](https://clawhub.ai/youens/clawstin) <br>
- [Clawstin website](https://clawstin.com) <br>
- [Clawstin events](https://clawstin.com/events) <br>
- [Clawstin machine-readable event and API information](https://clawstin.com/llms.txt) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or concise text with optional JSON API request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch live event information and, after user confirmation, submit RSVP, mailing list, or contact API requests.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
