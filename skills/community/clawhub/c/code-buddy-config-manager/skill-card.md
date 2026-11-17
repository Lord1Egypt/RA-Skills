## Description:

Auto-detect, install, update and verify all CodeBuddy configurations (MCP, Skill, Plugin, Model, CLI).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxc-dxc](https://clawhub.ai/user/dxc-dxc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect, install, update, and verify CodeBuddy MCP servers, skills, plugins, models, and CLI tools across project and global scopes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently modify CodeBuddy configuration files and system tooling from user-provided or discovered inputs.

Mitigation: Require explicit review and confirmation before package installation, MCP writes, plugin enablement, skill downloads, or global configuration changes.

Risk: Arbitrary or unverified URLs may provide unsafe configuration or skill content.

Mitigation: Prefer trusted marketplaces, pinned hashes or signatures, and reviewed source URLs; avoid arbitrary URLs for installation input.

Risk: Configuration changes may disrupt an existing CodeBuddy setup.

Mitigation: Back up ~/.codebuddy and project .codebuddy files before use and run the included status and verification checks after changes.

## Reference(s):

- [CodeBuddy configuration structure reference](references/config-structures.md)
- [ClawHub skill page](https://clawhub.ai/dxc-dxc/skills/code-buddy-config-manager)
- [Publisher profile](https://clawhub.ai/user/dxc-dxc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON status reports, verification reports, configuration snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform persistent CodeBuddy configuration changes when used by an agent with the requested permissions.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
