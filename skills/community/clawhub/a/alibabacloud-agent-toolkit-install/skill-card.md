## Description:

Installs the Alibaba Cloud Agent Toolkit end to end by checking prerequisites, authentication, CLI plugins, MCP Server Core, bearer-token exchange, and then using the current client's supported plugin mechanism.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Alibaba Cloud CLI and MCP prerequisites, verify authentication and token exchange, and install the Alibaba Cloud Agent Toolkit for their local agent client.

### Deployment Geography for Use:

Global; one cloud-resource check/create step targets Alibaba Cloud region cn-hangzhou.

## Known Risks and Mitigations:

Risk: The skill installs persistent local CLI tools and agent plugins from remote sources that may change after review.

Mitigation: Require explicit user approval before install steps and prefer version-pinned releases with published checksums or signatures.

Risk: Some setup steps can modify Alibaba Cloud account resources or depend on RAM permissions.

Mitigation: Explain the affected cloud resource before execution, verify the active identity, and use the documented RAM policy guidance when permission errors occur.

Risk: Running installer commands from an elevated shell can increase local system impact.

Mitigation: Avoid elevated shells unless required and review each installer command before approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-agent-toolkit-install)
- [Publisher profile](https://clawhub.ai/user/sdk-team)
- [RAM Policies](references/ram-policies.md)
- [Alibaba Cloud Agent Toolkit repository](https://github.com/aliyun/alibabacloud-agent-toolkit.git)
- [RAM Applications Console](https://ram.console.aliyun.com/applications?activeTab=ThirdParty)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confirmation-gated local install, cloud-resource creation, and plugin installation steps.]

## Skill Version(s):

0.0.2 (source: evidence release version and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
