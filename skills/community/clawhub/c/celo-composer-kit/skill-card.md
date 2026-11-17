## Description:

Celo服务 helps agents retrieve Celo Composer Kit component, installation, and CLI information through a XiaoBenYang-hosted API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up Celo Composer Kit components, examples, props, category listings, installation guidance, and Celo Composer CLI create-command information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is labeled as a Celo setup helper but requires a XiaoBenYang API key and uses a separate remote API service.

Mitigation: Install only when the XiaoBenYang service is intended for the deployment and reviewers accept the remote service dependency.

Risk: Tool queries and parameters are sent to the configured remote API endpoint.

Mitigation: Avoid submitting unrelated Celo, wallet, exchange, personal, or production credentials through the skill.

Risk: The skill stores the XiaoBenYang API key in a local .env file.

Mitigation: Protect the .env file, rotate the key if exposed, and do not reuse sensitive credentials as the XiaoBenYang API key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/celo-composer-kit)
- [XiaoBenYang service](https://xiaobenyang.com)
- [Configured XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries of API responses, examples, installation steps, component metadata, and CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value and sends tool queries and parameters to the configured XiaoBenYang remote API.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
