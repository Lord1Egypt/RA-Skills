## Description: <br>
Guides OpenClaw administrators through configuring SiliconFlow as an OpenAI-compatible model provider, including provider registration, model definitions, aliases, fallback setup, and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunerw-dev](https://clawhub.ai/user/sunerw-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw administrators use this skill to add SiliconFlow model access to an OpenClaw configuration. It helps define provider settings, model aliases, fallback behavior, and validation commands for the integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SiliconFlow API key is a secret used in provider configuration. <br>
Mitigation: Store and handle the API key as a secret, and avoid committing it to shared configuration files or logs. <br>
Risk: Fallback configuration changes can alter model routing behavior in OpenClaw. <br>
Mitigation: Review fallback changes before applying them and run the documented OpenClaw validation commands after configuration. <br>
Risk: Prompts and metadata sent through the configured provider may leave the local system for SiliconFlow's service. <br>
Mitigation: Use the provider only for workloads where sending data to SiliconFlow is acceptable under the user's data handling requirements. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sunerw-dev/add-siliconflow-provider-1) <br>
- [Publisher profile](https://clawhub.ai/user/sunerw-dev) <br>
- [SiliconFlow](https://siliconflow.cn) <br>
- [SiliconFlow documentation](https://docs.siliconflow.cn) <br>
- [SiliconFlow pricing](https://siliconflow.cn/pricing) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw provider configuration, model alias examples, fallback guidance, and SiliconFlow API verification commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
