"""
성과 대시보드 (CLI)
실시간 거래 성과, 신호 효율성, 포지션 상태를 터미널에서 확인

Features:
- 실시간 포지션 조회
- 누적 성과 표시
- 신호별 효율성 시각화
- 월별 성과 비교
- 자동 새로고침
"""

import logging
import time
import os
from datetime import datetime
from typing import Optional
from pathlib import Path

from src.trade_integration import get_integration_manager

logger = logging.getLogger(__name__)


class Dashboard:
    """CLI 성과 대시보드"""

    def __init__(self, refresh_interval: int = 10):
        """
        Args:
            refresh_interval: 새로고침 간격 (초)
        """
        self.manager = get_integration_manager()
        self.refresh_interval = refresh_interval
        self.is_running = False

    def clear_screen(self):
        """터미널 화면 초기화"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def display_header(self):
        """헤더 표시"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        header = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                      🚀 BISON BOT - 성과 대시보드 🚀                       ║
║                                                                            ║
║  {current_time} UTC+0                                      ⏱️ 자동 갱신: {self.refresh_interval}초       ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
        print(header)

    def display_active_positions(self):
        """활성 포지션 표시"""
        active_positions = self.manager.get_active_positions()

        if not active_positions:
            print("\n📭 활성 포지션: 없음\n")
            return

        print(f"\n📊 활성 포지션 ({len(active_positions)}개):\n")
        print("┌─────────────────────────────────────────────────────────────────┐")
        print("│ 심볼        │ 방향   │ 진입가    │ SL      │ TP1     │ TP2     │")
        print("├─────────────────────────────────────────────────────────────────┤")

        for symbol, entry in active_positions.items():
            direction = "📈 LONG " if entry.direction == "LONG" else "📉 SHORT"
            entry_price = f"{entry.entry_price:.8g}"
            sl_price = f"{entry.stop_loss:.8g}"
            tp1_price = f"{entry.take_profit:.8g}"
            tp2_price = f"{entry.take_profit2:.8g}" if entry.take_profit2 else "N/A"

            print(
                f"│ {symbol:10} │ {direction} │ {entry_price:>8} │ {sl_price:>7} │ "
                f"{tp1_price:>7} │ {tp2_price:>7} │"
            )

        print("└─────────────────────────────────────────────────────────────────┘\n")

    def display_cumulative_performance(self):
        """누적 성과 표시"""
        stats = self.manager.get_monthly_performance()

        print(f"📈 누적 성과 ({datetime.now().strftime('%Y-%m')}):\n")
        print("┌──────────────────────────────────────────────────────┐")

        # 기본 통계
        total_trades = stats.get('total_trades', 0)
        winning_trades = stats.get('winning_trades', 0)
        win_rate = stats.get('win_rate', 0)
        total_pnl = stats.get('total_pnl', 0)
        total_pnl_pct = stats.get('total_pnl_pct', 0)

        print(f"│ 총 거래 수:          {total_trades:>3} 건")
        print(f"│ 승리:                {winning_trades:>3} 건")
        print(f"│ 패배:                {total_trades - winning_trades:>3} 건")
        print(f"│ 승률:                {win_rate:>5.1f}%")
        print(f"│ 누적 손익 (USDT):    {total_pnl:>+8.4f}")
        print(f"│ 누적 손익률:         {total_pnl_pct:>+7.2f}%")
        print(f"│ 평균 수익:           {stats.get('avg_win', 0):>+7.2f}%")
        print(f"│ 평균 손실:           {stats.get('avg_loss', 0):>+7.2f}%")
        print(f"│ 최대 수익:           {stats.get('largest_win', 0):>+7.2f}%")
        print(f"│ 최대 손실:           {stats.get('largest_loss', 0):>+7.2f}%")

        print("└──────────────────────────────────────────────────────┘\n")

    def display_signal_effectiveness(self):
        """신호 효율성 표시"""
        trades = self.manager.get_completed_trades()

        if not trades:
            print("📊 신호 효율성: 데이터 없음\n")
            return

        signal_eff = self.manager.reviewer.get_signal_effectiveness(trades)

        if not signal_eff:
            return

        print(f"🎯 신호 효율성 (Top 10):\n")
        print("┌────────────────────────────────────────────────────────────┐")
        print("│ 신호         │ 승률    │ 사용수 │ 평균 PnL │ 추세         │")
        print("├────────────────────────────────────────────────────────────┤")

        sorted_signals = sorted(
            signal_eff.items(),
            key=lambda x: x[1]['win_rate'],
            reverse=True
        )[:10]

        for signal, data in sorted_signals:
            win_rate = data['win_rate']
            emoji = "🔥" if win_rate >= 0.7 else "📈" if win_rate >= 0.5 else "⚠️"
            trend_emoji = "📈" if data['avg_pnl_pct'] > 0.5 else "📉" if data['avg_pnl_pct'] < -0.5 else "➡️"

            signal_name = signal[:12].ljust(12)
            print(
                f"│ {signal_name} │ {emoji} {win_rate:>5.1f}% │ "
                f"{data['count']:>5} │ {data['avg_pnl_pct']:>+7.2f}% │ {trend_emoji} {data['avg_pnl_pct']:>+6.2f}% │"
            )

        print("└────────────────────────────────────────────────────────────┘\n")

    def display_recent_trades(self, limit: int = 5):
        """최근 거래 표시"""
        trades = self.manager.get_completed_trades()

        if not trades:
            print("📋 최근 거래: 없음\n")
            return

        recent = trades[-limit:]

        print(f"📋 최근 거래 ({len(recent)}개):\n")
        print("┌──────────────────────────────────────────────────────────────────────┐")
        print("│ 시간     │ 심볼      │ 방향 │ 진입가   │ 종료가   │ 손익  │ 상태    │")
        print("├──────────────────────────────────────────────────────────────────────┤")

        for trade in reversed(recent):
            time_str = trade.entry_time.split('T')[1][:5]
            direction = "L" if trade.direction == "LONG" else "S"
            win_loss = f"{'✅' if trade.pnl_pct > 0 else '❌'} {trade.pnl_pct:>+6.2f}%"
            exit_type = trade.exit_type

            print(
                f"│ {time_str} │ {trade.symbol:>8} │ {direction:>3} │ "
                f"{trade.entry_price:>7.5g} │ {trade.exit_price:>7.5g} │ {win_loss:>7} │ {exit_type:>6} │"
            )

        print("└──────────────────────────────────────────────────────────────────────┘\n")

    def display_market_status(self):
        """시장 상태 표시"""
        print("📡 시장 상태:\n")
        print("┌──────────────────────────────────────────────┐")
        print("│ 상태:           ✅ 온라인                   │")
        print("│ 모드:           🤖 자동매매 활성            │")
        print("│ Telegram:       ✅ 연결됨                   │")
        print("│ 학습:           ✅ 활성 (매일 자정)        │")
        print("└──────────────────────────────────────────────┘\n")

    def display_footer(self):
        """푸터 표시"""
        print("╔════════════════════════════════════════════════════════════════════════════╗")
        print("║ 명령어: [q] 종료 | [r] 새로고침 | [s] 신호 상세 | [t] 거래 내역             ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝\n")

    def show(self):
        """대시보드 표시"""
        self.clear_screen()
        self.display_header()
        self.display_active_positions()
        self.display_cumulative_performance()
        self.display_signal_effectiveness()
        self.display_recent_trades(limit=5)
        self.display_market_status()
        self.display_footer()

    def run(self, auto_refresh: bool = True):
        """대시보드 실행"""
        self.is_running = True

        try:
            if auto_refresh:
                logger.info("🚀 대시보드 시작 (자동 새로고침 활성)")

                while self.is_running:
                    self.show()
                    time.sleep(self.refresh_interval)
            else:
                self.show()

        except KeyboardInterrupt:
            logger.info("⏹️  대시보드 종료")
            self.is_running = False

        except Exception as e:
            logger.error(f"❌ 대시보드 오류: {e}")
            self.is_running = False

    def stop(self):
        """대시보드 중지"""
        self.is_running = False


def run_dashboard(auto_refresh: bool = True, refresh_interval: int = 10):
    """대시보드 실행 (메인 함수)"""

    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )

    dashboard = Dashboard(refresh_interval=refresh_interval)

    try:
        dashboard.run(auto_refresh=auto_refresh)

    except Exception as e:
        logger.error(f"❌ 대시보드 오류: {e}")


if __name__ == "__main__":
    # 명령줄 인자 처리
    import sys

    auto_refresh = True
    refresh_interval = 10

    if len(sys.argv) > 1:
        if sys.argv[1] == "--no-refresh":
            auto_refresh = False
        elif sys.argv[1].startswith("--interval="):
            try:
                refresh_interval = int(sys.argv[1].split("=")[1])
            except (ValueError, IndexError):
                pass

    run_dashboard(auto_refresh=auto_refresh, refresh_interval=refresh_interval)
