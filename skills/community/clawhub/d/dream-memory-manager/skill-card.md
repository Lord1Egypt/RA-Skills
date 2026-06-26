## Description: <br>
Actively maintains OpenClaw MEMORY.md by distilling daily memory notes, compressing stale context, preserving archived memories in a ledger, and indexing selected content for Obsidian. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teman2050](https://clawhub.ai/user/teman2050) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users use Dream to keep active memory concise while preserving older or completed memories in a searchable ledger. It is intended for agents that maintain personal or project memory files and need scheduled distillation, manual review, memory search, and Obsidian indexing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently rewrite MEMORY.md during scheduled or manual distillation. <br>
Mitigation: Review and back up OpenClaw memory files before enabling the 03:30 schedule or unattended memory maintenance. <br>
Risk: The permanent ledger is append-only and dream forget does not erase archived records. <br>
Mitigation: Do not use this skill for privacy-sensitive erasure workflows unless the ledger retention behavior is acceptable and separately governed. <br>
Risk: The skill writes memory and archive files under DREAM_VAULT_PATH and the OpenClaw workspace. <br>
Mitigation: Confirm DREAM_VAULT_PATH and OPENCLAW_WORKSPACE point to intended local locations before initialization or scheduled use. <br>


## Reference(s): <br>
- [Dream ClawHub release](https://clawhub.ai/teman2050/dream-memory-manager) <br>
- [Dream homepage](https://github.com/teman2050/dream-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and shell command guidance for OpenClaw memory, ledger, status, search, forget, and Obsidian indexing workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local file maintenance plans and commands; no network API output is described by the artifact.] <br>

## Skill Version(s): <br>
0.2.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
