## Description: <br>
Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aceundefeated](https://clawhub.ai/user/aceundefeated) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who manage Obsidian vaults use this skill to locate active vaults, search notes, and perform note create, move, rename, delete, and direct Markdown-edit workflows through obsidian-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to search local Obsidian notes, which may expose private note content. <br>
Mitigation: Run it only against vaults you intend the agent to inspect and review search terms and results before sharing them. <br>
Risk: The skill can guide create, move, edit, or delete operations on vault files. <br>
Mitigation: Confirm the active vault and exact note path before approving changes, and keep backups for important notes. <br>
Risk: The workflow depends on obsidian-cli installed from a Homebrew source. <br>
Mitigation: Install obsidian-cli only from a source you trust before allowing the agent to rely on it. <br>


## Reference(s): <br>
- [Obsidian Help](https://help.obsidian.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local Obsidian note searches and file-changing obsidian-cli commands for user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
