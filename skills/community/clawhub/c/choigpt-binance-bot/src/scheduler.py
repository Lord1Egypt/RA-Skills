"""
자동 학습 스케줄러
4시간 주기 자동 학습, 보고서 생성, Telegram 알림 자동화

Features:
- ⚡ 4시간마다 신호 학습 실행 (빠른 승률 개선)
- 매일 오전 7시에 일일 보고서 생성
- 매주 월요일 오전 8시에 주간 보고서 생성
- 실시간 모니터링 및 로깅
"""

import logging
import schedule
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.trade_integration import get_integration_manager
from scripts.report_manager import ReportManager
from scripts.learning_engine import LearningEngine
from scripts.telegram_trader_notifier import notify_daily_summary, notify_error

logger = logging.getLogger(__name__)


class TradeScheduler:
    """거래 자동 스케줄 관리자"""

    def __init__(self):
        self.manager = get_integration_manager()
        self.report_manager = ReportManager()
        self.learning_engine = LearningEngine()  # ★ 자동 학습 엔진
        self.is_running = False

        logger.info("🧠 Trade Scheduler 초기화 완료")

    def schedule_daily_learning(self):
        """4시간마다 자동 학습 실행 (신호 가중치 동적 조정) - 빠른 고도화를 위해 24시간 → 4시간 주기로 변경"""

        def job():
            try:
                logger.info("=" * 80)
                logger.info("🧠 자동 학습 시작 (4시간 주기) - 신호 가중치 동적 조정")
                logger.info("=" * 80)

                # 1. ★ 자동 학습 엔진: 거래 결과 기반 파라미터 최적화
                learning_report = self.learning_engine.daily_learning()

                logger.info(f"\n📊 학습 결과 요약:")
                logger.info(f"   ✅ 우수 신호: {learning_report.get('high_efficiency_count', 0)}개")
                logger.info(f"   ⚠️ 저수익 신호: {learning_report.get('low_efficiency_count', 0)}개")

                # 2. 우수 신호 출력
                if learning_report.get('high_performers'):
                    logger.info(f"\n🔥 우수 신호 (승률 75% 이상):")
                    for sig in learning_report['high_performers']:
                        logger.info(f"   • {sig['signal']}: {sig['win_rate']} ({sig['avg_pnl']})")

                # 3. 저수익 신호 출력
                if learning_report.get('low_performers'):
                    logger.info(f"\n⛔ 저수익 신호 (승률 40% 미만) - 배제 또는 강화 권장:")
                    for sig in learning_report['low_performers']:
                        logger.info(f"   • {sig['signal']}: {sig['win_rate']} ({sig['avg_pnl']})")

                logger.info(f"\n✅ 자동 학습 완료")
                logger.info(f"📝 상세 리포트: logs/learning_report_*.json")

            except Exception as e:
                logger.error(f"❌ 자동 학습 실패: {e}")
                notify_error(f"자동 학습 실패: {e}", severity="❌")

        # 4시간마다 실행 (빠른 승률 개선을 위해 일일 주기 → 4시간 주기로 변경)
        schedule.every(4).hours.do(job)

        logger.info("✅ 4시간마다 자동 학습 스케줄 등록 (신호 가중치 동적 조정 - 빠른 고도화)")

    def schedule_daily_report(self):
        """매일 오전 7시에 일일 보고서 생성"""

        def job():
            try:
                logger.info("=" * 80)
                logger.info("📊 일일 보고서 생성 시작")
                logger.info("=" * 80)

                # 1. 일일 통계 계산
                stats = self.manager.get_monthly_performance()

                logger.info(f"📊 일일 통계:")
                logger.info(f"   - 총 거래: {stats.get('total_trades', 0)}건")
                logger.info(f"   - 승률: {stats.get('win_rate', 0):.1f}%")
                logger.info(f"   - 누적 손익: {stats.get('total_pnl', 0):+.4f} USDT")

                # 2. 일일 보고서 생성
                report = self.manager.generate_daily_report()

                if report:
                    logger.info(f"✅ 일일 보고서 생성 완료")
                else:
                    logger.info("ℹ️  오늘 거래가 없습니다")

            except Exception as e:
                logger.error(f"❌ 일일 보고서 생성 실패: {e}")
                notify_error(f"일일 보고서 생성 실패: {e}", severity="⚠️")

        # 매일 오전 7시 (07:00) 실행
        schedule.every().day.at("07:00").do(job)

        logger.info("✅ 매일 오전 7시 보고서 스케줄 등록")

    def schedule_weekly_report(self):
        """매주 월요일 오전 8시에 주간 보고서 생성"""

        def job():
            try:
                logger.info("=" * 80)
                logger.info("📈 주간 보고서 생성 시작")
                logger.info("=" * 80)

                # 1. 거래 조회 (최근 7일)
                trades = self.manager.get_completed_trades()

                if not trades:
                    logger.info("ℹ️  이번 주 거래가 없습니다")
                    return

                # 2. 주간 통계 계산
                from datetime import timedelta
                one_week_ago = datetime.now() - timedelta(days=7)
                weekly_trades = [
                    t for t in trades
                    if datetime.fromisoformat(t.entry_time) > one_week_ago
                ]

                if weekly_trades:
                    wins = sum(1 for t in weekly_trades if t.pnl_pct > 0)
                    total_pnl = sum(t.realized_pnl for t in weekly_trades)

                    logger.info(f"📈 주간 통계:")
                    logger.info(f"   - 총 거래: {len(weekly_trades)}건")
                    logger.info(f"   - 승률: {(wins/len(weekly_trades)*100):.1f}%")
                    logger.info(f"   - 누적 손익: {total_pnl:+.4f} USDT")

            except Exception as e:
                logger.error(f"❌ 주간 보고서 생성 실패: {e}")

        # 매주 월요일 오전 8시 (08:00) 실행
        schedule.every().monday.at("08:00").do(job)

        logger.info("✅ 매주 월요일 오전 8시 보고서 스케줄 등록")

    def schedule_state_backup(self):
        """매 시간마다 상태 백업"""

        def job():
            try:
                self.manager.save_state()
                logger.debug("✅ 상태 백업 완료")

            except Exception as e:
                logger.warning(f"⚠️  상태 백업 실패: {e}")

        # 매 시간 정각마다 실행
        schedule.every().hour.do(job)

        logger.info("✅ 매 시간 상태 백업 스케줄 등록")

    def start(self):
        """스케줄러 시작"""

        logger.info("=" * 80)
        logger.info("🚀 Trade Scheduler 시작")
        logger.info("=" * 80)

        # 모든 스케줄 등록
        self.schedule_daily_learning()
        self.schedule_daily_report()
        self.schedule_weekly_report()
        self.schedule_state_backup()

        self.is_running = True

        # 스케줄 실행 루프
        logger.info("⏰ 스케줄 대기 중...")

        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # 1분마다 체크

            except KeyboardInterrupt:
                logger.info("⏹️  스케줄러 정지 요청됨")
                self.stop()
                break

            except Exception as e:
                logger.error(f"❌ 스케줄 실행 오류: {e}")
                time.sleep(60)

    def stop(self):
        """스케줄러 중지"""

        self.is_running = False
        schedule.clear()

        logger.info("🛑 스케줄러가 중지되었습니다")

    def show_schedule(self):
        """현재 스케줄 목록 표시"""

        logger.info("=" * 80)
        logger.info("📅 현재 등록된 스케줄")
        logger.info("=" * 80)

        jobs = schedule.get_jobs()

        if not jobs:
            logger.info("등록된 스케줄이 없습니다")
            return

        for i, job in enumerate(jobs, 1):
            logger.info(f"{i}. {job}")

        logger.info("=" * 80)


def run_scheduler():
    """스케줄러 실행 (메인 함수)"""

    # 로깅 설정
    from src.logger_utils import setup_rotating_logger
    logger = setup_rotating_logger(__name__, 'logs/scheduler.log')


    scheduler = TradeScheduler()

    try:
        scheduler.start()

    except KeyboardInterrupt:
        logger.info("⏹️  사용자 중지 요청")
        scheduler.stop()

    except Exception as e:
        logger.error(f"❌ 스케줄러 오류: {e}")
        scheduler.stop()


if __name__ == "__main__":
    run_scheduler()
