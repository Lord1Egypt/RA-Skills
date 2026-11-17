## Description:

Collect structured Google Maps place or business details from a known map URL, CID, location input, or Place ID. Do not use to discover nearby places or collect reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Builder jobs for Google Maps place or business detail collection by URL, CID, location, or Place ID, then receive the collected result after task monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends map targets, keywords, coordinates, and related collection parameters to Dataify.

Mitigation: Install and use it only when sharing those inputs with Dataify is acceptable for the intended task.

Risk: The skill depends on a Dataify API token and can submit third-party collection jobs.

Mitigation: Configure DATAIFY_API_TOKEN in the shell, do not paste tokens into chat, and verify the target mode and scope before execution.

Risk: The skill waits for results through a companion dataify-task-operations runtime.

Mitigation: Review or verify the companion runtime before allowing automatic task monitoring.

## Reference(s):

- [Modes and parameters](references/modes-and-parameters.md)
- [Google Country Options](references/google_countries.md)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-google-map-details)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands and JSON task or result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit a Dataify task, wait for asynchronous completion, and summarize large result payloads while preserving access to raw results.]

## Skill Version(s):

1.3.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
