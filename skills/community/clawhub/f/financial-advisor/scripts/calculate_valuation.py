#!/usr/bin/env python3
"""
估值分析脚本
- DCF 估值模型（三场景 Bear/Base/Bull + 敏感性分析）
- 可比公司分析（运营指标 + 估值倍数 + 统计基准）
- 三表财务建模分析（利润率/资本结构/运营效率/联动验证）
- 输入：fetch_stock_data.py 采集的数据文件
- 输出：JSON 格式估值结果
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

try:
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"错误：缺少必要的Python库: {e}")
    print("请运行: pip install pandas numpy")
    sys.exit(1)

try:
    import yfinance as yf
except ImportError:
    yf = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# 工具函数
# ============================================================

def safe_float(val, default=0.0):
    """安全转换为 float"""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def to_serializable(obj):
    """递归转换 numpy 类型为 Python 原生类型"""
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    if isinstance(obj, (np.floating, np.float64, np.float32)):
        return round(float(obj), 6)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_serializable(i) for i in obj]
    if isinstance(obj, pd.Timestamp):
        return str(obj)
    return obj


def load_csv_files(data_dir, pattern):
    """加载匹配 pattern 的 CSV 文件"""
    p = Path(data_dir)
    files = list(p.glob(pattern)) + list(p.rglob(pattern))
    for f in files:
        if f.is_file():
            try:
                return pd.read_csv(f)
            except Exception as e:
                logger.warning(f"读取 {f} 失败: {e}")
    return None


def load_json_file(data_dir, pattern):
    """加载匹配 pattern 的 JSON 文件"""
    p = Path(data_dir)
    files = list(p.glob(pattern)) + list(p.rglob(pattern))
    for f in files:
        if f.is_file():
            try:
                with open(f, 'r', encoding='utf-8') as fh:
                    return json.load(fh)
            except Exception as e:
                logger.warning(f"读取 {f} 失败: {e}")
    return None


def get_yfinance_symbol(symbol):
    """转换为 yfinance 格式"""
    symbol = symbol.strip().upper()
    if symbol.endswith(('.SS', '.SZ', '.HK')):
        return symbol
    if symbol.endswith('.SH'):
        return symbol.replace('.SH', '.SS')
    if symbol.isdigit():
        if len(symbol) == 6:
            return f"{symbol}.SS" if symbol.startswith('6') else f"{symbol}.SZ"
        if len(symbol) == 5:
            return f"{symbol}.HK"
    return symbol


# ============================================================
# DCF 估值模型
# ============================================================

def run_dcf(symbol, data_dir, risk_free_rate=0.028, projection_years=5, terminal_growth=0.025, erp=0.055):
    """
    DCF 估值分析
    返回三场景估值结果 + 敏感性矩阵
    """
    logger.info(f"开始 DCF 估值分析: {symbol}")

    # 1. 加载数据
    fundamental_df = load_csv_files(data_dir, '*_fundamental.csv')
    financial_df = load_csv_files(data_dir, '*_financial*.csv')
    realtime_df = load_csv_files(data_dir, '*_realtime.csv')
    history_df = load_csv_files(data_dir, '*_history.csv')

    # 2. 从 yfinance 补充数据
    yf_info = {}
    if yf:
        try:
            yf_sym = get_yfinance_symbol(symbol)
            ticker = yf.Ticker(yf_sym)
            yf_info = ticker.info or {}
        except Exception as e:
            logger.warning(f"yfinance 数据获取失败: {e}")

    # 3. 提取关键财务数据
    revenue = safe_float(yf_info.get('totalRevenue'), 0)
    ebitda = safe_float(yf_info.get('ebitda'), 0)
    net_income = safe_float(yf_info.get('netIncomeToCommon'), 0)
    total_debt = safe_float(yf_info.get('totalDebt'), 0)
    total_cash = safe_float(yf_info.get('totalCash'), 0)
    market_cap = safe_float(yf_info.get('marketCap'), 0)
    shares_outstanding = safe_float(yf_info.get('sharesOutstanding'), 0)
    current_price = safe_float(yf_info.get('currentPrice') or yf_info.get('regularMarketPrice'), 0)
    beta = safe_float(yf_info.get('beta'), 1.0)
    gross_margins = safe_float(yf_info.get('grossMargins'), 0)
    operating_margins = safe_float(yf_info.get('operatingMargins'), 0)
    profit_margins = safe_float(yf_info.get('profitMargins'), 0)
    revenue_growth = safe_float(yf_info.get('revenueGrowth'), 0)
    roe = safe_float(yf_info.get('returnOnEquity'), 0)

    # 从 realtime 补充当前价格
    if current_price == 0 and realtime_df is not None and not realtime_df.empty:
        current_price = safe_float(realtime_df.iloc[0].get('最新价', 0))

    # 从 fundamental 补充
    if fundamental_df is not None and not fundamental_df.empty:
        row = fundamental_df.iloc[0]
        if revenue == 0:
            revenue = safe_float(row.get('营收', row.get('revenue', 0)))
        if market_cap == 0:
            market_cap = safe_float(row.get('市值', row.get('marketCap', 0)))

    if revenue == 0:
        logger.error("无法获取营收数据，DCF 分析需要财务数据")
        return {'error': '营收数据缺失，无法执行 DCF 分析。请确保已采集 fundamental/financial 数据。'}

    # 4. 推算关键比率
    ebit_margin = operating_margins if operating_margins > 0 else 0.15
    da_ratio = 0.04  # D&A / Revenue 默认 4%
    capex_ratio = 0.05  # CapEx / Revenue 默认 5%
    nwc_ratio = 0.02  # ΔNWC / ΔRevenue 默认 2%
    tax_rate = 0.25  # 中国企业一般税率

    # 如果有 EBITDA，推算 D&A
    if ebitda > 0 and revenue > 0:
        ebitda_margin = ebitda / revenue
        if ebit_margin > 0:
            da_ratio = ebitda_margin - ebit_margin

    # 5. WACC 计算
    cost_of_equity = risk_free_rate + beta * erp
    net_debt = total_debt - total_cash
    if market_cap > 0:
        equity_weight = market_cap / (market_cap + max(net_debt, 0))
        debt_weight = 1 - equity_weight
    else:
        equity_weight = 0.8
        debt_weight = 0.2

    cost_of_debt = 0.04  # 默认税前债务成本
    if total_debt > 0 and revenue > 0:
        # 简化估计
        interest_expense = total_debt * 0.04
        cost_of_debt = interest_expense / total_debt if total_debt > 0 else 0.04

    wacc = cost_of_equity * equity_weight + cost_of_debt * (1 - tax_rate) * debt_weight
    wacc = max(wacc, 0.06)  # WACC 下限 6%

    # 6. 三场景预测
    base_growth = revenue_growth if revenue_growth > 0 else 0.10
    scenarios = {
        'bear': {
            'label': '保守 (Bear)',
            'growth_rates': [base_growth * 0.6] + [base_growth * 0.6 * (1 - 0.1 * i) for i in range(1, projection_years)],
            'ebit_margin_adj': -0.02,
        },
        'base': {
            'label': '基准 (Base)',
            'growth_rates': [base_growth] + [base_growth * (1 - 0.08 * i) for i in range(1, projection_years)],
            'ebit_margin_adj': 0,
        },
        'bull': {
            'label': '乐观 (Bull)',
            'growth_rates': [base_growth * 1.3] + [base_growth * 1.3 * (1 - 0.06 * i) for i in range(1, projection_years)],
            'ebit_margin_adj': 0.02,
        },
    }

    results = {}
    for scenario_key, scenario in scenarios.items():
        projected_revenue = [revenue]
        for i in range(projection_years):
            g = max(scenario['growth_rates'][i], terminal_growth)
            projected_revenue.append(projected_revenue[-1] * (1 + g))

        projected_fcf = []
        for i in range(1, projection_years + 1):
            rev = projected_revenue[i]
            rev_prev = projected_revenue[i - 1]
            margin = ebit_margin + scenario['ebit_margin_adj']
            ebit = rev * margin
            nopat = ebit * (1 - tax_rate)
            da = rev * da_ratio
            capex = rev * capex_ratio
            delta_nwc = (rev - rev_prev) * nwc_ratio
            fcf = nopat + da - capex - delta_nwc
            projected_fcf.append(fcf)

        # 终值
        terminal_fcf = projected_fcf[-1] * (1 + terminal_growth)
        terminal_value = terminal_fcf / (wacc - terminal_growth) if wacc > terminal_growth else 0

        # 折现（中年惯例）
        pv_fcfs = []
        for i, fcf in enumerate(projected_fcf):
            period = i + 0.5
            pv = fcf / ((1 + wacc) ** period)
            pv_fcfs.append(pv)

        pv_terminal = terminal_value / ((1 + wacc) ** (projection_years - 0.5))
        enterprise_value = sum(pv_fcfs) + pv_terminal
        equity_value = enterprise_value - net_debt
        per_share_value = equity_value / shares_outstanding if shares_outstanding > 0 else 0

        implied_return = (per_share_value / current_price - 1) * 100 if current_price > 0 else 0

        results[scenario_key] = {
            'label': scenario['label'],
            'growth_rates': [round(g * 100, 1) for g in scenario['growth_rates']],
            'ebit_margin': round((ebit_margin + scenario['ebit_margin_adj']) * 100, 1),
            'projected_revenue': [round(r / 1e8, 2) for r in projected_revenue[1:]],
            'projected_fcf': [round(f / 1e8, 2) for f in projected_fcf],
            'terminal_value': round(terminal_value / 1e8, 2),
            'pv_fcfs_sum': round(sum(pv_fcfs) / 1e8, 2),
            'pv_terminal': round(pv_terminal / 1e8, 2),
            'enterprise_value': round(enterprise_value / 1e8, 2),
            'equity_value': round(equity_value / 1e8, 2),
            'per_share_value': round(per_share_value, 2),
            'implied_return': round(implied_return, 1),
        }

    # 7. 敏感性分析
    sensitivity_wacc_growth = {}
    wacc_range = [wacc - 0.02, wacc - 0.01, wacc, wacc + 0.01, wacc + 0.02]
    growth_range = [0.015, 0.02, 0.025, 0.03, 0.035]

    for w in wacc_range:
        w_key = f"WACC_{round(w * 100, 1)}%"
        sensitivity_wacc_growth[w_key] = {}
        for g in growth_range:
            if w <= g:
                sensitivity_wacc_growth[w_key][f"g_{round(g * 100, 1)}%"] = 'N/A'
                continue
            # 简化 DCF：用 base case FCF
            base_fcf = results['base']['projected_fcf']
            tv = (base_fcf[-1] * 1e8 * (1 + g)) / (w - g)
            pv_sum = sum(f * 1e8 / ((1 + w) ** (i + 0.5)) for i, f in enumerate(base_fcf))
            pv_tv = tv / ((1 + w) ** (projection_years - 0.5))
            ev = pv_sum + pv_tv
            eq = ev - net_debt
            ps = eq / shares_outstanding if shares_outstanding > 0 else 0
            sensitivity_wacc_growth[w_key][f"g_{round(g * 100, 1)}%"] = round(ps, 2)

    dcf_result = {
        'mode': 'dcf',
        'symbol': symbol,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'inputs': {
            'revenue': round(revenue / 1e8, 2),
            'revenue_unit': '亿元',
            'ebit_margin': round(ebit_margin * 100, 1),
            'gross_margin': round(gross_margins * 100, 1),
            'net_margin': round(profit_margins * 100, 1),
            'revenue_growth': round(base_growth * 100, 1),
            'da_ratio': round(da_ratio * 100, 1),
            'capex_ratio': round(capex_ratio * 100, 1),
            'nwc_ratio': round(nwc_ratio * 100, 1),
            'tax_rate': round(tax_rate * 100, 1),
            'risk_free_rate': round(risk_free_rate * 100, 2),
            'beta': round(beta, 2),
            'erp': round(erp * 100, 1),
            'cost_of_equity': round(cost_of_equity * 100, 2),
            'wacc': round(wacc * 100, 2),
            'terminal_growth': round(terminal_growth * 100, 1),
            'net_debt': round(net_debt / 1e8, 2),
            'shares_outstanding': round(shares_outstanding / 1e8, 4),
            'current_price': round(current_price, 2),
        },
        'scenarios': results,
        'sensitivity': sensitivity_wacc_growth,
        'conclusion': {
            'bear_value': results['bear']['per_share_value'],
            'base_value': results['base']['per_share_value'],
            'bull_value': results['bull']['per_share_value'],
            'current_price': round(current_price, 2),
            'base_implied_return': results['base']['implied_return'],
        },
    }

    logger.info(f"DCF 分析完成: Base 每股价值 {results['base']['per_share_value']}, 隐含回报 {results['base']['implied_return']}%")
    return dcf_result


# ============================================================
# 可比公司分析
# ============================================================

def run_comps(symbol, data_dir, peers):
    """
    可比公司分析
    peers: 逗号分隔的可比公司代码列表
    """
    logger.info(f"开始可比公司分析: {symbol} vs {peers}")

    if not yf:
        return {'error': 'yfinance 未安装，无法获取可比公司数据'}

    peer_list = [p.strip() for p in peers.split(',') if p.strip()]
    all_symbols = [symbol] + peer_list

    companies_data = []
    for sym in all_symbols:
        yf_sym = get_yfinance_symbol(sym)
        try:
            ticker = yf.Ticker(yf_sym)
            info = ticker.info or {}

            companies_data.append({
                'symbol': sym,
                'name': info.get('shortName', sym),
                'market_cap': safe_float(info.get('marketCap'), 0),
                'enterprise_value': safe_float(info.get('enterpriseValue'), 0),
                'revenue': safe_float(info.get('totalRevenue'), 0),
                'revenue_growth': safe_float(info.get('revenueGrowth'), 0) * 100,
                'gross_margin': safe_float(info.get('grossMargins'), 0) * 100,
                'ebitda_margin': safe_float(info.get('ebitdaMargins'), 0) * 100,
                'operating_margin': safe_float(info.get('operatingMargins'), 0) * 100,
                'net_margin': safe_float(info.get('profitMargins'), 0) * 100,
                'roe': safe_float(info.get('returnOnEquity'), 0) * 100,
                'roa': safe_float(info.get('returnOnAssets'), 0) * 100,
                'debt_to_equity': safe_float(info.get('debtToEquity'), 0),
                'pe_ttm': safe_float(info.get('trailingPE'), 0),
                'pe_forward': safe_float(info.get('forwardPE'), 0),
                'pb': safe_float(info.get('priceToBook'), 0),
                'ps': safe_float(info.get('priceToSalesTrailing12Months'), 0),
                'ev_ebitda': safe_float(info.get('enterpriseToEbitda'), 0),
                'ev_revenue': safe_float(info.get('enterpriseToRevenue'), 0),
                'peg': safe_float(info.get('pegRatio'), 0),
                'dividend_yield': safe_float(info.get('dividendYield'), 0) * 100,
                'beta': safe_float(info.get('beta'), 0),
            })
            logger.info(f"  ✅ {sym}: {info.get('shortName', sym)}")
        except Exception as e:
            logger.warning(f"  ❌ {sym} 数据获取失败: {e}")
            companies_data.append({'symbol': sym, 'name': sym, 'error': str(e)})

    # 统计基准（仅对可比公司，不含目标公司）
    peer_data = [c for c in companies_data[1:] if 'error' not in c]
    statistics = {}
    metric_keys = ['revenue_growth', 'gross_margin', 'ebitda_margin', 'operating_margin', 'net_margin',
                   'roe', 'pe_ttm', 'pb', 'ps', 'ev_ebitda', 'peg', 'dividend_yield', 'beta']

    for key in metric_keys:
        values = [c[key] for c in peer_data if c.get(key, 0) > 0]
        if len(values) >= 2:
            statistics[key] = {
                'max': round(max(values), 2),
                'p75': round(float(np.percentile(values, 75)), 2),
                'median': round(float(np.median(values)), 2),
                'p25': round(float(np.percentile(values, 25)), 2),
                'min': round(min(values), 2),
            }

    # 隐含估值（基于中位数 PE）
    target = companies_data[0] if companies_data else {}
    implied_valuation = {}
    if 'error' not in target and 'pe_ttm' in statistics:
        target_eps = target.get('revenue', 0) * target.get('net_margin', 0) / 100
        if target_eps > 0 and target.get('market_cap', 0) > 0:
            shares = target['market_cap'] / (target['pe_ttm'] * target_eps / target['market_cap']) if target['pe_ttm'] > 0 else 0
            if shares > 0:
                median_pe = statistics['pe_ttm']['median']
                eps = target_eps / shares
                implied_price = median_pe * eps
                current_price_est = target['market_cap'] / shares
                premium_discount = (current_price_est / implied_price - 1) * 100 if implied_price > 0 else 0
                implied_valuation = {
                    'median_pe': median_pe,
                    'implied_price': round(implied_price, 2),
                    'current_price_est': round(current_price_est, 2),
                    'premium_discount_pct': round(premium_discount, 1),
                }

    comps_result = {
        'mode': 'comps',
        'symbol': symbol,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'target': target,
        'peers': companies_data[1:],
        'statistics': statistics,
        'implied_valuation': implied_valuation,
    }

    logger.info(f"可比公司分析完成: {len(peer_data)} 家可比公司")
    return comps_result


# ============================================================
# 三表财务建模分析
# ============================================================

def run_statements(symbol, data_dir):
    """
    三表财务分析
    分析利润率趋势、资本结构、运营效率、联动验证
    """
    logger.info(f"开始三表财务分析: {symbol}")

    if not yf:
        return {'error': 'yfinance 未安装，无法获取财务报表数据'}

    yf_sym = get_yfinance_symbol(symbol)
    try:
        ticker = yf.Ticker(yf_sym)
        info = ticker.info or {}
    except Exception as e:
        return {'error': f'yfinance 数据获取失败: {e}'}

    # 获取三表数据
    income_stmt = None
    balance_sheet = None
    cash_flow = None

    try:
        income_stmt = ticker.income_stmt
        if income_stmt is not None and hasattr(income_stmt, 'columns'):
            income_stmt = income_stmt.T.reset_index()
    except Exception:
        pass

    try:
        balance_sheet = ticker.balance_sheet
        if balance_sheet is not None and hasattr(balance_sheet, 'columns'):
            balance_sheet = balance_sheet.T.reset_index()
    except Exception:
        pass

    try:
        cash_flow = ticker.cashflow
        if cash_flow is not None and hasattr(cash_flow, 'columns'):
            cash_flow = cash_flow.T.reset_index()
    except Exception:
        pass

    # 利润表分析
    income_analysis = {}
    if income_stmt is not None and len(income_stmt) > 0:
        periods = []
        for _, row in income_stmt.iterrows():
            revenue = safe_float(row.get('Total Revenue', row.get('totalRevenue', 0)))
            gross_profit = safe_float(row.get('Gross Profit', row.get('grossProfit', 0)))
            ebitda = safe_float(row.get('EBITDA', row.get('ebitda', 0)))
            ebit = safe_float(row.get('EBIT', row.get('Operating Income', 0)))
            net_income = safe_float(row.get('Net Income', row.get('Net Income Common Stockholders', 0)))
            period_label = str(row.get('index', row.get('Date', '')))[:10]

            if revenue > 0:
                periods.append({
                    'period': period_label,
                    'revenue': round(revenue / 1e8, 2),
                    'gross_margin': round(gross_profit / revenue * 100, 1) if gross_profit else 0,
                    'ebitda_margin': round(ebitda / revenue * 100, 1) if ebitda else 0,
                    'ebit_margin': round(ebit / revenue * 100, 1) if ebit else 0,
                    'net_margin': round(net_income / revenue * 100, 1) if net_income else 0,
                })
        income_analysis = {
            'periods': periods[:5],
            'unit': '亿元',
        }

    # 资产负债表分析
    balance_analysis = {}
    if balance_sheet is not None and len(balance_sheet) > 0:
        periods = []
        for _, row in balance_sheet.iterrows():
            total_assets = safe_float(row.get('Total Assets', 0))
            total_liabilities = safe_float(row.get('Total Liabilities Net Minority Interest',
                                                    row.get('Total Liab', 0)))
            equity = safe_float(row.get('Stockholders Equity', row.get('Total Stockholder Equity', 0)))
            current_assets = safe_float(row.get('Current Assets', 0))
            current_liabilities = safe_float(row.get('Current Liabilities', 0))
            cash = safe_float(row.get('Cash And Cash Equivalents', row.get('Cash', 0)))
            total_debt = safe_float(row.get('Total Debt', 0))
            period_label = str(row.get('index', row.get('Date', '')))[:10]

            if total_assets > 0:
                periods.append({
                    'period': period_label,
                    'total_assets': round(total_assets / 1e8, 2),
                    'total_liabilities': round(total_liabilities / 1e8, 2),
                    'equity': round(equity / 1e8, 2),
                    'debt_ratio': round(total_liabilities / total_assets * 100, 1),
                    'current_ratio': round(current_assets / current_liabilities, 2) if current_liabilities > 0 else 0,
                    'cash': round(cash / 1e8, 2),
                    'net_debt': round((total_debt - cash) / 1e8, 2),
                })
        balance_analysis = {
            'periods': periods[:5],
            'unit': '亿元',
        }

    # 现金流分析
    cashflow_analysis = {}
    if cash_flow is not None and len(cash_flow) > 0:
        periods = []
        for _, row in cash_flow.iterrows():
            operating_cf = safe_float(row.get('Operating Cash Flow',
                                              row.get('Total Cash From Operating Activities', 0)))
            capex = abs(safe_float(row.get('Capital Expenditure',
                                           row.get('Capital Expenditures', 0))))
            fcf = safe_float(row.get('Free Cash Flow', operating_cf - capex))
            period_label = str(row.get('index', row.get('Date', '')))[:10]

            if operating_cf != 0:
                periods.append({
                    'period': period_label,
                    'operating_cf': round(operating_cf / 1e8, 2),
                    'capex': round(capex / 1e8, 2),
                    'free_cash_flow': round(fcf / 1e8, 2),
                })
        cashflow_analysis = {
            'periods': periods[:5],
            'unit': '亿元',
        }

    # 联动验证
    validation_checks = []
    if balance_sheet is not None and len(balance_sheet) > 0:
        latest = balance_sheet.iloc[0]
        ta = safe_float(latest.get('Total Assets', 0))
        tl = safe_float(latest.get('Total Liabilities Net Minority Interest',
                                    latest.get('Total Liab', 0)))
        eq = safe_float(latest.get('Stockholders Equity',
                                    latest.get('Total Stockholder Equity', 0)))
        if ta > 0:
            balance_diff = abs(ta - tl - eq) / ta * 100
            validation_checks.append({
                'check': 'BS 平衡 (资产=负债+权益)',
                'passed': balance_diff < 1,
                'detail': f"差异 {balance_diff:.2f}%",
            })

    # 运营效率
    operating_efficiency = {
        'roe': round(safe_float(info.get('returnOnEquity'), 0) * 100, 1),
        'roa': round(safe_float(info.get('returnOnAssets'), 0) * 100, 1),
    }

    statements_result = {
        'mode': 'statements',
        'symbol': symbol,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'income_statement': income_analysis,
        'balance_sheet': balance_analysis,
        'cash_flow': cashflow_analysis,
        'operating_efficiency': operating_efficiency,
        'validation': validation_checks,
    }

    logger.info("三表财务分析完成")
    return statements_result


# ============================================================
# 主程序
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='估值分析工具 - DCF/Comps/三表建模',
        epilog='示例: python calculate_valuation.py --symbol 600519.SH --data-dir ./data --output valuation.json --mode dcf'
    )
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--data-dir', required=True, help='数据文件目录')
    parser.add_argument('--output', required=True, help='输出 JSON 文件路径')
    parser.add_argument('--mode', required=True, choices=['dcf', 'comps', 'statements', 'all'],
                        help='分析模式: dcf=DCF估值, comps=可比公司, statements=三表分析, all=全部')
    parser.add_argument('--risk-free-rate', type=float, default=0.028, help='无风险利率（默认 2.8%）')
    parser.add_argument('--projection-years', type=int, default=5, help='预测年数（默认 5）')
    parser.add_argument('--terminal-growth', type=float, default=0.025, help='终值增长率（默认 2.5%）')
    parser.add_argument('--erp', type=float, default=0.055, help='股权风险溢价（默认 5.5%）')
    parser.add_argument('--peers', default='', help='可比公司代码（逗号分隔，comps 模式需要）')
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info(f"估值分析开始: {args.symbol}, 模式: {args.mode}")
    logger.info("=" * 60)

    results = {}

    if args.mode in ('dcf', 'all'):
        results['dcf'] = run_dcf(
            args.symbol, args.data_dir,
            risk_free_rate=args.risk_free_rate,
            projection_years=args.projection_years,
            terminal_growth=args.terminal_growth,
            erp=args.erp,
        )

    if args.mode in ('comps', 'all'):
        if not args.peers:
            logger.warning("comps 模式需要 --peers 参数")
            results['comps'] = {'error': '未指定可比公司，请使用 --peers 参数'}
        else:
            results['comps'] = run_comps(args.symbol, args.data_dir, args.peers)

    if args.mode in ('statements', 'all'):
        results['statements'] = run_statements(args.symbol, args.data_dir)

    # 保存结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    final = results if args.mode == 'all' else results.get(args.mode, results)
    final_clean = to_serializable(final)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_clean, f, ensure_ascii=False, indent=2)

    logger.info("=" * 60)
    logger.info(f"✅ 估值分析完成，结果已保存: {output_path}")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()
