# Daily Ops (Minimal)

Use `scripts/kb_daily.sh` for common day-to-day operations.

## Commands

> Optional shortcut:
> `export PATH="$HOME/.openclaw/workspace/bin:$PATH"`
> Then use `kb ...` instead of `bash scripts/kb_daily.sh ...`.
> (or set `OPENCLAW_WORKSPACE` and point PATH to `$OPENCLAW_WORKSPACE/bin`).

### 1) Add a source

```bash
bash scripts/kb_daily.sh add --source "https://arxiv.org/abs/2602.12430" --tags "ai,llm,agent"
```

Optional:
- `--repo ai-research`
- `--type paper|article|repo|spreadsheet|file`
- `--title "..."`
- `--notes "..."`
- `--no-build` / `--no-summarize`

---

### 2) Ask a question

```bash
bash scripts/kb_daily.sh ask --question "MCP agent security tradeoffs" --repo ai-research --top-k 8
```

Optional:
- `--format md|marp`
- `--file-back --target-concept mcp`
- `--root /path/to/kb` (override repo root)

---

### 3) Health check

```bash
bash scripts/kb_daily.sh check
```

Optional:
- `--repo ai-research`

---

## Notes

- Config file: `knowledge-bases/config/repos.json`
- Wrapper uses KB venv python when available:
  - `$OPENCLAW_WORKSPACE/.venvs/duru-kb/bin/python`
  - fallback: `$HOME/.openclaw/workspace/.venvs/duru-kb/bin/python`
- If venv python is missing, it falls back to `python3`.
