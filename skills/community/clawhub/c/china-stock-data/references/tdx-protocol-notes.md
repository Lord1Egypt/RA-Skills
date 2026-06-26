# 通达信 TDX 协议笔记

## 市场代码映射

pytdx 中 market 参数：
- `0` = 深圳（sz：00/30/20 开头）
- `1` = 上海（sh：60/68 开头）

```python
from pytdx.hq import TdxHq_API
api = TdxHq_API()
api.connect('218.6.170.47', 7709, time_out=3)

# 上海股票
data = api.get_security_quotes([(1, '600519')])  # 贵州茅台

# 深圳股票
data = api.get_security_quotes([(0, '300750')])  # 宁德时代
```

## ⚠️ 限速策略（防封关键）

通达信服务器对高频连接敏感——连接→断开→再连接的"短连接风暴"是 IP 被封的核心原因。

### 1. 全局间隔 ≥0.5 秒 + Jitter

```python
_LAST_TDX_TIME = 0

def tdx_throttle():
    global _LAST_TDX_TIME
    elapsed = time.time() - _LAST_TDX_TIME
    if elapsed < 0.5:
        time.sleep(round(0.5 - elapsed + random.random() * 0.2, 3))
    _LAST_TDX_TIME = time.time()
```

每个连接前强制等待，确保上一次调用结束到下一次开始之间有 ≥0.5 秒的间隔。加 0~0.2 秒随机 jitter 防止被反爬虫按模式识别。

### 2. 服务器轮询（不固定打一个 IP）

维护 4 台已验证的主站，用模运算轮询：

```python
TDX_HOSTS = [
    ('218.6.170.47', 7709),   # 上证云成都电信一
    ('123.125.108.14', 7709), # 上证云北京联通一
    ('180.153.18.170', 7709), # 上海电信主站Z1
    ('60.191.117.167', 7709), # 杭州电信主站J1
]
_TDX_HOST_IDX = 0

def tdx_connect():
    global _TDX_HOST_IDX
    tdx_throttle()
    for _ in range(len(TDX_HOSTS)):
        ip, port = TDX_HOSTS[_TDX_HOST_IDX % len(TDX_HOSTS)]
        _TDX_HOST_IDX += 1
        api = TdxHq_API()
        try:
            api.connect(ip, port, time_out=3)
            return api
        except:
            try: api.disconnect()
            except: pass
    return None
```

轮询确保连续两次调用不会命中间一 IP，降低单台服务器的连接频率感知。

### 3. 批量查询（替代循环查）

**错误做法：** 每个股票/指数建一次连接循环查
```python
# ❌ 6次独立连接，高危！
for mkt, code in indices:
    api = TdxHq_API()
    api.connect(...)
    q = api.get_security_quotes([(mkt, code)])  # 单次1个
    api.disconnect()
```

**正确做法：** 把多个代码放在一个 `get_security_quotes()` 调用中
```python
# ✅ 1次连接查完所有，field by index
api.connect(...)
codes = [(1, '000001'), (0, '399001'), (0, '399006'), (1, '000688'), (1, '000016'), (1, '000300')]
quotes = api.get_security_quotes(codes)  # 一次查6个
api.disconnect()
# quotes[0] = 上证, quotes[1] = 深证 ...
```

**限制：** `get_security_quotes` 一次最多查约 80 只股票，超出需分批次。

## 可用服务器列表

```python
from pytdx.config.hosts import hq_hosts
# 按 (name, ip, port) 格式，共 104 个
```

手动维护列表（经过生产验证）：

| 名称 | IP | 端口 | 已验证 |
|------|----|:----:|:------:|
| 上证云成都电信一 | 218.6.170.47 | 7709 | ✅ |
| 上证云北京联通一 | 123.125.108.14 | 7709 | ✅ |
| 上海电信主站Z1 | 180.153.18.170 | 7709 | ✅ |
| 杭州电信主站J1 | 60.191.117.167 | 7709 | ✅ |

> **经验：** 不同服务器返回的实时数据有微小差异（正常，不影响使用）。但某些服务器可能只支持特定市场（如只做沪市不做深市），轮询时自然跳过。

## K线分类编码

```python
cat = {'daily':9, 'weekly':5, 'monthly':6, '60min':3, '30min':2, '15min':1, '5min':0}
bars = api.get_security_bars(cat, market, code, start_offset, count)
```

K线查询相对较"重"（服务器端需要聚合计算），建议 K 线调用间隔 ≥1 秒，且不要超过 count=200。

## 返回字段说明

| 字段 | 说明 |
|:----|:----|
| `price` | 当前价 |
| `last_close` | 昨收 |
| `open/high/low` | 今开/最高/最低 |
| `vol` | 成交量（手） |
| `amount` | 成交额（元） |
| `bid1-5` / `ask1-5` | 5档买卖价格 |
| `bid_vol1-5` / `ask_vol1-5` | 5档买卖量（手） |
| `servertime` | 服务器时间（约3-5秒延迟） |

## 坑

1. **不同服务器返回的数据可能不同**（部分服务器只支持特定市场）
2. **连接超时**设 3 秒，否则卡住整个脚本
3. **`get_security_quotes` 一次最多查约 80 只**，批量超限会静默截断
4. 返回 `None` 不一定是对端关——可能是市场代码错了（最常见错误：沪市股票传了 market=0）
5. **Python 多进程不共享全局 `_LAST_TDX_TIME`** — 如果多个进程同时调 TDX（如 cron + 手动），各自有各自的限速器，不会相互感知。解决方案是只让一个进程调 TDX（如 news_aggregator 的日报 cronjob），单独的 scrape 进程另外控制。
6. **`pytdx` 有时会突然 hang** — 加 `time_out` 参数并在 `connect()` 外层套 try/except。如果连续 4 台都超时，说明网络或服务器端有问题，应放弃并降级到腾讯财经。
7. **交易时间 vs 非交易时间** — 盘后 `price` 等于当日收盘价，`last_close` 等于前一日收盘价，数据仍然可用。
