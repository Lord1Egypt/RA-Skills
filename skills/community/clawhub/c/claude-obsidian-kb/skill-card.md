## Description: <br>
Claude-Obsidian 知识引擎 helps an agent organize an Obsidian-style personal knowledge vault with raw, wiki, and output layers, frontmatter templates, bidirectional links, entity extraction, and maintenance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn notes, source material, and project knowledge into an Obsidian-style personal knowledge base with structured wiki pages, links, indexes, and maintenance reports. It is suited for personal knowledge management workflows where the agent can inspect and modify a local vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad automatic edits to an Obsidian-style vault. <br>
Mitigation: Use backups and preview or dry-run workflows before bulk changes. <br>
Risk: Persistent note metadata and cache files may expose private knowledge-base state. <br>
Mitigation: Keep vault caches private and review generated metadata before sharing notes. <br>
Risk: Private notes could be sent to external AI or API services if an agent adds that behavior. <br>
Mitigation: Do not allow private notes to leave the local environment unless the external service is explicitly disclosed and the user consents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zmy1006-sudo/claude-obsidian-kb) <br>
- [frontmatter 模板库](assets/frontmatter_templates.md) <br>
- [Claude-Obsidian × iBrain 整合方案](references/ibrain-integration.md) <br>
- [脚本使用指南](references/scripts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML frontmatter examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify markdown notes, indexes, cache files, and generated vault reports when run by an agent with filesystem access.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
