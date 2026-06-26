# GBrain Obsidian Vault — 发布手册

GitHub: https://github.com/spikesubingrui-design/gbrain-obsidian-vault

---

## 发布命令

```bash
bash ~/.openclaw/workspace/scripts/skill-publish-dual.sh gbrain-obsidian-vault -c "v1.0.0: Obsidian GUI for OpenClaw memory + gbrain graph"
```

---

## 社交媒体文案

### 中文 · X / 即刻

```
开源了一个 Skill：GBrain Obsidian Vault 💎

AI 的记忆在 SQLite 和 Postgres 里——你看不见。
这个 Skill 把 OpenClaw memory 日记 + gbrain 知识图谱接到 Obsidian：

• 单 vault，图谱可视化
• memory 软链，不重复入库
• gbrain export 物化 DB 页面，wikilink 解析 28%→84%

一键脚本 + Agent 工作流。MIT。

⭐ https://github.com/spikesubingrui-design/gbrain-obsidian-vault

#OpenClaw #Obsidian #第二大脑 #知识图谱
```

### 中文 · 小红书

**标题：** 我给 AI 的第二大脑装上了 Obsidian 界面

**正文：**

Agent 能 `memory_search`、能 `gbrain query`，但我看不见那张网。

**GBrain Obsidian Vault** 做了三件事：
1. `~/wiki` 当 Obsidian vault（people / projects / concepts…）
2. 把 OpenClaw 日记 `memory/` 软链进来，反链能跳到实体页
3. `gbrain export` 把只在数据库里的页面写成 markdown——图谱立刻饱满

不改你现有 cron，编辑仍自动 sync+embed。

开源 MIT，OpenClaw + Cursor 都能用。

👉 GitHub 求 Star：https://github.com/spikesubingrui-design/gbrain-obsidian-vault

### English · X

```
Shipped: GBrain Obsidian Vault — make your OpenClaw + gbrain knowledge graph *visible*.

• One Obsidian vault = gbrain wiki + symlinked daily memory
• gbrain export materializes DB-only pages (wikilink hit rate ~28% → 84%)
• Safe: memory gitignored; gbrain sync is git-diff only

MIT agent skill. No SaaS lock-in.

⭐ https://github.com/spikesubingrui-design/gbrain-obsidian-vault

#OpenClaw #Obsidian #SecondBrain #LocalFirst
```

### Show HN

**Title:** Show HN: Agent skill to view OpenClaw memory + gbrain graph in Obsidian

**Body:** Local-first stack: OpenClaw agents write markdown + Postgres graph. Obsidian only reads files. This skill wires symlink + export + config so one vault shows daily notes and entity graph without duplicate ingest. MIT, setup script included.

Repo: https://github.com/spikesubingrui-design/gbrain-obsidian-vault
