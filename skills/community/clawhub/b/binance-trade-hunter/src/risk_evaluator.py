"""
🛡️ Risk Evaluator v1.0
统一风险评估模块 - 币安交易机会捕手核心组件

功能:
1. 计算风险等级 (1-5)
2. 给出仓位建议
3. 给出止损止盈建议
4. 过滤高风险/低流动性信号
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# ============================================================
# 数据结构
# ============================================================
@dataclass
class RiskResult:
    risk_level: int      # 1-5
    risk_label: str      # 极低/低/中等/高/极高
    position_pct: str    # 仓位建议
    stop_loss: str       # 止损建议
    take_profit: str     # 止盈建议
    action: str          # 建议动作
    reason: str          # 解释原因


# ============================================================
# 风险评估器
# ============================================================
class RiskEvaluator:
    def __init__(self):
        pass

    def evaluate(self,
                 change_pct: float,
                 volume_usdt: float,
                 liquidity_usdt: Optional[float] = None,
                 is_new_coin: bool = False) -> RiskResult:
        """
        风险评估
        
        Args:
            change_pct: 价格涨幅 (%)
            volume_usdt: 24h 成交量
            liquidity_usdt: 流动性（可选）
            is_new_coin: 是否新币
        """
        # 基础风险 (涨幅驱动)
        if change_pct >= 30:
            risk = 5
            reason = "涨幅过大，追高风险极高"
        elif change_pct >= 20:
            risk = 4
            reason = "涨幅较大，追高风险高"
        elif change_pct >= 10:
            risk = 3
            reason = "涨幅明显，风险中等"
        elif change_pct >= 0:
            risk = 2
            reason = "温和波动，风险较低"
        else:
            risk = 2
            reason = "下跌中，风险较低但需谨慎"

        # 成交量调整
        if volume_usdt < 1_000_000:
            risk = min(5, risk + 2)
            reason = "成交量过低，流动性风险高"
        elif volume_usdt < 3_000_000:
            risk = min(5, risk + 1)
            reason = "成交量偏低，需注意滑点"
        elif volume_usdt > 50_000_000:
            risk = max(1, risk - 1)

        # 新币加权
        if is_new_coin:
            risk = min(5, risk + 1)
            reason = "新币波动大，风险上调"

        # 流动性调整（可选）
        if liquidity_usdt is not None:
            if liquidity_usdt < 500_000:
                risk = min(5, risk + 1)
                reason = "流动性不足，风险上调"

        return self.make_advice(risk, reason)

    def make_advice(self, risk: int, reason: str) -> RiskResult:
        """根据风险等级生成建议"""
        if risk <= 1:
            return RiskResult(1, "极低", "50-100%", "-8%", "+20%", "可积极参与", reason)
        if risk == 2:
            return RiskResult(2, "低", "20-50%", "-5%", "+15%", "可小仓试水", reason)
        if risk == 3:
            return RiskResult(3, "中等", "10-20%", "-3%", "+10%", "谨慎参与", reason)
        if risk == 4:
            return RiskResult(4, "高", "5-10%", "-2%", "+6%", "不建议追高", reason)
        return RiskResult(5, "极高", "<5%", "-1%", "+3%", "建议观望", reason)


# ============================================================
# Skill 接口函数
# ============================================================
_evaluator: Optional[RiskEvaluator] = None


def get_evaluator() -> RiskEvaluator:
    global _evaluator
    if _evaluator is None:
        _evaluator = RiskEvaluator()
    return _evaluator


def evaluate_risk(change_pct: float, volume_usdt: float,
                  liquidity_usdt: Optional[float] = None,
                  is_new_coin: bool = False) -> dict:
    """返回风险评估结果（dict）"""
    ev = get_evaluator()
    res = ev.evaluate(change_pct, volume_usdt, liquidity_usdt, is_new_coin)
    return res.__dict__


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    ev = RiskEvaluator()
    print(ev.evaluate(12.5, 2_000_000, is_new_coin=True))
