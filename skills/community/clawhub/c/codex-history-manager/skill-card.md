## Description: <br>
Search, read, export, hand off, clone, move, or rebind local Codex history stored under ~/.codex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[severinzhong](https://clawhub.ai/user/severinzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect local Codex sessions, export transcripts, create handoff notes, clone or move threads between workspaces, and rebind local provider metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exports, handoff notes, and backups can contain full conversation text, workspace paths, and local metadata. <br>
Mitigation: Treat generated files as sensitive, store them only in intended locations, and review them before sharing. <br>
Risk: Move, clone, and provider-rebinding commands can affect local Codex history metadata across one or many threads. <br>
Mitigation: Run dry runs first, review the affected thread counts and paths, and apply changes only after the scope matches the request. <br>
Risk: Dangerous history rewrites can modify stored conversation content. <br>
Mitigation: Generate a plan, present the warning and exact change list, and require explicit user approval before running the apply command. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/severinzhong/codex-history-manager) <br>
- [Command Details](references/commands.md) <br>
- [Write Safety and Backups](references/safety.md) <br>
- [Storage Model](references/storage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, jsonl, shell commands, guidance] <br>
**Output Format:** [Markdown, plain text, JSON, JSONL, and shell command proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local transcript exports, deterministic handoff notes, dry-run plans, and guarded apply commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
