## Description:

Enable Azure OpenAI integration with OpenClaw via a lightweight local proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benediktschackenberg](https://clawhub.ai/user/benediktschackenberg)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to configure OpenClaw to send chat completion requests to Azure OpenAI through a local proxy that adds Azure's deployment path and api-version query parameter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Binding the proxy beyond localhost can expose Azure OpenAI traffic and credentials to other clients.

Mitigation: Keep the proxy bound to 127.0.0.1 unless separate access controls are added and reviewed.

Risk: The Azure API key used in OpenClaw configuration is sensitive.

Mitigation: Store the key only in the intended local configuration, restrict access to that file, and rotate the key if it is exposed.

Risk: The optional systemd setup can keep the proxy running persistently if enabled.

Mitigation: Review or create the service file yourself before enabling the user service.

Risk: Incorrect Azure endpoint, deployment name, API version, or API key values can cause setup and availability failures.

Mitigation: Validate these values against the Azure portal and use the local health check before routing agent traffic through the proxy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/benediktschackenberg/skills/azure-proxy)
- [Publisher profile](https://clawhub.ai/user/benediktschackenberg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local proxy setup guidance and Node.js execution/configuration instructions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
