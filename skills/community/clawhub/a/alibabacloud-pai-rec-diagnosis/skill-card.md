## Description: <br>
Alibaba Cloud PAI-Rec Engine Diagnostic and Configuration Validation Skill for diagnosing PAI-Rec engine interface issues and validating engine configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to troubleshoot Alibaba Cloud PAI-Rec engine API behavior, inspect related EAS logs and engine configuration, and validate PAI-Rec configuration files before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud CLI access to inspect PAI-Rec services, logs, and configurations, which can expose sensitive operational data if permissions are too broad. <br>
Mitigation: Use a dedicated low-privilege RAM user or role and prefer the resource-specific read-only policy described in the bundled RAM policy reference. <br>
Risk: Raw diagnostic logs and engine configurations can contain credentials, tokens, request payloads, customer identifiers, or internal endpoints. <br>
Mitigation: Redact sensitive data before sharing output and use the bundled sanitizer before displaying retrieved configuration details. <br>
Risk: The workflow requires Aliyun CLI plugin updates, which can change local execution behavior. <br>
Mitigation: Review and approve CLI/plugin updates before running the workflow in a production environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-pai-rec-diagnosis) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Config Validation](references/config-validation.md) <br>
- [PAI-Rec Engine Configuration Examples](references/configuration-examples.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [Troubleshooting Guide](references/troubleshooting-guide.md) <br>
- [Verification Methods](references/verification-method.md) <br>
- [PAI-Rec Configuration Schema](references/schema.json) <br>
- [EAS API Reference](https://www.alibabacloud.com/help/eas/developer-reference/) <br>
- [PAI-RecService API Reference](https://www.alibabacloud.com/help/pai/developer-reference/) <br>
- [Aliyun CLI User Guide](https://www.alibabacloud.com/help/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate transient diagnostic files locally and should show only sanitized configuration or log output.] <br>

## Skill Version(s): <br>
0.0.3 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
