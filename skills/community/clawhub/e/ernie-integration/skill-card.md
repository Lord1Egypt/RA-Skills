## Description:

Step-by-step guide for integrating Baidu ERNIE 5.0 (Qianfan) models into Clawdbot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattheliu](https://clawhub.ai/user/mattheliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Baidu Qianfan as a Clawdbot model provider and verify ERNIE 5.0 model access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill helps configure an external Baidu Qianfan API provider and requires handling an API key.

Mitigation: Install only when Baidu Qianfan is an intended model provider, store the key in a secret manager or tightly permissioned local secrets file, and avoid exposing the full key in logs, screenshots, or support transcripts.

## Reference(s):

- [Configuration Examples](references/config-examples.md)
- [Baidu Qianfan Documentation](https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html)
- [Qianfan API Reference](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Fm2vrveyu)
- [Clawdbot Model Providers](https://docs.openclaw.ai/concepts/model-providers)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API-key environment variable guidance, provider configuration examples, model selection commands, and troubleshooting checks.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
