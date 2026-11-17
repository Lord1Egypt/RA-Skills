---
name: changelist-adoption
description: Set up and run a per-task changelist practice in any repo: one doc per task under docs/changelist/YYYYMMDD/, a two-level module index, commit-coupled agent rules. Use when the user mentions changelists, change records, 变更记录, 变更日志, or 按任务记录变更 — to adopt, port, write entries, or maintain the index.
---

# Changelist Adoption / 变更记录实践落地

This skill is bilingual: read the `## English` section or the `## 中文版` section below — use whichever matches the user's and the target project's language. The two sections are semantic mirrors; keep them in sync when editing. Bundled templates in `assets/` and `references/` are bilingual as well (pick one variant per project); bundled scripts are language-neutral.

## English

### Purpose

Set up and run a per-task changelist practice in any repository. Every completed code task becomes a small standalone document (what broke, why, what changed, what was decided, how it was verified), and a module index links to every document so months of agent- and human-driven changes stay searchable by functional area instead of being buried in `git log`.

Two modes:

- **bootstrap** — first-time setup in a target project: taxonomy design, index skeleton, agent-instruction rules, optional backfill.
- **per-change** — the loop that runs after adoption: write entry → update index → commit together.

### The practice in one view

| Artifact | Path | Role |
| --- | --- | --- |
| Entry | `docs/changelist/{YYYYMMDD}/{slug}.md` | one task = one file, written only when code changed AND verification passed |
| Index | `docs/changelist/README.md` | module > submodule two-level taxonomy, one relative link per entry, date ascending |
| Rules | target agent instruction file (`AGENTS.md` etc.) | trigger conditions, paths, formats, commit coupling — so later tasks follow the practice without this skill being re-read |
| Commit | explicit pathspec | code + tests + entry + index land in the same commit |

A changelist is NOT a release `CHANGELOG.md`. The release changelog summarizes user-visible changes per version; a changelist entry is an engineering record of one task (root cause, diff, decisions, validation proof). Keep both if the project has both, and keep the release changelog rules untouched.

### Mode 1 — bootstrap

1. **Survey the target repo first.** Read its agent instruction file(s) and docs layout, and check how it runs tests and commits. Never paste the rule template verbatim: adapt paths, language (match the project's docs language), commit policy, and the definition of "verified" (if the project has no tests, define the strongest verification it actually supports and name it explicitly in the rules).
2. **Design the module taxonomy from the real architecture.** Derive 5–12 top-level modules from the source tree — services, plugins, channels, UI, infra, whatever that project actually has — not from generic guesses. Two levels max (module > submodule). Seed only modules you expect to fill; the taxonomy grows by rule when entries don't fit, never by speculation.
3. **Create the index skeleton** from `assets/index-template.md` at `docs/changelist/README.md` (or the target's docs-root equivalent): header with a stats line and the maintenance rules, then the module tree.
4. **Write the rules into the instruction file** from `references/agents-rules-template.md`, adapting everything listed in step 1. If the target already has a "commit only when asked" policy, the pasted block must state its precedence explicitly, e.g. in a dedicated section that overrides the general policy. For multi-person repos, also fix the author-identity convention now (see Multi-person collaboration).
5. **Backfill only on request.** Classifying git history into entries is expensive and usually low value; do not invent entries for past work from `git log` alone. If the project already has scattered change records (docs/, wiki exports, old notes), classify those into the index and verify links.
6. **Verify** with `scripts/verify-index.mjs` (see Verification), then commit per the target's policy.

### Mode 2 — per-change loop

Runs at task end, after verification passes, before the commit:

1. **Check the trigger.** An entry is required iff (local code changed) AND (related verification passed). No entry for pure Q&A, docs-only edits, or read-only analysis — answer or report directly, no record, no auto-commit.
2. **Write the entry** at `docs/changelist/{YYYYMMDD}/{slug}.md`:
   - `{YYYYMMDD}` = local date the task finishes; `{slug}` = short kebab-case title.
   - Same task, same day → one file; continuing the task the next day → new file.
   - Structure from `assets/entry-template.md`: one-line summary / problem & root cause / changes / decisions & trade-offs / validation.
   - Header carries an author line when the project tags authors (see Multi-person collaboration).
   - Validation must carry the real command and its real result (exit code or pass count), never "tested OK".
3. **Update the index in the same task.** Append `- [YYYY-MM-DD title](YYYYMMDD/slug.md)` (with the author tag when the project tags authors) under the matching module > submodule, date ascending within the section. Categorize by the change's PRIMARY functional surface — what a future reader would search by — not by which files were touched: a fix in shared infrastructure code that changes login-page behavior belongs under the login/auth module, not under shared infra. Nothing fits → add a submodule; still nothing → add a module. Never introduce a third level; split submodules instead.
4. **Commit together.** Code + tests + entry + index in one commit, explicit pathspec, never `git add -A`. If the files to commit contain unrelated changes, stop and report instead of sweeping them in. No AI attribution trailers in commit messages (a default of this practice; adapt only if the target's policy explicitly differs).
5. **Never rewrite old entries to "keep them current."** An entry records that day's decision; corrections and follow-ups go in a new entry.

### Multi-person collaboration

When several people (or their agents) land changes into the same repo:

- **Author line in every entry** (`- Author: {identity}` in the header). The author is the human owner of the task — whoever initiated or reviews it — never an AI name, even when an agent did the work. Match the commit's git author identity or the project's standardized naming.
- **Author tag on index lines** — `- [YYYY-MM-DD title](YYYYMMDD/slug.md) — {author}` — so the index answers "who has been touching this module" at a glance and supports per-person grep.
- **Fix the identity convention at bootstrap** (display name, username, or employee id) and write it into the rules block; inconsistent identities defeat per-person search. Single-person projects may drop author tagging entirely.
- **Same-day slug collision between authors** resolves as `{author}-{slug}.md`.
- **Index merge conflicts are normal** — everyone appends. Resolve mechanically: keep both sides, re-sort by date within the section; `verify-index.mjs` then proves no entry was dropped.

### Verification

After any index edit, run the bundled checker from the skill directory:

```bash
node <skill-dir>/scripts/verify-index.mjs <changelist-root>
```

It fails (exit 1) on any of: a link whose target file is missing, an entry file on disk not referenced by the index (orphan), or a file referenced more than once. Linked count must equal on-disk count.

### Quality bar

A good entry: names the observed problem and the actual root cause with file references; lists changes per file with the key diff; records decisions including rejected alternatives; shows the exact verification command and result. A bad entry: "fixed a bug", changes described without the why, no validation evidence, or content that just duplicates the PR description — the PR says what merged, the entry says what was diagnosed and decided.

### Installation

The skill directory is self-contained: `SKILL.md` plus `references/`, `assets/`, and `scripts/`. Install it in the repository that should adopt the practice at `.agents/skills/changelist-adoption/`, or user-globally at `~/.zcode/skills/changelist-adoption/` or `~/.agents/skills/changelist-adoption/`, then trigger it by asking to set up change records there. If that repo's agent instruction file already owns equivalent changelist rules, follow them directly instead of re-bootstrapping.

## 中文版

### 目的

在任何仓库中落地并持续运行「按任务记录变更（changelist）」的实践。每个完成的代码任务都沉淀为一篇独立的小文档（什么坏了、为什么、改了什么、做了什么决策、如何验证），目录索引链接到每一篇文档，让数月的 agent 与人工变更始终可以按功能模块检索，而不是埋没在 `git log` 里。

两种模式：

- **bootstrap** —— 在目标项目首次落地：模块分类设计、索引骨架、写入 agent 指令规则、按需回填历史。
- **per-change** —— 落地后的日常循环：写条目 → 更新索引 → 同 commit 提交。

### 实践全景

| 工件 | 路径 | 作用 |
| --- | --- | --- |
| 条目 | `docs/changelist/{YYYYMMDD}/{slug}.md` | 一个任务一个文件，仅在「改了代码」且「验证通过」时写 |
| 索引 | `docs/changelist/README.md` | 模块 > 子模块两级分类，每个条目一条相对链接，按日期升序 |
| 规则 | 目标项目的 agent 指令文件（`AGENTS.md` 等） | 触发条件、路径、格式、提交耦合 —— 让后续任务无需重读本 skill 也能遵守 |
| 提交 | 显式 pathspec | code + tests + 条目 + 索引进入同一 commit |

changelist 不是 release `CHANGELOG.md`。release changelog 按版本汇总用户可见变更；changelist 条目是单个任务的工程记录（根因、diff、决策、验证证据）。两者可以并存，且不要改动项目原有的 release changelog 规则。

### 模式一 —— 首次落地（bootstrap）

1. **先调研目标仓库。** 阅读它的 agent 指令文件与文档结构，弄清它如何跑测试、如何提交。不要原样粘贴规则模板：路径、语言（跟随项目文档语言）、提交策略、"验证通过"的定义都要适配（如果项目没有测试，就定义它实际支持的最强验证方式并在规则里写明）。
2. **从真实架构推导模块分类。** 从源码目录结构得出 5–12 个顶层模块 —— 服务、插件、通道、UI、基础设施，以该项目实际拥有的为准 —— 不要用通用猜测。最多两级（模块 > 子模块）。只预置预期会被填充的模块；分类靠规则增长（条目放不下时新增），绝不靠预判扩张。
3. **创建索引骨架。** 从 `assets/index-template.md` 在 `docs/changelist/README.md`（或目标项目文档根目录的等价位置）创建：头部为统计行与维护规则，之后是模块树。
4. **把规则写入指令文件。** 从 `references/agents-rules-template.md` 取规则块，按步骤 1 列出的所有点适配。如果目标项目已有"仅在被要求时才提交"的策略，粘贴的规则块必须显式声明优先级，例如放在独立 section 中声明覆盖通用策略。多人协作仓库还要在此定好作者身份标识约定（见「多人协作」）。
5. **仅在用户要求时回填历史。** 从 git 历史反推条目成本高且通常价值低；不要仅凭 `git log` 为过去的工作编造条目。如果项目已有散落的变更记录（docs/、wiki 导出、旧笔记），把它们归类进索引并校验链接。
6. **校验。** 用 `scripts/verify-index.mjs`（见「校验」），然后按目标项目的策略提交。

### 模式二 —— 单次变更循环

在任务收尾、验证通过之后、提交之前执行：

1. **判断触发条件。** 仅当（修改了本地代码）且（相关验证通过）才需要写条目。纯问答、纯文档修改、只读分析都不写 —— 直接答复或汇报，不记录、不自动提交。
2. **写条目** 到 `docs/changelist/{YYYYMMDD}/{slug}.md`：
   - `{YYYYMMDD}` 为任务完成当天的本机日期；`{slug}` 为 kebab-case 短标题。
   - 同任务同天一个文件；跨天继续同一任务则另开新文件。
   - 结构见 `assets/entry-template.md`：一行摘要 / 问题与根因 / 改动 / 设计决策与取舍 / 验证。
   - 项目启用作者标注时，头部写作者行（见「多人协作」）。
   - 「验证」必须写真实命令与真实结果（退出码或通过数），绝不写 "tested OK"。
3. **同一任务内更新索引。** 在对应「模块 > 子模块」下追加 `- [YYYY-MM-DD 标题](YYYYMMDD/slug.md)`（项目启用作者标注时行末带作者），小节内按日期升序。按变更的主要功能面归类 —— 即未来读者会用来检索的维度 —— 而不是按改动了哪些文件：共享基建代码里的修复如果改变的是登录页行为，应归入 login/auth 模块而不是 shared infra。都放不下 → 新增子模块；仍放不下 → 新增模块。绝不引入第三级；用拆分子模块代替。
4. **一起提交。** code + tests + 条目 + 索引进同一 commit，显式 pathspec，绝不 `git add -A`。待提交文件含无关改动时，停下报告而不是卷进去。提交信息不加 AI 署名 trailer（本实践默认；仅当目标项目策略明确不同才适配）。
5. **绝不重写旧条目来"保持最新"。** 条目记录的是当天的决策；修正与后续放新条目。

### 多人协作

多个人（或各自的 agent）向同一仓库提交变更时：

- **每个条目头部写作者行**（`- 作者：{身份}`）。作者写该任务的人类负责人 —— 发起或审核该任务的人 —— 永远不写 AI 名字，即使工作由 agent 完成。与同 commit 的 git author 身份一致，或遵循项目统一命名。
- **索引行标注作者** —— `- [YYYY-MM-DD 标题](YYYYMMDD/slug.md)（{作者}）` —— 让目录一眼可见"谁最近在动这个模块"，也支持按人 grep。
- **bootstrap 时定死身份标识**（花名 / 用户名 / 工号）并写进规则块；标识不一致会让按人检索失效。单人项目可以完全省略作者标注。
- **同日不同作者的 slug 冲突**以 `{author}-{slug}.md` 解决。
- **索引合并冲突是常态** —— 每个人都在追加。机械解法：两边都保留、小节内按日期重排；`verify-index.mjs` 可证明没有条目丢失。

### 校验

索引任何改动之后，运行自带校验脚本：

```bash
node <skill-dir>/scripts/verify-index.mjs <changelist-root>
```

以下任一情况即失败（退出码 1）：链接目标文件缺失、磁盘上的条目文件未被索引引用（孤儿）、同一文件被引用多次。linked 数必须等于 onDisk 数。

### 质量标准

好条目：写出观察到的现象与真实根因并引用文件；按文件列改动并附关键 diff；记录决策包括被否决的备选；给出确切的验证命令与结果。坏条目："fixed a bug" 式的含糊描述、只说改了什么不说为什么、没有验证证据、或只是复述 PR 描述 —— PR 说的是合入了什么，条目说的是诊断与决策过程。

### 安装

skill 目录自包含：`SKILL.md` 加 `references/`、`assets/`、`scripts/`。安装到要采用该实践的仓库 `.agents/skills/changelist-adoption/`，或全局 `~/.zcode/skills/changelist-adoption/`、`~/.agents/skills/changelist-adoption/`，然后在那个仓库里请求建立变更记录即可触发。如果目标仓库的指令文件已拥有等价的 changelist 规则，直接遵循该规则，不要重复落地。
