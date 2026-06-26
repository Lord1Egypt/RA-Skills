## Description: <br>
Configures OpenClaw model provider settings for Chinese AI APIs including DeepSeek, Qwen, Zhipu GLM, Moonshot, Baichuan, and Yi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ironmanc2014](https://clawhub.ai/user/ironmanc2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate provider configuration JSON for supported Chinese model APIs, compare model options, and apply those settings through OpenClaw's configuration workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider API keys may be exposed if entered in shared terminals, command history, logs, or CI sessions. <br>
Mitigation: Use dedicated provider API keys with spending limits, avoid shared or logged execution environments, and review handling of keys before applying generated configuration. <br>
Risk: Future prompts may be routed to third-party model providers after the generated configuration is applied. <br>
Mitigation: Install and configure the skill only when the user is comfortable sending prompts to the selected provider and has reviewed the generated config.patch. <br>
Risk: Incorrect provider or model choices can cause failed requests, unexpected costs, or lower-quality outputs. <br>
Mitigation: Review the generated provider JSON, compare provider pricing and model behavior, and apply the configuration through OpenClaw's config.patch workflow. <br>


## Reference(s): <br>
- [CN API Router ClawHub page](https://clawhub.ai/ironmanc2014/cn-api-router) <br>
- [Provider configuration reference](references/providers.md) <br>
- [DeepSeek platform](https://platform.deepseek.com) <br>
- [Alibaba Cloud DashScope](https://dashscope.aliyun.com) <br>
- [Zhipu GLM platform](https://open.bigmodel.cn) <br>
- [Moonshot platform](https://platform.moonshot.cn) <br>
- [Baichuan AI platform](https://platform.baichuan-ai.com) <br>
- [01.AI platform](https://platform.lingyiwanwu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates OpenClaw config.patch JSON that includes provider base URLs, API key placeholders or supplied keys, API type, and model metadata.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
