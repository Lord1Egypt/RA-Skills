## Description:

Schedule a meeting for humans and their agents by creating a scheduling poll, distributing it, collecting votes, and finding the best time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkelk](https://clawhub.ai/user/mkelk)

### License/Terms of Use:


## Use Case:

Employees, external collaborators, and their agents use this skill to coordinate group meeting times through meetlark.ai polls, collect participant votes, and recommend or close on a winning time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting purpose, proposed time slots, participant names, or participant emails may be sent to meetlark.ai when creating or managing a poll.

Mitigation: Share only the participant details needed to coordinate the meeting and avoid including sensitive meeting content in poll metadata.

Risk: The admin token can be used to view poll results and close the poll.

Mitigation: Keep the admin token private and do not include it in messages sent to participants.

## Reference(s):

- [Coordinate a Meeting on ClawHub](https://clawhub.ai/mkelk/skills/coordinate-meeting)
- [meetlark.ai](https://meetlark.ai)
- [Meetlark OpenAPI Spec](https://meetlark.ai/api/v1/openapi.json)
- [Meetlark Interactive Docs](https://meetlark.ai/docs)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Guidance]

**Output Format:** [Markdown with API endpoint references and ready-to-send message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scheduling poll links, vote summaries, recommended meeting times, and confirmation text.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
