---
name: datahub
description: DataHub统一数据获取层 — 发布-订阅架构整合14个数据源，支持行情/财报/公告/宏观/研报/IR数据获取，智能缓存+优先级路由+模式匹配，提供quick_quote/quick_financial/quick_macro等便捷方法。触发词：获取数据、查行情、查财报、查宏观数据、DataHub、数据订阅、发布订阅。
origin: custom
version: 1.0
---

# DataHub 统一数据获取层

**版本**: v1.0
**状态**: 生产就绪
**代码位置**: `<YOUR_DATAHUB_PATH>`（请配置您的DataHub安装路径）

---

## When to Activate

- 用户需要**获取金融数据**（行情、财报、公告、宏观、研报、IR资讯）
- 用户需要**多数据源对比验证**
- 用户提到**发布-订阅、数据中枢、DataHub**
- 用户需要**批量获取数据**（多只股票、多个指标）
- 用户需要**自然语言查询金融数据**
- 用户需要**构建数据Pipeline**
- 触发词：获取数据、查行情、查财报、宏观经济、DataHub、数据订阅、发布订阅、数据源

---

## 快速开始

### 方式一：便捷函数（推荐）

```python
import asyncio
import sys
sys.path.insert(0, "<YOUR_DATAHUB_PATH>")

from datahub.production_startup import quick_quote, quick_financial, quick_macro, quick_query

async def main():
    # 1. 获取A股行情
    quote = await quick_quote("600519", market='cn')
    print(f"贵州茅台: {quote}")

    # 2. 获取港股行情
    quote_hk = await quick_quote("00656", market='hk')
    print(f"港股: {quote_hk}")

    # 3. 获取美股行情
    quote_us = await quick_quote("AAPL", market='us')
    print(f"Apple: {quote_us}")

    # 4. 获取财报数据
    financial = await quick_financial("600519", report_type='balance')
    print(f"资产负债表: {financial}")

    # 5. 获取宏观数据
    gdp = await quick_macro("GDP", source='fred')
    print(f"GDP数据: {gdp}")

    # 6. 自然语言查询
    result = await quick_query("贵州茅台股价")
    print(f"查询结果: {result}")

asyncio.run(main())
```

### 方式二：完整初始化

```python
import asyncio
import sys
sys.path.insert(0, "<YOUR_DATAHUB_PATH>")

from datahub import get_datahub, register_all_producers

async def main():
    # 初始化DataHub
    datahub = get_datahub()

    # 注册所有Producer（14个数据源）
    producers = register_all_producers(datahub)
    print(f"已注册 {len(producers)} 个Producer")

    # 订阅数据
    received = asyncio.Event()
    result = {}

    async def callback(data):
        result['data'] = data
        result['status'] = 'success'
        received.set()

    # 订阅主题
    datahub.subscribe("westock:cn:quote:600519", callback)

    # 请求刷新
    await datahub.request_refresh("westock:cn:quote:600519")

    # 等待数据
    await asyncio.wait_for(received.wait(), timeout=5.0)
    print(result)

asyncio.run(main())
```

### 方式三：生产环境管理器

```python
import asyncio
import sys
sys.path.insert(0, "<YOUR_DATAHUB_PATH>")

from datahub.production_startup import get_production

async def main():
    # 获取生产环境实例（自动初始化）
    prod = await get_production()

    # 使用便捷方法
    quote = await prod.get_quote("600519")
    financial = await prod.get_financial("600519", report_type='balance')

    # 获取统计信息
    stats = prod.get_stats()
    print(f"统计: {stats}")

asyncio.run(main())
```

---

## 主题命名规范

### 格式

```
{producer}:{data_type}:{market}:{code}
{producer}:{data_type}:{identifier}
```

### 示例

**A股数据**：
- `westock:cn:quote:600519` — 腾讯自选股A股行情
- `a-stock-financial:balance:600519` — A股财报资产负债表
- `a-stock-financial:income:600519` — A股财报利润表
- `a-stock-financial:cashflow:600519` — A股财报现金流量表
- `cninfo:announcement:600519` — 巨潮资讯公告
- `akshare:quote:600519` — AkShare行情
- `neodata:query:贵州茅台股价` — 自然语言查询

**港股数据**：
- `westock:hk:quote:00656` — 港股行情
- `hkex:annual:00656` — 港交所年报
- `irasia:news:00656` — IR Asia新闻

**美股数据**：
- `yfinance:quote:AAPL` — Yahoo Finance行情
- `sec:10k:AAPL` — SEC 10-K文件
- `seekingalpha:rating:AAPL` — Seeking Alpha评级

**宏观数据**：
- `fred:series:GDP` — FRED GDP数据
- `worldbank:indicator:NY.GDP.MKTP.CD` — 世界银行GDP
- `imf:dataflow:CPI` — IMF CPI数据
- `dbnomics:series:*` — DBnomics数据

**本地数据**：
- `wiki:entity:贵州茅台_600519.SH` — 本地Wiki实体
- `wiki:concept:DCF估值` — 本地Wiki概念
- `wiki:raw:某报告.pdf` — 本地Wiki原始文件

---

## 数据源优先级

| 优先级 | Producer | 数据源 | 类型 | API需求 |
|--------|----------|--------|------|---------|
| 1 | LocalWikiProducer | 本地Wiki | 本地 | 无 |
| 8 | CninfoProducer | 巨潮资讯 | 官方 | 无 |
| 9 | SECEdgarProducer | SEC EDGAR | 官方 | 无 |
| 9 | HKEXProducer | 港交所披露易 | 官方 | 无 |
| 10 | EastMoneyProducer | 东方财富 | 在线 | MX_APIKEY |
| 11 | THSProducer | 同花顺问财 | 在线 | IWENCAI_API_KEY |
| 12 | NeoDataProducer | NeoData | 在线 | 无 |
| 13 | WeStockProducer | 腾讯自选股 | 在线 | 无 |
| 15 | AkShareProducer | AkShare | 开源 | 无 |
| 15 | AStockFinancialProducer | A股财报 | 开源 | 无 |
| 16 | YFinanceProducer | YFinance | 开源 | 无 |
| 20 | SeekingAlphaProducer | Seeking Alpha | 第三方 | 无 |
| 30 | FREDProducer | FRED | 官方 | FRED_API_KEY |
| 31 | DBnomicsProducer | DBnomics | 官方 | 无 |
| 32 | WorldBankProducer | 世界银行 | 官方 | 无 |
| 33 | IMFProducer | IMF | 官方 | IMF_COOKIES |
| 40 | AlphaVantageProducer | Alpha Vantage | 第三方 | ALPHAVANTAGE_API_KEY |
| 50 | IRWebsiteProducer | IR网站 | IR | 无 |
| 50 | IRAsiaProducer | IR Asia | IR | 无 |

**优先级规则**：数字越小优先级越高。本地数据 > 官方数据 > 在线数据 > 开源数据 > 第三方数据

---

## 核心功能

### 1. 发布-订阅机制

```python
from datahub import get_datahub, register_all_producers

datahub = get_datahub()
register_all_producers(datahub)

# 精确订阅
def callback(data):
    print(f"收到数据: {data}")

datahub.subscribe("westock:cn:quote:600519", callback)

# 模式订阅（通配符）
datahub.subscribe_pattern("westock:cn:quote:*", callback)

# 请求刷新
await datahub.request_refresh("westock:cn:quote:600519")
```

### 2. 缓存系统

```python
from datahub import get_preconfigured_cache

# 预配置缓存类型
cache = get_preconfigured_cache('quote')  # 5分钟TTL

# 缓存操作
await cache.set("600519", {"price": 1800})
data = await cache.get("600519")
stats = cache.stats()  # {'size': 1, 'max_size': 500, 'ttl': 300}
```

**预配置缓存**：

| 类型 | TTL | 最大条目 | 适用场景 |
|------|-----|---------|---------|
| `quote` | 5分钟 | 500 | 实时行情 |
| `financial` | 1小时 | 200 | 财务报表 |
| `announcement` | 30分钟 | 300 | 公司公告 |
| `macro` | 1天 | 100 | 宏观数据 |
| `research` | 2小时 | 200 | 研报评级 |
| `ir` | 1小时 | 200 | IR资讯 |

### 3. 重试机制

```python
from datahub import with_retry

@with_retry(max_retries=3, base_delay=1.0, max_delay=60.0)
async def fetch_data():
    # 自动重试（指数退避：1秒、2秒、4秒）
    return await api_call()
```

### 4. 性能监控

```python
stats = datahub.get_stats()
print(f"总发布数: {stats['total_publishes']}")
print(f"总错误数: {stats['total_errors']}")
print(f"主题数: {stats['topics_count']}")
print(f"Producer数: {stats['producers_count']}")
```

---

## 常用场景

### 场景1：批量获取行情

```python
import asyncio
from datahub.production_startup import get_production

async def batch_quotes(codes: list) -> dict:
    """批量获取行情"""
    prod = await get_production()
    results = {}

    tasks = []
    for code in codes:
        tasks.append(prod.get_quote(code, market='cn'))

    quotes = await asyncio.gather(*tasks)

    for code, quote in zip(codes, quotes):
        if quote['status'] == 'success':
            results[code] = quote['data']

    return results

# 用法
async def main():
    quotes = await batch_quotes(["600519", "000858", "601318"])
    for code, data in quotes.items():
        print(f"{code}: {data}")

asyncio.run(main())
```

### 场景2：多数据源验证

```python
import asyncio
from datahub import get_datahub, register_all_producers

async def cross_verify_quote(code: str) -> dict:
    """多数据源验证行情"""
    datahub = get_datahub()
    register_all_producers(datahub)

    sources = {
        'westock': f"westock:cn:quote:{code}",
        'akshare': f"akshare:quote:{code}",
    }

    results = {}

    for source_name, topic in sources.items():
        received = asyncio.Event()
        result = {}

        async def callback(data):
            result['data'] = data
            result['status'] = 'success'
            received.set()

        datahub.subscribe(topic, callback)
        await datahub.request_refresh(topic)

        try:
            await asyncio.wait_for(received.wait(), timeout=5.0)
            results[source_name] = result.get('data')
        except asyncio.TimeoutError:
            results[source_name] = None

    return results
```

### 场景3：投研工作流集成

```python
import asyncio
from datahub.production_startup import get_production

async def stock_analysis(code: str) -> dict:
    """个股全面分析"""
    prod = await get_production()

    # 并发获取多维度数据
    quote_task = prod.get_quote(code, market='cn')
    balance_task = prod.get_financial(code, report_type='balance')
    income_task = prod.get_financial(code, report_type='income')

    quote, balance, income = await asyncio.gather(
        quote_task, balance_task, income_task
    )

    return {
        'code': code,
        'quote': quote.get('data') if quote['status'] == 'success' else None,
        'balance': balance.get('data') if balance['status'] == 'success' else None,
        'income': income.get('data') if income['status'] == 'success' else None,
    }
```

### 场景4：自然语言查询

```python
from datahub.production_startup import quick_query

async def main():
    # 自然语言查询
    result = await quick_query("贵州茅台股价")
    print(result)

    result = await quick_query("沪深300市盈率")
    print(result)

    result = await quick_query("中国GDP增长率")
    print(result)

asyncio.run(main())
```

### 场景5：宏观数据追踪

```python
from datahub.production_startup import quick_macro

async def macro_dashboard() -> dict:
    """宏观经济仪表盘"""
    indicators = {
        'GDP': ('GDP', 'fred'),
        'CPI': ('CPIAUCSL', 'fred'),
        'Unemployment': ('UNRATE', 'fred'),
    }

    results = {}
    tasks = []

    for name, (code, source) in indicators.items():
        tasks.append(quick_macro(code, source))

    data = await asyncio.gather(*tasks)

    for (name, _), result in zip(indicators.items(), data):
        results[name] = result

    return results
```

---

## API密钥配置

### 环境变量

```bash
# 同花顺问财
IWENCAI_API_KEY=your_key_here

# FRED美联储
FRED_API_KEY=your_key_here

# Alpha Vantage
ALPHAVANTAGE_API_KEY=your_key_here

# 东方财富妙想
MX_APIKEY=your_key_here

# IMF Cookies
IMF_COOKIES_BM_SV=your_cookie_here
IMF_COOKIES_AUTH=your_cookie_here
IMF_COOKIES_BM_S=your_cookie_here
```

### 加载配置

```python
from dotenv import load_dotenv
load_dotenv()

from datahub import init_datahub, register_all_producers

datahub = init_datahub()
producers = register_all_producers(datahub)
```

---

## 错误处理

### 错误类型

| 错误类型 | 原因 | 处理方式 |
|---------|------|---------|
| `timeout` | 网络超时 | 自动重试 |
| `not_found` | 主题无匹配Producer | 返回错误 |
| `api_error` | API密钥失效/配额耗尽 | 记录日志 |
| `parse_error` | 数据格式异常 | 记录日志 |

### 错误处理示例

```python
from datahub.production_startup import quick_quote

async def safe_get_quote(code: str) -> dict:
    """安全的行情获取"""
    try:
        result = await quick_quote(code, market='cn')

        if result['status'] == 'success':
            return result['data']
        elif result['status'] == 'timeout':
            print(f"获取 {code} 超时")
            return None
        else:
            print(f"获取 {code} 失败: {result.get('error')}")
            return None

    except Exception as e:
        print(f"异常: {e}")
        return None
```

---

## 性能指标

| 操作 | 耗时 | 说明 |
|------|------|------|
| DataHub初始化 | <10ms | 单例模式 |
| Producer注册 | <50ms | 14个Producer |
| 订阅主题 | <1ms | 模式匹配 |
| 缓存命中 | <10ms | LRU缓存 |
| 首次数据获取 | 0.1-2s | 网络请求 |
| 批量获取(10只) | 0.1-0.5s | 并发请求 |

---

## 故障排查

### Q: Producer未注册

```python
# 检查Producer注册状态
from datahub import get_datahub, register_all_producers

datahub = get_datahub()
producers = register_all_producers(datahub)
print(f"已注册Producer: {len(producers)}")
```

### Q: 主题匹配失败

```python
# 检查主题匹配
from datahub import get_datahub, register_all_producers

datahub = get_datahub()
register_all_producers(datahub)

topic = "westock:cn:quote:600519"
matched = datahub.pattern_index.match(topic)
print(f"匹配到的Producer: {len(matched)}")

for producer in matched:
    print(f"  - {producer.__class__.__name__}")
```

### Q: API密钥未配置

```python
# 检查API配置
from datahub.registry import api_registry

for name, config in api_registry.apis.items():
    status = "✅" if config.enabled else "❌"
    key_status = "已配置" if config.api_key else "未配置"
    print(f"{status} {name}: {key_status}")
```

---

## 相关文档

- `datahub/PRODUCTION_GUIDE.md` — 生产环境使用指南
- `datahub/examples_research_workflow.py` — 投研工作流示例
- `datahub/quick_test.py` — 核心功能测试脚本

---

**DataHub已生产就绪，可投入实际投研工作流使用！**
