---
name: gbrain-obsidian-vault
version: 1.0.0
homepage: https://github.com/spikesubingrui-design/gbrain-obsidian-vault
clawhub_slug: gbrain-obsidian-vault
description: >-
  把 Obsidian 变成 OpenClaw memory + gbrain 知识图谱的可视化 GUI：单 vault、wikilink 图谱、
  memory 日记软链、DB 页面物化导出，编辑仍回灌 sync/embed。触发词：obsidian脑库 / 第二大脑可视化 /
  gbrain obsidian / memory图谱 / 连点成面 / second brain vault
metadata:
  openclaw:
    emoji: "💎"
---

# GBrain Obsidian Vault — 给 AI 记忆装上「能看见的脑」

> **问题**：OpenClaw 的 `memory_search` 和 gbrain 的 Postgres 图谱对 agent 可见，对人不可见。  
> **解法**：Obsidian 打开 gbrain wiki 作 vault，软链 `memory/` 日记进来，可选 `gbrain export` 把 DB 页面物化成 markdown——**一套文件，三路索引**。

## 何时加载本 Skill

- 用户要把 Obsidian 和 OpenClaw memory / gbrain 打通
- 用户说「第二大脑可视化」「memory 图谱」「连点成面」「想在 Obsidian 里看 agent 写的记忆」
- 用户已有 gbrain + `~/wiki`（或同类 markdown 脑库），要加 GUI

## 架构（一图流）

```
OpenClaw workspace/memory/*.md  ──symlink──►  ~/wiki/memory/     ◄── Obsidian 浏览
gbrain Postgres (426+ pages)   ──export──►  ~/wiki/**/*.md       ◄── Obsidian 图谱
Agent cron                     ──sync────►  Postgres + vectors   ◄── 后台不变
```

**安全约束（必须遵守）**：
- `memory` 必须在 `~/wiki/.gitignore` 里 → gbrain `sync` 是 git-diff 驱动，不会把日记重复入库
- `.obsidian/` 被 gbrain `isSyncable` 跳过（隐藏目录）
- 不要改 `alwaysUpdateLinks: true`，避免 Obsidian 批量重写 gbrain 的 `[[路径式]]` 链接

## Phase 0 — 确认路径

| 变量 | 默认 | 说明 |
|------|------|------|
| `WIKI_DIR` | `~/wiki` | gbrain git 仓库根 |
| `MEMORY_DIR` | `~/.openclaw/workspace/memory` | OpenClaw 日记 MD |
| `GBRAIN_BIN` | `gbrain` | CLI 在 PATH |

## Phase 1 — 一键搭建（推荐）

```bash
bash skills/gbrain-obsidian-vault/scripts/setup-vault.sh
# 或指定路径：
WIKI_DIR=~/wiki MEMORY_DIR=~/.openclaw/workspace/memory bash scripts/setup-vault.sh
```

脚本会：创建 `memory` 软链、写入 `.gitignore`、预置 `.obsidian/app.json`（wikilink + absolute + 不自动改链）。

## Phase 2 — 物化 DB 页面（可选但强烈推荐）

若 Postgres 里页面多于磁盘 `.md`（常见于 MCP `put_page` 只写 DB）：

```bash
gbrain export --dir "$WIKI_DIR"
cd "$WIKI_DIR" && git add -A && git commit -m "materialize gbrain pages for Obsidian"
```

物化后 Obsidian 图谱 wikilink 解析率通常从 ~30% 升到 **80%+**。

## Phase 3 — 打开 Obsidian

1. Obsidian → **Open folder as vault** → 选 `WIKI_DIR`
2. 左侧 **Graph view**：看 people / projects / concepts / synthesis 簇
3. 打开 `memory/2026-MM-DD.md` → 右栏 **Backlinks → Unlinked mentions** 跳到引用该日记的 gbrain 页面

## Phase 4 — 验证清单

- [ ] `ls -la $WIKI_DIR/memory` 显示 symlink
- [ ] `cd $WIKI_DIR && git status` **不**出现 `memory/*.md`
- [ ] 图谱中有连线（说明 `[[projects/foo]]` 被解析）
- [ ] 编辑任意 gbrain 页面保存后 `git status` 有改动（cron 会 sync+embed）

## Agent 写入纪律（与 AGENTS.md 记忆桥接一致）

用户在 Obsidian 手改 markdown 后：
- gbrain 侧：link-maintenance / auto-ingest cron 会 `sync --no-embed` + `embed --stale`
- memory 侧：仍在 `workspace/memory/`，由 `memory_search` 索引，**不要**把 memory 提交进 wiki git

## 故障排除

| 症状 | 处理 |
|------|------|
| 图谱很空、大量悬空链接 | 跑 `gbrain export --dir $WIKI_DIR` |
| memory 在 git 里出现 | 确认 `.gitignore` 含 `memory` |
| Obsidian 把链接改成 `[text](path)` | 检查 `useMarkdownLinks: false` |
| `[[Naval Ravikant]]` 不解析 | 显示名链接；给目标页加 frontmatter `aliases` |

## 相关

- `skills/brain-ops` — gbrain 写入规范
- `skills/memory-setup-openclaw` — memory_search 配置
- `skills/planning-with-files` — 长任务落盘到 memory

详细架构与 mermaid 图见 `references/architecture.md`。
