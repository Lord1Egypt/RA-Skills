#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关键策略指标系统
功能：策略健康度、胜率追踪、最大回撤、夏普比率等
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import math

# ============ 绩效指标 ============

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
    """夏普比率"""
    if not returns or len(returns) < 2:
        return 0
    
    avg_return = sum(returns) / len(returns)
    excess_return = avg_return - risk_free_rate / 252  # 日化
    
    # 标准差
    variance = sum((r - avg_return) ** 2 for r in returns) / (len(returns) - 1)
    std_dev = math.sqrt(variance)
    
    if std_dev == 0:
        return 0
    
    return (excess_return / std_dev) * math.sqrt(252)  # 年化

def calculate_max_drawdown(equity_curve: List[float]) -> float:
    """最大回撤"""
    if not equity_curve:
        return 0
    
    peak = equity_curve[0]
    max_dd = 0
    
    for value in equity_curve:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak if peak > 0 else 0
        if drawdown > max_dd:
            max_dd = drawdown
    
    return max_dd

def calculate_win_rate(trades: List[Dict]) -> float:
    """胜率"""
    if not trades:
        return 0
    
    winning_trades = [t for t in trades if t.get('pnl', 0) > 0]
    return len(winning_trades) / len(trades)

def calculate_profit_factor(trades: List[Dict]) -> float:
    """盈亏比"""
    if not trades:
        return 0
    
    gross_profit = sum(t['pnl'] for t in trades if t['pnl'] > 0)
    gross_loss = abs(sum(t['pnl'] for t in trades if t['pnl'] < 0))
    
    if gross_loss == 0:
        return float('inf') if gross_profit > 0 else 0
    
    return gross_profit / gross_loss

def calculate_expectancy(trades: List[Dict]) -> float:
    """期望值"""
    if not trades:
        return 0
    
    total_pnl = sum(t['pnl'] for t in trades)
    return total_pnl / len(trades)

# ============ 策略健康度 ============

class StrategyHealth:
    """策略健康度评估"""
    
    def __init__(self, strategy_name: str):
        self.strategy_name = strategy_name
        self.trades = []
        self.equity_curve = [1000000]  # 初始资金 100 万
        self.daily_returns = []
        
    def add_trade(self, trade: Dict):
        """添加交易记录"""
        self.trades.append(trade)
        
        # 更新权益曲线
        current_equity = self.equity_curve[-1]
        new_equity = current_equity + trade.get('pnl', 0)
        self.equity_curve.append(new_equity)
        
        # 计算日收益率
        if len(self.equity_curve) > 1:
            daily_return = (self.equity_curve[-1] - self.equity_curve[-2]) / self.equity_curve[-2]
            self.daily_returns.append(daily_return)
    
    def get_health_report(self) -> Dict:
        """生成健康报告"""
        if not self.trades:
            return {"error": "No trades yet"}
        
        # 基础统计
        total_trades = len(self.trades)
        winning_trades = len([t for t in self.trades if t['pnl'] > 0])
        losing_trades = len([t for t in self.trades if t['pnl'] <= 0])
        
        # 盈亏统计
        total_pnl = sum(t['pnl'] for t in self.trades)
        avg_win = sum(t['pnl'] for t in self.trades if t['pnl'] > 0) / winning_trades if winning_trades > 0 else 0
        avg_loss = sum(t['pnl'] for t in self.trades if t['pnl'] < 0) / losing_trades if losing_trades > 0 else 0
        
        # 绩效指标
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        sharpe = calculate_sharpe_ratio(self.daily_returns)
        max_dd = calculate_max_drawdown(self.equity_curve)
        
        # 健康度评分 (0-100)
        health_score = 0
        
        # 胜率评分 (30 分)
        if win_rate > 0.6:
            health_score += 30
        elif win_rate > 0.5:
            health_score += 20
        elif win_rate > 0.4:
            health_score += 10
        
        # 盈亏比评分 (30 分)
        if profit_factor > 2:
            health_score += 30
        elif profit_factor > 1.5:
            health_score += 20
        elif profit_factor > 1:
            health_score += 10
        
        # 夏普比率评分 (20 分)
        if sharpe > 2:
            health_score += 20
        elif sharpe > 1:
            health_score += 15
        elif sharpe > 0:
            health_score += 10
        
        # 最大回撤评分 (20 分)
        if max_dd < 0.1:
            health_score += 20
        elif max_dd < 0.2:
            health_score += 15
        elif max_dd < 0.3:
            health_score += 10
        
        # 健康状态
        if health_score >= 80:
            health_status = "excellent"
            status_emoji = "🟢"
        elif health_score >= 60:
            health_status = "good"
            status_emoji = "🟡"
        elif health_score >= 40:
            health_status = "warning"
            status_emoji = "🟠"
        else:
            health_status = "critical"
            status_emoji = "🔴"
        
        return {
            "strategy": self.strategy_name,
            "timestamp": datetime.now().isoformat(),
            "health_score": health_score,
            "health_status": health_status,
            "status_emoji": status_emoji,
            
            "trade_stats": {
                "total_trades": total_trades,
                "winning_trades": winning_trades,
                "losing_trades": losing_trades,
                "win_rate": f"{win_rate:.2%}"
            },
            
            "pnl_stats": {
                "total_pnl": total_pnl,
                "avg_win": avg_win,
                "avg_loss": avg_loss,
                "profit_factor": f"{profit_factor:.2f}"
            },
            
            "risk_metrics": {
                "sharpe_ratio": f"{sharpe:.2f}",
                "max_drawdown": f"{max_dd:.2%}",
                "current_equity": self.equity_curve[-1]
            },
            
            "recommendations": self.generate_recommendations(win_rate, profit_factor, sharpe, max_dd)
        }
    
    def generate_recommendations(self, win_rate: float, profit_factor: float, 
                                sharpe: float, max_dd: float) -> List[str]:
        """生成改进建议"""
        recs = []
        
        if win_rate < 0.4:
            recs.append("⚠️  胜率偏低，建议优化入场时机或选股条件")
        
        if profit_factor < 1.5:
            recs.append("⚠️  盈亏比偏低，建议设置更合理的止盈止损")
        
        if sharpe < 1:
            recs.append("⚠️  风险调整后收益偏低，建议降低仓位或优化策略")
        
        if max_dd > 0.2:
            recs.append("🚨  最大回撤过大，建议加强风险控制")
        
        if not recs:
            recs.append("✅  策略运行良好，继续保持")
        
        return recs

# ============ 多策略对比 ============

def compare_strategies(strategies: List[StrategyHealth]) -> Dict:
    """多策略对比"""
    comparison = {
        "timestamp": datetime.now().isoformat(),
        "strategies": []
    }
    
    for strategy in strategies:
        report = strategy.get_health_report()
        comparison["strategies"].append({
            "name": strategy.strategy_name,
            "health_score": report.get("health_score", 0),
            "health_status": report.get("health_status", "unknown"),
            "total_pnl": report.get("pnl_stats", {}).get("total_pnl", 0),
            "win_rate": report.get("trade_stats", {}).get("win_rate", "0%"),
            "sharpe": report.get("risk_metrics", {}).get("sharpe_ratio", "0"),
            "max_dd": report.get("risk_metrics", {}).get("max_drawdown", "0%")
        })
    
    # 按健康度排序
    comparison["strategies"].sort(key=lambda x: x["health_score"], reverse=True)
    
    return comparison

# ============ 策略参数优化建议 ============

def suggest_parameter_adjustments(strategy_name: str, current_params: Dict, 
                                  performance: Dict) -> Dict:
    """建议参数调整"""
    suggestions = {}
    
    win_rate = float(performance.get("trade_stats", {}).get("win_rate", "0").replace("%", "")) / 100
    profit_factor = float(performance.get("pnl_stats", {}).get("profit_factor", "0"))
    max_dd = float(performance.get("risk_metrics", {}).get("max_drawdown", "0").replace("%", "")) / 100
    
    # 根据表现建议调整
    if win_rate < 0.4:
        suggestions["entry_criteria"] = "建议收紧入场条件，减少交易频率"
        if "min_change_rate" in current_params:
            suggestions["suggested_params"] = {
                "min_change_rate": current_params["min_change_rate"] * 1.5
            }
    
    if profit_factor < 1.5:
        suggestions["exit_strategy"] = "建议优化止盈止损设置"
        if "take_profit" in current_params:
            suggestions["suggested_params"] = {
                "take_profit": current_params.get("take_profit", 0.05) * 1.2,
                "stop_loss": current_params.get("stop_loss", -0.05) * 0.8
            }
    
    if max_dd > 0.2:
        suggestions["risk_management"] = "建议降低仓位或增加对冲"
        suggestions["suggested_params"] = {
            "position_size": current_params.get("position_size", 100) * 0.7
        }
    
    return {
        "strategy": strategy_name,
        "current_performance": performance,
        "suggestions": suggestions
    }

# ============ 主函数 ============

if __name__ == "__main__":
    # 示例：创建策略健康追踪
    print("📊 关键策略指标系统")
    print("=" * 60)
    
    # 模拟交易记录
    strategy = StrategyHealth("均值回归策略")
    
    # 添加模拟交易
    import random
    for i in range(20):
        pnl = random.gauss(500, 2000)  # 期望 500，标准差 2000
        strategy.add_trade({
            "date": (datetime.now() - timedelta(days=20-i)).isoformat(),
            "symbol": "700.HK",
            "side": "Buy",
            "pnl": pnl
        })
    
    # 生成报告
    report = strategy.get_health_report()
    
    print(f"\n策略：{report['strategy']}")
    print(f"健康度：{report['status_emoji']} {report['health_score']}分 ({report['health_status']})")
    print()
    
    print("📈 交易统计:")
    stats = report['trade_stats']
    print(f"  总交易：{stats['total_trades']}笔")
    print(f"  胜率：{stats['win_rate']}")
    print(f"  盈利：{stats['winning_trades']}笔 | 亏损：{stats['losing_trades']}笔")
    print()
    
    print("💰 盈亏统计:")
    pnl = report['pnl_stats']
    print(f"  总盈亏：{pnl['total_pnl']:+,.2f}")
    print(f"  平均盈利：{pnl['avg_win']:+,.2f}")
    print(f"  平均亏损：{pnl['avg_loss']:+,.2f}")
    print(f"  盈亏比：{pnl['profit_factor']}")
    print()
    
    print("⚠️  风险指标:")
    risk = report['risk_metrics']
    print(f"  夏普比率：{risk['sharpe_ratio']}")
    print(f"  最大回撤：{risk['max_drawdown']}")
    print(f"  当前权益：{risk['current_equity']:,.2f}")
    print()
    
    print("💡 改进建议:")
    for rec in report['recommendations']:
        print(f"  {rec}")
