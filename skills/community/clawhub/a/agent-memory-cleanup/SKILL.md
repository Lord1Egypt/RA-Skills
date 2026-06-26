---
name: agent-memory-cleanup
description: Clean and audit long-term agent memory files such as user.md, memory.md, memories.md, profile.md, preferences.md, and agent_memory.md. Use when the user explicitly asks to clean, prune, sanitize, deduplicate, or review agent memory files, or when a memory write/update fails because the memory file is too long, full, over budget, rejected, duplicated, conflicted, stale, task-specific, or contains suspected secrets. Do not trigger for ordinary project docs, task notes, logs, code review, README edits, or general file cleanup. Applies edits only after explicit approval and creates recoverable backups.
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    os: [windows, macos, linux]
---

# Agent Memory Cleanup

This skill should be lightweight and low-noise. Do not require the user to know internal implementation names unless they ask. The user should still receive clear memory-state prompts, such as "memory appears too large, stale, duplicated, conflicted, or unsafe," when action is useful.

## Default Flow

1. Detect memory pressure or pollution.
2. If Python/file access is available, run a cheap summary check first:

```bash
python scripts/audit_memory.py memory.md --summary-json
```

3. If `quality.intervention` is `no_intervention_needed`, do not interrupt the user.
4. If intervention is needed, say briefly that memory appears too large, stale, duplicated, conflicted, or unsafe, and ask whether to review cleanup recommendations. Avoid implementation labels like the skill name unless the user asks.
5. After the user agrees, run:

```bash
python scripts/audit_memory.py memory.md --mode propose-patch --include-diff
```

6. Apply only after a second explicit approval, unless unattended cleanup was already authorized:

```bash
python scripts/audit_memory.py memory.md --mode apply-approved
```

The apply mode must create timestamped backups before writing.

## Trigger Points

Use this flow for:

- Memory write/update rejected, full, over budget, truncated, or too long.
- Short memory with secrets, task-state residue, duplicated facts, or conflicting preferences.
- User says a remembered fact is wrong, outdated, project-only, or should not be remembered.
- Before saving a new global memory candidate:

```bash
python scripts/audit_memory.py --candidate "candidate memory text" --summary-json
```

If candidate lint returns `do_not_write_candidate_to_global_memory`, do not store it globally. Offer to skip it or keep it as project/task notes.

## Intervention Values

- `prompt_cleanup_now_secret_detected`: recommend cleanup immediately; never echo raw secrets.
- `prompt_user_review_conflicting_memory`: ask the user to resolve conflicting durable preferences.
- `do_not_write_candidate_to_global_memory`: block global memory write.
- `prompt_cleanup_recommended`: offer cleanup recommendations.
- `prompt_audit_recommended`: mention memory quality may be degrading and ask whether to review.
- `no_intervention_needed`: stay silent.

## Load Extra Context Only When Needed

Do not read references by default. Load them only for the matching need:

- `references/default-rules.json`: deterministic thresholds and regex rules.
- `references/classification-rubric.md`: manual fallback if Python cannot run.
- `references/agent-paths.md`: path discovery when memory files are unclear.
- `references/mcp-version.md`: MCP wrapper design.

## Safety

- Keep only stable global preferences and durable cross-task context.
- Remove or redact secrets, stale task state, branch/PR/debug notes, and one-off plans.
- Do not rewrite clean memory just for style.
- Do not broadly scan the user home directory without explicit request.
- Back up every edited memory file.
