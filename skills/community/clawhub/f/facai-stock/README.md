# facai-stock

A股实时行情查询、自选股管理与价格监控工具。

- **行情数据**：雪球 JSON API，token 本地缓存，首次约 2–3 秒，后续 < 500ms
- **自选股**：持久化到本地文件，增删即时生效
- **监控自选股**：独立后台子进程，仅在 A 股交易时段运行，价格偏离基准阈值时通过 openclaw 发送消息提醒

---

## 安装

```bash
pip install -r requirements.txt
```

依赖：`akshare >= 1.10.0`、`pandas >= 1.5.0`、`requests >= 2.28.0`，Python 3.10+，需能访问 xueqiu.com。

---

## 目录结构

```
f:/stock/
├── quote.py          # get_detail, get_detail_by_name（雪球 JSON API）
├── search.py         # search_by_name, get_all_stocks（全量股票列表缓存）
├── watchlist.py      # 自选股增删查清，联动监控进程
├── monitor.py        # 后台监控子进程
├── config.py         # 持久化配置读写（data/config.json）
├── cache.py          # A股列表本地缓存
├── market.py         # 市场前缀工具
├── main.py           # CLI 交互入口
├── data/             # 运行时数据（自动创建）
│   ├── config.json          # 持久化配置（monitor_target 等）
│   ├── watchlist.json       # 自选股列表
│   ├── stock_id.info        # A股代码/名称缓存
│   ├── xueqiu_token.json    # 雪球 token 缓存（6小时有效）
│   └── monitor.pid          # 监控进程 PID
├── logs/             # 监控日志（自动创建）
│   └── monitor_<timestamp>.log
├── SKILL.md          # Cursor Agent Skill 指令
├── clawhub.json      # ClawHub 发布元数据
└── requirements.txt
```

---

## 功能概览

| 模块 | 函数 | 说明 |
|------|------|------|
| `quote.py` | `get_detail(code)` | 按6位代码查询完整实时行情 |
| `quote.py` | `get_detail_by_name(name)` | 按精确名称查询（唯一匹配直接返回） |
| `search.py` | `search_by_name(name)` | 按名称关键字模糊搜索 |
| `search.py` | `get_all_stocks()` | 获取全量 A 股列表（带缓存） |
| `watchlist.py` | `list_all()` | 查看自选股列表 |
| `watchlist.py` | `add(query)` | 添加自选股（代码或精确名称），返回含 `monitor_status` |
| `watchlist.py` | `remove(query)` | 删除自选股（代码或精确名称），返回含 `monitor_status` |
| `watchlist.py` | `clear()` | 清空自选股列表，返回含 `monitor_status` |
| `monitor.py` | `start_monitor()` | 启动后台监控进程 |
| `monitor.py` | `stop_monitor()` | 停止监控进程 |
| `monitor.py` | `restart_monitor()` | 重启监控进程 |
| `monitor.py` | `is_running()` | 检查监控进程是否存活 |
| `config.py` | `get(key)` | 读取配置项 |
| `config.py` | `set(key, value)` | 写入配置项（持久化） |
| `config.py` | `all_config()` | 返回全部配置 |

---

## 行情查询

以下代码在 `f:/stock/` 目录下执行。

### 按代码查询

```python
from quote import get_detail

detail = get_detail('000001')
```

### 按精确名称查询

```python
from quote import get_detail_by_name

detail = get_detail_by_name('平安银行')
# 匹配多只时抛出 ValueError 并列出候选
```

### 模糊搜索

```python
from search import search_by_name

candidates = search_by_name('平安')
# → [{"code": "000001", "name": "平安银行"}, {"code": "601318", "name": "中国平安"}, ...]
```

### 返回字段

| 字段 | 说明 |
|------|------|
| `代码` / `名称` | 6位代码 / 股票简称 |
| `最新价` | 当前价格（元） |
| `涨跌幅` | 百分比，正数上涨、负数下跌 |
| `涨跌额` | 涨跌金额（元） |
| `今开` / `昨收` | 开盘价 / 昨日收盘价 |
| `最高` / `最低` | 今日价格区间 |
| `成交量` | 单位：手（100股/手） |
| `成交额` | 单位：元 |
| `总市值` | 单位：元，除以 1e8 得亿元 |
| `市盈率TTM` | 动态市盈率 |
| `市净率` / `股息率TTM` | 市净率 / 股息率（%） |
| `52周最高` / `52周最低` | 年内价格区间 |

---

## 自选股管理

自选股保存在 `data/watchlist.json`，增删操作**不会自动启停监控进程**，返回值中包含 `monitor_status` 字段供调用方判断是否需要手动启动监控。

### 查看

```python
from watchlist import list_all

stocks = list_all()
# → [{"code": "000001", "name": "平安银行"}, ...]
```

### 添加

```python
from watchlist import add

result = add('平安银行')   # 按名称（须精确唯一）
result = add('000001')    # 按6位代码
# → {"code": "000001", "name": "平安银行", "monitor_status": "监控未启动"}
```

已存在则跳过，不重复添加。`monitor_status` 为 `"监控未启动"` 时，需手动调用 `start_monitor()`。

### 删除

```python
from watchlist import remove

result = remove('平安银行')   # → {"code": ..., "name": ..., "monitor_status": "..."}，未找到返回 None
result = remove('000001')    # 按代码删除
```

### 清空

```python
from watchlist import clear

result = clear()   # → {"cleared": 2, "monitor_status": "监控已启动"}
```

### data/watchlist.json 格式

```json
[
  {"code": "000001", "name": "平安银行"},
  {"code": "600519", "name": "贵州茅台"}
]
```

---

## 价格监控

### 监控逻辑

- 每隔 10 秒查询一次所有自选股
- **仅在 A 股交易时段运行**（北京时间：09:30–11:30、13:00–15:00，周一至周五）
- 非交易时段每 20 秒检测一次是否开盘，等待期间不消耗接口配额
- 开盘/收盘切换时清空基准价，避免隔夜价差误触发
- **基于上次告警价比较**：价格相对上次告警价偏离 ≥ 2% 才触发；触发后以当前价为新基准，重新计数
- 自选股文件变化时自动热加载，无需重启进程

### 配置接收目标

`target` 的解析优先级：**调用时传入 > `data/config.json` 的 `monitor_target` > 报错退出**。

ou_xxxx是用户的openId，推荐首次使用前写入配置，后续无需重复传入：

```python
import config
config.set("monitor_target", "user:ou_xxxx")
```

### 启动监控

自选股操作**不会自动启动监控**，需手动调用。

```python
from monitor import start_monitor

# target 已在配置文件中，直接调用
pid = start_monitor()

# 或显式传入（覆盖配置文件）
pid = start_monitor("user:ou_xxxx")

# 自定义参数
pid = start_monitor(
    "user:ou_xxxx",
    interval=30,     # 查询间隔（秒），默认 10
    threshold=1.5,   # 触发告警的偏离幅度（%），默认 2.0
)
```

### 停止 / 重启

```python
from monitor import stop_monitor, restart_monitor

stop_monitor()
restart_monitor()                                              # target 从配置读取
restart_monitor("user:ou_xxxx")   # 或显式传入
```

### 检查状态

```python
from monitor import is_running

print(is_running())   # True / False
```

### 告警消息格式

```
【股价提醒】广汇能源（600256）价格下跌 2.15%，当前价 6.595 元（上次 6.740 元）｜今开 6.720 元，距开盘 -1.86%
```

通过以下命令发送：

```bash
openclaw message send \
  --target "user:ou_xxxx" \
  --message "【股价提醒】..."
```

### 日志

写入 `logs/monitor_<timestamp>.log`，单文件上限 2 MB，最多保留 5 个轮转备份（总占用 ≤ 12 MB）。

```
[09:30:01] 已进入交易时段，开始行情监控
[09:30:01] 自选股已更新：['广汇能源', '贵州茅台']
[09:30:01] 广汇能源(600256)  基准价 6.740 元  今开 6.720 元  距开盘 +0.30%
[09:30:11] 广汇能源(600256)  6.741 元  距基准 +0.01%  今开 6.720 元  距开盘 +0.31%
[09:30:11] ⚠  贵州茅台(600519) 偏离基准 +2.10%，触发提醒
[09:30:11] 已发送提醒 → 【股价提醒】贵州茅台（600519）价格上涨 2.10%，当前价 1551.920 元（上次 1520.000 元）｜今开 1510.000 元，距开盘 +2.77%
[11:30:00] 已进入非交易时段，暂停行情查询（每分钟检测开盘）
```

### 停止进程

```bash
# Python
python -c "from monitor import stop_monitor; stop_monitor()"

# 或直接 kill
taskkill /PID <pid> /F        # Windows
kill <pid>                    # macOS / Linux
```

---

## 雪球 Token 缓存

首次查询时自动访问 xueqiu.com 获取 token，缓存至 `data/xueqiu_token.json`，有效期 6 小时。

- **首次调用**：约 2–3 秒（获取 token）
- **缓存命中**：< 500ms
- **Token 失效**（401 响应）：自动刷新后重试，对调用方透明

---

## 常见问题

**添加自选股时报 ValueError？**
名称匹配到多只股票，先用 `search_by_name()` 找到精确名称，或直接传6位代码：`add('000001')`。

**添加自选股后监控没有启动？**
自选股操作不再自动启动监控。`add()`/`remove()`/`clear()` 返回的 `monitor_status` 字段会告知当前状态，为 `"监控未启动"` 时手动调用 `start_monitor()`。

**手动修改 watchlist.json 后会生效吗？**
会。监控进程检测文件 mtime，变化时自动热加载。

**非交易时段会误触发告警吗？**
不会。非交易时段进程休眠，开盘时清空基准价重新建立，避免隔夜涨跌触发。

**查询失败会退出监控吗？**
不会。失败只记日志，下次轮询继续重试。
