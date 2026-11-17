---
name: bigtimer
description: "🕐 BigTimer · 定时任务管家 — 定时任务·定时消息推送·任务管家·定时推送·定时提醒·定时报告统一管理（cron 调度 + 消息推送，飞书/多端）。OpenClaw 环境自动走 openclaw cron + message send，DSH 环境自动走 crontab + 飞书 webhook。支持定时任务增删改查、立即执行、调度条目生成，biga/eyes/bigfocus/listform 等技能的定时消息推送可统一接入。触发词：定时任务、定时消息推送、消息推送、任务管家、定时推送、定时提醒、定时报告、定时扫描。| Scheduled tasks & message push manager — cron jobs, scheduled message push, task manager, auto push to Feishu/multi-channel, dual-env (OpenClaw/DSH)."
triggers:
  - 定时任务
  - 定时推送
  - bigtimer
  - BigTimer
  - 定时器
  - 定时提醒
  - 定时报告
  - 定时汇报
  - 消息推送
  - 推送管家
  - 定时扫描
---

# 🕐 BigTimer · 定时任务 + 消息推送管家

统一管理**定时任务**（cron 调度）与**消息推送**（飞书/多端），双端兼容 OpenClaw 与 DSH。

## 🌍 环境兼容

> - **OpenClaw**：脚本在技能目录下执行（`python3 scripts/bigtimer.py`），数据默认 `~/.openclaw/workspace/memory/`；调度用 `openclaw cron`，推送用 `openclaw message send`。
> - **DSH**：无 `openclaw` CLI，数据走 `$DSH_WORKSPACE/memory`（默认 `~/.dsh/workspace/memory`）；调度写 crontab，推送用飞书自定义机器人 webhook（自动检测）。

## 📋 功能

| 命令 | 说明 |
|------|------|
| `add` | 新建任务（cron 表达式 + 执行动作 + 推送方式） |
| `list` | 列出所有任务 |
| `remove` | 删除任务 |
| `status` | 查看单个任务详情（含上次执行结果） |
| `run` | 立即执行一次（测试用） |
| `cron-gen` | 生成调度条目（不写入系统，先看效果） |
| `install` | 写入系统调度（OpenClaw → openclaw cron；DSH → crontab） |

## 🚀 快速开始

### 1. 新建任务

```bash
# 每天早上8点执行 biga 扫描，推送方式自动（OpenClaw 发消息 / DSH 走 webhook）
python3 scripts/bigtimer.py add \
  --name biga-morning \
  --schedule "0 8 * * *" \
  --action "python3 scripts/biga-scan.py --segments" \
  --push auto

# 指定飞书 webhook（DSH 环境推荐）
python3 scripts/bigtimer.py add \
  --name biga-morning \
  --schedule "0 8 * * *" \
  --action "python3 scripts/biga-scan.py --segments" \
  --push webhook --webhook "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

### 2. 查看 & 测试

```bash
python3 scripts/bigtimer.py list        # 所有任务
python3 scripts/bigtimer.py run biga-morning   # 立即执行一次（验证动作+推送）
python3 scripts/bigtimer.py cron-gen biga-morning  # 看生成的调度条目
```

### 3. 写入系统调度

```bash
python3 scripts/bigtimer.py install biga-morning
```

- **OpenClaw 环境**：输出 `openclaw cron add` 命令供确认后执行（或直接用 gateway cron 添加）
- **DSH 环境**：自动写入 crontab（机器级可靠，不依赖 DSH 进程）

## 🔧 推送方式（--push）

| 模式 | 行为 |
|------|------|
| `auto`（默认） | 有 openclaw CLI → `openclaw message send`（超长自动分段）；否则有 webhook → 飞书 webhook；都没有 → stdout 输出 |
| `openclaw` | 强制用 `openclaw message send`（需 `--channel`/`--target`，或读取 `memory/biga-send-config.json`） |
| `webhook` | 强制用飞书自定义机器人 webhook（需 `--webhook` URL） |
| `stdout` | 只输出到 stdout（供对话回复/调试） |

## 💡 集成其他技能

biga / eyes / bigfocus / listform 的定时推送统一接入：

```bash
# eyes 整点扫描（每整点）
python3 scripts/bigtimer.py add \
  --name eyes-hourly \
  --schedule "0 * * * *" \
  --action "python3 scripts/eyes-utils.py scan --json | python3 scripts/eyes-utils.py format" \
  --push auto

# bigfocus 价格监控（每30分钟）
python3 scripts/bigtimer.py add \
  --name bigfocus-scan \
  --schedule "*/30 * * * *" \
  --action "python3 scripts/bigfocus.py scan" \
  --push auto
```

## 📝 数据文件

- 任务表：`memory/bigtimer-tasks.json`
- 运行日志：`memory/bigtimer.log`（含每次执行与推送结果）
