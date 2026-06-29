"""
股海罗盘 (ghdata) - A股股票分析工具包（无MCP版）
======================================
16维数据直接HTTP采集 + WebAPI量化分析 + 14章报告生成

数据采集（全部HTTP直连，无需MCP）:
  fetch_realtime(code)       → 实时行情（新浪+腾讯双源）
  fetch_kline(code, days)    → 日K线（腾讯财经）
  fetch_today_tick(code)     → 今日分时数据
  fetch_money_flow(code)     → 资金流向（同花顺）
  fetch_financial(code)      → 业绩报表（东方财富）
  fetch_balance_sheet(code)  → 资产负债表
  fetch_income_statement(code) → 利润表
  fetch_cashflow(code)       → 现金流量表
  fetch_margin_trading(code) → 融资融券
  fetch_main_holdings(code)  → 机构持仓
  fetch_shareholder_trade(code) → 股东增减持
  fetch_executive_change(code) → 高管持股变动
  fetch_dividend(code)       → 分红历史
  fetch_research_report(code) → 券商研报
  fetch_institutional_survey(code) → 机构调研
  fetch_unlock_data(code)    → 限售解禁

量化分析（需WebAPI）:
  analyze(code)              → WebAPI全量分析（技术指标/信号/规律/准确率/预测）
  screen_stocks(...)          → 基础选股（方向/评分/准确率条件过滤）
  advanced_screen(...)        → 高级选股（动量/反转/技术信号分析）

报告生成:
  generate_report(code)      → 生成14章DOCX分析报告
  chart(code)                → 生成K线图PNG
"""

from . import config
from . import data_fetcher as fetcher
from . import db_manager as db
from . import predictor
from . import pattern_miner
from . import analyzer
from . import chart
from . import reporter

__version__ = "1.0.0"
__author__ = "ghdata"

# ===== 16维数据采集（全部HTTP直连）=====
fetch_realtime = fetcher.fetch_realtime
fetch_kline = fetcher.fetch_kline
fetch_today_tick = fetcher.fetch_today_tick
fetch_money_flow = fetcher.fetch_money_flow
fetch_financial = fetcher.fetch_financial
fetch_balance_sheet = fetcher.fetch_balance_sheet
fetch_income_statement = fetcher.fetch_income_statement
fetch_cashflow = fetcher.fetch_cashflow
fetch_margin_trading = fetcher.fetch_margin_trading
fetch_main_holdings = fetcher.fetch_main_holdings
fetch_shareholder_trade = fetcher.fetch_shareholder_trade
fetch_executive_change = fetcher.fetch_executive_change
fetch_dividend = fetcher.fetch_dividend
fetch_research_report = fetcher.fetch_research_report
fetch_institutional_survey = fetcher.fetch_institutional_survey
fetch_unlock_data = fetcher.fetch_unlock_data
get_company_info = fetcher.get_company_info
fetch_industry_info = fetcher.fetch_industry_info

# ===== 量化分析（需WebAPI）=====
analyze = analyzer.analyze
predict = predictor.analyze
acc_stats = db.get_accuracy_stats
mine_patterns = pattern_miner.mine_all
screen_stocks = db.screen_stocks
advanced_screen = db.advanced_screen

# ===== 报告生成 =====
generate_report = reporter.generate
generate_kline_chart = chart.generate


