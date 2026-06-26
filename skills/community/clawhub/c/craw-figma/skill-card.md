## Description: <br>
Full bidirectional Figma integration for reading files via REST API, creating, modifying, and deleting layers through a local connector and Figma plugin, auditing accessibility, extracting design tokens, and exporting assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[missionarteemis-cloud](https://clawhub.ai/user/missionarteemis-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to let an agent inspect Figma files, generate or update design layers through Figma Desktop, extract design-system tokens, export assets, and check accessibility findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give a local AI workflow broad ability to edit, delete, or export content from the active Figma file. <br>
Mitigation: Use copies or versioned files, review commands before execution, and avoid sensitive customer or proprietary designs unless the access is required. <br>
Risk: The skill requires sensitive Figma credentials for REST API access. <br>
Mitigation: Store the token in an environment variable, use the least-privileged token available, and revoke or rotate it when the workflow is complete. <br>
Risk: The local connector enables real-time interaction with Figma while it is running. <br>
Mitigation: Verify connector code before running it, keep it local, and stop the connector when work is finished. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/missionarteemis-cloud/craw-figma) <br>
- [Figma REST API Reference](references/figma-api-reference.md) <br>
- [UI Design Patterns - Figma Best Practices](references/design-patterns.md) <br>
- [Figma Plugin API Overview](https://www.figma.com/plugin-docs/api/api-overview/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a Figma access token, Figma Desktop, and a local connector for write operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
