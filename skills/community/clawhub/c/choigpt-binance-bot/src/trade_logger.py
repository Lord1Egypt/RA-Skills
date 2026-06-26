"""
거래 복기 및 로깅 시스템 (V4.2)
종료된 거래의 상세 분석 기록
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class TradeLogger:
    """거래 기록 및 복기 관리"""

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # 거래 기록 파일
        self.trade_log_file = self.log_dir / f"trade_history_{datetime.now().strftime('%Y%m%d')}.json"
        self.stats_file = self.log_dir / "trade_stats.json"

        # 메모리 캐시
        self.closed_trades = []
        self._load_existing_trades()

    def _load_existing_trades(self):
        """기존 거래 기록 로드"""
        if self.trade_log_file.exists():
            try:
                with open(self.trade_log_file, 'r', encoding='utf-8') as f:
                    self.closed_trades = json.load(f)
                logger.info(f"기존 거래 {len(self.closed_trades)}개 로드")
            except Exception as e:
                logger.error(f"거래 기록 로드 실패: {e}")
                self.closed_trades = []

    def log_trade_closed(self, trade_data: Dict) -> None:
        """거래 종료 기록

        Args:
            trade_data: {
                'symbol': str,
                'direction': 'LONG'|'SHORT',
                'entry_price': float,
                'entry_time': str (ISO format),
                'exit_price': float,
                'exit_time': str (ISO format),
                'exit_reason': 'TP1'|'TP2'|'SL'|'MANUAL'|'ERROR',
                'quantity': float,
                'pnl': float (PnL in USDT),
                'pnl_pct': float (PnL %),
                'stop_loss': float,
                'take_profit1': float,
                'take_profit2': float,
                'duration_minutes': int,
                'confidence': float (신호 신뢰도),
                'rr_ratio': float (손익비),
                'leverage': int,
            }
        """
        try:
            # 타임스탐프 추가
            trade_data['closed_at'] = datetime.now().isoformat()

            # 메모리에 추가
            self.closed_trades.append(trade_data)

            # 파일에 저장
            with open(self.trade_log_file, 'w', encoding='utf-8') as f:
                json.dump(self.closed_trades, f, indent=2, ensure_ascii=False)

            # 통계 업데이트
            self._update_stats()

            logger.info(
                f"✅ 거래 기록: {trade_data['symbol']} {trade_data['direction']} "
                f"{trade_data['exit_reason']} | PnL: {trade_data['pnl_pct']:+.2f}%"
            )

        except Exception as e:
            logger.error(f"거래 기록 실패: {e}")

    def _update_stats(self) -> None:
        """통계 계산 및 저장"""
        if not self.closed_trades:
            return

        try:
            wins = [t for t in self.closed_trades if t.get('pnl', 0) > 0]
            losses = [t for t in self.closed_trades if t.get('pnl', 0) <= 0]

            win_count = len(wins)
            loss_count = len(losses)
            total_trades = win_count + loss_count

            win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0

            total_pnl = sum(t.get('pnl', 0) for t in self.closed_trades)
            avg_win = sum(t.get('pnl', 0) for t in wins) / len(wins) if wins else 0
            avg_loss = sum(t.get('pnl', 0) for t in losses) / len(losses) if losses else 0

            # 종료 이유별 통계
            exit_reasons = {}
            for trade in self.closed_trades:
                reason = trade.get('exit_reason', 'UNKNOWN')
                if reason not in exit_reasons:
                    exit_reasons[reason] = {'count': 0, 'pnl': 0, 'win_count': 0}
                exit_reasons[reason]['count'] += 1
                exit_reasons[reason]['pnl'] += trade.get('pnl', 0)
                if trade.get('pnl', 0) > 0:
                    exit_reasons[reason]['win_count'] += 1

            # 심볼별 통계
            symbol_stats = {}
            for trade in self.closed_trades:
                symbol = trade.get('symbol')
                if symbol not in symbol_stats:
                    symbol_stats[symbol] = {'count': 0, 'pnl': 0, 'win_count': 0}
                symbol_stats[symbol]['count'] += 1
                symbol_stats[symbol]['pnl'] += trade.get('pnl', 0)
                if trade.get('pnl', 0) > 0:
                    symbol_stats[symbol]['win_count'] += 1

            stats = {
                'updated_at': datetime.now().isoformat(),
                'total_trades': total_trades,
                'win_count': win_count,
                'loss_count': loss_count,
                'win_rate_pct': win_rate,
                'total_pnl': total_pnl,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'profit_factor': abs(sum(t.get('pnl', 0) for t in wins) / sum(t.get('pnl', 0) for t in losses)) if losses and sum(t.get('pnl', 0) for t in losses) != 0 else 0,
                'exit_reason_stats': exit_reasons,
                'symbol_stats': {
                    sym: {
                        'count': data['count'],
                        'pnl': data['pnl'],
                        'win_rate': (data['win_count'] / data['count'] * 100) if data['count'] > 0 else 0
                    }
                    for sym, data in symbol_stats.items()
                }
            }

            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)

            logger.debug(f"📊 통계 업데이트: WR={win_rate:.1f}%, PnL=${total_pnl:+.2f}")

        except Exception as e:
            logger.error(f"통계 계산 실패: {e}")

    def get_stats(self) -> Dict:
        """현재 통계 반환"""
        try:
            if self.stats_file.exists():
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"통계 로드 실패: {e}")

        return {}

    def get_closed_trades(self, symbol: Optional[str] = None, limit: int = None) -> list:
        """종료된 거래 목록 반환"""
        trades = self.closed_trades

        if symbol:
            trades = [t for t in trades if t.get('symbol') == symbol]

        if limit:
            trades = trades[-limit:]

        return trades

    def print_summary(self) -> None:
        """복기 요약 출력"""
        stats = self.get_stats()

        if not stats:
            print("아직 종료된 거래가 없습니다.")
            return

        print("\n" + "="*60)
        print("📊 거래 복기 요약")
        print("="*60)
        print(f"총 거래: {stats.get('total_trades', 0)}개")
        print(f"승리: {stats.get('win_count', 0)}개 | 패배: {stats.get('loss_count', 0)}개")
        print(f"승률: {stats.get('win_rate_pct', 0):.1f}%")
        print(f"총 PnL: ${stats.get('total_pnl', 0):+.2f}")
        print(f"평균 승리: ${stats.get('avg_win', 0):+.2f} | 평균 손실: ${stats.get('avg_loss', 0):+.2f}")
        print(f"Profit Factor: {stats.get('profit_factor', 0):.2f}")

        print("\n📌 종료 이유별 분석:")
        for reason, data in stats.get('exit_reason_stats', {}).items():
            wr = (data['win_count'] / data['count'] * 100) if data['count'] > 0 else 0
            print(f"  {reason}: {data['count']}건 (WR: {wr:.1f}%, PnL: ${data['pnl']:+.2f})")

        print("\n📌 종목별 분석:")
        for symbol, data in stats.get('symbol_stats', {}).items():
            print(f"  {symbol}: {data['count']}건 (WR: {data['win_rate']:.1f}%, PnL: ${data['pnl']:+.2f})")

        print("="*60 + "\n")
