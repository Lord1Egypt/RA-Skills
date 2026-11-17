## Description:

Make real phone calls with two-way voice conversations for wake-up calls, reminders, alerts, or other user-requested calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcospgp](https://clawhub.ai/user/marcospgp)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to place real phone calls only when the user explicitly asks, such as wake-up calls, reminders, alerts, or requested follow-up conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on mutable remote API documentation and sends call requests to clawr.ing.

Mitigation: Use the skill only after reviewing the current clawr.ing API documentation and deciding that the remote service is trusted for the intended use.

Risk: The skill uses an API key and may expose phone numbers, call content, quota, or account activity to the remote service.

Mitigation: Protect CLAWRING_API_KEY, avoid sharing unnecessary personal data, and review account activity through the service dashboard.

Risk: The local memory file can store phone numbers and preferences in plaintext.

Mitigation: Save only authorized contacts, keep the memory file protected, and provide a way to delete or update stored contact information.

Risk: The skill can initiate real phone calls, creating safety, consent, nuisance, or billing concerns.

Mitigation: Place calls only when the user explicitly asks and confirm the intended recipient and purpose before calling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcospgp/skills/clawring)
- [Publisher profile](https://clawhub.ai/user/marcospgp)
- [clawr.ing homepage](https://clawr.ing)
- [clawr.ing API documentation](https://clawr.ing/llms-full.txt)
- [clawr.ing dashboard](https://clawr.ing/dashboard)

## Skill Output:

**Output Type(s):** [API Calls, Files, Guidance]

**Output Format:** [Text guidance, HTTP API requests, and a local Markdown memory file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWRING_API_KEY and may use clawr.ing-memory.md to store contacts and calling preferences.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
