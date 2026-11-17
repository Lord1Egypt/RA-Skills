# Agent-instruction rule block (adapt before use)

Copy ONE language variant of the block below into the target project's agent
instruction file (`AGENTS.md` / `CLAUDE.md` / equivalent), then adapt:

- Paths — move if the docs root differs (`docs/changelist/...` is the default).
- Language — match the project's docs language; delete the unused variant.
- "Verification passed" — name the project's real gate (tests, typecheck, build, live check). If it has none, define the strongest check it actually supports.
- Commit policy — if the project's general policy is "commit only when asked", place this block in its own section and state that it overrides the general policy; otherwise drop the auto-commit bullets.
- Author convention — for multi-person repos, fix ONE identity format (display name / username / employee id); single-person projects can delete the author bullets below.

## 中文（源形态）

### 变更记录（changelist，仅当改动本地代码且验证通过时写）

- 触发条件：同时满足「修改了本地代码」与「相关验证已通过」。二者缺一不写。
- 不触发：纯问答、纯文档修改、只读分析。这些情况直接答复，不写记录、不自动提交。
- 路径：`docs/changelist/{YYYYMMDD}/{slug}.md`，`{YYYYMMDD}` 为任务完成的本机日期，`{slug}` 为 kebab-case 任务短标题。
- 同任务同天合并为一个文件；跨天另开新文件。
- 内容：一行摘要、问题/根因、改动（文件 + 关键 diff）、设计决策/取舍、验证（真实命令 + 真实结果）。
- 多人协作：条目头部写「作者：{按项目约定的人类身份}」，目录条目行末尾标注（{作者}）。作者写人类负责人（发起/审核该任务的人），不写 AI；身份标识全项目统一并与 git author 对齐。
- 目录索引：写完后同步更新 `docs/changelist/README.md`，在对应「模块 > 子模块」下追加 `- [YYYY-MM-DD 标题](YYYYMMDD/slug.md)`（相对链接，按日期升序）。归属按本次改动的主要功能面判断；无合适子模块时新增子模块，无合适模块时新增模块，保持两级结构。README 更新随 changelist 文件进入同一 commit。

### 自动提交（如项目采用）

- changelist 写完后自动提交到当前分支，code/tests/changelist/README 进同一 commit。
- 用显式 pathspec，不 `git add -A`；要提交的文件含无关内容时停下报告。
- 提交信息不加任何 AI 署名 trailer。

## English mirror

### Change records (changelist — only when local code changed AND verification passed)

- Trigger: BOTH "local code changed" and "related verification passed". If either is missing, write nothing.
- Never triggered by: Q&A-only work, docs-only edits, read-only analysis — answer directly, no record, no auto-commit.
- Path: `docs/changelist/{YYYYMMDD}/{slug}.md` — `{YYYYMMDD}` is the local finish date, `{slug}` a kebab-case task title.
- One file per task per day; continue the same task on another day in a new file.
- Content: one-line summary, problem/root cause, changes (files + key diff), decisions/trade-offs, validation (real command + real result).
- Multi-person: every entry header carries `Author: {project-standardized human identity}`, and index entry lines end with the author tag. The author is the human owner of the task (who initiated or reviewed it), never an AI; one identity format project-wide, aligned with git author.
- Index: after writing, update `docs/changelist/README.md` under the matching module > submodule with `- [YYYY-MM-DD title](YYYYMMDD/slug.md)` (relative link, date ascending). Categorize by the change's primary functional surface; add a submodule when none fits, add a module when still none, keep two levels max. The index update lands in the same commit as the entry.

### Auto-commit (if the project adopts it)

- After the entry is written, auto-commit to the current branch: code + tests + entry + index in one commit.
- Explicit pathspec only, never `git add -A`; stop and report if intended files contain unrelated changes.
- No AI attribution trailers in commit messages.
