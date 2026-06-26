## Description: <br>
Azure OpenAI Proxy enables OpenClaw to use Azure OpenAI through a lightweight local proxy that adds the required deployment path and api-version parameter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BenediktSchackenberg](https://clawhub.ai/user/BenediktSchackenberg) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to run a local proxy that forwards OpenClaw chat-completion requests to their Azure OpenAI deployment and to configure OpenClaw with the proxy endpoint and API key header. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw prompts and Azure API keys pass through this local proxy to the configured Azure OpenAI resource. <br>
Mitigation: Install only when that routing is intended, protect the OpenClaw configuration that contains the API key, and use a dedicated Azure OpenAI key with appropriate access controls. <br>
Risk: Changing the bind address from the default localhost setting can expose the proxy on a network. <br>
Mitigation: Keep AZURE_PROXY_BIND set to 127.0.0.1 unless network exposure is deliberate and separately protected. <br>
Risk: Enabling the optional systemd user service can keep the proxy running beyond the current shell session. <br>
Mitigation: Enable the service only when persistent operation is desired and review the service environment before starting it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BenediktSchackenberg/azure-proxy) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON configuration, and JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
