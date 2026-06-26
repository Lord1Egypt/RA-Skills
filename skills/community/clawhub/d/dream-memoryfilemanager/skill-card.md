## Description: <br>
Dream actively distills OpenClaw memory into a bounded MEMORY.md, an append-only ledger, and optional Obsidian indexes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teman2050](https://clawhub.ai/user/teman2050) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and developers use Dream to keep long-term local memory compact, searchable, and periodically reviewed while preserving older context in a ledger. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains a long-lived local profile by persisting and rewriting personal memory. <br>
Mitigation: Use a private DREAM_VAULT_PATH, review MEMORY.md and ledger.md regularly, and avoid storing secrets or highly sensitive personal data. <br>
Risk: Forgotten content can remain in the append-only ledger even after active memory is cleared. <br>
Mitigation: Treat dream forget as active-memory cleanup only and manually review or purge ledger entries when permanent removal is required. <br>
Risk: No-confirm deletion and scheduled distillation can change memory files without an interactive checkpoint. <br>
Mitigation: Add backups or confirmation steps before using dream forget or scheduled distillation in environments where memory changes need review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teman2050/dream-memoryfilemanager) <br>
- [Project homepage](https://github.com/teman2050/dream-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown and text responses, plus local Markdown and JSON files maintained through shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to MEMORY.md, ledger files, metadata files, and Obsidian index files under the configured local workspace and DREAM_VAULT_PATH.] <br>

## Skill Version(s): <br>
0.2.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
