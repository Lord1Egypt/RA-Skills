## Description: <br>
Enables OpenAI Codex CLI to use Chinese mainland AI model providers through protocol conversion and automatic Codex configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckKiven](https://clawhub.ai/user/luckKiven) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers use this skill to configure Codex CLI to route requests through a local protocol bridge to supported providers such as Aliyun Qwen, Kimi, and GLM. It is intended for coding and general assistant workflows where those providers are approved for the user's data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Codex prompts, conversation content, and related request data may be sent to configured third-party model providers. <br>
Mitigation: Use only with data approved for those providers, and avoid secrets, regulated data, or proprietary code unless provider terms, retention settings, and data-handling controls are approved. <br>
Risk: Provider API keys are required and can be exposed if copied into public files or shared environments. <br>
Mitigation: Store keys in the documented private environment file or user environment variables, and do not publish or share files containing real keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luckKiven/codex-cn-bridge) <br>
- [Source repository](https://github.com/luckKiven/codex-cn-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, service-control, model-selection, and troubleshooting guidance for Codex CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
