## Description: <br>
Structured memory system for OpenClaw agents with context death resilience, structured storage, Obsidian-compatible markdown, local semantic search, and session transcript repair. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pin-alt](https://clawhub.ai/user/pin-alt) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw agents use ClawVault to keep structured memory across sessions, recover from context loss, search local markdown vaults, and repair broken session transcripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and displays session identifiers and includes broad file, Git, and transcript mutation features beyond simple memory search. <br>
Mitigation: Review before installing, use a dedicated vault path, avoid storing secrets or customer/private data in memories, inspect shell-init output before appending it to shell startup files, and use --no-git on sleep unless repository-wide commit prompts are desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pin-alt/2026-02-10-clawhub-clawvault-1-5-1) <br>
- [README](README.md) <br>
- [Context Death Resilience](docs/context-death.md) <br>
- [Auto-Linking Spec](docs/auto-linking.md) <br>
- [ClawVault Hook](hooks/clawvault/HOOK.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [qmd](https://github.com/Versatly/qmd) <br>
- [npm package](https://www.npmjs.com/package/clawvault) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local vault markdown, checkpoint, handoff, index, and session-repair files when the recommended CLI commands are executed.] <br>

## Skill Version(s): <br>
1.5.1 (source: SKILL.md frontmatter, package.json, CHANGELOG; ClawHub release version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
