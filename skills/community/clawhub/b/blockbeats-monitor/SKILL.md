---
name: blockbeats-monitor
description: 监听 BlockBeats 律动新闻和文章，按 Avenir Group、李林、币安美股、加密平台美股交易、币股互通关键词组归类统计，存入 SQLite，并生成 Telegram 舆情日报。
metadata:
  openclaw:
    emoji: "📊"
    install:
      - id: python3
        kind: system
        label: Python 3
    requires:
      bins:
        - python3
    os:
      - darwin
      - linux
      - win32
    tags:
      - blockbeats
      - crypto
      - news
      - monitor
      - telegram
  version: 0.1.0
---

<!-- 本文件用于告诉 Codex/OpenClaw 何时使用本 skill，以及如何运行舆情监控脚本。 -->

# BlockBeats 舆情监控 Skill

用于监听律动 BlockBeats Pro API 的 24h 快讯、文章和重要内容，按固定关键词组归类，写入本地 SQLite，并生成日报推送到 Telegram 群。

## 触发场景

当用户要求执行以下任务时使用本 skill：

- 监听律动、BlockBeats、区块律动新闻。
- 统计 Avenir Group、李林、币安上美股、加密平台美股交易、币股互通相关舆情。
- 生成过去 24h 的舆情日报。
- 将 BlockBeats 舆情日报推送到 Telegram 群。

## 数据边界

只使用当前 BlockBeats Pro API 已确认的内容字段：标题、摘要、正文、链接、发布时间、类型、原始 JSON。

不要采集、入库或展示未确认的互动类指标。日报只输出提及次数、周期变化、主要相关内容和重点相关内容。

## 配置文件

优先建议使用 `config.toml` 配置运行环境，可从 `config.example.toml` 复制：

```bash
cp config.example.toml config.toml
```

默认读取 `./config.toml`，也可以使用 `--config /path/to/config.toml` 指定路径。

配置项：

- `blockbeats.api_key`：BlockBeats Pro API key。
- `blockbeats.lang`：请求语言，默认 `cn`。
- `telegram.bot_token`：Telegram Bot token。
- `telegram.chat_id`：Telegram 群、频道或用户 ID。
- `storage.db_path`：SQLite 数据库路径，默认 `./data/blockbeats_monitor.sqlite`。
- `report.timezone`：日报时区，默认 `Asia/Shanghai`。

## 常用命令

```bash
python3 scripts/blockbeats_monitor.py init-db
python3 scripts/blockbeats_monitor.py ingest
python3 scripts/blockbeats_monitor.py report
python3 scripts/blockbeats_monitor.py send-telegram --text-file report.md
python3 scripts/blockbeats_monitor.py run-daily
```

## 工作流

1. 先执行 `init-db` 创建 SQLite 表并写入关键词组。
2. 定时执行 `ingest` 拉取律动 24h 和 important 内容，做关键词匹配并去重入库。
3. 执行 `report` 统计当前 24h 和上一 24h 的提及次数，生成 Markdown 日报。
4. 执行 `run-daily` 完成采集、统计、保存日报和 Telegram 推送。

## 重要舆情规则

“昨日重点相关内容”使用确定性排序：

1. 命中关键词且来自 `/v1/newsflash/important` 或 `/v1/article/important` 的内容优先。
2. 不足 5 条时，从普通 24h 快讯和文章补齐。
3. 命中关键词组数量多的优先。
4. 标题和正文同时命中的优先。
5. 发布时间新的优先。

## 定时日报触发语

当用户想要定时收到日报时，优先把需求理解为“由 OpenClaw 的定时能力在指定时间触发 `run-daily`”。

示例触发语：

- `请每天上午 11:00 执行 BlockBeats 舆情监控日报，并把结果推送到 Telegram。配置文件用 /path/to/blockbeat_monitor/config.toml。`
- `请每天晚上 23:00 执行 BlockBeats 舆情监控日报，并把结果推送到 Telegram。配置文件用 /path/to/blockbeat_monitor/config.toml。`

OpenClaw 真正应执行的命令：

```bash
python3 /path/to/blockbeat_monitor/scripts/blockbeats_monitor.py --config /path/to/blockbeat_monitor/config.toml run-daily
```

`run-daily` 会自动抓取以下 4 个端点：

- `/v1/newsflash/24h`
- `/v1/article/24h`
- `/v1/newsflash/important`
- `/v1/article/important`
