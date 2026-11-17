## Description:

Access Garmin Connect health, fitness, and activity data via a non-interactive CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voydz](https://clawhub.ai/user/voydz)

### License/Terms of Use:


## Use Case:

Developers and Garmin Connect users use this skill to have an agent propose gc CLI commands for retrieving health, fitness, activity, device, workout, and raw API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose Garmin account credentials, MFA codes, and sensitive health or activity data.

Mitigation: Use a trusted and verified source for the gc CLI, avoid placing passwords or MFA codes directly in shell commands or prompts, and treat exported Garmin data as sensitive personal information.

Risk: The skill includes write operations such as uploads and workout create, update, or delete commands.

Mitigation: Require explicit confirmation before any upload, workout create, update, or delete action.

Risk: The skill documents raw API calls, including POST requests, with broad access to Garmin Connect endpoints.

Mitigation: Require explicit confirmation before raw POST or broad API calls and review target endpoints and request bodies before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/voydz/skills/garmin-cli)
- [Publisher profile](https://clawhub.ai/user/voydz)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Markdown, JSON, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill recommends JSON output for programmatic parsing and may direct the CLI to write exported data to files.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
