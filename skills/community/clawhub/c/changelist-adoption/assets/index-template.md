# Changelist index template

Create this file at the target project's `docs/changelist/README.md` (or docs-root
equivalent). Pick ONE language variant, fill the stats line after each index update,
and seed the module tree from that project's real architecture (5–12 top-level
modules, submodules only where entries are expected soon).

## 中文

```markdown
# Changelist 目录

按功能模块两级分类索引全部变更记录，条目链接指向对应文档，方便按模块快速定位。
共 {N} 篇（{最早日期} ~ {最新日期}）。

维护规则（与 {AGENTS.md 的规则 section} 保持一致）：

- 新增 changelist 后，同步在本目录对应「模块 > 子模块」下追加一行：
  `- [YYYY-MM-DD 标题](YYYYMMDD/slug.md)`（相对链接，按日期升序）。
- 归属按本次改动的主要功能面判断；无合适子模块时新增子模块，无合适模块时新增模块，保持两级结构。
- 多人协作项目在条目行末尾标注作者，格式 `- [YYYY-MM-DD 标题](YYYYMMDD/slug.md)（{作者}）`；单人项目可省略。
- 该 README 的更新随 changelist 文件一起进入同一 commit。

## 1. {模块 A}

### 1.1 {子模块 a}

- [YYYY-MM-DD {标题}](YYYYMMDD/{slug}.md)（{作者}）

### 1.2 {子模块 b}

## 2. {模块 B}

### 2.1 {子模块 a}
```

## English

```markdown
# Changelist Index

All change records indexed by functional module in two levels; each entry links to
its document for fast lookup by area. {N} entries ({earliest} ~ {latest}).

Maintenance rules (kept in sync with the rules section in {AGENTS.md}):

- After adding a changelist entry, append one line under the matching
  module > submodule: `- [YYYY-MM-DD title](YYYYMMDD/slug.md)` (relative link,
  date ascending).
- Categorize by the change's primary functional surface; add a submodule when
  none fits, add a module when still none; two levels max.
- In multi-person projects, tag the author at the end of each entry line:
  `- [YYYY-MM-DD title](YYYYMMDD/slug.md) — {author}`; single-person projects
  may omit it.
- This README update lands in the same commit as the entry.

## 1. {Module A}

### 1.1 {Submodule a}

- [YYYY-MM-DD {title}](YYYYMMDD/{slug}.md) — {author}

### 1.2 {Submodule b}

## 2. {Module B}

### 2.1 {Submodule a}
```
