"""
Risk Control Gate & State Machine
P0: Pre-trade risk checks, circuit breakers, position limits
"""
import sys
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

# ============ Configuration ============
ENABLE_RISK_GATE = True
MAX_POSITION_PCT = 0.10        # 单标的最大仓位 10%
MAX_LEVERAGE = 2.0              # 最大杠杆
STOP_LOSS_PCT = 0.02             # 单笔止损 2%
TAKE_PROFIT_PCT = 0.04          # 止盈 4%
MAX_DAILY_DRAWDOWN_PCT = 0.03   # 日内最大回撤 3%
MAX_CONSECUTIVE_LOSSES = 4      # 连亏熔断
COOLDOWN_MINUTES = 60           # 熔断冷却


class RiskState(Enum):
    """风控状态机"""
    NORMAL = "normal"           # 正常运行
    WARNING = "warning"         # 警告（接近阈值）
    CIRCUIT_BREAKER = "circuit_breaker"  # 熔断中
    COOLDOWN = "cooldown"       # 冷却中
    RECOVERED = "recovered"     # 已恢复


class TradeDecision(Enum):
    """交易决策"""
    ALLOW = "allow"            # 允许交易
    BLOCK = "block"             # 阻止交易
    REDUCE = "reduce"           # 减少仓位


@dataclass
class RiskMetrics:
    """风险指标快照"""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    current_pnl: float = 0.0           # 当前盈亏
    daily_pnl: float = 0.0            # 今日盈亏
    daily_peak: float = 0.0           # 今日最高
    daily_drawdown: float = 0.0      # 今日回撤
    consecutive_losses: int = 0       # 连亏次数
    total_trades: int = 0             # 总交易次数
    winning_trades: int = 0           # 盈利次数
    losing_trades: int = 0            # 亏损次数
    win_rate: float = 0.0             # 胜率
    avg_win: float = 0.0              # 平均盈利
    avg_loss: float = 0.0             # 平均亏损


@dataclass
class RiskCheckResult:
    """风险检查结果"""
    decision: TradeDecision
    blocked: bool
    reason: str
    details: Dict[str, Any] = field(default_factory=dict)
    metrics: Optional[RiskMetrics] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision": self.decision.value,
            "blocked": self.blocked,
            "reason": self.reason,
            "details": self.details,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


class RiskMetricsTracker:
    """风险指标追踪器"""
    
    def __init__(self):
        self.metrics = RiskMetrics()
        self.trade_history: List[Dict] = []
        self.daily_start_equity: float = 0.0
        self.peak_equity: float = 0.0
    
    def record_trade(self, trade_result: Dict):
        """记录交易结果"""
        self.trade_history.append({
            "timestamp": datetime.now(timezone.utc),
            "pnl": trade_result.get("pnl", 0),
            "outcome": trade_result.get("outcome", "unknown")  # win/loss
        })
        
        # 更新统计
        self.metrics.total_trades += 1
        pnl = trade_result.get("pnl", 0)
        self.metrics.current_pnl += pnl
        
        if pnl > 0:
            self.metrics.winning_trades += 1
            self.metrics.consecutive_losses = 0
        elif pnl < 0:
            self.metrics.losing_trades += 1
            self.metrics.consecutive_losses += 1
        
        # 计算胜率
        if self.metrics.total_trades > 0:
            self.metrics.win_rate = self.metrics.winning_trades / self.metrics.total_trades
        
        # 计算平均盈亏
        if self.metrics.winning_trades > 0:
            wins = [t["pnl"] for t in self.trade_history if t["pnl"] > 0]
            self.metrics.avg_win = np.mean(wins) if wins else 0
        if self.metrics.losing_trades > 0:
            losses = [t["pnl"] for t in self.trade_history if t["pnl"] < 0]
            self.metrics.avg_loss = abs(np.mean(losses)) if losses else 0
    
    def update_daily_metrics(self, current_equity: float):
        """更新每日指标"""
        if self.daily_start_equity == 0:
            self.daily_start_equity = current_equity
            self.peak_equity = current_equity
        
        # 更新峰值
        if current_equity > self.peak_equity:
            self.peak_equity = current_equity
        
        # 计算回撤
        self.metrics.daily_peak = self.peak_equity
        self.metrics.daily_pnl = current_equity - self.daily_start_equity
        self.metrics.daily_drawdown = (self.peak_equity - current_equity) / self.peak_equity if self.peak_equity > 0 else 0
    
    def reset_daily(self):
        """重置每日统计"""
        self.daily_start_equity = 0
        self.peak_equity = 0
        self.metrics.daily_pnl = 0
        self.metrics.daily_peak = 0
        self.metrics.daily_drawdown = 0
    
    def get_metrics(self) -> RiskMetrics:
        return self.metrics


class RiskStateMachine:
    """风控状态机"""
    
    def __init__(self):
        self.state = RiskState.NORMAL
        self.state_since = datetime.now(timezone.utc)
        self.triggered_rules: List[str] = []
        self.metrics_tracker = RiskMetricsTracker()
        
        # Cooldown tracking
        self.last_cooldown_end: Optional[datetime] = None
    
    def transition_to(self, new_state: RiskState, reason: str = ""):
        """状态转换"""
        if self.state != new_state:
            self.state = new_state
            self.state_since = datetime.now(timezone.utc)
            if reason:
                self.triggered_rules.append(f"{new_state.value}: {reason}")
    
    def check_circuit_breaker(self) -> bool:
        """检查是否触发熔断"""
        metrics = self.metrics_tracker.get_metrics()
        
        # 连亏检查
        if metrics.consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
            self.transition_to(RiskState.CIRCUIT_BREAKER, f"连亏{metrics.consecutive_losses}次")
            return True
        
        # 日内回撤检查
        if metrics.daily_drawdown >= MAX_DAILY_DRAWDOWN_PCT:
            self.transition_to(RiskState.CIRCUIT_BREAKER, f"日内回撤{metrics.daily_drawdown:.1%}")
            return True
        
        return False
    
    def get_cooldown_remaining(self) -> int:
        """获取冷却剩余时间（秒）"""
        if self.last_cooldown_end is None:
            return 0
        
        now = datetime.now(timezone.utc)
        if now < self.last_cooldown_end:
            return (self.last_cooldown_end - now).seconds
        return 0
    
    def recover(self):
        """恢复正常状态"""
        self.transition_to(RiskState.RECOVERED, "人工恢复")
        self.triggered_rules = []


class RiskGate:
    """交易前风控闸门"""
    
    def __init__(self):
        self.state_machine = RiskStateMachine()
        self.enabled = ENABLE_RISK_GATE
    
    def check(
        self,
        signal_confidence: float,
        signal_direction: str,  # bullish/bearish/neutral
        proposed_position_pct: float,
        current_equity: float
    ) -> RiskCheckResult:
        """
        执行风控检查
        
        Args:
            signal_confidence: 信号置信度 0-1
            signal_direction: 信号方向
            proposed_position_pct: 建议仓位比例
            current_equity: 当前资金
            
        Returns:
            RiskCheckResult: 检查结果
        """
        if not self.enabled:
            return RiskCheckResult(
                decision=TradeDecision.ALLOW,
                blocked=False,
                reason="风控已禁用"
            )
        
        # 更新每日指标
        self.state_machine.metrics_tracker.update_daily_metrics(current_equity)
        
        # 1. 状态机检查
        if self.state_machine.state == RiskState.CIRCUIT_BREAKER:
            cooldown_rem = self.state_machine.get_cooldown_remaining()
            return RiskCheckResult(
                decision=TradeDecision.BLOCK,
                blocked=True,
                reason=f"熔断中，冷却剩余 {cooldown_rem} 秒",
                details={
                    "state": self.state_machine.state.value,
                    "triggered_rules": self.state_machine.triggered_rules[-3:]
                }
            )
        
        # 2. 连亏熔断检查
        if self.state_machine.check_circuit_breaker():
            return RiskCheckResult(
                decision=TradeDecision.BLOCK,
                blocked=True,
                reason=f"触发熔断规则: {self.state_machine.triggered_rules[-1]}",
                details={"state": self.state_machine.state.value}
            )
        
        # 3. 仓位检查
        if proposed_position_pct > MAX_POSITION_PCT:
            return RiskCheckResult(
                decision=TradeDecision.REDUCE,
                blocked=False,
                reason=f"仓位超过上限 ({proposed_position_pct:.1%} > {MAX_POSITION_PCT:.1%})",
                details={
                    "requested": proposed_position_pct,
                    "max_allowed": MAX_POSITION_PCT,
                    "adjusted": MAX_POSITION_PCT
                }
            )
        
        # 4. 置信度检查
        MIN_SIGNAL_CONFIDENCE = 0.60
        if signal_confidence < MIN_SIGNAL_CONFIDENCE:
            return RiskCheckResult(
                decision=TradeDecision.BLOCK,
                blocked=True,
                reason=f"信号置信度不足 ({signal_confidence:.2f} < {MIN_SIGNAL_CONFIDENCE})",
                details={"confidence": signal_confidence}
            )
        
        # 5. 方向检查
        if signal_direction == "neutral":
            return RiskCheckResult(
                decision=TradeDecision.BLOCK,
                blocked=True,
                reason="中性信号，不建议交易",
                details={"direction": signal_direction}
            )
        
        # 6. 检查是否接近熔断阈值（警告）
        metrics = self.state_machine.metrics_tracker.get_metrics()
        warnings = []
        
        if metrics.consecutive_losses >= MAX_CONSECUTIVE_LOSSES - 1:
            warnings.append(f"连亏警告: {metrics.consecutive_losses}/{MAX_CONSECUTIVE_LOSSES}")
        
        if metrics.daily_drawdown >= MAX_DAILY_DRAWDOWN_PCT * 0.8:
            warnings.append(f"回撤警告: {metrics.daily_drawdown:.1%} / {MAX_DAILY_DRAWDOWN_PCT:.1%}")
        
        if warnings:
            self.state_machine.transition_to(RiskState.WARNING, "; ".join(warnings))
        
        return RiskCheckResult(
            decision=TradeDecision.ALLOW,
            blocked=False,
            reason="通过风控检查",
            details={
                "state": self.state_machine.state.value,
                "warnings": warnings,
                "position_approved": min(proposed_position_pct, MAX_POSITION_PCT)
            },
            metrics=metrics
        )
    
    def record_outcome(self, trade_result: Dict):
        """记录交易结果（用于后续风控判断）"""
        self.state_machine.metrics_tracker.record_trade(trade_result)
        
        # 检查是否需要进入冷却
        metrics = self.state_machine.metrics_tracker.get_metrics()
        if metrics.consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
            self.state_machine.last_cooldown_end = datetime.now(timezone.utc) + timedelta(minutes=COOLDOWN_MINUTES)
    
    def get_status(self) -> Dict[str, Any]:
        """获取风控状态"""
        metrics = self.state_machine.metrics_tracker.get_metrics()
        return {
            "enabled": self.enabled,
            "state": self.state_machine.state.value,
            "state_since": self.state_machine.state_since.isoformat(),
            "cooldown_remaining_sec": self.state_machine.get_cooldown_remaining(),
            "triggered_rules": self.state_machine.triggered_rules[-5:],
            "metrics": {
                "total_trades": metrics.total_trades,
                "win_rate": f"{metrics.win_rate:.1%}",
                "consecutive_losses": metrics.consecutive_losses,
                "daily_pnl": f"${metrics.daily_pnl:.2f}",
                "daily_drawdown": f"{metrics.daily_drawdown:.1%}",
                "avg_win": f"${metrics.avg_win:.2f}",
                "avg_loss": f"${metrics.avg_loss:.2f}"
            }
        }


# Global risk gate instance
_risk_gate: Optional[RiskGate] = None

def get_risk_gate() -> RiskGate:
    global _risk_gate
    if _risk_gate is None:
        _risk_gate = RiskGate()
    return _risk_gate


def check_trade_risk(
    signal_confidence: float,
    signal_direction: str,
    proposed_position_pct: float = 0.1,
    current_equity: float = 10000.0
) -> RiskCheckResult:
    """便捷函数：快速风控检查"""
    gate = get_risk_gate()
    return gate.check(signal_confidence, signal_direction, proposed_position_pct, current_equity)
