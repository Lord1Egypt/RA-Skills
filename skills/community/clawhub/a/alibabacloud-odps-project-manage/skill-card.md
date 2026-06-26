## Description: <br>
Alibaba Cloud MaxCompute Project Management Skill for creating, querying, and listing MaxCompute projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud MaxCompute projects through guided Aliyun CLI workflows for listing, inspecting, creating, and verifying projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide creation of Alibaba Cloud MaxCompute resources that may incur cost. <br>
Mitigation: Require explicit user approval before resource creation and confirm region, project name, quota, and command body before execution. <br>
Risk: The skill depends on Alibaba Cloud credentials and permissions. <br>
Mitigation: Use least-privilege or temporary credentials, verify only masked credential status, and never display access key or secret values. <br>
Risk: Setup steps may install or update the Aliyun CLI and plugins, including enabling automatic plugin installation. <br>
Mitigation: Prefer a verified package-manager or signed installer path, review plugin state after use, and disable automatic plugin installation when it is no longer needed. <br>
Risk: Evidence notes broader and riskier actions in setup and references than the main project-management description promises. <br>
Mitigation: Keep execution scoped to supported list, get, and create workflows, and do not run project deletion commands. <br>


## Reference(s): <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Alibaba Cloud MaxCompute API Reference](https://api.aliyun.com/product/MaxCompute) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided region, project name, quota selection, and configured Alibaba Cloud credentials.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
