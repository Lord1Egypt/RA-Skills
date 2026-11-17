## Description:

Byted Mediakit Shared guides agents through mediakit-cli setup, authentication, command discovery, cloud and local media workflows, async task polling, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcvnebot](https://clawhub.ai/user/volcvnebot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to operate MediaKit CLI consistently across media editing and video workflows, including initialization, schema lookup, cloud/local mode selection, and querying asynchronous cloud tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive API credentials may be exposed if real API keys are passed on the command line or stored without review.

Mitigation: Use a reviewed credential path, avoid passing real API keys on the command line, and confirm how ~/.mediakit/config.json is protected before cloud use.

Risk: A broad global mediakit-cli installation can increase supply-chain or privilege risk.

Mitigation: Prefer a pinned, reviewed mediakit-cli version and avoid elevated or global installation where possible.

Risk: Cloud mode can send private media and task data to the configured MediaKit service.

Mitigation: Review endpoint and mode configuration before processing private media, and use cloud mode only when the data handling path is acceptable.

## Reference(s):

- [Query Task Reference](reference/query_task.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI command patterns, configuration requirements, async task polling guidance, and security cautions for API credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
