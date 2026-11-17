## Description: <br>
Helps agents guide Azure basic resource management for virtual machines, storage accounts, virtual networks, network security groups, and resource groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and automation teams use this skill to prepare and review basic Azure resource management tasks such as creating or managing virtual machines, storage accounts, virtual networks, network security groups, and resource groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad Azure command execution and cloud resource changes. <br>
Mitigation: Use it only in a constrained Azure subscription or resource group, and grant service principals the minimum permissions needed. <br>
Risk: Azure operations may stop, delete, or change network-access resources. <br>
Mitigation: Require the agent to show a preflight plan and obtain explicit approval before destructive or network-impacting changes. <br>
Risk: Azure credentials or service principal secrets may be exposed if copied into project files. <br>
Mitigation: Store credentials in environment variables or a managed secret store, and avoid committing secrets to the workspace. <br>
Risk: The server security verdict is suspicious because safety scoping and confirmation guidance are insufficient. <br>
Mitigation: Review and constrain the skill before installation, especially before enabling execution tools against live Azure environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-toolkit-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples, configuration snippets, and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Azure resource operations that require credentials, scoped permissions, and explicit user approval before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
