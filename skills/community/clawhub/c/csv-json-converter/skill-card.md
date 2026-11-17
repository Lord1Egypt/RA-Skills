## Description:

Converts CSV input into JSON object arrays through an agent-facing Expanso workflow, with Chinese interaction support for API integration and automation use cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, integration teams, and automation builders use this skill to convert CSV data into JSON arrays for API integration, platform handoffs, data synchronization, and workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the release suspicious because it asks for broad read, write, and exec authority that is not clearly scoped to CSV-to-JSON conversion.

Mitigation: Review before installing and grant only the minimum permissions needed for explicit CSV-to-JSON conversion tasks.

Risk: The security guidance notes API credentials, network/API calls, and command execution in the skill instructions.

Mitigation: Use it only in an environment where those capabilities are acceptable, keep credentials in environment variables, and avoid workflows that execute unreviewed commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/csv-json-converter)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces CSV-to-JSON conversion guidance and example structured results for agent workflows.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
