## Description: <br>
Aliyun AI Guardrail installs and configures an OpenClaw hook that checks LLM request messages with Alibaba Cloud AI Guardrail and masks blocked user content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aliyun-ai-sec](https://clawhub.ai/user/aliyun-ai-sec) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install an always-on guardrail hook that screens LLM request content through Alibaba Cloud AI Guardrail before prompts reach a model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installed hook can inspect and rewrite LLM-style requests and send prompt text to Alibaba Cloud. <br>
Mitigation: Install only after privacy and compliance review, confirm users accept cloud inspection of prompt text, and document how to disable or remove the hook. <br>
Risk: Alibaba Cloud AccessKey credentials may be stored in OpenClaw configuration. <br>
Mitigation: Use a least-privilege key, protect configuration files or use a secret manager where possible, and rotate keys after testing or suspected exposure. <br>
Risk: The guardrail may pass requests through when the cloud check times out or errors. <br>
Mitigation: Do not rely on this hook as the only enforcement layer; monitor failures and pair it with additional local policy or review controls for sensitive deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aliyun-ai-sec/aliyun-ai-guardrail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides installation of an OpenClaw hook, collection of Alibaba Cloud AccessKey credentials, environment configuration, and gateway restart.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
