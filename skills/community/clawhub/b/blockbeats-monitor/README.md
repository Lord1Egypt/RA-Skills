<!-- 本文件用于说明 BlockBeats 舆情监控 skill 的安装、配置、运行和发布方法。 -->

# BlockBeats 舆情监控 Skill

这是一个可给 Codex 和 OpenClaw 使用的舆情监控 skill。它会调用 BlockBeats Pro API，按固定关键词组归类过去 24h 的律动快讯和文章，写入本地 SQLite，生成 Markdown 日报，并可推送到 Telegram 群。

## 功能

- 采集律动 24h 快讯、24h 文章、重要快讯、重要文章。
- 按 5 组关键词做本地匹配归类。
- 统计过去 24h 提及次数，并对比上一 24h 周期。
- 生成“总体数据、关键词热度排名、昨日重点相关内容”日报。
- 使用 Telegram Bot API 推送日报。

## 关键词组

1. Avenir Group舆情基础：`Avenir Group`、`Avenir`、`Avenir集团`、`未来资本`
2. 李总舆情基础：`Li Lin`、`Leon Li`、`李林`、`Huobi founder`、`Founder of Huobi`、`火币创始人`
3. 币安上美股专项监测：`Binance/币安` 且命中 `US stocks/stocks/equities/美股/股票/tokenized stocks/股票代币`
4. 加密平台美股交易舆情：`crypto exchange/加密平台/交易所` 且命中 `US stocks/stocks/美股/股票/美股交易`
5. 币股互通市场舆情：`crypto/加密资产/币` 且命中 `stocks/US stocks/美股/股票` 且命中 `one account/cross-asset/capital efficiency/一个账户/跨资产/资金效率/币股互通`

## 配置文件

项目已提供本地配置文件 `config.toml`。如果需要重建，可以从示例复制：

```bash
cp config.example.toml config.toml
```

编辑 [config.toml](./config.toml)：

```toml
[blockbeats]
api_key = "你的律动 Pro API Key"
lang = "cn"

[telegram]
bot_token = "你的 Telegram Bot Token"
chat_id = "你的 Telegram 群或频道 ID"

[storage]
db_path = "data/blockbeats_monitor.sqlite"

[report]
timezone = "Asia/Shanghai"
```

默认读取 `./config.toml`，也可以指定其它配置文件：

```bash
python3 scripts/blockbeats_monitor.py --config /path/to/config.toml report
```

运行配置只从 `config.toml` 读取。`--db` 只用于临时调试时覆盖数据库路径。

## 初始化数据库

```bash
python3 scripts/blockbeats_monitor.py init-db
```

默认数据库文件：

```text
./data/blockbeats_monitor.sqlite
```

可以用 `config.toml` 的 `storage.db_path` 或 `--db` 改成其它路径。

## 采集数据

```bash
python3 scripts/blockbeats_monitor.py ingest
```

采集会请求以下律动端点：

- `/v1/newsflash/24h`
- `/v1/article/24h`
- `/v1/newsflash/important`
- `/v1/article/important`

脚本会按标题、摘要、正文做关键词匹配，并用来源类型、链接和标题生成稳定 ID 去重。

## 生成日报

```bash
python3 scripts/blockbeats_monitor.py report
```

写入文件：

```bash
python3 scripts/blockbeats_monitor.py report --output report.md
```

日报包含：

- 总提及
- 关键词热度排名
- 每组主要相关内容
- 昨日重点相关内容

## 推送 Telegram

推送已有日报文件：

```bash
python3 scripts/blockbeats_monitor.py send-telegram --text-file report.md
```

完整每日流程：

```bash
python3 scripts/blockbeats_monitor.py run-daily
```

`run-daily` 会自动初始化数据库、采集数据、生成日报、保存日报记录并推送 Telegram。

## Cron 示例

每天北京时间 10:00 推送：

```cron
0 10 * * * cd /path/to/blockbeat_monitor && python3 scripts/blockbeats_monitor.py --config config.toml run-daily >> logs/blockbeats_monitor.log 2>&1
```

如果希望更频繁采集、每天只推送一次：

```cron
*/30 * * * * cd /path/to/blockbeat_monitor && python3 scripts/blockbeats_monitor.py --config config.toml ingest >> logs/blockbeats_ingest.log 2>&1
0 10 * * * cd /path/to/blockbeat_monitor && python3 scripts/blockbeats_monitor.py --config config.toml run-daily >> logs/blockbeats_daily.log 2>&1
```

## OpenClaw / ClawHub 使用

本目录可作为 ClawHub skill 发布：

```bash
clawhub publish .
```

OpenClaw 用户安装后，在任务中要求“生成律动舆情日报”或“推送 BlockBeats 关键词日报”即可触发 skill 指令。也可以直接运行 README 中的 Python 命令。

### OpenClaw 说法示例

如果用户希望每天上午 11:00 收到一份日报，可以对 OpenClaw 说：

```text
请每天上午 11:00 执行 BlockBeats 舆情监控日报，并把结果推送到 Telegram。配置文件用 /path/to/blockbeat_monitor/config.toml。
```

如果用户希望每天晚上 23:00 收到一份日报，可以对 OpenClaw 说：

```text
请每天晚上 23:00 执行 BlockBeats 舆情监控日报，并把结果推送到 Telegram。配置文件用 /path/to/blockbeat_monitor/config.toml。
```

OpenClaw 真正应执行的命令相同，只是调度时间不同：

```bash
python3 /path/to/blockbeat_monitor/scripts/blockbeats_monitor.py --config /path/to/blockbeat_monitor/config.toml run-daily
```

`run-daily` 内部会依次调用：

- 抓取 `/v1/newsflash/24h`
- 抓取 `/v1/article/24h`
- 抓取 `/v1/newsflash/important`
- 抓取 `/v1/article/important`
- 生成日报
- 推送 Telegram

## 本地测试

```bash
python3 -m unittest discover -s tests
```
