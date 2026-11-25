## Description:

Helps developers integrate Didit Event Monitoring to submit, review, and analyze user activity events through Didit's event API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add event monitoring to backend services and browser or mobile clients. It provides request examples and guidance for sending activity events, reading results, and creating event rules in Didit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration uses DIDIT_API_KEY and sends event data to Didit; mishandled credentials or unnecessary personal data could expose account or user information.

Mitigation: Keep the API key in secret storage and send only necessary event fields; follow the skill's guidance to use references or hashes instead of raw secrets.

Risk: The security scan reports partial component coverage and degraded tool misuse analysis, so its benign verdict has incomplete evidence.

Mitigation: Review the integration and its event data handling before deployment, and limit credentials and submitted data to what the use case requires.

## Reference(s):

- [Didit Event Monitoring](https://docs.didit.me/transaction-monitoring/events)
- [SDK Event Submission](https://docs.didit.me/transaction-monitoring/sdk-event-submission)
- [Event Rules](https://docs.didit.me/transaction-monitoring/event-rules)
- [Event Rules Library](https://docs.didit.me/transaction-monitoring/rules-library)
- [Didit Event Monitoring Skill on ClawHub](https://clawhub.ai/rosasalberto/skills/didit-event-monitoring)

## Skill Output:

**Output Type(s):** [Code, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python and shell examples, JSON request payloads, and integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use the DIDIT_API_KEY environment variable; client-side submission can use scoped monitoring tokens.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
