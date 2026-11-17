## Description: <br>
Deploy AI models as PAI-EAS inference services for LLM, image generation, speech synthesis, and related model-serving workloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to select Alibaba Cloud PAI-EAS images and resources, build service configuration JSON, deploy a new inference service with Aliyun CLI, and report service status and invocation endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can provision paid Alibaba Cloud inference services. <br>
Mitigation: Use a tightly scoped account, budget controls, least-privilege RAM credentials, and explicit approval before create-service. <br>
Risk: Deployment output can expose live service access tokens in chat or logs. <br>
Mitigation: Redact AccessToken values before sharing output, keep deployment logs private, and rotate tokens if they are exposed. <br>
Risk: CLI setup can modify the local Aliyun CLI/plugin installation and may use a curl-to-bash installer. <br>
Mitigation: Install or update the CLI through a trusted channel, verify the installer independently, and run the workflow in a controlled environment. <br>
Risk: Shared gateway endpoints may be publicly reachable without authentication by default. <br>
Mitigation: Prefer private or authenticated endpoints and configure token authentication or VPC-only access for deployed services. <br>
Risk: The workflow requires broad cloud discovery permissions plus service creation permissions. <br>
Mitigation: Use a dedicated deployment role limited to the documented EAS, AIWorkspace, OSS, VPC, ECS, and NLB actions required for the target environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-pai-eas-service-deploy) <br>
- [Deployment Workflow](references/deployment-workflow.md) <br>
- [Service Config Field Reference](references/config-schema.md) <br>
- [Complete Config Pattern Examples](references/config-patterns.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Service Invocation Examples](references/service-invoke-examples.md) <br>
- [API Reference](references/api-reference.md) <br>
- [Model-Image Matching Guide](references/model-image-matching.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, bash commands, and deployment result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated service JSON, Aliyun CLI commands, validation findings, service status, endpoints, and invocation examples.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
