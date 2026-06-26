"""
Backtrader回测示例
基于视频第3集内容整理

包含：
1. 基础回测框架
2. 因子选股策略
3. IC分析
4. 参数优化
"""

import backtrader as bt
import pandas as pd
import numpy as np
from datetime import datetime


# ============================================
# 1. 因子回测策略
# ============================================

class FactorBacktestStrategy(bt.Strategy):
    """
    基于因子的多因子选股策略
    
    调仓逻辑：
    1. 每周/每5天调仓一次
    2. 选取因子排名前N的标的
    3. 等权配置
    """
    
    params = (
        ('hold_days', 5),      # 调仓周期
        ('top_n', 20),          # 选股数量
        ('factor_col', 'mfi'),  # 排序因子
        ('printlog', False),
    )
    
    def __init__(self):
        self.order_dict = {}  # 跟踪订单
        self.rebalance_count = 0
        
    def log(self, txt, dt=None):
        if self.params.printlog:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()} {txt}')
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'买入执行, {order.data._name}, 价格: {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'卖出执行, {order.data._name}, 价格: {order.executed.price:.2f}')
        
        self.order_dict[order.data._name] = None
    
    def next(self):
        # 非调仓日不操作
        self.rebalance_count += 1
        if self.rebalance_count % self.params.hold_days != 0:
            return
        
        # 获取当前日期
        date = self.datas[0].datetime.date(0)
        
        # 获取所有标的的因子值
        factor_values = {}
        for d in self.datas:
            try:
                factor_val = d.factor_col[0] if hasattr(d, 'factor_col') else 0
                factor_values[d._name] = factor_val
            except:
                factor_values[d._name] = 0
        
        # 选取因子值最高的前N只
        sorted_stocks = sorted(factor_values.items(), key=lambda x: x[1], reverse=True)
        selected = [s[0] for s in sorted_stocks[:self.params.top_n]]
        
        # 当前持仓
        current_positions = [d._name for d in self.datas if self.getposition(d).size > 0]
        
        # 调仓
        target_weight = 1.0 / len(selected) if selected else 0
        
        for d in self.datas:
            pos = self.getposition(d).size
            
            if d._name in selected:
                # 需要持有
                if pos == 0:
                    # 买入
                    target_value = self.broker.getvalue() * target_weight
                    size = int(target_value / d.close[0] / 100) * 100  # 整手
                    if size > 0:
                        self.buy(data=d, size=size)
            else:
                # 不需要持有
                if pos > 0:
                    # 卖出
                    self.close(data=d)
    
    def stop(self):
        if self.params.printlog:
            self.log(f'策略结束, 资金: {self.broker.getvalue():.2f}')


# ============================================
# 2. IC分析器
# ============================================

class ICAnalyzer(bt.Analyzer):
    """
    计算因子IC值
    """
    
    def __init__(self):
        self.ic_series = []
        
    def next(self):
        # 获取当日所有标的的因子值和收益
        factors = {}
        returns = {}
        
        for d in self.datas:
            try:
                factors[d._name] = d.factor_col[0] if hasattr(d, 'factor_col') else 0
                returns[d._name] = d.ret[0] if hasattr(d, 'ret') else 0
            except:
                pass
        
        if len(factors) > 2:
            # 计算IC（Spearman相关）
            from scipy.stats import spearmanr
            factor_vals = list(factors.values())
            return_vals = list(returns.values())
            
            ic, _ = spearmanr(factor_vals, return_vals)
            if not np.isnan(ic):
                self.ic_series.append(ic)
    
    def get_analysis(self):
        ic_series = np.array(self.ic_series)
        return {
            'ic_mean': ic_series.mean(),
            'ic_std': ic_series.std(),
            'ic_ir': ic_series.mean() / ic_series.std() if ic_series.std() > 0 else 0,
        }


# ============================================
# 3. 运行回测
# ============================================

def run_backtest(data_dict, initial_cash=1000000):
    """
    运行回测
    
    Parameters:
    -----------
    data_dict : dict
        {symbol: pd.DataFrame} 行情数据
    initial_cash : float
        初始资金
    
    Returns:
    --------
    cerebro : Cerebro
        回测引擎
    """
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(initial_cash)
    cerebro.broker.setcommission(commission=0.001)  # 千分之一手续费
    
    # 添加数据
    for symbol, df in data_dict.items():
        data_feed = bt.feeds.PandasData(
            dataname=df,
            datetime=0,
            open=1,
            high=2,
            low=3,
            close=4,
            volume=5,
            openinterest=-1
        )
        cerebro.adddata(data_feed, name=symbol)
    
    # 添加策略
    cerebro.addstrategy(FactorBacktestStrategy, hold_days=5, top_n=20)
    
    # 添加分析器
    cerebro.addanalyzer(ICAnalyzer, _name='ic')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    
    # 运行
    results = cerebro.run()
    
    return cerebro, results


# ============================================
# 4. 参数优化
# ============================================

def optimize_parameters(data_dict):
    """
    优化调仓周期和选股数量
    """
    best_params = None
    best_value = 0
    
    for hold_days in [3, 5, 10, 20]:
        for top_n in [10, 20, 30, 50]:
            cerebro, results = run_backtest(
                data_dict,
                hold_days=hold_days,
                top_n=top_n
            )
            final_value = cerebro.broker.getvalue()
            
            print(f'hold_days={hold_days}, top_n={top_n}, '
                  f'final_value={final_value:.2f}')
            
            if final_value > best_value:
                best_value = final_value
                best_params = (hold_days, top_n)
    
    print(f'\n最佳参数: hold_days={best_params[0]}, top_n={best_params[1]}')
    return best_params


# ============================================
# 5. 示例使用
# ============================================

if __name__ == '__main__':
    # 准备数据
    # data_dict = load_factor_data()  # 从QuestDB加载
    
    # 运行回测
    # cerebro, results = run_backtest(data_dict)
    
    # 获取分析结果
    # ic_analysis = results[0].analyzers.ic.get_analysis()
    # print(f"IC均值: {ic_analysis['ic_mean']:.4f}")
    # print(f"IC_IR: {ic_analysis['ic_ir']:.4f}")
    
    print("Backtrader回测示例")
    print("请加载真实因子数据后运行")
