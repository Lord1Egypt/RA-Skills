## Description:

Make real phone calls to businesses. Book reservations, cancel subscriptions, navigate IVR menus. Get transcripts and recordings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanmellata](https://clawhub.ai/user/yanmellata)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to have an agent place business phone calls, poll call status, and return the outcome, summary, transcript, and recording URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real outbound phone calls on a user's behalf.

Mitigation: Require confirmation of the target number, business, objective, and any account-changing request before placing a call.

Risk: Call transcripts and recording URLs may contain sensitive or regulated information.

Mitigation: Avoid submitting sensitive private URLs in the website field and consider consent, recording, and transcription rules for all call participants.

Risk: Placeholder phone numbers in examples could be used incorrectly.

Mitigation: Replace placeholders with a user-confirmed E.164 phone number and stop if the number is missing or invalid.

## Reference(s):

- [AgentPhone API documentation](https://agentphone.app/docs)
- [AgentPhone website](https://agentphone.app)
- [ClawHub AgentPhone skill page](https://clawhub.ai/yanmellata/skills/agentphone)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline bash, Python, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTPHONE_API_KEY and curl; produces call status, outcome, summary, transcript, and recording URL when available.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
