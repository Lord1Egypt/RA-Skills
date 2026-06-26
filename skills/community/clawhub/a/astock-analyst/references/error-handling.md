# 报错处理手册

## 原则

**永远不信第一次拿到的数据**，遇到报错先自查，再换方案，别卡死。
每次拿到数据，第一步验证合理性：价格在正常范围？字段不是空？数量对？

---

## 一、网络请求报错

### curl: (52) Empty reply from server

**原因**：IPv6连接被拒，或服务器不响应IPv6。

**解决**：
```bash
# 加 --ipv4 强制走IPv4
curl -s --max-time 10 --ipv4 -H "User-Agent: Mozilla/5.0" "https://..."
```

### curl: (28) Operation timed out

**原因**：网络慢或服务器超时。

**解决**：
```bash
# 增加超时时间，单只请求，不批量
curl -s --max-time 15 --ipv4 ...

# 如果单只也超时，等5秒重试一次
sleep 5 && curl -s --max-time 15 --ipv4 ...
```

### curl: (35) SSL connect error

**原因**：SSL握手失败，通常是网络问题。

**解决**：
```bash
# 跳过SSL验证（仅内部数据用，不涉及敏感操作）
curl -s -k --max-time 10 --ipv4 ...
```

### HTTP 403 / 被拦截返回空

**原因**：缺少User-Agent或请求频率过高。

**解决**：
```bash
# 加完整UA头
curl -s --ipv4 -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" ...

# 批量请求时加间隔
sleep 0.5
```

---

## 二、数据解析报错

### JSONDecodeError: Expecting value

**原因**：curl返回空或非JSON内容（被重定向到错误页面）。

**解决**：
```bash
# 先把结果存文件，检查原始内容
curl -s --ipv4 ... > /tmp/debug.json
cat /tmp/debug.json  # 看看返回了什么
```

```python
# Python中加容错
import json
try:
    d = json.loads(raw)
except json.JSONDecodeError:
    print(f"JSON解析失败，原始内容: {raw[:200]}")
    # 使用上一次缓存的数据，或跳过这只股票
```

### KeyError: 'data' 或 'klines'

**原因**：API返回了错误码，data字段为null或结构不同。

**解决**：
```python
d = json.load(f)
if d.get('rc') != 0 or not d.get('data'):
    print(f"API返回异常: rc={d.get('rc')}, msg={d.get('msg','')}")
    # 换备用方案或跳过

klines = d.get('data', {}).get('klines', [])
if len(klines) < 20:
    print(f"K线数据不足({len(klines)}条)，指标计算可能不准")
```

### 价格数据明显异常（如价格=1.69而不是169）

**原因**：API有时返回"分"为单位，有时返回"元"。

**验证方式**：
```python
price = d['data']['f43']
# 验证合理性：A股价格通常在1~3000元
if price < 1 or price > 5000:
    print(f"价格异常: {price}，可能需要÷100")
    price = price / 100
```

**经验规则**：
- push2 stock API（`/qt/stock/get`）：`fltt=2` 时返回元，`fltt=1` 时返回分
- 始终加 `fltt=2` 参数，避免歧义
- 拿到价格后，和常识比对（瑞芯微应该在100~200区间）

---

## 三、指标计算报错

### division by zero（涨跌量不对称比）

**原因**：60日内没有一天上涨（极端情况）。

**解决**：
```python
ratio = dn_vol / up_vol if up_vol > 0 else 999
# 999视为极度出货信号
```

### RSI计算结果异常

**原因**：数据量不足14日，或全部单边涨/跌。

**解决**：
```python
def rsi_f(c, n=14):
    if len(c) < n + 1:
        return None  # 数据不足，跳过RSI
    # ... 计算逻辑 ...
    if loss == 0: return 100  # 全部上涨
    if ag == 0: return 0      # 全部下跌
    return 100 - 100 / (1 + ag / loss)
```

### MACD结果异常（DIF和DEA差距巨大）

**原因**：数据量太少，EMA初始值不稳定（需至少26+9=35日数据）。

**解决**：
```python
klines = d['data']['klines']
if len(klines) < 40:
    print(f"K线仅{len(klines)}条，MACD结果仅供参考")
# 建议用60日以上数据
```

### 布林带计算结果std=0

**原因**：近20日价格完全相同（停牌或数据异常）。

**解决**：
```python
import statistics
window = closes[-20:]
if len(set(window)) == 1:
    print("价格无波动，布林带无法计算（可能停牌）")
else:
    std = statistics.stdev(window)
```

---

## 四、K线字段顺序陷阱

东方财富 push2his K线字段**不是**标准OHLCV顺序：

```
index: 0      1     2     3     4     5
       日期   开盘  收盘  最高  最低  成交量
```

**收盘是p[2]，最高是p[3]，最低是p[4]**，和直觉相反，必须牢记。

验证方法：当日最高>=开盘、收盘、最低，用这个做sanity check：
```python
for k in klines[-5:]:
    p = k.split(',')
    open_, close, high, low = float(p[1]), float(p[2]), float(p[3]), float(p[4])
    assert high >= max(open_, close) and low <= min(open_, close), f"字段顺序可能有误: {k}"
```

---

## 五、datasaver（浏览器工具）报错

### 连接超时 / 工具不可用

**原因**：Chrome插件未启动，或MCP端点失效。

**解决**：
- 检查Chrome是否开启了datasaver插件
- curl直接测试endpoint是否通：
  ```bash
  curl -s -H "Authorization: Bearer mb_xxx" "https://datasaver.deepminingai.com/api/v2/.../mcp" 2>&1 | head -5
  ```
- 如果不通，改用其他数据源（东方财富网页直接fetch）

### 页面内容提取为空

**原因**：页面用JS渲染，需要等待加载完成。

**解决**：在chrome_navigate后等待2~3秒再get_web_content，或重试一次。

---

## 六、通用容错模板

每次拉多只股票，用这个模式，单只失败不影响其他：

```bash
results=""
for item in "1.603893:瑞芯微" "1.603618:杭电股份"; do
  secid="${item%%:*}"; name="${item##*:}"
  data=$(curl -s --max-time 10 --ipv4 -H "User-Agent: Mozilla/5.0" \
    "https://push2.eastmoney.com/api/qt/stock/get?secid=${secid}&fields=f43,f46,f60,f47&fltt=2&invt=2" 2>/dev/null)
  
  if [ -z "$data" ] || echo "$data" | grep -q '"rc":1'; then
    echo "${name}: 获取失败，跳过"
    continue
  fi
  echo "${name}: ${data}"
done
```

Python版：
```python
import urllib.request, json

def fetch_stock(secid, name):
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f46,f60,f47&fltt=2&invt=2"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            d = json.loads(resp.read().decode())
        if d.get('rc') != 0 or not d.get('data'):
            print(f"{name}: API返回异常")
            return None
        return d['data']
    except Exception as e:
        print(f"{name}: 获取失败 - {e}")
        return None
```

---

## 七、数据合理性速查表

拿到数据后，先对照这个表做sanity check：

| 字段 | 合理范围 | 异常处理 |
|------|----------|----------|
| 股价 | 1~3000元 | 检查是否需÷100 |
| 成交量（手） | 100~5000万 | 0或极大值=停牌或数据错误 |
| 涨跌幅 | -10%~+10%（含涨跌停） | 超出范围=数据错误 |
| K线条数 | 请求lmt条，实际≥lmt-5 | 明显不足=数据截断，重新请求 |
| OBV | 任意正负整数 | NaN=计算逻辑有问题 |
| RSI | 0~100 | 超出范围=计算bug |
| 不对称比 | 0.3~3.0 | 极端值=单边市或数据问题 |
