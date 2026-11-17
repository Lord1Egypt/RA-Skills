## Description:

asclaude-compact helps an OpenClaw agent compact long local sessions by archiving conversation JSONL, creating Markdown summaries, and clearing older tool results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miaoxingjun](https://clawhub.ai/user/miaoxingjun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to manage long-running local agent conversations by archiving sessions, retaining concise Markdown memory, and reducing old tool output. It is most relevant when conversation history has grown large or when prior decisions need to be preserved outside the active context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session archives, Markdown summaries, and backup files may persist sensitive conversation content, private code, credentials, or personal data on disk.

Mitigation: Run the skill only on sessions appropriate for local persistence, review generated files before sharing, and delete archives, summaries, and backups when they are no longer needed.

Risk: The security evidence reports an unvalidated session-id path issue that can read or rewrite out-of-scope JSONL files.

Mitigation: Use only trusted session IDs and avoid path-like or user-supplied session arguments until the session-id handling is constrained and validated.

Risk: Micro-compaction rewrites session files after creating a backup, which can remove older tool-result content from the active session history.

Mitigation: Confirm that the backup exists before relying on the compacted session, and restore from the backup if important tool output was cleared.

Risk: The packaged workspace_search.py artifact appears incomplete and may fail if invoked.

Mitigation: Treat workspace search behavior as unavailable unless the script is corrected and tested separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miaoxingjun/skills/asclaude-compact)
- [Publisher profile](https://clawhub.ai/user/miaoxingjun)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands; scripts produce terminal output, JSONL archives, backups, and Markdown summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against OpenClaw session files and may persist archives, summaries, and backups on disk.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
