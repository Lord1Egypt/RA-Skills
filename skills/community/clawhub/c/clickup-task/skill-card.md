## Description:

Create tasks in Vision Play ClickUp lists (visionplay or inbox).

This skill is ready for commercial/non-commercial use.

## Publisher:

[visionplay303](https://clawhub.ai/user/visionplay303)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill to create ClickUp tasks in the configured Vision Play lists, choosing either the visionplay or inbox destination with a required title and optional description.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task text passed through a shell command string can create command-injection exposure.

Mitigation: Call the ClickUp creation script with structured arguments and shell interpretation disabled.

Risk: Unexpected list values could route task creation outside the intended destinations.

Mitigation: Enforce the visionplay and inbox allowlist before invoking the task creation script.

Risk: Error output may expose sensitive integration details or credentials.

Mitigation: Redact sensitive error output before returning responses to users.

Risk: User-supplied task titles and descriptions are sent to ClickUp.

Mitigation: Clearly warn users that task content is transmitted to ClickUp before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/visionplay303/skills/clickup-task)
- [ClawHub Publisher Profile](https://clawhub.ai/user/visionplay303)

## Skill Output:

**Output Type(s):** [text, shell commands, API calls]

**Output Format:** [Text response containing the ClickUp API response or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, CLICKUP_TOKEN, CLICKUP_LIST_VISIONPLAY, and CLICKUP_LIST_INBOX.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
