# 价格监控定时任务

> OpenClaw automations + amazon-scraper + 飞书多维表格 + Discord 推送

## 架构

```
openclaw automations（每 6 小时，command，不另起一轮模型）
  └─ pickleball_price_monitor.py
      ├─ Docker amazon-scraper 抓取 ASIN 价格
      ├─ SQLite 存储历史价格（~/.openclaw/amazon-scraper/）
      ├─ 飞书多维表格写入每次检查记录 (lark-cli base +record-batch-create)
      └─ 价格变化时 → stdout → 按 automation 的 delivery 推送
          无变化时 → stdout 为空
```

## 创建飞书多维表格

```bash
lark-cli base +base-create --name "监控表名" --table-name "价格记录" \
  --fields '[
    {"name":"ASIN","type":"text"},
    {"name":"商品标题","type":"text"},
    {"name":"当前价格","type":"number"},
    {"name":"上次价格","type":"number"},
    {"name":"价格变化","type":"number"},
    {"name":"变化幅度","type":"text"},
    {"name":"检查时间","type":"datetime"},
    {"name":"状态","type":"text"}
  ]' --as user
```

返回 `base_token` 和 `table.id`，填入脚本的 `BASE_TOKEN` 和 `TABLE_ID`。

## 飞书写入格式 (lark-cli base +record-batch-create)

`--json` 必须是 `{"fields":[...],"rows":[[...]]}` 格式，不是对象数组：

```python
batch_json = json.dumps({
    "fields": ["ASIN", "商品标题", "当前价格", "上次价格", "价格变化", "变化幅度", "检查时间", "状态"],
    "rows": [
        ["B0F6XSV7XB", "商品标题", 42.99, 45.99, -3.00, "↓ -6.5%", 1720000000000, "降价"],
        # ...
    ]
}, ensure_ascii=False)
```

- `检查时间` datetime 字段需**毫秒时间戳**（秒级 × 1000）
- `ensure_ascii=False` 保留中文
- 单批最多 200 行

## 创建定时任务

`--command` 在 Gateway 主机上直接跑脚本，不另起一轮模型。`--every 6h` 与时区无关。

```bash
openclaw automations add \
  --every 6h \
  --name "Pickleball价格监控" \
  --command "python3 ~/.openclaw/skills/amazon-scraper/scripts/pickleball_price_monitor.py" \
  --session isolated \
  --announce
```

每天北京时间 9:00 用 cron 表达式，并显式指定时区，不要靠把小时减 8：

```bash
openclaw automations create "0 9 * * *" \
  --name "每天9点价格监控" \
  --tz Asia/Shanghai \
  --command "python3 ~/.openclaw/skills/amazon-scraper/scripts/asin_price_monitor.py" \
  --session isolated \
  --announce
```

## 时区

不带 `--tz` 时，cron 表达式按 **Gateway 主机时区**计算，不是固定 UTC。要固定北京时间就加 `--tz Asia/Shanghai`，表达式里直接写北京时间的小时。`--every 6h` 这种间隔不受时区影响。

## command 任务的输出

- `--command` 只跑进程，不调用模型
- 脚本在有价格变化时把 Markdown 打到 stdout；无变化时 stdout 为空
- `--announce` 把这次运行的输出按任务的 delivery 送出（例如 Discord）
- 脚本 stderr 是日志，不要把报告打到 stderr

## 修改监控 ASIN 列表

编辑脚本顶部的 `ASINS` 列表：
```python
ASINS = ["B0F6XSV7XB", "B0FTQWG86Q", "B0G6CTNVQT"]
```

修改后无需重启 cron，下次执行自动生效（脚本每次运行时读取）。

## 依赖

- `amazon-scraper` Docker 镜像（已构建）
- `lark-cli` 已安装并认证（`lark-cli auth login`）
- Python 3.11+（sqlite3 内置）
