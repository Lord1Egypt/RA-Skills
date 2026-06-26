## Description: <br>
Use when preserving, searching, reviewing, or exporting user-owned agent memory across OpenClaw, Codex, Claude, OpenCode, Hermes, Qoder, Obsidian, and Git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wildprogrammer](https://clawhub.ai/user/wildprogrammer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Memory Sync to preserve local agent conversations, memory signals, handoff summaries, profiles, and skill inventories into an Obsidian and Git-backed memory layer they control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect broad local chat history, prompts, project details, local paths, and inferred profile data into a memory vault. <br>
Mitigation: Install only when a local cross-agent memory vault is intended, review the vault path before use, and treat generated vault contents as sensitive. <br>
Risk: Git sync can push sensitive memory assets to a remote repository. <br>
Mitigation: Set GIT_PUSH_ENABLED=false unless pushing is intentional, review the Git remote, and avoid public remotes for memory vaults. <br>
Risk: Conversation scanning can store more transcript data than expected. <br>
Mitigation: Avoid scanning conversations or using --all until the user is comfortable storing those transcripts. <br>
Risk: Vault cleanup behavior can delete generated vault content. <br>
Mitigation: Review Memory Sync status and generated indexes before cleanup, and keep Git history or backups for sensitive vaults. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/Wildprogrammer/memory-sync-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Obsidian memory pages, machine-readable indexes, portable agent context, profile exports, skill inventories, and optional Git sync commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
