# agent-self-rollback

**为 AI agent 自身打造的「误操作回滚机制」skill——三层防线（自律规则 + 时间戳快照 + 双兜底恢复），配可移植 PowerShell 脚本（snapshot / list / restore / verify），任何 agent 改两行配置即可部署。全脱敏。**

**A skill for AI agents to deploy their own mistake-proof rollback mechanism — three layers (self-discipline rules + timestamped snapshots + double-buffered restore), plus a portable PowerShell script (snapshot / list / restore / verify). Any agent can deploy it after editing two lines of config. Fully desensitized.**

[中文](#中文) | [English](#english)

---

## 中文

### 这是什么

AI agent 会写文件、会改自己 —— 所以也会写坏自己。这套 skill 让 agent 拥有"后悔药"：即使把自己的持久记忆（身份 / 用户画像 / 事实库 / 事件日志）覆盖坏了，也能从快照链里捞回旧魂。

沉淀自真实落地案例：给 AI Assistant 建立误操作回滚机制的项目要求与实施经验，**全部脱敏**。

- **三层防线**：预防层（把「改前先存档」写进 agent 行为准则）+ 备份层（会话启动/改关键文件前自动快照）+ 恢复层（`restore` 回滚，恢复前自动先存「当前态」兜底，滚错了还能再滚回来）。
- **可移植脚本 `scripts/rollback.ps1`**：四个子命令（snapshot / list / restore / verify），配 MD5 校验；只改脚本顶部 `$AgentDir` / `$CoreFiles` 两处即可用于任意 agent。
- **覆盖两类误操作**：agent 自身记忆文件改坏（SOUL.md / USER.md / FACT.md / JOURNAL 等），以及项目文件误改误删（`-Arg` 附加路径一起快照）。
- **铁律清单 + 部署后自检表**：装上就能自查是否部署到位。
- 每条快照含文件本体 + `MANIFEST.txt` + `HASHES.md5` + `REASON.txt`，完整可追溯。

### 安装

```bash
git clone https://github.com/mowenQWQ/agent-self-rollback.git
cp -r agent-self-rollback/scripts /your/agent/tools/self-rollback/
# 然后按 SKILL.md 部署步骤：改配置 → 首次 snapshot → 写入自律规则 → 自检清单过一遍
```

适用于支持 Skill 格式的 AI 编码助手（Claude Code / CherryStudio / CodeBuddy / OpenClaw 等），按 description 关键词自动触发。

### 快速上手

```powershell
# 1) 首次部署，改好脚本顶部两处配置后先建基线快照
powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 snapshot

# 2) 日常启动/改重要文件前打点
powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 snapshot

# 3) 怀疑记忆被动过 → 对比 MD5
powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 verify

# 4) 确认改坏 → 回滚（先自动存 pre-restore 兜底，输入 yes 确认）
powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 restore 2

# 5) 列全部快照
powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 list
```

---

## English

### What is this

AI agents write files — and sometimes write *themselves* into a corner. This skill gives an agent a "do-over": even if it corrupts its own persistent memory (identity, user profile, fact base, event log), it can recover from a snapshot chain.

Born from a real deployment: building a mistake-proof rollback mechanism for an AI assistant. **Fully desensitized.**

- **Three layers**: prevention (write "archive before you edit" into the agent's own rules) + backup (auto-snapshot at session start / before editing key files) + recovery (`restore`, which first saves the current state as a pre-restore fallback so you can roll back a wrong restore).
- **Portable `scripts/rollback.ps1`**: four subcommands (snapshot / list / restore / verify) with MD5 checks. Edit just `$AgentDir` / `$CoreFiles` at the top to use it with any agent.
- **Covers both kinds of mistakes**: corrupting the agent's own memory files (SOUL.md / USER.md / FACT.md / JOURNAL ...) and mis-editing/deleting project files (pass extra paths via `-Arg`).
- **Iron rules + post-deploy checklist**: verify your own setup.
- Every snapshot stores the files plus `MANIFEST.txt` + `HASHES.md5` + `REASON.txt` — fully traceable.

### Install

```bash
git clone https://github.com/mowenQWQ/agent-self-rollback.git
cp -r agent-self-rollback/scripts /your/agent/tools/self-rollback/
# then follow SKILL.md: edit config → first snapshot → write self-discipline rules → run the checklist
```

Works with skill-aware AI coding assistants (Claude Code / CherryStudio / CodeBuddy / OpenClaw etc.), triggered automatically by description keywords.

### Quick start

```powershell
# 1) first deploy: after editing the two config lines, take a baseline snapshot
powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 snapshot

# 2) checkpoint at session start / before editing important files
powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 snapshot

# 3) suspect your memory was touched? compare MD5
powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 verify

# 4) confirmed corruption? restore (auto-saves a pre-restore fallback first; type yes)
powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 restore 2

# 5) list all snapshots
powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 list
```

---

## License

MIT — see [LICENSE](LICENSE).

---

## 🤖 AI 使用声明 / AI Usage Disclosure

本项目在开发与维护过程中使用了 AI 编程助手（Claude / Anthropic）辅助代码编写、文档整理与问题排查；核心决策、内容审核与最终发布由维护者完成。

This project was developed and maintained with the assistance of an AI coding assistant (Claude / Anthropic) for coding, documentation, and troubleshooting. Core decisions, content review, and final releases are made by the maintainer.