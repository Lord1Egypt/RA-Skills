# Session Migrate

Move sessions between project directories (e.g., main repo → worktree) and delete empty sessions.

## Quick Start

```bash
/session migrate                           # classify + move code sessions to worktree
/session migrate --dry-run                 # preview only, no changes
/session migrate <source> <target>         # specify source/target projects
```

## When to Use

- Reorganizing sessions after setting up a worktree
- Moving code-modification sessions to a worktree project while keeping infra sessions in main repo
- Bulk-deleting empty/tiny sessions

## Workflow

### 1. Identify Source and Target Projects

```bash
# List all project directories for the repo
ls -d ~/.claude/projects/*<repo-name>*
```

Typical projects for a repo with a worktree:

| Project | Path Pattern |
|---------|-------------|
| Main repo | `C--Users-es6kr-ghq-...-{repo}` |
| Worktree | `C--Users-es6kr-ghq-...-{repo}--claude-worktrees-{name}` |

### 2. Classify Sessions

For each `.jsonl` file in the source project, extract:

```bash
for f in "$SOURCE_DIR"/*.jsonl; do
  sid=$(basename "$f" .jsonl)
  msg_count=$(cat "$f" | grep -c '"type":"user"' || true)
  ew=$(cat "$f" | grep -c '"name":"Edit"\|"name":"Write"' || true)
  infra=$(grep -cE '\b(ssh|kubectl|docker|ansible|terraform|helm)\b' "$f" || true)
done
```

Classification categories:

| Category | Criteria | Default Action |
|----------|----------|---------------|
| **TINY** | msg_count <= 3 | Delete (AskUserQuestion) |
| **READ** | Edit/Write count = 0 | Keep in source |
| **CODE** | Edit/Write > 0, infra <= 5 | Move to target |
| **INFRA** | Edit/Write > 0, infra > 5 | Keep in source |

### 3. Present Classification via AskUserQuestion

Show counts per category and ask:

1. Which categories to move (CODE only, CODE+INFRA, date cutoff, etc.)
2. What to do with TINY sessions (delete or keep)

### 4. Execute

```bash
# Move sessions (JSONL + subagents dir)
mv "$SOURCE_DIR/$sid.jsonl" "$TARGET_DIR/$sid.jsonl"
[ -d "$SOURCE_DIR/$sid" ] && mv "$SOURCE_DIR/$sid" "$TARGET_DIR/$sid"

# Delete tiny sessions
rm "$SOURCE_DIR/$sid.jsonl"
[ -d "$SOURCE_DIR/$sid" ] && rm -r "$SOURCE_DIR/$sid"
```

### 5. Report

| Metric | Count |
|--------|-------|
| Moved to target | N |
| Deleted (TINY) | N |
| Remaining in source | N |
| Now in target | N |

## Limitations

- Session JSONL contains `projectPath` referencing the original project — file references inside may break
- Conversation content and summaries remain fully functional after move
- `sessions-index.json` is not updated (Claude Code rebuilds it automatically)

## Requirements

- Direct filesystem access to `~/.claude/projects/`
- AskUserQuestion for delete/move confirmation
