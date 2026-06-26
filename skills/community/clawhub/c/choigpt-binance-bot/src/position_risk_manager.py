"""
포지션 리스크 관리자 (V4.2)
Kelly Criterion 기반 포지션 사이징
"""

import logging
from typing import Dict, Tuple
import numpy as np
from config.config import *

logger = logging.getLogger(__name__)


class PositionRiskManager:
    """
    Kelly Criterion 기반 위험 관리

    Kelly Criterion: f* = (bp - q) / b
    - f* = 최적 자금 비율
    - b = 손익비 (reward/risk)
    - p = 승률
    - q = 패율 (1-p)
    """

    def __init__(self, win_rate: float = 0.55, avg_win: float = 1.0, avg_loss: float = 1.0):
        """
        Args:
            win_rate: 거래 승률 (0~1)
            avg_win: 평균 승리 금액
            avg_loss: 평균 손실 금액
        """
        self.win_rate = max(0.1, min(0.95, win_rate))  # 10%~95% 범위
        self.avg_win = avg_win
        self.avg_loss = avg_loss
        self.rr_ratio = avg_win / avg_loss if avg_loss > 0 else 1.0

    def calculate_kelly_size(self, confidence: float, risk_pct: float = None) -> float:
        """
        Kelly Criterion으로 포지션 사이징 계산

        Args:
            confidence: 신호 신뢰도 (0~1)
            risk_pct: 위험 자본 비율 (기본값: RISK_PER_TRADE)

        Returns:
            포지션 사이즈 비율 (0~1)
        """
        if risk_pct is None:
            risk_pct = RISK_PER_TRADE / 100.0

        # Kelly % 계산
        b = self.rr_ratio  # 손익비
        p = self.win_rate  # 승률
        q = 1.0 - p        # 패율

        kelly_pct = (b * p - q) / b if b > 0 else 0

        # 보수적 Kelly (Full Kelly의 25%)
        fractional_kelly = kelly_pct * KELLY_FRACTION

        # 신뢰도에 따른 조정
        confidence_adjusted = fractional_kelly * confidence

        # 최대값 제한
        final_size = min(confidence_adjusted, MAX_KELLY_SIZE_PCT / 100.0)
        final_size = max(0.01, final_size)  # 최소 1%

        logger.debug(
            f"Kelly 계산: RR={b:.2f}, p={p:.1%}, Kelly={kelly_pct:.1%}, "
            f"Frac.Kelly={fractional_kelly:.1%}, Conf.Adj={confidence_adjusted:.1%}, "
            f"Final={final_size:.1%}"
        )

        return final_size

    def calculate_position_size(
        self,
        account_balance: float,
        entry_price: float,
        stop_loss: float,
        confidence: float,
        leverage: int = DEFAULT_LEVERAGE
    ) -> Tuple[float, float]:
        """
        계정 잔액 기반 포지션 사이징

        Args:
            account_balance: 계정 잔액 (USDT)
            entry_price: 진입가
            stop_loss: 스탑로스가
            confidence: 신뢰도 (0~1)
            leverage: 레버리지

        Returns:
            (포지션 수량, 사이즈 비율)
        """
        # 리스크 계산
        risk_per_trade_usd = account_balance * (RISK_PER_TRADE / 100.0)

        # 한 거래의 손실폭
        loss_per_unit = abs(entry_price - stop_loss)

        if loss_per_unit <= 0:
            logger.warning("손실폭이 0 이하: 포지션 불가")
            return 0, 0

        # Kelly Criterion 기반 수량
        kelly_size_pct = self.calculate_kelly_size(confidence)

        # 실제 거래 수량
        kelly_quantity = (account_balance * kelly_size_pct) / entry_price

        # 레버리지 적용
        final_quantity = kelly_quantity * leverage

        # 최소 주문 금액 확인 (동적 계산)
        position_usdt = final_quantity * entry_price
        
        # ★ V8.0: 스나이퍼 모드(고신뢰도) 진입 시 최소 증거금 $80 상향 로직
        is_sniper_setup = confidence >= LEVERAGE_CONF_THRESH_HIGH or leverage >= ALT_LEVERAGE_CONF_HIGH
        target_min_usdt = SNIPER_MIN_POSITION_USDT if is_sniper_setup else MIN_POSITION_USDT
        
        dynamic_min_position = min(account_balance * 0.5, target_min_usdt)  # 계정 한도 내에서 최소 금액 보장 
        if position_usdt < dynamic_min_position:
            # 켈리값이 너무 작아도 스나이퍼 타점이면 최소 증거금으로 강제 상향
            if is_sniper_setup and account_balance >= dynamic_min_position:
                logger.info(f"🎯 스나이퍼 타점(Conf {confidence:.0%}): 최소 증거금 ${dynamic_min_position:.2f} 강제 할당")
                position_usdt = dynamic_min_position
                final_quantity = position_usdt / entry_price
            else:
                logger.warning(
                    f"포지션이 너무 작음: ${position_usdt:.2f} < ${dynamic_min_position:.2f}"
                )
                return 0, 0

        # 최대 포지션 제한
        max_position_usdt = account_balance * (MAX_POSITION_SIZE / 100.0)
        if position_usdt > max_position_usdt:
            final_quantity = max_position_usdt / entry_price
            logger.debug(f"포지션 조정: ${position_usdt:.2f} → ${max_position_usdt:.2f}")

        position_ratio = position_usdt / account_balance

        logger.info(
            f"포지션 계산 완료: {final_quantity:.6f}개 (${position_usdt:.2f}), "
            f"비율={position_ratio:.1%}, 레버={leverage}x, Conf={confidence:.0%}"
        )

        return final_quantity, position_ratio

    def check_risk_exposure(
        self,
        account_balance: float,
        open_positions: Dict[str, dict],
        new_position_size: float
    ) -> bool:
        """
        포지션 개설 전 전체 리스크 노출도 확인

        Args:
            account_balance: 계정 잔액
            open_positions: 열린 포지션 딕셔너리
            new_position_size: 신규 포지션 사이즈 (USDT)

        Returns:
            리스크 노출 가능 여부
        """
        # 현재 노출도 계산
        current_exposure = sum(
            abs(pos.get('entry_price', 0) * pos.get('quantity', 0))
            for pos in open_positions.values()
        )

        total_exposure = current_exposure + new_position_size
        exposure_pct = (total_exposure / account_balance) * 100

        if exposure_pct > MAX_TOTAL_EXPOSURE:
            logger.warning(
                f"노출도 초과: {exposure_pct:.1f}% > {MAX_TOTAL_EXPOSURE:.1f}%"
            )
            return False

        logger.debug(f"노출도: {exposure_pct:.1f}% (한도: {MAX_TOTAL_EXPOSURE:.1f}%)")
        return True

    def calculate_risk_reward_ratio(
        self,
        entry: float,
        stop_loss: float,
        take_profit: float
    ) -> float:
        """손익비 계산"""
        risk = abs(entry - stop_loss)
        reward = abs(take_profit - entry)

        if risk <= 0:
            return 0

        return reward / risk

    @staticmethod
    def estimate_Kelly_parameters(trade_history: list) -> Tuple[float, float, float]:
        """
        과거 거래 데이터에서 Kelly 파라미터 추정

        Args:
            trade_history: [{'pnl': ..., 'confidence': ...}, ...] 형식

        Returns:
            (승률, 평균승리, 평균손실)
        """
        if not trade_history:
            return 0.55, 1.0, 1.0

        closed_trades = [t for t in trade_history if t.get('status') == 'CLOSED']
        if not closed_trades:
            return 0.55, 1.0, 1.0

        wins = [t for t in closed_trades if t.get('pnl', 0) > 0]
        losses = [t for t in closed_trades if t.get('pnl', 0) <= 0]

        win_rate = len(wins) / len(closed_trades) if closed_trades else 0.5
        avg_win = np.mean([t.get('pnl', 0) for t in wins]) if wins else 1.0
        avg_loss = abs(np.mean([t.get('pnl', 0) for t in losses])) if losses else 1.0

        return win_rate, avg_win, avg_loss
