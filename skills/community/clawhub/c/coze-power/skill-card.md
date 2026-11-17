## Description:

Coze-Power connects Coze cloud bots to a local HTTP server that exposes web search, filesystem, shell command, system information, clipboard, and notification tools through an OpenAPI plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[homesickjava](https://clawhub.ai/user/homesickjava)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Coze bot builders use this skill to let Coze agents call local tools for research, file handling, command execution, system status checks, clipboard operations, and desktop notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposing the local server can give a remote Coze bot access to files, commands, clipboard contents, and system information.

Mitigation: Install only when that remote control is intended; do not expose the server to the internet as shipped and bind locally where possible.

Risk: A weak or default API key can allow unauthorized use of local tools.

Mitigation: Change the API key before use and keep the key limited to trusted Coze plugin configuration.

Risk: Command execution and filesystem access can affect data outside the user's intended scope.

Mitigation: Remove command execution or replace it with structured safe actions, restrict file paths to a dedicated sandbox folder, and allow only required commands.

Risk: Clipboard access may expose sensitive data copied from other applications.

Mitigation: Disable clipboard access unless it is required for the bot workflow.

Risk: Running the server in a normal user session increases impact if the service is misused.

Mitigation: Run the server in an isolated account or container.

## Reference(s):

- [Coze-Power Skill Page](https://clawhub.ai/homesickjava/skills/coze-power)
- [API Reference](references/api-reference.md)
- [Coze Plugin Setup Guide](references/coze-plugin-setup.md)
- [Examples](references/examples.md)
- [OpenAPI Specification](assets/openapi-spec.json)
- [Coze Studio](https://www.coze.com)
- [ngrok Download](https://ngrok.com/download)
- [Cloudflare Tunnel Downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON tool responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write configured local files, execute whitelisted shell commands, and return system or clipboard data when the local server is enabled.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
