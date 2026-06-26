"""
Risk Assessment - 风险评估工具

功能：
- VaR 计算
- 压力测试
- 仓位管理建议
"""

import akshare as ak
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict
from datetime import datetime, timedelta


def calculate_var(code: str, confidence: float = 0.95, days: int = 252) -> Dict:
    """计算 VaR (风险价值)"""
    try:
        df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")
        returns = df['涨跌幅'].dropna()
        
        # 参数法 VaR
        mu = returns.mean()
        sigma = returns.std()
        var_param = stats.norm.ppf(1 - confidence) * sigma - mu
        
        # 历史模拟法 VaR
        var_historical = np.percentile(returns, (1 - confidence) * 100)
        
        return {
            "code": code,
            "updated": datetime.now().isoformat(),
            "confidence": confidence,
            "var_param": round(var_param * 100, 2),
            "var_historical": round(var_historical * 100, 2),
            "volatility": round(sigma * 100, 2),
            "interpretation": f"有{confidence*100}%的把握，单日最大损失不超过{round(abs(var_param)*100, 2)}%"
        }
    except Exception as e:
        return {"error": str(e)}


def position_suggestion(total_capital: float, risk_tolerance: float, stock_price: float, stop_loss: float) -> Dict:
    """仓位建议"""
    try:
        # 基于风险承受能力的仓位计算
        risk_per_share = stock_price * stop_loss
        max_shares = int((total_capital * risk_tolerance) / risk_per_share)
        position_value = max_shares * stock_price
        position_pct = position_value / total_capital * 100
        
        return {
            "updated": datetime.now().isoformat(),
            "total_capital": total_capital,
            "stock_price": stock_price,
            "stop_loss_pct": stop_loss * 100,
            "risk_tolerance": risk_tolerance * 100,
            "max_shares": max_shares,
            "position_value": round(position_value, 2),
            "position_pct": round(position_pct, 2),
            "recommendation": "建议仓位" if position_pct < 30 else "仓位偏高"
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print("测试风险评估")
    print("=" * 50)
    
    var_result = calculate_var("300308")
    print(f"VaR 结果：{var_result}")
    
    position_result = position_suggestion(
        total_capital=1000000,
        risk_tolerance=0.02,
        stock_price=534.80,
        stop_loss=0.10
    )
    print(f"仓位建议：{position_result}")
