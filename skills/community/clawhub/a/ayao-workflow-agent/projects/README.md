# 项目记忆库

每个项目一个目录，目录名即 slug（通常是 GitHub repo 名）。

- `context.md` — 项目背景、架构决策、注意事项（由 cc-plan 或人工维护）
- `retro.jsonl` — 每个 swarm 任务完成后自动追加的回顾记录

## Slug 约定

读取 `swarm/active-tasks.json` 里 `repo` 字段的最后一段路径，或直接用 `project` 字段。
