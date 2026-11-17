# Cortex API Reference

> 量化策略回测与仿真引擎 - 策略代码 API 文档
> 基于 source code 重构（2026-04-22）

---

## ⚠️ 与聚宽 API 差异概览

| 功能 | 聚宽 API | Cortex API | 差异说明 |
|------|----------|------------|----------|
| **驱动模式** | 数据推送模式 | **数据+时间双重驱动** | ⚠️ 回调不附带数据项 |
| **context.portfolio** | 主账户信息 | 主账户对象 | ✅ 一致 |
| **context.subportfolios** | 子账户数组 | 子账户数组 | ✅ 一致 |
| **多账户结构** | 数组形式 | 数组形式 | ✅ 完全一致 |
| **代码格式** | MIC 格式 (.XSHG/.XSHE) | MIC + Classic 混用 | ✅ 自动转换 |
| **数据源** | 聚宽内部数据 | pyqdt 数据源 | ⚠️ 数据源不同 |
| **未开启真实价格默认复权** | 前复权 (pre) | **后复权 (post)** | ⚠️ 默认值不同 |
| **动态复权（use_real_price）** | 基准日随时间变动 | 基准日=`current_dt` | ✅ 机制一致 |
| **get_price end_date** | 默认昨天 | 默认昨天 | ✅ 一致 |
| **停牌填充** | 默认填充 | 默认填充 (`skip_paused=False`) | ✅ 一致 |
| **T+1 规则** | `closeable_amount` | `closeable_amount` | ✅ 一致 |
| **撮合模式** | 资金不严格限制（可超限） | **宽松+严谨双模式** | ⚠️ Cortex 支持严谨模式 |
| **order_target_value** | 调整市值 | 调整市值 | ✅ 一致 |

---

## 策略回调函数

| 函数名 | 必须 | 触发时机 | 与聚宽差异 |
|--------|------|----------|------------|
| `initialize(context)` | ✅ 必须 | 策略初始化时 | ✅ 一致 |
| `handle_data(context, bar)` | ❌ **不支持** | - | ⚠️ **未来规划**，当前不支持 |
| `before_trading_start(context)` | 可选 | 开盘前 (9:00) | ✅ 一致 |
| `after_trading_end(context)` | 可选 | 收盘后 (15:30) | ✅ 一致 |
| `on_strategy_end(context)` | 可选 | 策略结束 | ✅ 一致 |

**⚠️ 重要差异：**
- Cortex 采用**时间触发模式**（不支持数据推送模式）
- **handle_data 不支持**（未来规划：数据推送模式）
- 策略通过 `run_daily()` 注册定时任务 + `get_bars()` 主动获取数据

---

## 策略设置函数

| 函数 | 参数 | 说明 | 与聚宽差异 |
|------|------|------|------------|
| `set_benchmark(security)` | security: str | 设置基准 | ✅ 一致 |
| `set_option(key, value)` | key, value | 设置选项 | ✅ 一致 |
| `set_order_cost(order_cost, type)` | OrderCost, type | 设置手续费 | ✅ 一致 |
| `set_slippage(slippage, type)` | Slippage, type | 设置滑点 | ✅ 一致 |
| `run_daily(func, time)` | func, time | 注册定时任务 | ✅ 一致 |
| `run_weekly(func, weekday, time)` | func, weekday, time | 注册每周任务 | ✅ 一致 |
| `run_monthly(func, monthday, time)` | func, monthday, time | 注册每月任务 | ✅ 一致 |

### OrderCost 配置

```python
# 聚宽风格
OrderCost(
    close_tax=0.001,          # 卖出印花税（千分之一）
    open_commission=0.0003,   # 买入佣金（万分之三）
    close_commission=0.0003,  # 卖出佣金（万分之一）
    min_commission=5          # 最低佣金（5元）
)

# Cortex 使用 CortexOrderCost（参数一致）
from cortex.strategy_settings import CortexOrderCost
set_order_cost(CortexOrderCost(...), type='stock')
```

### Slippage 配置

```python
# 聚宽风格
PriceRelatedSlippage(0.00246)  # 百分比滑点
FixedSlippage(0.01)            # 固定滑点

# Cortex 使用 CortexSlippage（参数一致）
from cortex.strategy_settings import CortexSlippage
PriceRelatedSlippage(0.00246)  # Cortex 提供 wrapper 函数
FixedSlippage(0.01)
```

### run_daily 时间点

| time 参数 | 触发时机 | 说明 |
|-----------|----------|------|
| `'before_open'` | 9:00 | 开盘前 |
| `'open'` / `'market_open'` | 9:30 | 开盘时 |
| `'after_close'` / `'after_market_close'` | 15:30 | 收盘后 |
| `'every_bar'` | 每个 Bar | Cortex 双重驱动模式可使用 |

---

## 数据获取函数

### 行情数据

| 函数 | 说明 |
|------|------|
| `get_price` | 历史价格数据 |
| `get_bars` | 高性能 K 线数据 |
| `get_trades` | 当日成交记录 |

### 标的信息

| 函数 | 说明 |
|------|------|
| `get_all_securities` | 所有证券列表 |
| `get_security_info` | 证券详细信息 |
| `get_index_stocks` | 指数成分股 |
| `get_index_weights` | 指数成分权重 |

### 行业/概念

| 函数 | 说明 |
|------|------|
| `get_industries` | 行业分类列表 |
| `get_industry_stocks` | 行业成分股 |
| `get_concepts` | 概念板块列表 |
| `get_concept_stocks` | 概念成分股 |

### 交易日历

| 函数 | 说明 |
|------|------|
| `get_trade_days` | 交易日列表（区间） |
| `get_all_trade_days` | 所有交易日 |

### 因子数据

| 函数 | 说明 |
|------|------|
| `get_all_factors` | 因子列表 |
| `get_factor_values` | 因子数据 |

---

### get_price

```python
get_price(
    security,           # 证券代码（支持 MIC/Classic）
    period='day',       # 周期（day/min/tick）
    start_date=None,    # 开始日期
    end_date=None,      # 结束日期（默认昨天）
    count=None,         # 数据数量
    fq=None,            # 复权方式（pre/post/None）
    fields=None,        # 字段列表
    skip_paused=False   # 是否跳过停牌（默认填充）
)
```

**返回：** DataFrame (单标的) 或 dict (多标的)

**示例：**
```python
df = get_price('000001.XSHE', count=30, fq='pre')
```

---

### get_bars

```python
get_bars(
    security,           # 证券代码
    count,              # 数据数量
    unit='1d',          # 周期（1d/5m/3m 等）
    fields=None,        # 字段列表
    include_now=False,  # 是否包含当前 bar
    fq_ref_date=None,   # 复权参考日
    df=False            # 返回格式（False=ndarray）
)
```

**返回：** ndarray (df=False) 或 DataFrame (df=True)

---

### get_trades

```python
get_trades()
```

**返回：** dict 当日成交记录

---

### get_all_securities

```python
get_all_securities(types=['stock'], date=None)
```

**参数：**

| 参数 | 说明 |
|------|------|
| `types` | 类型列表，默认 `['stock']` |
| `date` | 查询日期，默认当前 |

**返回：** DataFrame (display_name, name, start_date, end_date, type)

---

### get_security_info

```python
get_security_info(security)
```

**返回：** DataFrame 证券详细信息

---

### get_index_stocks

```python
get_index_stocks(index_symbol, date=None)
```

**参数：**

| 参数 | 说明 |
|------|------|
| `index_symbol` | 指数代码（如 '000300.XSHG'） |
| `date` | 查询日期 |

**返回：** list 成分股代码

**示例：**
```python
stocks = get_index_stocks('000300.XSHG')
```

---

### get_index_weights

```python
get_index_weights(index_symbol, date=None)
```

**返回：** DataFrame (date, weight, display_name)

---

### get_industries

```python
get_industries(name='zjw', date=None)
```

**参数：**

| 参数 | 说明 |
|------|------|
| `name` | 分类体系，仅支持 `'zjw'`（证监会） |
| `date` | 查询日期 |

**返回：** DataFrame 行业列表

---

### get_industry_stocks

```python
get_industry_stocks(industry_code, date=None)
```

**返回：** list 行业成分股

---

### get_concepts

```python
get_concepts()
```

**返回：** DataFrame 概念板块列表

---

### get_concept_stocks

```python
get_concept_stocks(concept_code, date=None)
```

**返回：** list 概念成分股

---

### get_trade_days

```python
get_trade_days(start_date=None, end_date=None, count=None)
```

**返回：** list[date] 交易日列表

---

### get_all_trade_days

```python
get_all_trade_days()
```

**返回：** list[date] 所有交易日（2005-2028）

---

### get_all_factors

```python
get_all_factors(category=None)
```

**参数：**

| 参数 | 说明 |
|------|------|
| `category` | 因子类别，如 `'quality'`，默认全部 |

**返回：** DataFrame (factor, factor_intro, category)

---

### get_factor_values

```python
get_factor_values(
    securities,     # 股票池
    factors,        # 因子名称
    start_date=None,  # 开始日期（与 count 二选一）
    end_date=None,    # 结束日期
    count=None        # 交易日数量
)
```

**返回：** dict {因子名: DataFrame(index=日期, columns=股票代码)}

---

---

## 下单函数

| 函数 | 说明 |
|------|------|
| `order_target_value` | 调整市值到目标值 |
| `order_target_percent` | 调整比例到目标值 |
| `order_shares` | 买卖指定股数 |
| `order_value` | 按价值买入 |
| `order_target` | 调整到目标数量 |
| `order` | order_shares 别名 |

### order_target_value

```python
order_target_value(code, value, price=None)
```

**参数：**

| 参数 | 说明 |
|------|------|
| `code` | 证券代码 |
| `value` | 目标市值 |
| `price` | 交易价格（默认当前价） |

---

### order_target_percent

```python
order_target_percent(code, percent, price=None)
```

---

### order_shares

```python
order_shares(code, shares, price=None)
```

---

## 全局变量 `g`

```python
g.stock = '000001.XSHE'       # 持久化
g.__temp_cache = {}           # 不持久化（__开头）
```

---

## context 对象

| 属性 | 说明 |
|------|------|
| `portfolio` | 主账户 (= subportfolios[0]) |
| `subportfolios` | 资金账户数组 |
| `current_dt` | 当前时间 |
| `previous_date` | 前一交易日 |
| `g` | 全局变量 |

---

## portfolio 对象

| 属性 | 说明 |
|------|------|
| `total_assets` | 总资产 |
| `total_value` | 总资产（别名） |
| `available_cash` | 可用现金 |
| `positions` | 持仓字典 |
| `market_value` | 持仓市值 |
| `returns` | 累计收益率 |

---

## position 对象

| 属性 | 说明 |
|------|------|
| `total_amount` | 持仓数量 |
| `closeable_amount` | 可卖数量（T+1） |
| `avg_cost` | 平均成本 |
| `price` | 当前价格 |
| `value` | 市值 |

---

## 策略示例

```python
def initialize(context):
    # 聚宽风格设置
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    set_order_cost(OrderCost(
        close_tax=0.001,
        open_commission=0.0003,
        close_commission=0.0003,
        min_commission=5
    ), type='stock')
    
    # 股票池
    g.stock_pool = get_index_stocks('000300.XSHG')
    g.ma_short = 5
    g.ma_long = 20
    
    # 定时任务
    run_daily(rebalance, time='open')

def rebalance(context):
    """开盘时执行"""
    # 获取因子快照
    factors = get_factor_values(
        securities=g.stock_pool,
        factors=['roe_ttm', 'pe_ratio', 'circulating_market_cap'],
        end_date=context.current_dt
    )
    
    roe = factors['roe_ttm'].iloc[-1]
    pe = factors['pe_ratio'].iloc[-1]
    cap = factors['circulating_market_cap'].iloc[-1]
    
    # 选股：ROE > 15, PE < 20, 市值最小的10只
    candidates = roe[(roe > 15) & (pe < 20)].index.tolist()
    candidates.sort(key=lambda x: cap[x])
    selected = candidates[:10]
    
    # 调仓
    for stock in context.portfolio.positions:
        if stock not in selected:
            order_target_value(stock, 0)
    
    for stock in selected:
        order_target_value(stock, context.portfolio.total_assets * 0.1)

def after_trading_end(context):
    """收盘后"""
    log.info(f"总资产: {context.portfolio.total_assets:.2f}")
```

---

## 与聚宽 API 差异附录

### ⚠️ 重要差异

| 功能 | 聚宽 | Cortex | 说明 |
|------|------|--------|------|
| **驱动模式** | 数据推送 | 数据+时间双重驱动 | 回调不附带数据 |
| **handle_data** | ✅ 支持 | ❌ 不支持 | 未来规划 |
| **默认复权** | 前复权 (pre) | 后复权 (post) | set_option 可调整 |
| **撮合模式** | 单一模式 | 双模式（loose/strict） | 严谨模式拟真实柜台 |

### ✅ 一致的特性

| 功能 | 状态 |
|------|------|
| 策略回调函数（initialize/after_trading_end 等） | ✅ 一致 |
| 设置函数（set_benchmark/set_order_cost 等） | ✅ 一致 |
| 下单函数（order_target_value 等） | ✅ 一致 |
| 动态复权机制（use_real_price=True） | ✅ 一致 |
| T+1 规则（closeable_amount） | ✅ 一致 |
| 全局变量 `g` | ✅ 一致 |
| 多账户结构（subportfolios 数组） | ✅ 一致 |

### ✅ 数据获取函数兼容性

| 函数 | 聚宽 | Cortex | 状态 |
|------|------|--------|------|
| `get_price` | ✅ | ✅ | 一致 |
| `get_bars` | ✅ | ✅ | 一致 |
| `get_trades` | ✅ | ✅ | 一致 |
| `get_all_securities` | ✅ | ✅ | 一致 |
| `get_security_info` | ✅ | ✅ | 一致 |
| `get_index_stocks` | ✅ | ✅ | 一致（不支持历史截面） |
| `get_index_weights` | ✅ | ✅ | 一致（不支持历史截面） |
| `get_industries` | ✅ | ✅ | 仅支持 zjw 分类 |
| `get_industry_stocks` | ✅ | ✅ | 一致（不支持历史截面） |
| `get_concepts` | ✅ | ✅ | 一致 |
| `get_concept_stocks` | ✅ | ✅ | 一致（不支持历史截面） |
| `get_trade_days` | ✅ | ✅ | 一致 |
| `get_all_trade_days` | ✅ | ✅ | 一致 |
| `get_all_factors` | ✅ | ✅ | **新增** |
| `get_factor_values` | ✅ | ✅ | **新增** |

### ⚠️ 历史截面数据限制

| 函数 | 聚宽 | Cortex |
|------|------|--------|
| `get_index_stocks(date)` | ✅ 支持历史 | ❌ 仅支持当前 |
| `get_industry_stocks(date)` | ✅ 支持历史 | ❌ 仅支持当前 |
| `get_concept_stocks(date)` | ✅ 支持历史 | ❌ 仅支持当前 |

**原因：** pyqdt 数据源不提供历史截面数据

---

---

## 版本信息

- **模块版本:** Cortex v1.1
- **新增功能:** 因子 API（get_all_factors, get_factor_values）
- **文档重构时间:** 2026-04-22
- **因子功能更新:** 2026-04-29
- **数据获取函数补全:** 2026-04-29
- **数据源:** pyqdt v0.8.2
- **兼容性:** Python 3.10+