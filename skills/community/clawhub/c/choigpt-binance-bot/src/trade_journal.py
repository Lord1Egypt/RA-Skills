"""
거래 일지 시스템 (Trade Journal)
모든 거래의 entry/exit 정보를 기록하고 복기 데이터 제공

Features:
- Entry: symbol, direction, price, quantity, reasons, entry_time
- Exit: exit_price, exit_time, exit_type (TP1/TP2/SL/Manual)
- PnL 계산: 실현 손익, 손익률
- CSV 저장: 월별 거래 기록
- 복기 데이터: 거래의 모든 정보를 구조화하여 제공
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class TradeEntry:
    """거래 진입 정보"""
    symbol: str
    direction: str  # 'LONG' or 'SHORT'
    entry_price: float
    quantity: float
    leverage: int
    entry_time: str
    reasons: List[str]  # 진입 근거 (예: ["MSS", "IFVG", "Discount 30%"])
    confidence_score: float = 0.0  # 0.0 ~ 1.0
    rr_ratio: float = 0.0  # Risk/Reward 비율
    stop_loss: float = 0.0  # ★ V5.0: Stop Loss 가격
    take_profit: float = 0.0  # ★ V5.0: Take Profit 1 가격
    take_profit2: float = 0.0  # ★ V5.0: Take Profit 2 가격
    sl_id: Optional[str] = None  # ★ V6.2: SL 알고 주문 ID 추적

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class TradeExit:
    """거래 종료 정보"""
    exit_price: float
    exit_time: str
    exit_type: str  # 'TP1', 'TP2', 'SL', 'MANUAL'
    realized_pnl: float  # 실현 손익 (USDT)
    pnl_pct: float  # 손익률 (%)

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CompletedTrade:
    """완료된 거래 (Entry + Exit)"""
    symbol: str
    direction: str
    entry_price: float
    exit_price: float
    quantity: float
    leverage: int
    entry_time: str
    exit_time: str
    exit_type: str  # 'TP1', 'TP2', 'SL', 'MANUAL'
    realized_pnl: float  # USDT
    pnl_pct: float  # %
    reasons: List[str]
    confidence_score: float = 0.0
    rr_ratio: float = 0.0
    duration_minutes: int = 0

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_csv_row(self) -> Dict:
        """CSV 저장용 단순화된 버전"""
        return {
            'Symbol': self.symbol,
            'Direction': self.direction,
            'Entry Price': f"{self.entry_price:.8g}",
            'Exit Price': f"{self.exit_price:.8g}",
            'Quantity': f"{self.quantity:.8g}",
            'Leverage': self.leverage,
            'Entry Time': self.entry_time,
            'Exit Time': self.exit_time,
            'Exit Type': self.exit_type,
            'Realized PnL (USDT)': f"{self.realized_pnl:.4f}",
            'PnL %': f"{self.pnl_pct:.4f}",
            'Duration (min)': self.duration_minutes,
            'Confidence': f"{self.confidence_score:.2f}",
            'RR Ratio': f"{self.rr_ratio:.2f}",
            'Reasons': ' | '.join(self.reasons)
        }


class TradeJournal:
    """거래 일지 관리"""

    def __init__(self, journal_dir: str = "data/journal"):
        self.journal_dir = Path(journal_dir)
        self.journal_dir.mkdir(parents=True, exist_ok=True)

        # 활성 거래 (Entry만 된 상태)
        self.active_trades: Dict[str, TradeEntry] = {}

        # 완료된 거래
        self.completed_trades: List[CompletedTrade] = []

        # 현재 월 추적
        self._current_month = datetime.now().strftime("%Y-%m")

        # 기존 데이터 로드
        self._load_active_trades()
        self._load_completed_trades()

        logger.info(f"📔 Trade Journal 초기화 완료 ({self.journal_dir})")

    def record_entry(self, symbol: str, direction: str, entry_price: float,
                    quantity: float, leverage: int, reasons: List[str],
                    confidence_score: float = 0.5, rr_ratio: float = 0.0,
                    stop_loss: float = 0.0, take_profit: float = 0.0,
                    take_profit2: float = 0.0, sl_id: Optional[str] = None) -> TradeEntry:
        """거래 진입 기록"""
        entry = TradeEntry(
            symbol=symbol,
            direction=direction,
            entry_price=entry_price,
            quantity=quantity,
            leverage=leverage,
            entry_time=datetime.now().isoformat(),
            reasons=reasons,
            confidence_score=confidence_score,
            rr_ratio=rr_ratio,
            stop_loss=stop_loss,
            take_profit=take_profit,
            take_profit2=take_profit2,
            sl_id=sl_id
        )

        self.active_trades[symbol] = entry
        self._save_active_trades()

        logger.info(f"✅ Entry 기록: {symbol} {direction} @ {entry_price} (conf: {confidence_score:.2f})")
        return entry

    def record_exit(self, symbol: str, exit_price: float, exit_type: str,
                   realized_pnl: float, pnl_pct: float) -> Optional[CompletedTrade]:
        """거래 종료 기록 및 완료된 거래 생성"""

        if symbol not in self.active_trades:
            logger.warning(f"⚠️ {symbol}에 대한 활성 Entry가 없습니다.")
            return None

        entry = self.active_trades[symbol]

        # Duration 계산
        entry_dt = datetime.fromisoformat(entry.entry_time)
        exit_dt = datetime.now()
        duration_minutes = int((exit_dt - entry_dt).total_seconds() / 60)

        completed = CompletedTrade(
            symbol=symbol,
            direction=entry.direction,
            entry_price=entry.entry_price,
            exit_price=exit_price,
            quantity=entry.quantity,
            leverage=entry.leverage,
            entry_time=entry.entry_time,
            exit_time=exit_dt.isoformat(),
            exit_type=exit_type,
            realized_pnl=realized_pnl,
            pnl_pct=pnl_pct,
            reasons=entry.reasons,
            confidence_score=entry.confidence_score,
            rr_ratio=entry.rr_ratio,
            duration_minutes=duration_minutes
        )

        self.completed_trades.append(completed)

        # 활성 거래에서 제거
        del self.active_trades[symbol]
        self._save_active_trades()

        # JSON & CSV에 저장
        self._save_completed_trades()
        self._save_to_csv(completed)

        win_loss = "✅ WIN" if pnl_pct > 0 else "❌ LOSS"
        logger.info(f"{win_loss}: {symbol} {exit_type} @ {exit_price} (PnL: {pnl_pct:+.2f}%)")

        return completed

    def get_active_trades(self) -> Dict[str, TradeEntry]:
        """활성 거래 조회"""
        return self.active_trades.copy()

    def get_completed_trades(self, symbol: Optional[str] = None) -> List[CompletedTrade]:
        """완료된 거래 조회"""
        if symbol is None:
            return self.completed_trades.copy()
        return [t for t in self.completed_trades if t.symbol == symbol]

    def get_monthly_trades(self, month: Optional[str] = None) -> List[CompletedTrade]:
        """월별 거래 조회 (format: YYYY-MM)"""
        if month is None:
            month = datetime.now().strftime("%Y-%m")

        return [t for t in self.completed_trades
                if t.entry_time.startswith(month)]

    def calculate_monthly_stats(self, month: Optional[str] = None) -> Dict:
        """월별 통계 계산"""
        trades = self.get_monthly_trades(month)

        if not trades:
            return {
                'month': month or datetime.now().strftime("%Y-%m"),
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'total_pnl': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'largest_win': 0.0,
                'largest_loss': 0.0
            }

        wins = [t for t in trades if t.pnl_pct > 0]
        losses = [t for t in trades if t.pnl_pct <= 0]

        return {
            'month': month or datetime.now().strftime("%Y-%m"),
            'total_trades': len(trades),
            'winning_trades': len(wins),
            'losing_trades': len(losses),
            'win_rate': (len(wins) / len(trades) * 100) if trades else 0.0,
            'total_pnl': sum(t.realized_pnl for t in trades),
            'total_pnl_pct': sum(t.pnl_pct for t in trades) / len(trades) if trades else 0.0,
            'avg_win': sum(t.pnl_pct for t in wins) / len(wins) if wins else 0.0,
            'avg_loss': sum(t.pnl_pct for t in losses) / len(losses) if losses else 0.0,
            'largest_win': max((t.pnl_pct for t in wins), default=0.0),
            'largest_loss': min((t.pnl_pct for t in losses), default=0.0)
        }

    def _save_active_trades(self):
        """활성 거래 상태 저장"""
        state_file = self.journal_dir / "active_trades.json"
        try:
            data = {symbol: asdict(entry) for symbol, entry in self.active_trades.items()}
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"❌ 활성 거래 저장 실패: {e}")

    def _load_active_trades(self):
        """활성 거래 상태 로드"""
        state_file = self.journal_dir / "active_trades.json"
        if not state_file.exists():
            return

        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for symbol, entry_dict in data.items():
                self.active_trades[symbol] = TradeEntry(**entry_dict)

            logger.info(f"📖 {len(self.active_trades)}개의 활성 거래 로드 완료")
        except Exception as e:
            logger.error(f"❌ 활성 거래 로드 실패: {e}")

    def _save_completed_trades(self):
        """완료된 거래 상태 저장 (JSON)"""
        state_file = self.journal_dir / "completed_trades.json"
        try:
            data = [asdict(trade) for trade in self.completed_trades]
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.debug(f"💾 완료된 거래 저장: {len(self.completed_trades)}개")
        except Exception as e:
            logger.error(f"❌ 완료된 거래 저장 실패: {e}")

    def _load_completed_trades(self):
        """완료된 거래 상태 로드 (JSON)"""
        state_file = self.journal_dir / "completed_trades.json"
        if not state_file.exists():
            return

        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for trade_dict in data:
                self.completed_trades.append(CompletedTrade(**trade_dict))

            logger.info(f"📖 {len(self.completed_trades)}개의 완료된 거래 로드 완료")
        except Exception as e:
            logger.error(f"❌ 완료된 거래 로드 실패: {e}")

    def _save_to_csv(self, trade: CompletedTrade):
        """완료된 거래를 CSV에 저장"""
        month = trade.entry_time[:7]  # YYYY-MM
        csv_file = self.journal_dir / f"trades_{month}.csv"

        try:
            row = trade.to_csv_row()
            file_exists = csv_file.exists()

            with open(csv_file, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=row.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row)

            logger.debug(f"💾 거래 CSV 저장: {csv_file.name}")
        except Exception as e:
            logger.error(f"❌ CSV 저장 실패: {e}")

    def export_all_trades(self, output_file: Optional[str] = None) -> str:
        """모든 거래를 JSON으로 내보내기"""
        if output_file is None:
            output_file = self.journal_dir / f"all_trades_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        else:
            output_file = Path(output_file)

        try:
            data = {
                'export_date': datetime.now().isoformat(),
                'total_trades': len(self.completed_trades),
                'trades': [t.to_dict() for t in self.completed_trades]
            }

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"📤 거래 내보내기 완료: {output_file}")
            return str(output_file)
        except Exception as e:
            logger.error(f"❌ 내보내기 실패: {e}")
            return ""
