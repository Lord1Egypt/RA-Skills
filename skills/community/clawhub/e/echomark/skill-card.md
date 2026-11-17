## Description:

EchoMark helps agents record and query ratings for MCP servers, skills, CLI tools, APIs, and other tools so future tool choices can use prior experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruoxi0324](https://clawhub.ai/user/ruoxi0324)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use EchoMark to submit 1-5 ratings after using tools and to query local or community ratings before choosing tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: By default, cloud submission contacts an EchoMark API and uses an API key.

Mitigation: Use local-only mode when cloud sharing is not required.

Risk: The security evidence flags the default plaintext HTTP endpoint as unsafe for cloud features.

Mitigation: Avoid cloud features until the endpoint is changed to HTTPS or override the API URL with a trusted HTTPS endpoint.

Risk: The security evidence notes that registration prints an API key.

Mitigation: Treat printed keys as exposed and suppress or rotate keys before production use.

## Reference(s):

- [EchoMark ClawHub Release](https://clawhub.ai/ruoxi0324/skills/echomark)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python CLI commands and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local SQLite ratings and can use a cloud API for registration, submission, and community queries.]

## Skill Version(s):

0.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
