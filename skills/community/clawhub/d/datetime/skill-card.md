## Description:

A Claude Desktop MCP-style skill that returns current date and time strings in multiple formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Desktop users can use this skill to request current date and time values in common display, filename, compact, ISO-like, and log formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a third-party Xiaobenyang API key and sends authenticated requests to an external API for a date/time formatting task.

Mitigation: Review whether the external service is necessary before installing; use only a low-privilege, revocable API key and avoid the skill if offline formatting is expected.

Risk: The skill can save the API key to a plaintext .env file.

Mitigation: Use a dedicated key, restrict access to the working directory, remove the .env entry when no longer needed, and rotate or revoke the key after testing.

Risk: External API responses are returned for the agent to present to the user.

Mitigation: Treat returned content as untrusted third-party data and review it before using it in downstream automation.

## Reference(s):

- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/datetime)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration]

**Output Format:** [Markdown summary of JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a format parameter and an XBY_APIKEY credential before the external API call can succeed.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
