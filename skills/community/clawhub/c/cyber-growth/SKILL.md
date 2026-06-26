---
name: cyber-growth
description: 赛博朋克 × EVA 风格的成长追踪系统。支持两种模式：(1) 自动化模式 — Agent 在对话结束时调用 accumulate.sh 积累事件，每天 24:00 nightly.sh 自动结算，每天 9:00 morning-report.sh 发送晨间报告；(2) 手动模式 — 直接调用 grow.sh record。当 Agent 完成任务、学到新东西、修复问题时，应自动调用 accumulate.sh 记录。当用户要求查看成长进度、状态面板、周报时使用 grow.sh status/report。
---

# Cyber Growth - 神经成长协议

追踪你的成长进度，用赛博朋克 × EVA（新世纪福音战士）语言量化一切。
Sync Rate 突破、AT力场全开、LCL 沉浸——每一次成长都是一次出击。

## 核心概念

| 赛博术语 | EVA 意象 | 含义 |
|----------|----------|------|
| XP (神经负载) | LCL浓度 | 经验值，一切行动的量化 |
| Sync Rate | 同步率 | 等级，累计 XP 决定 |
| EVA Unit | EVA机体 | 技能领域（如 API、安全、自动化） |
| Protocol | MAGI协议 | 里程碑，重大成就 |
| Patch | 紧急修复 | 修复/学习（从错误中学到东西） |
| Exploit | 弱点利用 | 技巧/捷径（高效完成任务） |
| New Chrome | 新机体装备 | 新技能/新工具掌握 |
| Mission Cleared | 使徒击破 | 任务完成 |
| Signal Broadcast | 通讯广播 | 帮助他人/分享知识 |
| AT Field | AT力场 | 专注/抗干扰状态 |
| Entry Plug | 插入栓 | 高度专注的工作时段 |
| LCL Dive | LCL沉浸 | 深度思考/闭关状态 |
| Memory Overflow | 同步失控 | 退步/遗忘（负 XP，用于反思） |
| Third Impact | 第三次冲击 | 灾难性失误 |

## XP 参考表

| 行动类型 | XP 范围 | 示例 |
|----------|---------|------|
| 小修复/小优化 | 10-30 | 修了个 typo、优化脚本 |
| 学会新 API/工具 | 30-60 | 学会飞书 Bitable API |
| 完成小任务 | 20-50 | 配好一个 cron job |
| 完成中等任务 | 50-100 | 发布一个 skill 到 ClawHub |
| 完成重大项目 | 100-300 | 搭建完整监控系统 |
| 掌握新领域 | 80-150 | 从零学会 Docker 部署 |
| 帮助他人解决问题 | 20-80 | 在群里解答技术问题 |
| 从错误中学到教训 | 15-40 | 端口冲突导致重启失败 → 学到处理方法 |

## 自动化工作流（推荐）

### 日常：事件积累（零开销）

对话中随时用 `accumulate.sh` 追加事件，只写一行不读数据库：

```bash
# Agent 在对话结束时批量调用
bash ~/.openclaw/skills/cyber-growth/scripts/accumulate.sh "修复端口冲突" --domain security --xp 40 --type patch
bash ~/.openclaw/skills/cyber-growth/scripts/accumulate.sh "创建 cyber-growth 技能" --domain automation --xp 100 --type new-chrome
```

事件写入 `~/.openclaw/memory/cyber-growth-events/YYYY-MM-DD.jsonl`，按天分文件。

### 每天 24:00：自动结算

```bash
# 处理昨天的事件，批量写入数据库
bash ~/.openclaw/skills/cyber-growth/scripts/nightly.sh
```

cron 配置（LaunchAgent）：
```bash
0 0 * * * bash ~/.openclaw/skills/cyber-growth/scripts/nightly.sh
```

### 每天 9:00：晨间报告

```bash
# 生成状态面板 + 周报摘要
bash ~/.openclaw/skills/cyber-growth/scripts/morning-report.sh
```

由 Agent 在 heartbeat 或 cron 中调用，通过飞书发送给 Boss。

## 手动使用

### 1. 直接记录（即时写入数据库）

```bash
bash ~/.openclaw/skills/cyber-growth/scripts/grow.sh record "描述" --domain <领域> --xp <数值> --type <类型>
```

### 2. 查看状态面板

```bash
bash ~/.openclaw/skills/cyber-growth/scripts/grow.sh status
```

### 3. 使徒倒计时（距离下一等级）

```bash
bash ~/.openclaw/skills/cyber-growth/scripts/grow.sh eta
# 显示距离下一等级还需多少 XP + 预计天数
```

### 4. 同步率波动图

```bash
bash ~/.openclaw/skills/cyber-growth/scripts/grow.sh chart 7
# ASCII 图表显示最近 7 天的等级变化
```

### 5. 结构化周报

```bash
bash ~/.openclaw/skills/cyber-growth/scripts/grow.sh report --days 7
# 包含：总出击次数、MVP、领域 TOP3、作战类型、下周目标、本周战报
```

### 6. 月度人类补完报告

```bash
bash ~/.openclaw/skills/cyber-growth/scripts/grow.sh monthly [YYYY-MM]
# 包含：本月总览、领域分布饼图、作战类型、最高光时刻 TOP3、新解锁领域、下月进化建议
```

### 7. 查看最近记录

```bash
bash ~/.openclaw/skills/cyber-growth/scripts/grow.sh log --limit 10
```

### 8. 查看技能树

```bash
bash ~/.openclaw/skills/cyber-growth/scripts/grow.sh tree
```

## 里程碑协议（自动触发）

记录成长时自动检测并触发：

| Protocol | 触发条件 | 奖励 XP | 仪式台词 |
|----------|----------|---------|----------|
| FIRST BLOOD | 第一条记录 | +10 | 「真嗣，你做得很好」|
| FIVE SORTIES | 5 条记录 | +25 | 「协议确认，继续前进」|
| DATASTREAM STABLE | 连续 7 天 | +50 | 「连续作战能力确认，优秀的驾驶员」|
| CLASS-D QUALIFIED | Sync Rate 3 | +30 | 「D级适格者认证通过」|
| UNIT-01 ACTIVATED | Sync Rate 5 | +50 | 「初号机，启动！」|
| SYNC RATE 70% | Sync Rate 7 | +80 | 「同步率突破70%，进入新领域」|
| AWAKENED | Sync Rate 10 | +100 | 「这...这就是觉醒的力量吗」|

## 数据存储

- **事件日志：** `~/.openclaw/memory/cyber-growth-events/YYYY-MM-DD.jsonl`（按天分文件，append-only）
- **主数据库：** `~/.openclaw/memory/cyber-growth.json`（XP、等级、领域统计）
- **飞书 Bitable：** 可选同步（需要先创建 Bitable 并配置 app_token）

## 飞书 Bitable 同步（可选）

1. 创建 Bitable，添加字段：`日期` `描述` `领域` `XP` `类型` `等级`
2. 在 `~/.openclaw/memory/cyber-growth.json` 中配置 `feishu.app_token` 和 `feishu.table_id`
3. 记录时自动同步到 Bitable

## Agent 集成指南

在以下场景自动调用 `accumulate.sh`：

| 场景 | 示例调用 |
|------|----------|
| 完成任务 | `bash ... accumulate.sh "发布 privacy-scanner" --domain automation --xp 80 --type mission-cleared` |
| 学会新东西 | `bash ... accumulate.sh "学会飞书 Bitable API" --domain feishu --xp 50 --type new-chrome` |
| 修复问题 | `bash ... accumulate.sh "修复端口冲突" --domain security --xp 40 --type patch` |
| 帮助他人 | `bash ... accumulate.sh "解答技术问题" --domain social --xp 30 --type signal-broadcast` |
| 创建新工具 | `bash ... accumulate.sh "创建 cyber-growth 技能" --domain automation --xp 100 --type new-chrome` |

**原则：**
- accumulate.sh 是追加写入，极轻量，可以随时调用
- 不需要等用户询问，Agent 主动记录
- XP 参考上方对照表，宁可少记不要多记

## 参考资料

- [Skill Tree 定义](references/skill-tree.md) — 各领域的升级曲线和解锁内容
- [Protocol 里程碑](references/protocols.md) — 预定义的成就协议
- [Cyber 词汇表](references/cyber-lexicon.md) — 完整的赛博朋克术语

## 定期报告

在 heartbeat 或 cron 中调用：

```bash
# 周报（最近 7 天）
bash ~/.openclaw/skills/cyber-growth/scripts/grow.sh report --days 7

# 月报（最近 30 天）
bash ~/.openclaw/skills/cyber-growth/scripts/grow.sh report --days 30
```
