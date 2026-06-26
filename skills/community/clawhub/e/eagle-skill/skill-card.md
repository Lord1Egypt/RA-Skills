## Description: <br>
Control Eagle application for digital asset management - search, organize, tag items, manage folders and tag groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roaycl](https://clawhub.ai/user/roaycl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a local Eagle digital asset library from an agent, including searching assets, organizing folders, and managing item tags and tag groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change an Eagle library through bulk edits, trash moves, tag merges, tag group deletion, and folder or tag changes. <br>
Mitigation: Require explicit user confirmation before running broad or destructive operations, and preview target item, folder, tag, or group IDs where practical. <br>
Risk: The CLI can target a custom Eagle server URL through configuration. <br>
Mitigation: Use the default trusted local endpoint unless the user intentionally sets a trusted EAGLE_SERVER_URL or server flag. <br>
Risk: AI Search commands require the Eagle AI Search plugin and may be unavailable or still syncing. <br>
Mitigation: Check AI Search status before semantic or similarity searches and fall back to normal item queries when the plugin is not ready. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/roaycl/eagle-skill) <br>
- [App Tools](references/app-tools.md) <br>
- [Item Tools](references/item-tools.md) <br>
- [Folder Tools](references/folder-tools.md) <br>
- [Tag Tools](references/tag-tools.md) <br>
- [Tag Group Tools](references/tag-group-tools.md) <br>
- [AI Search Tools](references/ai-search-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a local Eagle API server and return JSON or text responses from the CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
