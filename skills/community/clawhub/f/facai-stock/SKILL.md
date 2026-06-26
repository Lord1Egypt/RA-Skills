---
name: facai-stock
description: 查询A股实时行情、管理自选股、启动股票价格监控。当用户询问股票价格、涨跌、行情、查股票、看股价，或要求添加自选股、删除自选股、查看自选股、清空自选股、监控股票、盯盘、价格提醒、股价变动提醒时使用本技能。支持6位股票代码或股票名称关键字。
---

# A股实时行情查询、自选股管理与价格监控

**所有命令须在项目根目录当前文档目录下执行。**

---

## 配置接收目标（首次必须），这是后续监控异动发生后消息推送目标

`target` 解析优先级：**调用时传入 > `data/config.json` 的 `monitor_target` > 报错退出**。

```bash
python -c "
import config
config.set('monitor_target', 'user:ou_xxxx')
"
```

ou_xxxx是用户的openId，配置持久化在 `data/config.json`，后续所有启动/重启自动读取。

---

## 查询行情

### 按股票代码查询

```bash
python -c "
import json
from quote import get_detail
print(json.dumps(get_detail('000001'), ensure_ascii=False, indent=2))
"
```

### 按股票名称查询（名称唯一时）

```bash
python -c "
import json
from quote import get_detail_by_name
print(json.dumps(get_detail_by_name('平安银行'), ensure_ascii=False, indent=2))
"
```

若名称匹配多只股票，抛出 `ValueError` 并列出候选 → 询问用户后改用代码查询。

### 名称模糊时先搜索

```bash
python -c "
import json
from search import search_by_name
print(json.dumps(search_by_name('平安'), ensure_ascii=False, indent=2))
"
```

取候选列表中的 `code`，再调用 `get_detail(code)`。

### 向用户展示结果

以易读格式回答，例如：

> **平安银行（000001）** 当前价 **10.71 元**，今日 ▼ 1.56%（-0.17 元）。
> 今日区间 10.67 ~ 10.84，成交额 11.68 亿元，总市值 2078 亿元。

---

## 自选股管理

自选股持久化在 `data/watchlist.json`，操作不自动启停监控，返回值中包含 `monitor_status` 供判断。

### 查看自选股列表

```bash
python -c "
import json
from watchlist import list_all
print(json.dumps(list_all(), ensure_ascii=False, indent=2))
"
```

输出：`[{"code": "000001", "name": "平安银行"}, ...]`，空列表时为 `[]`。

### 添加自选股

```bash
python -c "
import json
from watchlist import add
print(json.dumps(add('平安银行'), ensure_ascii=False))
"
```

返回示例：`{"code": "000001", "name": "平安银行", "monitor_status": "监控未启动"}`

- 接受6位代码或精确名称；已存在则直接返回，不重复添加
- `monitor_status` 为 `"监控未启动"` 时，提示用户手动启动监控

**名称不唯一时的处理流程：**
1. `add()` 内部调用 `get_detail_by_name()`，若抛出 `ValueError` 说明名称模糊
2. 先用 `search_by_name()` 列出候选，询问用户选择
3. 用户确认后改用6位代码添加：`add('000001')`

### 删除自选股

```bash
python -c "
import json
from watchlist import remove
print(json.dumps(remove('平安银行'), ensure_ascii=False))
"
```

返回示例：`{"code": "000001", "name": "平安银行", "monitor_status": "监控已启动"}`

未找到时返回 `null`。同样接受6位代码。

### 清空自选股

```bash
python -c "
import json
from watchlist import clear
print(json.dumps(clear(), ensure_ascii=False))
"
```

返回示例：`{"cleared": 2, "monitor_status": "监控已启动"}`

---

## 股票价格监控

监控进程读取 `data/watchlist.json`，每隔 10 秒查询一次，**仅在 A 股交易时段运行**，价格距上次告警偏离 ≥ 2% 时发送 openclaw 消息。**自选股操作不再自动启停进程，需手动管理。**

### 查看监控进程状态

```bash
python -c "
from monitor import is_running
print('运行中' if is_running() else '未运行')
"
```

### 启动监控

```bash
python -c "from monitor import start_monitor; start_monitor()"
```

覆盖 target 或修改参数时：

```bash
python -c "
from monitor import start_monitor
start_monitor(
    'user:ou_xxxx',   # 可选，不传则从配置文件读取
    interval=30,      # 查询间隔（秒），默认 10
    threshold=1.5,    # 触发告警的偏离幅度（%），默认 2.0
)
"
```

输出示例：
```
[monitor] 监控子进程已启动  PID=12345  日志→ f:\stock\logs\monitor_20260304_153000.log
```

### 停止监控

```bash
python -c "from monitor import stop_monitor; stop_monitor()"
```

### 重启监控

```bash
python -c "from monitor import restart_monitor; restart_monitor()"
```

### 告知用户结果

向用户确认：已监控哪些股票（调用 `list_all()` 获取）、查询间隔（默认10秒）、触发条件（距上次告警价偏离 ≥ 2%，触发后以当前价为新基准）、告警方式（openclaw 消息推送，含今开价和距开盘涨幅）。

---

## 返回字段说明

| 字段 | 说明 |
|------|------|
| `最新价` | 当前价格（元） |
| `涨跌幅` | 百分比，正数上涨、负数下跌 |
| `涨跌额` | 涨跌金额（元） |
| `今开` / `昨收` | 开盘价 / 昨日收盘价 |
| `最高` / `最低` | 今日区间 |
| `成交量` | 单位：手（100股/手） |
| `成交额` | 单位：元 |
| `总市值` | 单位：元，除以 1e8 得亿元 |
| `市盈率TTM` | 动态市盈率 |
| `52周最高` / `52周最低` | 年内区间 |

---

## 注意事项

- 非交易时段返回最近交易日收盘数据
- 自选股文件变化时监控进程**自动热加载**，无需重启
- 子进程独立于父进程运行，日志同时输出到控制台和文件
- 日志写入 `logs/monitor_<timestamp>.log`，单文件上限 2 MB，最多保留 5 个备份
- 查询失败（如雪球限速）时自动跳过本次，不影响监控持续运行
