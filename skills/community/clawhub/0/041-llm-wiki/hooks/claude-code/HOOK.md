# Claude Code Integration

## Native Support

Claude Code works with llm-wiki out of the box via **protocol mode**:

```bash
# In Claude Code, just say:
"请摄入 sources/my-paper.pdf 到 wiki"
```

The agent will:
1. Read `CLAUDE.md` to understand the protocol
2. Execute the ingest workflow
3. Update wiki pages and log

## Optional: Project Settings

Create `.claude/settings.local.json` for project-specific preferences:

```json
{
  "context": {
    "files": ["CLAUDE.md", "AGENTS.md"]
  }
}
```

This ensures Claude Code always loads the protocol files.

## CLI Integration

If you want to use CLI commands from within Claude Code:

```bash
# Check if CLI is available
which python && python -c "from src.llm_wiki.core import WikiManager"

# If yes, you can use:
./scripts/wiki-status.sh
./scripts/wiki-lint.sh
```

## Verification

To verify llm-wiki is working:

1. Check `wiki/index.md` exists
2. Add a test file to `sources/`
3. Ask Claude: "请摄入 sources/test.md 到 wiki"
4. Verify `wiki/` has new content and `log.md` is updated
