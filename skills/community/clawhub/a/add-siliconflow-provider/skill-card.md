## Description: <br>
Configures SiliconFlow as an OpenClaw model provider, including provider registration, model definitions, aliases, fallback setup, and validation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jooey](https://clawhub.ai/user/jooey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw administrators use this skill to add SiliconFlow-hosted chat models to an OpenClaw configuration and expose selected models through aliases and fallback chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider, alias, and fallback changes can alter which models OpenClaw uses for requests. <br>
Mitigation: Review the proposed OpenClaw configuration changes before applying them and validate the result with the documented OpenClaw checks. <br>
Risk: SiliconFlow API keys are required and could be exposed through shared terminals, chat transcripts, or unprotected configuration files. <br>
Mitigation: Use a dedicated API key, avoid pasting real keys into shared contexts, and protect the OpenClaw configuration file where the key is stored. <br>
Risk: Model pricing, free-tier availability, and rate limits may change outside the skill release. <br>
Mitigation: Verify current SiliconFlow pricing, free-tier limits, and account balance before relying on the configured models. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jooey/add-siliconflow-provider) <br>
- [SiliconFlow documentation](https://docs.siliconflow.cn) <br>
- [SiliconFlow pricing](https://siliconflow.cn/pricing) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes provider, alias, fallback, validation, and API utility guidance for OpenClaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
