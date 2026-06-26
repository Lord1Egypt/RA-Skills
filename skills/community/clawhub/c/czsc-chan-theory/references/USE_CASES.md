# Known Use Cases (KUC)

Total: **10**

## `KUC-101`
**Source**: `docs/source/conf.py`

Configuring Sphinx documentation builder for the czsc project, ensuring proper Python path setup and Rust version priority.

## `KUC-102`
**Source**: `examples/develop/czsc_benchmark.py`

Benchmarking CZSC analysis performance with varying K-line counts to measure initialization speed and memory usage.

## `KUC-103`
**Source**: `examples/develop/test_trading_view_kline.py`

Testing and demonstrating K-line visualization using trading_view_kline function with mock data.

## `KUC-104`
**Source**: `examples/signals_dev/bar_volatility_V241013.py`

Classifying market volatility into three tiers (low/middle/high) based on recent K-line price ranges for signal generation.

## `KUC-105`
**Source**: `examples/signals_dev/signal_match.py`

Parsing and analyzing signal definitions from czsc.signals module using SignalsParser for research and configuration purposes.

## `KUC-106`
**Source**: `examples/use_backtest_report.py`

Generating HTML and PDF backtest reports from trading strategy performance data for analysis and presentation.

## `KUC-107`
**Source**: `examples/use_cta_research.py`

Using CTAResearch framework to develop and test CTA trading strategies with mock data through backtesting.

## `KUC-108`
**Source**: `examples/use_html_report_builder.py`

Creating flexible HTML reports with custom headers, performance metrics, charts, and tables using HtmlReportBuilder.

## `KUC-109`
**Source**: `examples/use_optimize.py`

Optimizing entry and exit trading signals by systematically searching candidate signal combinations to find optimal parameters.

## `KUC-110`
**Source**: `examples/事件策略研究工具使用案例.ipynb`

Researching event-based trading strategies using CZSC objects for K-line analysis,笔 detection, and chart visualization.
