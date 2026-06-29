## Description: <br>
Use when preserving, searching, reviewing, or exporting user-owned agent memory across OpenClaw, Codex, Claude, OpenCode, Hermes, Qoder, Obsidian, and Git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wildprogrammer](https://clawhub.ai/user/wildprogrammer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Memory Sync to preserve local agent memory, conversation archives, handoff summaries, and personal knowledge into an owned Obsidian and Git memory layer. It helps review candidate memories, rebuild indexes and profiles, export cross-agent context, and optionally sync versioned memory assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect and persist broad local agent history, rule files, profile/config files, and skill inventories into an Obsidian vault and optionally Git. <br>
Mitigation: Install only when a local memory system is intended, keep the vault and any Git remote private, and review archived sources and staged files before sharing or publishing. <br>
Risk: Sensitive information can become durable memory if local conversations or configuration files include secrets, regulated data, or confidential material. <br>
Mitigation: Do not store API keys, passwords, private keys, regulated data, or confidential customer material as durable memory; review candidate memories before promotion. <br>
Risk: Git sync can publish memory artifacts beyond the local machine if push is enabled. <br>
Mitigation: Leave Git push disabled unless staged files and remote visibility have been reviewed, and enable remote push only intentionally. <br>
Risk: Cleanup can permanently delete generated Obsidian copies when hard-delete mode is enabled. <br>
Mitigation: Use the default recoverable trash cleanup mode and enable permanent deletion only after confirming the cleanup scope. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wildprogrammer/skills/agent-memory-sync) <br>
- [Clawdis Homepage](https://github.com/Wildprogrammer/memory-sync-skill) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Configuration Files](config/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON files with command-line workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local Obsidian vault content, memory indexes, profile/context exports, source archives, skill inventories, and optional Git commits when configured.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
