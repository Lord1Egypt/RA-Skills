# 📈 A股量化工具包 (Finance Toolkit)

A股量化交易工具包，基于腾讯行情API（零依赖、免注册），提供完整的实时行情、技术指标、策略回测、监控评分、日报生成功能。

## 核心模块

| 模块 | 文件 | 功能 |
|------|------|------|
| 🚀 实时行情 | `mini_realtime.py` | 腾讯API直取实时报价/日K/分时，零依赖 |
| 📊 数据获取 | `astock_data.py` | A股全市场数据获取（基于akshare，需安装akshare） |
| ⚙️ 数据引擎 | `astock_engine.py` | 腾讯行情API封装，含缓存和curl调用 |
| 🧮 策略集 | `astock_strategies.py` | 均线金叉/RSI/布林带/KDJ等策略 |
| 🔬 回测系统 | `backtest_v3.py` | 10个策略一键回测+参数搜索+敏感性分析 |
| 📡 实时监控 | `monitor_v3.py` | 6维60分评分体系+FFT频谱分析 |
| 🎯 策略引擎 | `strategy_v4.py` | 多指标融合策略（布林带+RSI+KDJ+MACD） |
| 📋 日报系统 | `daily_report.py` | 自动生成A股市场分析日报 |
| 🔄 FFT分析 | `fourier_analyzer.py` | K线FFT频谱分析，识别主周期 |
| ⚡ 盯盘系统 | `strategy_engine.py` | 腾讯API实时盯盘，技术位判断 |

## 依赖

**最小运行时（实时行情/监控/FFT分析）：零外部依赖**，仅需 Python 3 标准库。
- `mini_realtime.py` — 仅用 `urllib`、`json`、`struct`
- `monitor_v3.py` — 仅用标准库
- `fourier_analyzer.py` — 纯Python FFT

**完整功能需要：**
- pandas、numpy（回测和多指标分析必需）
- akshare（仅 `astock_data.py` 需要，可用 `mini_realtime.py` 替代）
- matplotlib、mplfinance（仅K线图报告 `kline_report.py` 需要）

## 快速开始

### 1. 实时行情（零依赖）

```python
from finance_toolkit.mini_realtime import TencentStockAPI

api = TencentStockAPI()

# 获取实时报价
q = api.get_quote("000009")
print(f"{q['name']}: ¥{q['price']} ({q['change_pct']:+.2f}%)")

# 获取60日日K线
klines = api.get_klines("000009", 60)
closes = [k['close'] for k in klines]
print(f"最新收盘价: {closes[-1]}")
```

### 2. 60分评分体系

```python
from finance_toolkit.mini_realtime import TencentStockAPI, calc_sma, calc_rsi
from finance_toolkit.monitor_v3 import score_stock

api = TencentStockAPI()
result = score_stock("000009", api)
print(f"评分: {result['score']}/60")
print(f"信号: {result['signals']}")
```

### 3. 一键回测10个策略

```python
from finance_toolkit.backtest_v3 import DataFetcher, BacktestEngine, BacktestReport

fetcher = DataFetcher()
df = fetcher.get("sz000009", 500)  # 获取500日K线
dp = BacktestEngine._prepare(df)

# 10个策略对比排名
results = BacktestReport.brief(dp, "中国宝安")
```

### 4. 实时监控+FFT分析

```python
from finance_toolkit.monitor_v3 import monitor_all
from finance_toolkit.mini_realtime import TencentStockAPI
from finance_toolkit.fourier_analyzer import analyze_spectrum, get_strategy_hints

# 监控所有股票
results = monitor_all()

# FFT频谱分析
api = TencentStockAPI()
klines = api.get_klines("000009", 200)
closes = [k['close'] for k in klines]
spectrum = analyze_spectrum(closes)
hints = get_strategy_hints(spectrum)
print(f"主周期: {hints['dominant_cycle']}天")
print(f"建议: {hints['advice']}")
```

### 5. 策略引擎（多指标融合）

```python
from finance_toolkit.strategy_v4 import DataSource, Backtest

ds = DataSource()
df = ds.get_kline("sz000009", 500)
bt = Backtest(df)
result = bt.run("bollinger_rsi_fusion")
print(result['metrics'])
```

### 6. 日报生成

```python
from finance_toolkit.daily_report import generate_daily_report

report = generate_daily_report()
print(report['market_overview'])
```

## 命令行用法

```bash
# 快速回测
python -m finance_toolkit.backtest_v3 brief

# 完整回测+分段分析
python -m finance_toolkit.backtest_v3 full

# 参数扫描优化
python -m finance_toolkit.backtest_v3 scan

# 融合策略参数搜索
python -m finance_toolkit.backtest_v3 fusion_scan
```

## 数据源说明

所有模块默认使用 **腾讯行情API**（`qt.gtimg.cn`），优势：
- ✅ 无需注册，无需API密钥
- ✅ 免费，无调用限制
- ✅ 实时数据，延迟<1秒
- ✅ 支持沪深全市场股票

## 注意事项

- 股票代码格式：沪市 `sh600519`，深市 `sz000009`（腾讯API）或直接 `000009`（mini_realtime）
- 回测使用前复权数据
- 交易策略仅供参考，实盘需谨慎
- 工作日9:30-15:00为实时交易时段，非交易时段返回最新收盘价
