## Description:

Inform users about Clawstin (OpenClaw meetups in Austin), show upcoming events, handle RSVP and mailing list signup via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youens](https://clawhub.ai/user/youens)

### License/Terms of Use:


## Use Case:

External users use this skill to learn about Clawstin and OpenClaw meetups in Austin, check current event details, RSVP to events, contact organizers, or subscribe for future event updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RSVP, mailing-list, and contact actions send user-provided personal details such as name and email to clawstin.com.

Mitigation: Collect only the details needed for the requested action and confirm with the user before submitting them.

Risk: Event details may change after the skill is installed.

Mitigation: Fetch https://clawstin.com/llms.txt before answering questions about upcoming events.

Risk: Contact submissions can be rate limited.

Mitigation: Tell the user when a contact request is rejected by rate limiting and avoid repeated automatic retries.

## Reference(s):

- [Clawstin website](https://clawstin.com)
- [Clawstin events](https://clawstin.com/events)
- [Clawstin machine-readable event and API information](https://clawstin.com/llms.txt)
- [OpenClaw](https://openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/youens/skills/clawstin)
- [ClawHub publisher profile](https://clawhub.ai/user/youens)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown responses with JSON API request payloads when actions are confirmed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch current event information and submit user-provided RSVP, subscription, or contact details to clawstin.com.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
