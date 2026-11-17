## Description:

Collect reviews and comments for a known Google Maps place URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify collection tasks for Google Maps reviews from a known place URL and receive the collected JSON result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API credentials and may pass a Dataify token to a companion task runtime.

Mitigation: Use a session-scoped environment variable or a secret manager for DATAIFY_API_TOKEN, avoid passing tokens on the command line or in chat, and review the companion dataify-task-operations runtime before using result-waiting behavior.

Risk: The security verdict is suspicious because credential handling and the unbundled local runtime require review before installation.

Mitigation: Review the skill and its local runtime dependency before deployment, and execute it only in an environment where Dataify credentials are appropriately scoped.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-google-maps-reviews)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a task ID and resume command if monitoring times out or is interrupted.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
