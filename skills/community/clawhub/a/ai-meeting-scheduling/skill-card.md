## Description:

SkipUp schedules and coordinates asynchronous meetings with 2-50 participants via email across time zones, with status checks, pause, resume, and cancellation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dheerg](https://clawhub.ai/user/dheerg)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, and agents use this skill to create and manage SkipUp meeting requests for multi-participant scheduling, status checks, pausing, resuming, cancellation, and workspace-member verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends meeting details and participant email addresses to SkipUp, and SkipUp may contact participants by email.

Mitigation: Install only when this data sharing is intended, avoid sensitive meeting context unless needed, and confirm with the user before creating requests.

Risk: Create, cancel, pause, and resume actions can change live meeting coordination state.

Mitigation: Require clear user confirmation before state-changing actions and confirm cancellation notification preferences before cancelling.

Risk: Retries can create duplicate meeting requests if not made idempotently.

Mitigation: Use a unique Idempotency-Key when creating meeting requests.

Risk: A broad or leaked API key could expose meeting request or workspace-member data.

Mitigation: Use a scoped SKIPUP_API_KEY with only the required meeting_requests and members permissions, and never hardcode it.

## Reference(s):

- [API reference](references/api-reference.md)
- [Natural language to API examples](references/examples.md)
- [SkipUp homepage](https://skipup.ai)
- [Meeting scheduling API reference](https://support.skipup.ai/api/meeting-requests/)
- [OpenClaw integration guide](https://support.skipup.ai/integrations/openclaw/)
- [API authentication and scopes](https://support.skipup.ai/api/authentication/)
- [SkipUp llms.txt](https://skipup.ai/llms.txt)
- [About SkipUp](https://blog.skipup.ai/llm/index)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON API responses with concise user-facing status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKIPUP_API_KEY with meeting_requests.read, meeting_requests.write, and members.read scopes.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
