## Description: <br>
One-stop enterprise AI assistant solution integrating Feishu and OpenClaw for quick deployment of smart customer service, group chat assistants, and workflow automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Enterprise developers and operators use this skill to deploy a Feishu bot connected to OpenClaw for customer support, group chat assistance, reminders, approvals, and daily report workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enterprise chat messages and assistant prompts may be sent to the configured OpenClaw endpoint. <br>
Mitigation: Confirm the data flow is allowed by the organization's data policy before connecting production chat channels. <br>
Risk: Feishu app credentials and OpenClaw API keys may be exposed through config files or shell history. <br>
Mitigation: Use environment variables or a secrets manager, protect config.json, and avoid recording secrets in command history. <br>
Risk: The webhook should not be exposed publicly without additional request controls. <br>
Mitigation: Add request verification, channel or user allowlists, rate limiting, and minimal Feishu app permissions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/enterprise-ai-assistant-bundle) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with shell commands, Python scripts, and JSON configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu application credentials and an OpenClaw API key; the deployment flow creates config.json and a skills directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
