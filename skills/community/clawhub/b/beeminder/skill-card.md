## Description:

Beeminder API for goal tracking and commitment devices. Use when checking Beeminder goals, adding datapoints, viewing due goals, managing commitments, or tracking habits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruigomeseu](https://clawhub.ai/user/ruigomeseu)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Beeminder goals, find due commitments, and manage datapoints through authenticated Beeminder API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated commands can create, update, or delete Beeminder datapoints.

Mitigation: Require explicit user approval before any add, update, or delete datapoint command is executed.

Risk: The Beeminder auth token may be exposed through shared logs or transcripts.

Mitigation: Use only a token the user is comfortable granting to an agent, avoid logging the token, and rotate it if exposure is suspected.

## Reference(s):

- [Beeminder API base URL](https://www.beeminder.com/api/v1/)
- [Beeminder auth token endpoint](https://www.beeminder.com/api/v1/auth_token.json)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Beeminder username and auth token environment variables; API responses are JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
