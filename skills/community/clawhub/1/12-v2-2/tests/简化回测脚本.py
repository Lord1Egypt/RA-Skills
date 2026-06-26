#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================
AI量化交易系统 V2.2 简化版回测脚本
===================================

基于V2.1优化版本，添加2个新因子：
1. 量比因子 (5%)
2. 筹码集中度因子 (5%)

版本: V2.2 Simple
创建时间: 2026-02-27
基于: run_backtest_optimized.py (V2.1)
"""

import yaml
import pandas as pd
import numpy as np
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# 配置加载
# ============================================

def load_config(config_file='optimizer_config.yaml'):
    """加载配置文件"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logger.info(f"配置文件加载成功: {config_file}")
        return config
    except Exception as e:
        logger.error(f"配置文件加载失败: {e}")
        # 返回默认配置
        return {
            'strategy': {
                'buy_signal_threshold': 8.5,
                'sell_signal_threshold': 6.5,
                'stop_loss_pct': -0.05,
                'take_profit_pct': 0.10,
                'trailing_stop_pct': 0.03,
                'max_holding_days': 60
            }
        }

# ============================================
# 数据获取
# ============================================

def get_stock_data(stock_code, start_date, end_date):
    """
    获取股票历史数据

    Args:
        stock_code: 股票代码
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        DataFrame: 包含OHLCV数据
    """
    try:
        import akshare as ak

        logger.info(f"获取 {stock_code} 数据: {start_date} ~ {end_date}")

        # 获取数据
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=start_date.replace('-', ''),
            end_date=end_date.replace('-', ''),
            adjust="qfq"  # 前复权
        )

        if df is None or df.empty:
            logger.error(f"未获取到 {stock_code} 的数据")
            return None

        # 标准化列名
        df = df.rename(columns={
            '日期': 'date',
            '开盘': 'open',
            '最高': 'high',
            '最低': 'low',
            '收盘': 'close',
            '成交量': 'volume',
            '成交额': 'amount',
            '涨跌幅': 'pct_chg'
        })

        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)

        logger.info(f"成功获取 {stock_code} 数据: {len(df)} 条")
        return df

    except Exception as e:
        logger.error(f"获取 {stock_code} 数据失败: {e}")
        return None

# ============================================
# V2.2 新增因子计算
# ============================================

def calculate_volume_ratio_signal(df, index):
    """
    量比因子计算 - V2.2新增

    Args:
        df: 数据DataFrame
        index: 当前索引

    Returns:
        float: 信号评分 (0-10)
    """
    if index < 5:
        return 5.0  # 数据不足，返回中性

    # 当前成交量
    current_vol = df.loc[index, 'volume']

    # 5日平均成交量
    avg_vol_5d = df.loc[index-5:index, 'volume'].mean()

    if avg_vol_5d == 0:
        return 5.0

    # 量比
    volume_ratio = current_vol / avg_vol_5d

    # 评分
    if 1.0 <= volume_ratio < 2.0:
        return 6.0  # 正常量能
    elif 2.0 <= volume_ratio < 3.0:
        return 8.0  # 温和放量
    elif 3.0 <= volume_ratio < 5.0:
        return 9.0  # 明显放量
    elif volume_ratio >= 5.0:
        return 5.0  # 巨量，风险增加
    else:
        return 3.0  # 缩量


def calculate_chip_signal(df, index):
    """
    筹码集中度因子计算 - V2.2新增（简化版）

    使用价格波动作为筹码集中度的代理指标
    CV（变异系数）越小，筹码越集中

    Args:
        df: 数据DataFrame
        index: 当前索引

    Returns:
        float: 信号评分 (0-10)
    """
    if index < 60:
        return 5.0  # 数据不足，返回中性

    # 获取最近60天的收盘价
    prices = df.loc[index-60:index, 'close']

    # 计算变异系数
    std_dev = prices.std()
    mean_price = prices.mean()

    if mean_price == 0:
        return 5.0

    cv = (std_dev / mean_price) * 100  # 百分比形式

    # 评分（CV越小，筹码越集中）
    if cv < 5:
        return 9.0   # 高度集中
    elif cv < 10:
        return 7.0   # 较集中
    elif cv < 15:
        return 5.0   # 中等
    elif cv < 20:
        return 4.0   # 较分散
    else:
        return 3.0   # 高度分散


# ============================================
# 技术指标计算
# ============================================

def calculate_indicators(df):
    """
    计算技术指标

    V2.2: 保持V2.1的所有指标，新增量比和筹码计算
    """
    df = df.copy()

    # 1. 移动平均线
    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma10'] = df['close'].rolling(window=10).mean()
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['ma60'] = df['close'].rolling(window=60).mean()

    # 2. 动量指标
    df['momentum'] = df['close'].pct_change(5)  # 5日涨跌幅

    # 3. 均线偏离度
    df['ma_dev'] = (df['close'] - df['ma20']) / df['ma20']

    # 4. 成交量比率
    df['vol_ratio'] = df['volume'] / df['volume'].rolling(window=5).mean()

    # 5. 波动率
    df['volatility'] = df['close'].pct_change().rolling(window=20).std()

    # 6. MACD
    df['ema12'] = df['close'].ewm(span=12).mean()
    df['ema26'] = df['close'].ewm(span=26).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['macd_signal'] = df['macd'].ewm(span=9).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']

    # 7. 布林带
    df['bb_middle'] = df['close'].rolling(window=20).mean()
    df['bb_std'] = df['close'].rolling(window=20).std()
    df['bb_upper'] = df['bb_middle'] + 2 * df['bb_std']
    df['bb_lower'] = df['bb_middle'] - 2 * df['bb_std']
    df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])

    return df


# ============================================
# V2.2 信号计算（8因子）
# ============================================

def calculate_signal_v22(df, index, config):
    """
    V2.2 信号计算 - 8因子评分系统

    因子权重:
    1. 动量指标 - 25%
    2. 均线偏离 - 20%
    3. 成交量 - 15%
    4. 波动率 - 10%
    5. MACD - 10%
    6. 布林带 - 10%
    7. 量比 - 5% (新增)
    8. 筹码集中度 - 5% (新增)

    Returns:
        float: 信号评分 (0-10)
    """
    # 1. 动量指标 (25%)
    momentum = df.loc[index, 'momentum'] if pd.notna(df.loc[index, 'momentum']) else 0
    momentum_signal = ((momentum + 0.15) / 0.30 * 10).clip(0, 10) * 0.25

    # 2. 均线偏离 (20%)
    ma_dev = df.loc[index, 'ma_dev'] if pd.notna(df.loc[index, 'ma_dev']) else 0
    ma_dev_signal = (1 - (ma_dev + 0.10) / 0.20 * 5).clip(0, 10) * 0.20

    # 3. 成交量 (15%)
    vol_ratio = df.loc[index, 'vol_ratio'] if pd.notna(df.loc[index, 'vol_ratio']) else 1
    vol_signal = ((vol_ratio - 0.5) / 1.5 * 5 + 5).clip(0, 10) * 0.15

    # 4. 波动率 (10%)
    volatility = df.loc[index, 'volatility'] if pd.notna(df.loc[index, 'volatility']) else 0.03
    volatility_signal = (1 - volatility / 0.10 * 5).clip(0, 10) * 0.10

    # 5. MACD (10%)
    macd_hist = df.loc[index, 'macd_hist'] if pd.notna(df.loc[index, 'macd_hist']) else 0
    macd_signal = ((macd_hist + 0.05) / 0.10 * 5 + 5).clip(0, 10) * 0.10

    # 6. 布林带 (10%)
    bb_position = df.loc[index, 'bb_position'] if pd.notna(df.loc[index, 'bb_position']) else 0.5
    bb_signal = bb_position * 10 * 0.10

    # ===== V2.2 新增因子 =====
    # 7. 量比 (5%)
    vr_signal = calculate_volume_ratio_signal(df, index) * 0.05

    # 8. 筹码集中度 (5%)
    chip_signal = calculate_chip_signal(df, index) * 0.05

    # 综合评分
    signal = (
        momentum_signal + ma_dev_signal + vol_signal +
        volatility_signal + macd_signal + bb_signal +
        vr_signal + chip_signal  # V2.2新增
    ).clip(0, 10)

    return signal


# ============================================
# 回测引擎
# ============================================

def run_backtest(stock_list, start_date, end_date, config):
    """
    运行回测

    Args:
        stock_list: 股票列表
        start_date: 开始日期
        end_date: 结束日期
        config: 配置字典

    Returns:
        dict: 回测结果
    """
    logger.info("=" * 60)
    logger.info("开始V2.2回测")
    logger.info("=" * 60)
    logger.info(f"股票数量: {len(stock_list)}")
    logger.info(f"回测期间: {start_date} ~ {end_date}")

    # 结果存储
    results = {}

    for stock_code in stock_list:
        logger.info(f"\n{'='*60}")
        logger.info(f"回测股票: {stock_code}")
        logger.info(f"{'='*60}")

        # 获取数据
        df = get_stock_data(stock_code, start_date, end_date)
        if df is None or len(df) < 60:
            logger.warning(f"跳过 {stock_code}（数据不足）")
            continue

        # 计算技术指标
        df = calculate_indicators(df)

        # 回测参数
        buy_threshold = config['strategy']['buy_signal_threshold']
        sell_threshold = config['strategy']['sell_signal_threshold']
        stop_loss = config['strategy']['stop_loss_pct']
        take_profit = config['strategy']['take_profit_pct']
        max_holding_days = config['strategy']['max_holding_days']

        # 初始化
        position = None  # 持仓信息
        trades = []      # 交易记录
        equity = []      # 净值曲线
        initial_capital = 100000
        cash = initial_capital
        shares = 0
        max_price = 0

        logger.info(f"买入阈值: {buy_threshold}")
        logger.info(f"卖出阈值: {sell_threshold}")
        logger.info(f"止损: {stop_loss*100}%")
        logger.info(f"止盈: {take_profit*100}%")

        # 逐日回测
        for i in range(60, len(df)):
            current_date = df.loc[i, 'date']
            current_price = df.loc[i, 'close']

            # 计算V2.2信号
            try:
                signal = calculate_signal_v22(df, i, config)
            except Exception as e:
                logger.error(f"信号计算错误 (索引{i}): {e}")
                signal = 5.0

            # 持仓逻辑
            if shares > 0:
                # 计算收益率
                pnl = (current_price - position['buy_price']) / position['buy_price']

                # 更新最高价
                if current_price > max_price:
                    max_price = current_price

                # 卖出判断（优先级）
                sell_reason = None

                # 1. 止损
                if pnl <= stop_loss:
                    sell_reason = "止损"

                # 2. 止盈
                elif pnl >= take_profit:
                    sell_reason = "止盈"

                # 3. 移动止盈
                elif pnl > 0.05 and current_price < max_price * 0.97:
                    sell_reason = "移动止盈"

                # 4. MACD死叉
                elif i > 0 and df.loc[i-1, 'macd_hist'] > 0 and df.loc[i, 'macd_hist'] < 0:
                    sell_reason = "MACD死叉"

                # 5. 信号减弱
                elif signal <= sell_threshold:
                    sell_reason = "信号减弱"

                # 6. 持仓到期
                elif (current_date - position['buy_date']).days >= max_holding_days:
                    sell_reason = "持仓到期"

                # 执行卖出
                if sell_reason:
                    cash = shares * current_price
                    logger.info(f"{current_date.date()} 卖出: "
                              f"价格={current_price:.2f}, "
                              f"原因={sell_reason}, "
                              f"收益={pnl*100:.2f}%")

                    trades.append({
                        'date': current_date,
                        'action': 'sell',
                        'price': current_price,
                        'reason': sell_reason,
                        'pnl': pnl,
                        'signal': signal
                    })

                    shares = 0
                    position = None
                    max_price = 0

            # 无持仓逻辑
            else:
                # 买入判断
                if signal >= buy_threshold:
                    # MACD金叉确认
                    macd_ok = df.loc[i, 'macd_hist'] > 0 or \
                             (i > 0 and df.loc[i-1, 'macd_hist'] < 0 and df.loc[i, 'macd_hist'] > 0)

                    if macd_ok:
                        # 买入
                        shares = int(cash / current_price)
                        cash -= shares * current_price
                        buy_price = current_price

                        position = {
                            'buy_date': current_date,
                            'buy_price': buy_price,
                            'signal': signal
                        }

                        max_price = buy_price

                        logger.info(f"{current_date.date()} 买入: "
                                  f"价格={buy_price:.2f}, "
                                  f"信号={signal:.2f}")

                        trades.append({
                            'date': current_date,
                            'action': 'buy',
                            'price': buy_price,
                            'signal': signal
                        })

            # 计算净值
            total_value = cash + shares * current_price
            equity.append({
                'date': current_date,
                'equity': total_value,
                'signal': signal
            })

        # 最终结算
        if shares > 0:
            final_price = df.loc[len(df)-1, 'close']
            cash = shares * final_price
            shares = 0

        # 计算性能指标
        final_equity = cash
        total_return = (final_equity - initial_capital) / initial_capital

        equity_df = pd.DataFrame(equity)
        if len(equity_df) > 1:
            equity_df['return'] = equity_df['equity'].pct_change()
            sharpe_ratio = equity_df['return'].mean() / equity_df['return'].std() * np.sqrt(252)
            equity_df['cummax'] = equity_df['equity'].cummax()
            equity_df['drawdown'] = (equity_df['equity'] - equity_df['cummax']) / equity_df['cummax']
            max_drawdown = equity_df['drawdown'].min()
        else:
            sharpe_ratio = 0
            max_drawdown = 0

        # 统计交易次数
        buy_trades = [t for t in trades if t['action'] == 'buy']
        sell_trades = [t for t in trades if t['action'] == 'sell']
        profitable_trades = [t for t in sell_trades if t.get('pnl', 0) > 0]

        results[stock_code] = {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'total_trades': len(buy_trades),
            'profitable_trades': len(profitable_trades),
            'win_rate': len(profitable_trades) / len(sell_trades) if sell_trades else 0
        }

        logger.info(f"\n{stock_code} 回测完成:")
        logger.info(f"  总收益: {total_return*100:.2f}%")
        logger.info(f"  夏普比率: {sharpe_ratio:.2f}")
        logger.info(f"  最大回撤: {max_drawdown*100:.2f}%")
        logger.info(f"  交易次数: {len(buy_trades)}")
        logger.info(f"  盈利次数: {len(profitable_trades)}")
        logger.info(f"  胜率: {results[stock_code]['win_rate']*100:.1f}%")

    return results


# ============================================
# 主程序
# ============================================

def main():
    """主程序"""
    # 加载配置
    config = load_config('optimizer_config.yaml')

    # 测试股票列表
    stock_list = [
        '000858',  # 五粮液
        '000651',  # 格力电器
        '600036',  # 招商银行
        '600276',  # 恒瑞医药
        '000333',  # 美的集团
        '601318',  # 中国平安
        '600519',  # 贵州茅台
        '000002',  # 万科A
        '600030',  # 中信证券
    ]

    # 回测时间
    start_date = '2023-01-01'
    end_date = '2026-02-27'

    # 运行回测
    results = run_backtest(stock_list, start_date, end_date, config)

    # 汇总结果
    logger.info("\n" + "=" * 60)
    logger.info("V2.2回测结果汇总")
    logger.info("=" * 60)

    # 计算平均指标
    avg_return = np.mean([r['total_return'] for r in results.values()])
    avg_sharpe = np.mean([r['sharpe_ratio'] for r in results.values()])
    avg_drawdown = np.mean([r['max_drawdown'] for r in results.values()])
    avg_win_rate = np.mean([r['win_rate'] for r in results.values()])

    # 盈利股票比例
    profitable_stocks = sum(1 for r in results.values() if r['total_return'] > 0)
    profitable_ratio = profitable_stocks / len(results) if results else 0

    logger.info(f"平均收益: {avg_return*100:.2f}%")
    logger.info(f"夏普比率: {avg_sharpe:.2f}")
    logger.info(f"最大回撤: {avg_drawdown*100:.2f}%")
    logger.info(f"胜率: {avg_win_rate*100:.1f}%")
    logger.info(f"盈利股票: {profitable_stocks}/{len(results)} ({profitable_ratio*100:.1f}%)")

    # 详细结果
    logger.info("\n详细结果:")
    for code, result in results.items():
        logger.info(f"  {code}: "
                  f"收益={result['total_return']*100:6.2f}%, "
                  f"夏普={result['sharpe_ratio']:5.2f}, "
                  f"回撤={result['max_drawdown']*100:6.2f}%")

    # 保存结果
    output_file = 'backtest_results_v22_simple.csv'
    results_df = pd.DataFrame(results).T
    results_df.to_csv(output_file)
    logger.info(f"\n结果已保存到: {output_file}")

    logger.info("\n" + "=" * 60)
    logger.info("V2.2回测完成")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
