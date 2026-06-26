## Description: <br>
Auto-detect, install, update and verify CodeBuddy configurations for MCP servers, skills, plugins, models, and CLI tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxc-dxc](https://clawhub.ai/user/dxc-dxc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CodeBuddy users use this skill to inspect, install, update, and validate persistent CodeBuddy configuration for project or global scopes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install packages, import remote configuration, and change persistent CodeBuddy settings. <br>
Mitigation: Use trusted URLs and known package names, review MCP JSON and skill or plugin changes before applying them, and treat global scope or CLI installs as high-impact changes. <br>
Risk: Search-derived installs or ambiguous package names can lead to incorrect or untrusted configuration. <br>
Mitigation: Prefer explicit user-provided sources and verify the source before installing or enabling a discovered component. <br>
Risk: Some configuration workflows may involve API keys, tokens, or other sensitive credentials. <br>
Mitigation: Avoid embedding secrets in shared configuration text and review generated or imported configuration before storing it. <br>


## Reference(s): <br>
- [CodeBuddy configuration structures](references/config-structures.md) <br>
- [ClawHub skill page](https://clawhub.ai/dxc-dxc/code-buddy-config-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status or verification reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in persistent CodeBuddy configuration changes when installation scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
