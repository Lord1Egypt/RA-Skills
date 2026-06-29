# Tool Fallback Master Table

## Tool Fallbacks

| Tool | Primary | Fallback 1 | Fallback 2 | Fallback 3 |
|------|---------|------------|------------|------------|
| Codebase discovery | `exec find` | `exec ls -R` | Read key files | Skip |
| `update_plan` | Normal call | Mental plan | STATE.md note | Skip |
| ACP coding agent | Cursor ACP | Cursor CLI | Alternative ACP | Manual `edit` |
| Sub-agent | Sub-agent | Web search | Memory search | Ask human |
| `edit` tool | `edit` tool | `exec sed` | `write` full file | Manual |
| Build | `npm run build` | `tsc --noEmit` | `node --check` | Skip |
| Test | Test suite | Specific file | Manual | Document |
| Vision Q&A | Cloud vision | Local vision | Laptop | Describe |
| Browser | Browser tool | `curl` | Describe | Skip |
| Memory search | Semantic | `lcm_grep` | `exec grep` | Skip |
| Workboard | workboard tools | STATE.md | In-memory | Skip |

## Script Fallbacks

| Script | Fallback |
|--------|----------|
| `log-session.sh` | Manual append to `session_log.md` |
| `log-decision.sh` | Manual ADR in `.planning/ADRs/` |
| `check-prices.sh` | Manual `web_fetch` |
| `test-model.sh` | Manual API probe |
| `init-project.sh` | Manual `mkdir` + file creation |
| `discover-models.sh` | Manual provider check |
