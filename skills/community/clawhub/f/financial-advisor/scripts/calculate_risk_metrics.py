#!/usr/bin/env python3
"""
风险指标计算脚本
- 计算波动率、最大回撤、夏普比率、Beta、VaR等风险指标
- 输入：历史K线数据（CSV/JSON）
- 输出：风险指标数据（JSON）
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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def calculate_returns(prices):
    """计算收益率"""
    return prices.pct_change().dropna()


def calculate_volatility(returns, periods_per_year=252):
    """计算年化波动率"""
    return returns.std() * np.sqrt(periods_per_year)


def calculate_max_drawdown(prices):
    """计算最大回撤"""
    cumulative = (1 + prices.pct_change()).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_dd = drawdown.min()
    
    # 找到最大回撤的起止点（使用 iloc 避免 DatetimeIndex 切片 KeyError）
    try:
        trough_idx = int(drawdown.argmin())
        end_date = drawdown.index[trough_idx]
        subset = cumulative.iloc[: trough_idx + 1]
        peak_date = subset.idxmax()
        peak_str, trough_str = str(peak_date), str(end_date)
    except Exception:
        peak_str, trough_str = '', ''
    
    return {
        'max_drawdown': max_dd,
        'max_drawdown_pct': max_dd * 100,
        'peak_date': peak_str,
        'trough_date': trough_str
    }


def calculate_sharpe_ratio(returns, risk_free_rate=0.03, periods_per_year=252):
    """计算夏普比率"""
    if returns.std() == 0 or len(returns) < 2:
        return 0.0
    excess_returns = returns - risk_free_rate / periods_per_year
    return float(np.sqrt(periods_per_year) * excess_returns.mean() / returns.std())


def calculate_sortino_ratio(returns, risk_free_rate=0.03, periods_per_year=252):
    """计算索提诺比率（只考虑下行波动）"""
    downside_returns = returns[returns < 0]
    if len(downside_returns) == 0 or downside_returns.std() == 0:
        return 0.0
    excess_returns = returns - risk_free_rate / periods_per_year
    return float(np.sqrt(periods_per_year) * excess_returns.mean() / downside_returns.std())


def calculate_beta(stock_returns, market_returns):
    """计算Beta系数"""
    covariance = np.cov(stock_returns, market_returns)[0][1]
    market_variance = market_returns.var()
    return covariance / market_variance


def calculate_var(returns, confidence_level=0.95):
    """计算VaR（风险价值）"""
    return np.percentile(returns, (1 - confidence_level) * 100)


def calculate_cvar(returns, confidence_level=0.95):
    """计算CVaR（条件风险价值）"""
    var = calculate_var(returns, confidence_level)
    return returns[returns <= var].mean()


def calculate_calmar_ratio(returns, prices, periods_per_year=252):
    """计算卡玛比率（年化收益率/最大回撤）"""
    annual_return = (1 + returns.mean()) ** periods_per_year - 1
    max_dd = calculate_max_drawdown(prices)['max_drawdown']
    return annual_return / abs(max_dd) if max_dd != 0 else 0


def calculate_all_risk_metrics(df, market_df=None, risk_free_rate=0.03):
    """计算所有风险指标"""
    logger.info("开始计算风险指标...")
    
    prices = df['Close']
    returns = calculate_returns(prices)
    
    # 基础指标（使用 iloc 避免 DatetimeIndex 下 [0] 引发 KeyError）
    symbol_val = ''
    if '股票代码' in df.columns:
        try:
            symbol_val = str(df['股票代码'].iloc[0]) if len(df) > 0 else ''
        except (KeyError, IndexError):
            pass
    metrics = {
        '股票代码': symbol_val,
        '计算时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '数据来源': '风险指标计算',
        '数据期间': f"{df.index[0]} 至 {df.index[-1]}",
        '数据天数': len(df),
        
        # 收益指标
        '累计收益率': ((prices.iloc[-1] / prices.iloc[0]) - 1),
        '累计收益率_百分比': f"{((prices.iloc[-1] / prices.iloc[0]) - 1) * 100:.2f}%",
        '年化收益率': (1 + returns.mean()) ** 252 - 1,
        '年化收益率_百分比': f"{((1 + returns.mean()) ** 252 - 1) * 100:.2f}%",
        '平均日收益率': returns.mean(),
        '平均日收益率_百分比': f"{returns.mean() * 100:.4f}%",
        
        # 波动率指标
        '日波动率': returns.std(),
        '日波动率_百分比': f"{returns.std() * 100:.2f}%",
        '年化波动率': calculate_volatility(returns),
        '年化波动率_百分比': f"{calculate_volatility(returns) * 100:.2f}%",
        
        # 最大回撤
        '最大回撤': calculate_max_drawdown(prices),
        
        # 风险调整收益指标
        '夏普比率': calculate_sharpe_ratio(returns, risk_free_rate),
        '索提诺比率': calculate_sortino_ratio(returns, risk_free_rate),
        '卡玛比率': calculate_calmar_ratio(returns, prices),
        
        # VaR指标
        'VaR_95': calculate_var(returns, 0.95),
        'VaR_95_百分比': f"{calculate_var(returns, 0.95) * 100:.2f}%",
        'VaR_99': calculate_var(returns, 0.99),
        'VaR_99_百分比': f"{calculate_var(returns, 0.99) * 100:.2f}%",
        'CVaR_95': calculate_cvar(returns, 0.95),
        'CVaR_95_百分比': f"{calculate_cvar(returns, 0.95) * 100:.2f}%",
        
        # 收益分布
        '正收益天数': (returns > 0).sum(),
        '负收益天数': (returns < 0).sum(),
        '胜率': (returns > 0).sum() / len(returns),
        '胜率_百分比': f"{(returns > 0).sum() / len(returns) * 100:.2f}%",
        '最大单日涨幅': returns.max(),
        '最大单日涨幅_百分比': f"{returns.max() * 100:.2f}%",
        '最大单日跌幅': returns.min(),
        '最大单日跌幅_百分比': f"{returns.min() * 100:.2f}%",
    }
    
    # 如果提供了市场数据，计算Beta
    if market_df is not None and 'Close' in market_df.columns:
        market_returns = calculate_returns(market_df['Close'])
        # 对齐日期
        aligned_stock, aligned_market = returns.align(market_returns, join='inner')
        if len(aligned_stock) > 0:
            metrics['Beta'] = calculate_beta(aligned_stock, aligned_market)
            metrics['相关系数'] = np.corrcoef(aligned_stock, aligned_market)[0][1]
    
    # 添加英文键供 generate_html_report 等下游使用
    max_dd_dict = metrics['最大回撤']
    metrics['max_drawdown'] = max_dd_dict.get('max_drawdown', 0)
    metrics['sharpe_ratio'] = metrics['夏普比率']
    metrics['annual_volatility'] = metrics['年化波动率']
    metrics['sortino_ratio'] = metrics['索提诺比率']
    metrics['calmar_ratio'] = metrics['卡玛比率']
    metrics['VaR_95'] = metrics.get('VaR_95', 0)
    metrics['annual_return'] = metrics['年化收益率']
    if 'Beta' in metrics:
        metrics['beta'] = metrics['Beta']

    logger.info("风险指标计算完成")
    return metrics


def main():
    parser = argparse.ArgumentParser(description='风险指标计算工具')
    parser.add_argument('--input', required=True, help='输入文件路径（历史K线数据）')
    parser.add_argument('--output', required=True, help='输出文件路径（JSON）')
    parser.add_argument('--market', help='市场指数数据（用于计算Beta）')
    parser.add_argument('--risk-free-rate', type=float, default=0.03, help='无风险利率(default 3%%)')
    args = parser.parse_args()
    
    # 读取数据
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"输入文件不存在: {input_path}")
        sys.exit(1)
    
    if input_path.suffix == '.csv':
        df = pd.read_csv(input_path)
        # 列名映射（兼容中文和英文）
        column_mapping = {
            '日期': 'Date', '开盘': 'Open', '收盘': 'Close', '最高': 'High', 
            '最低': 'Low', '成交量': 'Volume'
        }
        df.rename(columns=column_mapping, inplace=True)
        
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], utc=True)
            df.set_index('Date', inplace=True)
        else:
            df.index = pd.to_datetime(df.index, utc=True)
    elif input_path.suffix == '.json':
        df = pd.read_json(input_path)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], utc=True)
            df.set_index('Date', inplace=True)
    else:
        logger.error("不支持的文件格式，仅支持 CSV 和 JSON")
        sys.exit(1)
    
    # 确保有Close列
    if 'Close' not in df.columns:
        logger.error(f"数据中缺少Close列，当前列: {list(df.columns)}")
        sys.exit(1)
    
    # 读取市场数据（如果提供）
    market_df = None
    if args.market:
        market_path = Path(args.market)
        if market_path.exists():
            if market_path.suffix == '.csv':
                market_df = pd.read_csv(market_path, index_col=0, parse_dates=True)
            elif market_path.suffix == '.json':
                market_df = pd.read_json(market_path)
                if 'Date' in market_df.columns:
                    market_df['Date'] = pd.to_datetime(market_df['Date'])
                    market_df.set_index('Date', inplace=True)
    
    # 计算风险指标
    metrics = calculate_all_risk_metrics(df, market_df, args.risk_free_rate)
    
    # 保存结果（转换 numpy 类型为 Python 原生类型以支持 JSON 序列化）
    def to_serializable(obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {k: to_serializable(v) for k, v in obj.items()}
        return obj

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_clean = to_serializable(metrics)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metrics_clean, f, ensure_ascii=False, indent=2)
    
    logger.info(f"风险指标已保存: {output_path}")
    
    # 打印关键指标
    logger.info(f"\n=== 风险指标摘要 ===")
    logger.info(f"累计收益率: {metrics['累计收益率_百分比']}")
    logger.info(f"年化收益率: {metrics['年化收益率_百分比']}")
    logger.info(f"年化波动率: {metrics['年化波动率_百分比']}")
    logger.info(f"最大回撤: {metrics['最大回撤']['max_drawdown_pct']:.2f}%")
    logger.info(f"夏普比率: {metrics['夏普比率']:.2f}")
    logger.info(f"索提诺比率: {metrics['索提诺比率']:.2f}")
    logger.info(f"VaR(95%): {metrics['VaR_95_百分比']}")
    logger.info(f"胜率: {metrics['胜率_百分比']}")


if __name__ == '__main__':
    main()
