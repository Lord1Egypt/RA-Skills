## Description: <br>
Configure OpenClaw to use Alibaba Cloud Bailian provider (Pay-As-You-Go or Coding Plan) through a strict interactive flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[extraterrest](https://clawhub.ai/user/extraterrest) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add, switch, or repair Alibaba Cloud Bailian and Qwen provider configuration in OpenClaw. It guides plan and site selection, API key validation, model selection, config backup, and OpenClaw JSON updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify OpenClaw provider configuration and optionally set Bailian as the default model provider. <br>
Mitigation: Review the target config path and default-provider choice before running; confirm the timestamped backup after any write. <br>
Risk: API keys may be exposed if stored inline in configuration or passed on the command line. <br>
Mitigation: Prefer environment-variable storage, avoid command-line API key arguments, and verify the selected environment variable is available before writing config. <br>
Risk: Selecting the wrong plan type, site, or endpoint can cause failed authentication or unavailable model IDs. <br>
Mitigation: Validate the API key against the selected site and compare the generated base URL and model list with the selected Pay-As-You-Go or Coding Plan option. <br>


## Reference(s): <br>
- [OpenClaw Alibaba Cloud Bailian Configuration](references/openclaw_alibaba_cloud.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run an interactive Python helper that writes OpenClaw provider configuration after validating the API key.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata, artifact metadata, and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
