## Description:

Helps agents configure DeepSeek V3 as the OpenClaw model provider with API key setup, YAML examples, connection testing, and troubleshooting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure DeepSeek V3 or deepseek-chat as their model provider, store the API key in local OpenClaw configuration, test connectivity, and tune basic options such as streaming and temperature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts sent through the configured DeepSeek provider may be processed by DeepSeek.

Mitigation: Use the provider only for data that is appropriate to send to DeepSeek under the user's applicable policies.

Risk: The DeepSeek API key can grant access to paid model usage if exposed.

Mitigation: Store the API key only in trusted local OpenClaw configuration and avoid sharing it in prompts, logs, or public files.

## Reference(s):

- [DeepSeek Platform](https://platform.deepseek.com/)
- [Deepseek Quick Config on ClawHub](https://clawhub.ai/yang1002378395-cmyk/skills/deepseek-quick-config)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes external service setup steps and local configuration examples; does not execute commands automatically.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
