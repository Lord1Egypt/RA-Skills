# publish plan

## Release positioning

Suggested public positioning:

> Local-first memory retrieval for agent workspaces.
> Markdown-based memory store, Chinese-friendly anchors, auto rebuild, optional rerank, and explainable retrieval.

## Before publishing to ClawHub

- [ ] run smoke tests on a fresh workspace
- [ ] confirm workspace auto-detection works outside the current repo
- [ ] add example output snippets to docs
- [x] add regression queries for Chinese + mixed English anchors
- [ ] decide whether to include rerank as optional or disabled-by-default in public docs
- [ ] package and inspect the generated archive for accidental private files
- [ ] verify no secrets, local paths, or user-specific examples leak into the skill

## Suggested smoke tests

```bash
python scripts/agent_memory_local.py doctor
python scripts/agent_memory_local.py build-index
python scripts/agent_memory_local.py query "记忆检索 主路由" -k 5
python scripts/agent_memory_local.py smart-query "飞书昨天为什么断联了" -k 5
```

## Suggested future release notes

### v0.1.0
- initial public release
- local Markdown memory indexing
- direct retrieval + smart query rewrite
- auto rebuild and explainable retrieval
- optional rerank enhancement
