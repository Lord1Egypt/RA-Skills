## Description:

Code Right Publish creates a Code-Right task that sends a software system name and recipient email to generate software copyright registration materials, package them, and email a ZIP download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziyiyu](https://clawhub.ai/user/ziyiyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and service providers use this skill to create software copyright material generation tasks for software systems. It is suitable when task creation needs to be initiated from an agent workflow or integrated into an automation or ticketing process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the software system name and recipient email to softcraft.cloud for document generation and email delivery.

Mitigation: Use it only when that external service is acceptable for the workflow; avoid confidential project names or personal emails unless they are approved for that service.

Risk: An optional access token can be sent to the external service when provided.

Mitigation: Use an appropriate session token and avoid exposing it in shared logs, tickets, or command history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziyiyu/skills/code-right-create-task)
- [Code-Right task service](https://softcraft.cloud)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates remote tasks through softcraft.cloud and may email ZIP materials after processing.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
