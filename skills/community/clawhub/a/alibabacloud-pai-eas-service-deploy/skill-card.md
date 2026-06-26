## Description: <br>
Deploy AI models as Alibaba Cloud PAI-EAS inference services, including LLM, image generation, speech synthesis, and related model-serving deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML platform engineers use this skill to configure, validate, and deploy AI models as Alibaba Cloud PAI-EAS inference services using Aliyun CLI workflows. It covers image and GPU spec validation, service JSON construction, service creation, endpoint discovery, and invocation reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make high-impact Alibaba Cloud changes, including service creation, plugin installation, and CLI configuration changes. <br>
Mitigation: Review before installing, use an isolated environment where possible, and personally confirm service creation, plugin installation, CLI configuration, or delete/recreate actions before execution. <br>
Risk: Live service tokens may appear in normal output. <br>
Mitigation: Do not print or store real service tokens in chat logs; redact tokens in shared output and prefer HTTPS or private endpoints. <br>
Risk: The skill requires sensitive cloud credentials and broad deployment permissions. <br>
Mitigation: Use a least-privilege RAM user, avoid root or broad account credentials, and grant only the permissions needed for the target deployment. <br>
Risk: The server security verdict is suspicious even though risk findings are empty. <br>
Mitigation: Review the skill and its referenced behavior before installation and execution. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/sdk-team/alibabacloud-pai-eas-service-deploy) <br>
- [Deployment Workflow](references/deployment-workflow.md) <br>
- [Service Config Field Reference](references/config-schema.md) <br>
- [Complete Config Pattern Examples](references/config-patterns.md) <br>
- [Network Configuration Rules](references/network-config.md) <br>
- [Storage Mount Configuration Guide](references/storage-mount.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [Model-Image Matching Guide](references/model-image-matching.md) <br>
- [Verification Methods](references/verification-method.md) <br>
- [Service Invocation Examples](references/service-invoke-examples.md) <br>
- [Related API List](references/related-apis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployment summaries, endpoint details, service invocation examples, and validation guidance.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
