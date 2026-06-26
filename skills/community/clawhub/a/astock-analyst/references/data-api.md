# 数据采集 API 手册

## 通用注意事项

- **始终加 `--ipv4`**：避免 IPv6 连接超时（代码52）
- **价格字段**：有时单位是"分"，需÷100，拿到数据先验证合理性
- **User-Agent**：加 `-H "User-Agent: Mozilla/5.0"` 防被拦截
- **超时**：`--max-time 10`，批量时每只单独请求

---

## 1. 股票代码搜索

```bash
curl -s --max-time 10 --ipv4 -H "User-Agent: Mozilla/5.0" \
  "https://search-codetable.eastmoney.com/codetable/search/web?client=web&clientVersion=lastest&keyword=青鸟消防&type=0&pageIndex=1&pageSize=5"
```

返回字段：`code`（代码）、`market`（0=深市, 1=沪市）、`shortName`（名称）

secid 格式：`{market}.{code}`，例如沪市603893 → `1.603893`

---

## 2. 实时行情（单只）

```bash
curl -s --max-time 10 --ipv4 -H "User-Agent: Mozilla/5.0" \
  "https://push2.eastmoney.com/api/qt/stock/get?secid=1.603893&fields=f43,f44,f45,f46,f60,f47,f58&fltt=2&invt=2"
```

| 字段 | 含义 |
|------|------|
| f43 | 最新价 |
| f44 | 最高价 |
| f45 | 最低价 |
| f46 | 今开 |
| f60 | 昨收 |
| f47 | 成交量（手） |
| f48 | 成交额 |
| f58 | 股票名称 |
| f116 | 总市值 |
| f168 | 换手率 |

---

## 3. 批量实时行情

```bash
for item in "1.603893:瑞芯微" "1.601991:大唐发电" "0.300961:深水海纳"; do
  secid="${item%%:*}"; name="${item##*:}"
  data=$(curl -s --max-time 10 --ipv4 -H "User-Agent: Mozilla/5.0" \
    "https://push2.eastmoney.com/api/qt/stock/get?secid=${secid}&fields=f43,f44,f45,f46,f60,f47&fltt=2&invt=2")
  echo "${name}: ${data}"
done
```

---

## 4. 历史K线（日线）

```bash
curl -s --max-time 10 --ipv4 -H "User-Agent: Mozilla/5.0" \
  "https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.603893&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f58&klt=101&fqt=1&lmt=60&end=20260317" \
  > /tmp/stock.json
```

参数说明：
- `klt=101`：日线；`klt=102`：周线；`klt=103`：月线
- `fqt=1`：前复权；`fqt=0`：不复权
- `lmt=60`：最近60条
- `end=YYYYMMDD`：截止日期

K线字段顺序（逗号分隔）：`日期, 开盘, 收盘, 最高, 最低, 成交量, 成交额, 振幅`

**注意：字段2是收盘，字段3是最高，字段4是最低**（非常规顺序，别搞错）

解析示例：
```python
import json
with open('/tmp/stock.json') as f:
    d = json.load(f)
klines = d['data']['klines']
for k in klines:
    p = k.split(',')
    date, open_, close, high, low, vol = p[0], float(p[1]), float(p[2]), float(p[3]), float(p[4]), float(p[5])
```

---

## 5. 资金流向（需 datasaver）

URL：`https://data.eastmoney.com/zjlx/{代码}.html`（如 603893）

提取字段：超大单净额、大单净额、中单净额、小单净额

判断：
- 超大单净卖 + 中单净买 → 主力派发给散户
- 连续多日超大单净流出 → 机构撤退

---

## 6. 千股千评（需 datasaver）

URL：`https://data.eastmoney.com/stockcomment/stock/{代码}.html`

提取字段：综合评分、控盘度、主力成本、次日上涨概率

---

## 7. 融资融券（需 datasaver）

URL：`https://data.eastmoney.com/rzrq/detail/{代码}.html`

提取字段：融资余额、融资净买入、融券余额

---

## 常用 Python 计算模板

保存数据到 /tmp/stock.json 后，用以下模板计算所有指标：

```python
import json

with open('/tmp/stock.json') as f:
    d = json.load(f)
klines = d['data']['klines']

days = []
for k in klines:
    p = k.split(',')
    days.append({'date': p[0], 'open': float(p[1]), 'close': float(p[2]),
                 'high': float(p[3]), 'low': float(p[4]), 'vol': float(p[5])})

closes = [x['close'] for x in days]

# 均线
def ma(data, n): return sum(data[-n:]) / n
ma5 = ma(closes, 5); ma10 = ma(closes, 10)
ma20 = ma(closes, 20); ma60 = ma(closes, 60)

# 涨跌量不对称比
up_vol = sum(x['vol'] for x in days if x['close'] > x['open'])
dn_vol = sum(x['vol'] for x in days if x['close'] < x['open'])
ratio = dn_vol / up_vol if up_vol > 0 else 999

# OBV
obv = 0; prev = days[0]['close']; obv_list = []
for x in days[1:]:
    if x['close'] > prev: obv += x['vol']
    elif x['close'] < prev: obv -= x['vol']
    obv_list.append(obv); prev = x['close']

# MACD
def ema_f(data, n):
    k = 2 / (n + 1); e = data[0]; res = []
    for x in data: e = x * k + e * (1 - k); res.append(e)
    return res
e12 = ema_f(closes, 12); e26 = ema_f(closes, 26)
dif = [e12[i] - e26[i] for i in range(len(closes))]
dea = ema_f(dif, 9)

# RSI(14)
def rsi_f(c, n=14):
    ag = loss = 0
    for i in range(1, n + 1):
        chg = c[i] - c[i-1]
        if chg > 0: ag += chg
        else: loss += abs(chg)
    ag /= n; loss /= n
    for i in range(n + 1, len(c)):
        chg = c[i] - c[i-1]
        if chg > 0: ag = (ag * (n-1) + chg) / n; loss = loss * (n-1) / n
        else: ag = ag * (n-1) / n; loss = (loss * (n-1) + abs(chg)) / n
    return 100 if loss == 0 else 100 - 100 / (1 + ag / loss)

# 期望值
up_d = [(x['close']-x['open'])/x['open']*100 for x in days if x['close'] > x['open']]
dn_d = [(x['close']-x['open'])/x['open']*100 for x in days if x['close'] < x['open']]
up_p = len(up_d) / len(days)
ev = up_p * (sum(up_d)/len(up_d)) + (1 - up_p) * (sum(dn_d)/len(dn_d))

# 最大回撤
peak = closes[0]; max_dd = 0
for c in closes:
    if c > peak: peak = c
    dd = (peak - c) / peak
    if dd > max_dd: max_dd = dd
```
