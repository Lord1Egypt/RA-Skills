"""
거래 시스템 통합 레이어 (Trade Integration Layer)
- Trade Journal과 data_fetcher 통합
- Trade Review 자동 실행
- Strategy Learner 자동 학습 및 피드백
- Telegram 보고서 전송

이 모듈은 live_trader.py 또는 main.py에서 호출됩니다.
"""

import logging
from datetime import datetime
from typing import Optional, List
import json

from src.trade_journal import TradeJournal, CompletedTrade
from src.trade_review import TradeReviewAnalyzer
from scripts.strategy_learner import StrategyLearner
from scripts.telegram_trader_notifier import (
    notify_entry, notify_exit, notify_daily_summary,
    notify_signal_effectiveness, notify_error
)

logger = logging.getLogger(__name__)


class TradeIntegrationManager:
    """거래 시스템 통합 관리자"""

    def __init__(self):
        self.journal = TradeJournal()
        self.reviewer = TradeReviewAnalyzer()
        self.learner = StrategyLearner(self.journal)

        logger.info("🔗 Trade Integration Manager 초기화 완료")

    def record_trade_entry(self, symbol: str, direction: str, entry_price: float,
                          quantity: float, leverage: int, reasons: List[str],
                          confidence_score: float = 0.5, rr_ratio: float = 0.0,
                          stop_loss: float = 0.0, take_profit: float = 0.0,
                          take_profit2: float = 0.0, sl_id: Optional[str] = None,
                          notify_telegram: bool = True):
        """거래 진입 기록"""

        self.journal.record_entry(
            symbol=symbol,
            direction=direction,
            entry_price=entry_price,
            quantity=quantity,
            leverage=leverage,
            reasons=reasons,
            confidence_score=confidence_score,
            rr_ratio=rr_ratio,
            stop_loss=stop_loss,
            take_profit=take_profit,
            take_profit2=take_profit2,
            sl_id=sl_id
        )

        # Telegram 알림
        if notify_telegram:
            try:
                notify_entry(
                    symbol=symbol,
                    direction=direction,
                    entry_price=entry_price,
                    quantity=quantity,
                    leverage=leverage,
                    reasons=reasons,
                    confidence_score=confidence_score,
                    rr_ratio=rr_ratio
                )
            except Exception as e:
                logger.warning(f"⚠️ Telegram 진입 알림 실패: {e}")

    def record_trade_exit(self, symbol: str, exit_price: float, exit_type: str,
                         realized_pnl: float, pnl_pct: float,
                         notify_telegram: bool = True) -> Optional[CompletedTrade]:
        """
        거래 종료 기록 및 자동 복기

        Args:
            symbol: 거래 심볼
            exit_price: 종료 가격
            exit_type: 종료 유형 ('TP1', 'TP2', 'SL', 'MANUAL')
            realized_pnl: 실현 손익 (USDT)
            pnl_pct: 손익률 (%)
            notify_telegram: Telegram 알림 여부

        Returns:
            완료된 거래 객체 및 자동 복기 분석
        """

        # 1. 거래 종료 기록
        completed_trade = self.journal.record_exit(
            symbol=symbol,
            exit_price=exit_price,
            exit_type=exit_type,
            realized_pnl=realized_pnl,
            pnl_pct=pnl_pct
        )

        if completed_trade is None:
            return None

        # 2. 자동 복기 분석
        review = self.reviewer.analyze_trade(completed_trade)

        # 3. 복기 결과 로깅
        self._log_trade_review(completed_trade, review)

        # 4. Telegram 알림
        if notify_telegram:
            try:
                notify_exit(completed_trade)
            except Exception as e:
                logger.warning(f"⚠️ Telegram 종료 알림 실패: {e}")

        # 5. 실시간 학습 (선택사항: 매 거래마다 또는 배치)
        # self.learner.learn()  # 매 거래마다 학습 (성능 주의)

        return completed_trade

    def learn_from_trades(self, trades: Optional[List[CompletedTrade]] = None,
                         notify_telegram: bool = True):
        """
        축적된 거래로부터 학습 실행
        일반적으로 일일 주기로 호출됩니다.
        """

        self.learner.learn(trades)

        # 학습 결과 리포트 생성
        summary = self.learner.get_performance_summary()
        logger.info(f"\n{summary}")

        # Telegram 알림
        if notify_telegram:
            try:
                trades = trades or self.journal.completed_trades
                signal_eff = self.reviewer.get_signal_effectiveness(trades)
                if signal_eff:
                    notify_signal_effectiveness(signal_eff)
            except Exception as e:
                logger.warning(f"⚠️ Telegram 학습 알림 실패: {e}")

        return summary

    def get_signal_confidence(self, reasons: List[str],
                            base_confidence: float = 0.5) -> tuple:
        """
        신호 분석 및 Confidence Score 추천

        Returns:
            (confidence_score, warnings_list)
        """

        return self.learner.get_signal_recommendation(
            reasons=reasons,
            current_confidence=base_confidence
        )

    def get_monthly_performance(self, month: Optional[str] = None) -> dict:
        """월별 성과 조회"""

        stats = self.journal.calculate_monthly_stats(month)

        # 신호별 효율성 추가
        trades = self.journal.get_monthly_trades(month)
        signal_eff = self.reviewer.get_signal_effectiveness(trades)

        stats['signal_effectiveness'] = signal_eff

        return stats

    def generate_daily_report(self) -> str:
        """일일 복기 보고서 생성"""

        trades = self.journal.get_monthly_trades()
        report = self.reviewer.generate_review_report(trades)

        return report

    def get_active_positions(self) -> dict:
        """현재 활성 포지션 조회"""

        return self.journal.get_active_trades()

    def get_completed_trades(self, symbol: Optional[str] = None,
                            month: Optional[str] = None) -> List[CompletedTrade]:
        """완료된 거래 조회"""

        if month is not None:
            return self.journal.get_monthly_trades(month)

        return self.journal.get_completed_trades(symbol)

    def export_journal(self, output_file: Optional[str] = None) -> str:
        """거래 일지 내보내기"""

        return self.journal.export_all_trades(output_file)

    def _log_trade_review(self, trade: CompletedTrade, review: dict):
        """복기 결과 상세 로깅"""

        is_win = trade.pnl_pct > 0
        win_loss = "✅ WIN" if is_win else "❌ LOSS"

        logger.info(f"\n{'='*60}")
        logger.info(f"📋 거래 복기: {win_loss}")
        logger.info(f"{'='*60}")
        logger.info(f"심볼: {trade.symbol} | 방향: {trade.direction}")
        logger.info(
            f"진입: {trade.entry_price} → 종료: {trade.exit_price} "
            f"({trade.exit_type})"
        )
        logger.info(
            f"손익: {trade.pnl_pct:+.2f}% ({trade.realized_pnl:+.4f} USDT) "
            f"| 보유: {trade.duration_minutes}분"
        )

        logger.info(f"신호 강도: {review['signal_analysis']['signal_strength']}")

        for rec in review['recommendations']:
            logger.info(f"  💡 {rec}")

        logger.info(f"{'='*60}\n")

    def save_state(self, state_file: str = "data/bot_state.json"):
        """현재 상태를 bot_state.json에 통합 저장"""

        try:
            import json
            from pathlib import Path

            state_path = Path(state_file)
            state_path.parent.mkdir(parents=True, exist_ok=True)

            # 현재 상태 구성
            state = {
                'timestamp': datetime.now().isoformat(),
                'active_positions': {
                    symbol: {
                        'direction': entry.direction,
                        'entry_price': entry.entry_price,
                        'quantity': entry.quantity,
                        'leverage': entry.leverage,
                        'entry_time': entry.entry_time,
                        'reasons': entry.reasons,
                        'confidence_score': entry.confidence_score,
                        'rr_ratio': entry.rr_ratio
                    }
                    for symbol, entry in self.journal.active_trades.items()
                },
                'completed_trades': [
                    t.to_dict() for t in self.journal.completed_trades[-50:]  # 최근 50개
                ],
                'monthly_stats': self.get_monthly_performance(),
                'learner_summary': {
                    'total_signal_weights': len(self.learner.signal_weights),
                    'total_signal_combinations': len(self.learner.signal_combinations)
                }
            }

            with open(state_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)

            logger.info(f"💾 상태 저장 완료: {state_file}")

        except Exception as e:
            logger.error(f"❌ 상태 저장 실패: {e}")


# 글로벌 싱글톤 인스턴스 (모듈 로드 시 자동 초기화)
_integration_manager: Optional[TradeIntegrationManager] = None


def get_integration_manager() -> TradeIntegrationManager:
    """싱글톤 인스턴스 취득"""

    global _integration_manager

    if _integration_manager is None:
        _integration_manager = TradeIntegrationManager()

    return _integration_manager


# 편의 함수들
def record_entry(symbol: str, direction: str, entry_price: float,
                quantity: float, leverage: int, reasons: List[str],
                confidence_score: float = 0.5, rr_ratio: float = 0.0):
    """거래 진입 기록 (전역 함수)"""

    get_integration_manager().record_trade_entry(
        symbol=symbol,
        direction=direction,
        entry_price=entry_price,
        quantity=quantity,
        leverage=leverage,
        reasons=reasons,
        confidence_score=confidence_score,
        rr_ratio=rr_ratio
    )


def record_exit(symbol: str, exit_price: float, exit_type: str,
               realized_pnl: float, pnl_pct: float) -> Optional[CompletedTrade]:
    """거래 종료 기록 (전역 함수)"""

    return get_integration_manager().record_trade_exit(
        symbol=symbol,
        exit_price=exit_price,
        exit_type=exit_type,
        realized_pnl=realized_pnl,
        pnl_pct=pnl_pct
    )


def get_signal_confidence(reasons: List[str], base_confidence: float = 0.5) -> tuple:
    """신호 Confidence 계산 (전역 함수)"""

    return get_integration_manager().get_signal_confidence(
        reasons=reasons,
        base_confidence=base_confidence
    )


def learn_from_all_trades():
    """모든 거래로부터 학습 (전역 함수)"""

    return get_integration_manager().learn_from_trades()
