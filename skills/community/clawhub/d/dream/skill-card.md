## Description: <br>
Dream helps an OpenClaw agent maintain MEMORY.md by distilling daily memory notes, compressing active context, archiving older entries, and detecting memories that re-emerge after removal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teman2050](https://clawhub.ai/user/teman2050) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and agent operators use Dream to keep active memory concise while preserving a searchable long-term archive. It is intended for personal memory distillation, scheduled review, active-memory cleanup, and Obsidian-style indexing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dream can retain and rewrite sensitive personal memory data in MEMORY.md and the configured Dream vault. <br>
Mitigation: Choose a safe DREAM_VAULT_PATH, back up MEMORY.md before enabling reviews, and avoid storing secrets or highly sensitive personal data. <br>
Risk: The forget command clears active memory but does not remove entries from the permanent archive. <br>
Mitigation: Treat dream forget as active-memory cleanup and manually review archive files when full deletion is required. <br>
Risk: Scheduled reviews and broad natural-language triggers may update memory with limited confirmation. <br>
Mitigation: Prefer explicit dream commands, review memory changes regularly, and enable scheduled reviews only when persistent local memory maintenance is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teman2050/dream) <br>
- [Dream skill homepage](https://github.com/teman2050/dream-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown memory updates, shell command invocations, configuration steps, and concise status or search text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update MEMORY.md and append ledger, metadata, and Obsidian index files under the configured Dream vault.] <br>

## Skill Version(s): <br>
0.2.1 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
