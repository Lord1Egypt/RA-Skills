## Description:

CloudNap helps agents list AWS EC2 instances, start or stop instances, and create or delete instance schedules through the CloudNap API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bhushan21z](https://clawhub.ai/user/bhushan21z)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to inspect CloudNap-managed EC2 resources, change instance power state, and maintain start/stop schedules from an agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change EC2 instance state or delete automation schedules, including in production or cost-sensitive environments.

Mitigation: Use it only where the agent is expected to manage EC2 state, and require explicit user confirmation before stopping, starting, creating schedules, or deleting schedules.

Risk: The skill relies on a CloudNap API key for all requests.

Mitigation: Provide the key through CLOUDNAP_API_KEY only, and do not print, log, or request the API key in conversation.

## Reference(s):

- [CloudNap skill page](https://clawhub.ai/bhushan21z/skills/cloudnap)
- [CloudNap API base URL](https://cloudnap.in/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Concise Markdown text with CloudNap API requests and user-facing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLOUDNAP_API_KEY and should avoid exposing credentials in responses or logs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
