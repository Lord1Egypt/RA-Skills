# 📈 A股量化工具包 (Finance Toolkit)

A股量化交易分析工具包，基于腾讯行情API直取数据，零外部依赖即可运行。

## 功能一览

- **实时行情** — 腾讯API直取，无需注册/API密钥
- **技术指标** — MA、RSI、布林带、KDJ、MACD
- **10策略回测** — 一键对比、参数搜索、敏感性分析
- **60分评分** — 6维度实时监控评分体系
- **FFT频谱分析** — K线傅里叶分析，识别主周期
- **多指标融合策略** — 布林带+RSI+KDJ+MACD融合
- **日报生成** — 自动生成A股市场分析日报

## 快速示例

```python
from finance_toolkit.mini_realtime import TencentStockAPI

api = TencentStockAPI()
q = api.get_quote("000009")
print(f"{q['name']}: ¥{q['price']}")
```

更多示例见 [SKILL.md](SKILL.md)。

## 目录

```
finance_toolkit/
├── mini_realtime.py     # 零依赖实时行情（核心）
├── monitor_v3.py        # 实时监控+60分评分
├── backtest_v3.py       # 统一回测框架
├── strategy_v4.py       # 多指标融合策略引擎
├── astock_data.py       # A股数据获取（需akshare）
├── astock_engine.py     # 腾讯行情引擎
├── astock_strategies.py # 策略集（备选）
├── fourier_analyzer.py  # FFT频谱分析
├── strategy_engine.py   # 盯盘策略系统
├── daily_report.py      # 日报生成
└── kline_report.py      # K线图报告
```
