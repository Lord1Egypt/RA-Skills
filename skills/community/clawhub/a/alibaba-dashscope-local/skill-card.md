## Description: <br>
Configure OpenClaw to use Alibaba Cloud Bailian provider (Pay-As-You-Go or Coding Plan) through a strict interactive flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[papabearclaw](https://clawhub.ai/user/papabearclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add, switch, or repair OpenClaw configuration for Alibaba Cloud DashScope/Qwen models. It guides plan and site selection, validates a DashScope API key, backs up existing configuration, and writes provider settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles paid DashScope credentials and can write them into local agent configuration. <br>
Mitigation: Prefer environment-variable storage, keep OpenClaw configuration and backups private, and rotate the DashScope key if it may have been exposed. <br>
Risk: Pay-As-You-Go model calls can incur charges even when generated configuration examples list zero costs. <br>
Mitigation: Verify Alibaba Cloud billing terms and model pricing before using the configured provider. <br>
Risk: Bundled metadata differs from the registry context. <br>
Mitigation: Review the ClawHub publisher/package identity before installing or running the setup flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/papabearclaw/alibaba-dashscope-local) <br>
- [OpenClaw Alibaba Cloud Bailian Configuration](artifact/references/openclaw_alibaba_cloud.md) <br>
- [Pay-As-You-Go China endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>
- [Pay-As-You-Go International endpoint](https://dashscope-intl.aliyuncs.com/compatible-mode/v1) <br>
- [Pay-As-You-Go US endpoint](https://dashscope-us.aliyuncs.com/compatible-mode/v1) <br>
- [Coding Plan China endpoint](https://coding.dashscope.aliyuncs.com/v1) <br>
- [Coding Plan International endpoint](https://coding-intl.dashscope.aliyuncs.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON configuration output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update local OpenClaw-style JSON configuration and create timestamped backups when the bundled setup script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
