"""
바이낸스 선물 실전 자동매매 봇

[수정 이력]
- V7.3 BUG FIX 1: _calculate_kelly_size — balance_info 미정의 변수 참조 오류 수정
  (기존: _execute_trade의 지역 변수를 참조 → NameError 발생)
  (수정: 함수 내부에서 직접 잔고 조회)
- V7.3 BUG FIX 2: _sync_with_exchange — 들여쓰기 오류 + if 조건 누락 수정
  (기존: qty > 0 이면 무조건 덮어쓰기, 신규 포지션 판단 누락)
  (수정: symbol not in self.open_positions 조건 추가)
- V7.3 BUG FIX 3: _update_positions — last_exit_times 이중 할당 제거
  (기존: 루프 상단과 하단에서 2회 할당)
  (수정: 상단 1회만 유지)
"""

import sys
# ★ V6.1: Windows cp949 인코딩 오류 방지 - stdout/stderr UTF-8 강제
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import time
import logging
import threading
from datetime import datetime, timezone
from typing import Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import requests
import importlib
import config.config as config
from config.config import *

from src.data_fetcher import BinanceFetcher
from src.strategy import ChoiGPTStrategy, AnalysisResult
from src.indicators import TradeSignal
from src.trade_logger import TradeLogger
from src.trade_integration import get_integration_manager
from src.logger_utils import setup_rotating_logger


logger = setup_rotating_logger(__name__, 'logs/live_trader.log')


class LiveTrader:
    """실전 자동매매 봇"""

    def __init__(self, api_key: str = API_KEY, api_secret: str = API_SECRET,
                 use_testnet: bool = USE_TESTNET):
        self.fetcher = BinanceFetcher(api_key, api_secret, use_testnet)
        self.strategy = ChoiGPTStrategy(min_confidence=AUTO_TRADE_MIN_CONFIDENCE)
        self.trade_logger = TradeLogger()
        self.trade_manager = get_integration_manager()
        self.is_running = False
        self.open_positions: Dict[str, dict] = {}
        self.trade_log: list = []
        self.check_interval = 60
        self.cycle_count = 0
        self.start_time = datetime.now()
        self.total_scans = 0
        self._lock = threading.Lock()
        self.last_analysis: Dict[str, AnalysisResult] = {}
        self.last_exit_times: Dict[str, datetime] = {}
        self.channel_monitor = None

    def start(self, symbols: list = None):
        """봇 시작"""
        if symbols is None:
            symbols = SYMBOLS

        logger.info("="*50)
        logger.info("🚀 ChoiGPT 방법론 자동매매 봇 시작!")
        logger.info(f"📊 심볼: {symbols}")
        logger.info(f"⚙️  전략 신뢰도 임계값: {self.strategy.min_confidence:.0%}")
        logger.info("="*50)

        self.is_running = True

        # ★ V6.2: 텔레그램 채널 모니터 시작
        if ENABLE_CHANNEL_MONITOR:
            try:
                from scripts.channel_monitor import get_channel_monitor
                self.channel_monitor = get_channel_monitor()
                self.channel_monitor.start()
                logger.info("📡 텔레그램 채널 모니터링 활성화")
            except Exception as e:
                logger.warning(f"📡 채널 모니터 시작 실패 (무시): {e}")

        # 스캘핑 스레드 시작
        if SCALP_SYMBOLS:
            scalp_thread = threading.Thread(target=self._scalp_loop, daemon=True)
            scalp_thread.start()

        # 초기 설정
        for symbol in symbols:
            try:
                self.fetcher.set_margin_type(symbol, 'ISOLATED')
                logger.debug(f"✅ {symbol}: 격리 마진 설정 확인")
            except Exception:
                pass

        # ★ V5.2.1: 거래소와 포지션 상태 동기화
        self._sync_with_exchange()

        # 텔레그램 시작 알림
        symbol_info = f"시총/거래량 상위 {DYNAMIC_SYMBOL_COUNT}개 종목" if USE_DYNAMIC_SYMBOLS else f"{len(symbols)}개 종목"
        self._send_telegram(
            f"⚙️ <b>ChoiGPT V7.3 트레이딩 엔진 가동</b>\n"
            f"대상: {symbol_info}\n"
            f"레버리지: x{DEFAULT_LEVERAGE} | Kelly: {KELLY_FRACTION*100:.0f}% | 최대 {MAX_KELLY_SIZE_PCT:.0f}%\n"
            f"방침: 한 번에 ${MIN_POSITION_USDT} 기준 진입\n"
            f"현재 시장 스캔 중입니다..."
        )

        # ★ V6.4 BUG FIX: 메인 루프를 _reload_config에서 분리
        while self.is_running:
            try:
                # 1. 동적 심볼 업데이트
                current_symbols = symbols
                if USE_DYNAMIC_SYMBOLS:
                    try:
                        dynamic_list = self.fetcher.get_top_symbols(DYNAMIC_SYMBOL_COUNT)
                        if dynamic_list:
                            current_symbols = dynamic_list
                            logger.info(f"🔄 동적 심볼 업데이트 완료 ({len(current_symbols)}개)")
                            # ★ 동적으로 추가된 심볼들도 무조건 격리(ISOLATED) 마진 적용
                            for s in current_symbols:
                                try:
                                    self.fetcher.set_margin_type(s, 'ISOLATED')
                                except Exception:
                                    pass
                    except Exception as e:
                        logger.warning(f"⚠️ 동적 심볼 업데이트 실패: {e}")

                # 2. 실시간 설정 재로드
                self._reload_config()

                # 3. 일반 분석 사이클
                self._run_cycle(current_symbols)

            except KeyboardInterrupt:
                logger.info("⏹️  봇 정지 요청됨")
                self.stop()
                break
            except Exception as e:
                logger.error(f"❌ 메인 사이클 오류: {e}")
                time.sleep(10)

            time.sleep(self.check_interval)

    def _reload_config(self):
        """★ V6.4: 설정 파일 실시간 재로드"""
        try:
            importlib.reload(config)
            global AUTO_TRADE_ENABLED
            AUTO_TRADE_ENABLED = getattr(config, 'AUTO_TRADE_ENABLED', AUTO_TRADE_ENABLED)
            
            # ★ V3.1: 타점 문턱값 실시간 동기화
            new_conf = getattr(config, 'AUTO_TRADE_MIN_CONFIDENCE', 0.75)
            if self.strategy.min_confidence != new_conf:
                self.strategy.min_confidence = new_conf
                logger.info(f"⚙️ 타점 문턱값 업데이트: {new_conf:.0%}")

            if not AUTO_TRADE_ENABLED:
                logger.debug("⏸️ 자동매매 OFF 상태 (실시간 감지)")
        except Exception as e:
            logger.error(f"⚠️ 설정 재로드 실패: {e}")

    def _scalp_loop(self):
        """스캘핑 전용 루프 (별도 스레드)"""
        if not SCALP_SYMBOLS:
            return

        logger.info(f"⚡ 스캘핑 스레드 시작 (대상: {SCALP_SYMBOLS})")
        while self.is_running:
            try:
                self._reload_config()
                self._run_scalp_cycle(SCALP_SYMBOLS)
            except Exception as e:
                logger.error(f"❌ 스캘핑 루프 오류: {e}")

            time.sleep(min(60, self.check_interval))

    def _run_scalp_cycle(self, symbols: list):
        """
        ★ V5.8: ICT Sniper 스캘핑 사이클
        1m(진입) + 5m(MSS 확인) + 15m(스윕 탐지) + SMT 다이버전스
        """
        from src.indicators import get_current_session
        session = get_current_session(datetime.utcnow())

        is_killzone = session.get('is_killzone', False)
        is_allowed_session = session.get('is_allowed', False)

        if not (is_killzone or is_allowed_session):
            kst_hour = (datetime.utcnow().hour + 9) % 24
            logger.info(f"⏰ [SCALP] 비활성 시간대 → 스캔 스킵 (UTC {datetime.utcnow().hour}시 / KST {kst_hour}시)")
            return

        logger.info(f"\n{'⚡'*20}")
        logger.info(f"⏰ 스캘핑 사이클: {datetime.utcnow().strftime('%H:%M:%S UTC')}")

        # ★ V5.8: SMT 상관 자산 데이터 미리 수집
        smt_cache = {}
        for sym in ['BTCUSDT', 'ETHUSDT']:
            try:
                smt_cache[sym] = self.fetcher.get_klines(sym, SCALP_HIGHER_TF, limit=30)
            except Exception:
                pass

        for symbol in symbols:
            try:
                df_daily = self.fetcher.get_klines(symbol, "1d", limit=20)
                df_1m  = self.fetcher.get_klines(symbol, SCALP_ENTRY_TF, limit=100)
                df_5m  = self.fetcher.get_klines(symbol, '5m', limit=60)
                df_15m = self.fetcher.get_klines(symbol, SCALP_HIGHER_TF, limit=60)

                daily_bias = "NEUTRAL"
                if len(df_daily) >= 2:
                    prev_day = df_daily.iloc[-2]
                    curr_price = df_1m['close'].iloc[-1]
                    if curr_price > prev_day['high']:
                        daily_bias = "BULLISH"
                    elif curr_price < prev_day['low']:
                        daily_bias = "BEARISH"

                    last_day = df_daily.iloc[-1]
                    if daily_bias == "BULLISH" and last_day['close'] < last_day['open']:
                        daily_bias = "NEUTRAL"
                    elif daily_bias == "BEARISH" and last_day['close'] > last_day['open']:
                        daily_bias = "NEUTRAL"

                if len(df_1m) < 50:
                    continue

                correlated_sym = 'ETHUSDT' if symbol == 'BTCUSDT' else 'BTCUSDT'
                correlated_df  = smt_cache.get(correlated_sym)

                analysis = self.strategy.analyze_scalp(
                    df_1m, symbol, df_15m,
                    df_5m=df_5m,
                    correlated_df=correlated_df,
                    daily_bias=daily_bias
                )

                if analysis.signal and AUTO_TRADE_ENABLED:
                    sig = analysis.signal
                    logger.info(f"🚀 [SCALP] {symbol} 신호! {sig.direction} 확신도:{sig.confidence:.0%}")
                    logger.info(f"   이유: {' | '.join(sig.reasons[:3])}")
                    self._execute_trade(symbol, analysis)

                time.sleep(0.1)
            except Exception as e:
                logger.error(f"❌ {symbol} 스캘핑 분석 실패: {e}")

    def stop(self):
        """봇 중지"""
        self.is_running = False
        logger.info("🛑 봇이 중지되었습니다.")
        self._send_telegram("🛑 <b>ChoiGPT Bot 중지됨</b>")

    def _run_cycle(self, symbols: list):
        """단일 분석 사이클 실행"""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        logger.info(f"\n{'─'*40}")
        logger.info(f"⏰ 분석 사이클: {timestamp}")

        self._update_positions()

        with self._lock:
            current_open = len(self.open_positions)

        if current_open >= MAX_OPEN_POSITIONS:
            logger.info(f"⚠️  최대 포지션 수 도달: {current_open}/{MAX_OPEN_POSITIONS}")
            return

        for i, symbol in enumerate(symbols):
            try:
                self.total_scans += 1
                progress = f"[{i+1:02d}/{len(symbols):02d}]"
                uptime = str(datetime.now() - self.start_time).split('.')[0]

                print(f"\r🚀 {uptime} | {progress} 🔍 분석 중: {symbol:<10}", end="", flush=True)
                logger.info(f"🔍 {progress} {symbol} 분석 중... (Total Scans: {self.total_scans})")

                self._analyze_and_trade(symbol)
                time.sleep(0.3)
            except Exception as e:
                print(f"\n❌ {symbol} 처리 실패: {e}")
                logger.error(f"❌ {symbol} 처리 실패: {e}")

        print(f"\n✅ 사이클 #{self.cycle_count+1} 완료 | 대기 중...")

        self.cycle_count += 1
        if self.cycle_count % 10 == 0:
            self._send_heartbeat()

    def _analyze_and_trade(self, symbol: str):
        """심볼 분석 및 매매 실행"""
        try:
            if symbol in EXCLUDED_SYMBOLS:
                logger.debug(f"⏭️  {symbol}: 제외 목록에 있음 - 스킵")
                return

            with self._lock:
                if symbol in self.open_positions:
                    pos = self.open_positions[symbol].copy()
                    has_position = True
                else:
                    has_position = False

            if has_position:
                self._monitor_position(symbol, pos)
                return

            # ★ V5.9.3: 킬존 외 시간에는 신규 진입 차단 (Ross Only 모드 시 우회)
            ross_only = getattr(config, 'ROSS_ONLY_MODE', False)
            from src.indicators import get_current_session
            session = get_current_session(datetime.utcnow())
            if not ross_only and not session.get('is_killzone', False):
                kst_hour = (datetime.utcnow().hour + 9) % 24
                logger.info(
                    f"⏰ {symbol}: 킬존 외 시간 → 신규 진입 스킵 "
                    f"(UTC {datetime.utcnow().hour}시 / KST {kst_hour}시)"
                )
                return

            # 데이터 수집 (병렬화) - ★ V7.3: 1D(400개), 1W(100개) 추가
            try:
                with ThreadPoolExecutor(max_workers=5) as executor:
                    f_entry  = executor.submit(self.fetcher.get_klines, symbol, ENTRY_TF, limit=200)
                    f_higher = executor.submit(self.fetcher.get_klines, symbol, HIGHER_TF, limit=1000)
                    f_1h     = executor.submit(self.fetcher.get_klines, symbol, "1h", limit=400)
                    f_daily  = executor.submit(self.fetcher.get_klines, symbol, "1d", limit=400)
                    f_weekly = executor.submit(self.fetcher.get_klines, symbol, "1w", limit=100)

                    corr_sym = "ETHUSDT" if symbol == "BTCUSDT" else "BTCUSDT"
                    f_corr = executor.submit(self.fetcher.get_klines, corr_sym, ENTRY_TF, limit=100)

                df_entry  = f_entry.result()
                df_higher = f_higher.result()
                df_1h     = f_1h.result()
                df_daily  = f_daily.result()
                df_weekly = f_weekly.result()
                df_corr   = f_corr.result()

                # Daily Bias 판단
                daily_bias = "NEUTRAL"
                if len(df_daily) >= 2:
                    prev_day = df_daily.iloc[-2]
                    curr_price = df_entry['close'].iloc[-1]
                    if curr_price > prev_day['high']:
                        daily_bias = "BULLISH"
                    elif curr_price < prev_day['low']:
                        daily_bias = "BEARISH"

                    last_day = df_daily.iloc[-1]
                    if daily_bias == "BULLISH" and last_day['close'] < last_day['open']:
                        daily_bias = "NEUTRAL"
                    elif daily_bias == "BEARISH" and last_day['close'] > last_day['open']:
                        daily_bias = "NEUTRAL"

            except Exception as fe:
                logger.error(f"📡 {symbol} 데이터 수집 실패: {fe}")
                return

            if len(df_entry) < 50:
                logger.warning(f"⚠️ {symbol}: 데이터 부족")
                return

            # ★ V6.2: 유동성 필터 (24h Volume 체크)
            try:
                from config.config import MIN_24H_VOLUME_USDT
                ticker_24h = self.fetcher._get('/fapi/v1/ticker/24hr', {'symbol': symbol})
                volume_24h = float(ticker_24h.get('quoteVolume', 0))
                if volume_24h < MIN_24H_VOLUME_USDT:
                    logger.warning(f"🚫 {symbol}: 유동성 부족 (${volume_24h:,.0f} < ${MIN_24H_VOLUME_USDT:,.0f}) - 진입 거부")
                    return
            except Exception as ve:
                logger.debug(f"유동성 체크 실패 (무시): {ve}")

            # 전략 분석 (★ V7.3: df_1d, df_1w 추가 전달)
            analysis = self.strategy.analyze(
                df_entry, symbol, df_higher, df_1h,
                df_1d=df_daily, df_1w=df_weekly,
                correlated_df=df_corr, daily_bias=daily_bias
            )

            self.last_analysis[symbol] = analysis

            if analysis.signal:
                logger.info(f"✅ {symbol}: 신호 발생! ({analysis.signal.direction}, {analysis.signal.confidence:.1%})")
            else:
                reasons = getattr(analysis, 'no_signal_reasons', ["조건 미달"])
                logger.info(f"⏸️  {symbol}: 거래 보류 - {', '.join(reasons)}")

            if analysis.signal and AUTO_TRADE_ENABLED:
                self._execute_trade(symbol, analysis)

        except Exception as e:
            logger.error(f"❌ {symbol} 분석 중 중대한 오류 발생: {e}")

    def _execute_trade(self, symbol: str, analysis: AnalysisResult):
        """거래 실행"""
        sig = analysis.signal

        # ★ V6.2.1 FIX: SL=0.0 버그 방지
        from scripts.sl_validator import validate_signal_before_entry
        if sig and not validate_signal_before_entry(sig):
            logger.error(f"🚨 {symbol}: 신호 검증 실패 - 진입 거부")
            return

        with self._lock:
            try:


                # ★ V6.2: 쿨다운 체크
                from config.config import SYMBOL_COOLDOWN_MINUTES
                last_exit = self.last_exit_times.get(symbol)
                if last_exit:
                    elapsed = (datetime.utcnow() - last_exit).total_seconds() / 60
                    if elapsed < SYMBOL_COOLDOWN_MINUTES:
                        remaining = int(SYMBOL_COOLDOWN_MINUTES - elapsed)
                        logger.info(f"⏳ [{symbol}] 쿨다운 중 - {remaining}분 후 재진입 가능 (보복매매 방지)")
                        return

                # ★ V6.2: 채널 컨센서스 체크
                if self.channel_monitor:
                    try:
                        from config.config import CHANNEL_VETO_COUNT
                        cs = self.channel_monitor.get_consensus(symbol)
                        if cs['count'] > 0:
                            if cs['consensus'] != 'NEUTRAL' and cs['consensus'] != sig.direction:
                                logger.warning(
                                    f"⚠️ [채널] {symbol} 불일치: 봇={sig.direction} / 채널={cs['consensus']} "
                                    f"({cs['detail']})"
                                )
                                if cs['count'] >= CHANNEL_VETO_COUNT:
                                    logger.warning(f"🚫 [채널] {symbol} 채널 {cs['count']}개 반대 → 진입 보류")
                                    return
                            else:
                                if cs['consensus'] == sig.direction:
                                    logger.info(
                                        f"✅ [채널] {symbol} 컨센서스 일치: {sig.direction} "
                                        f"({cs['detail']})"
                                    )
                    except Exception as ce:
                        logger.debug(f"채널 컨센서스 조회 실패 (무시): {ce}")

                # ★ V5.4: 기존 포지션 여부 실시간 재확인
                try:
                    live_positions = self.fetcher.get_all_positions()
                    actual_pos = next((p for p in live_positions if p.get('symbol') == symbol), None)

                    if actual_pos:
                        # ★ BUG FIX: 봇이 관리하지 않는 수동 포지션이면 DCA(물타기) 전면 금지
                        if symbol not in self.open_positions:
                            logger.info(f"⏭️ {symbol}: 봇이 관리하지 않는 수동 포지션입니다. 추가 진입(DCA) 시그널을 무시합니다.")
                            return

                        pos_amt = float(actual_pos.get('size', 0))
                        pos_dir = actual_pos.get('side', 'LONG')
                        entry_price_avg = float(actual_pos.get('entry_price', actual_pos.get('entryPrice', 0)))
                        current_price = self.fetcher.get_price(symbol)

                        if pos_dir != sig.direction:
                            logger.info(f"⏭️  {symbol}: 반대 방향 포지션 보유 중. 신호 무시")
                            return

                        from config.config import DCA_DROP_PCT, MAX_POSITIONS_PER_SYMBOL, BASE_ENTRY_USDT
                        margin_used = (pos_amt * current_price) / sig.leverage
                        current_dca_count = max(1, round(margin_used / BASE_ENTRY_USDT))

                        if current_dca_count >= MAX_POSITIONS_PER_SYMBOL:
                            logger.info(f"⏭️  {symbol}: 최대 물타기 횟수 도달 ({current_dca_count}/{MAX_POSITIONS_PER_SYMBOL})")
                            return

                        if pos_dir == 'LONG':
                            loss_pct = (entry_price_avg - current_price) / entry_price_avg * 100
                        else:
                            loss_pct = (current_price - entry_price_avg) / entry_price_avg * 100

                        if loss_pct < DCA_DROP_PCT:
                            logger.info(f"⏭️  {symbol}: 물타기 조건 미달 (손실 {loss_pct:.2f}% < {DCA_DROP_PCT}%)")
                            return

                        logger.info(f"💧 {symbol}: 전략적 물타기(DCA) 진행! (현재 {current_dca_count}차, 손실 {loss_pct:.2f}%)")
                        sig.mode = f"DCA_{current_dca_count+1}"
                    else:
                        try:
                            self.fetcher.set_leverage(symbol, sig.leverage)
                            logger.info(f"⚙️  {symbol}: 레버리지 {sig.leverage}x 설정")
                        except Exception as le:
                            logger.warning(f"⚠️ {symbol}: 레버리지 설정 실패 (무시): {le}")
                except Exception as pe:
                    logger.warning(f"⚠️ {symbol}: 포지션 확인 실패: {pe} - 진행 계속")

                current_price = self.fetcher.get_price(symbol)

                # ★ V7.7: 호가창 불균형(Level 2 Imbalance) 필터 적용
                # 극심한 매도/매수벽 확인 시 가짜 돌파(Fakeout) 방지
                try:
                    ob_data = self.fetcher.get_order_book(symbol, limit=20)
                    imb_ratio = ob_data.get('imbalance_ratio', 1.0)
                    
                    if sig.direction == 'LONG' and imb_ratio < 0.5:
                        logger.warning(f"🚫 {symbol}: [Level 2] 매도 잔량 극우위 (Imbalance: {imb_ratio:.2f}) → LONG 진입 취소 (Fakeout 방지)")
                        return
                    elif sig.direction == 'SHORT' and imb_ratio > 2.0:
                        logger.warning(f"🚫 {symbol}: [Level 2] 매수 잔량 극우위 (Imbalance: {imb_ratio:.2f}) → SHORT 진입 취소 (Fakeout 방지)")
                        return
                except Exception as e:
                    logger.debug(f"{symbol} Level 2 체크 실패 (무시): {e}")

                is_limit_entry = getattr(sig, 'entry_type', 'MARKET') == 'LIMIT'
                limit_price = getattr(sig, 'limit_price', current_price)

                if is_limit_entry:
                    dist_pct = abs(current_price - limit_price) / current_price * 100
                    if dist_pct > 3.0:
                        logger.warning(f"⚠️ {symbol}: OB/FVG/Fib Sniper 거리 {dist_pct:.2f}% > 3% — 신호 유효성 소멸 스킵")
                        return

                    mode_text = "🎯 [SNIPER]" if getattr(sig, 'mode', '') == 'SNIPER' else "🎯 [LIMIT]"
                    logger.info(f"{mode_text} {symbol}: 진입 대기 @ {limit_price:,.4f} (현재가 {current_price:,.4f}, 거리 {dist_pct:.2f}%)")
                else:
                    price_diff_pct = abs(current_price - sig.entry_price) / sig.entry_price * 100
                    if price_diff_pct > 0.5:
                        logger.warning(f"⚠️ {symbol}: 가격 이격 {price_diff_pct:.2f}% — 진입 스킵")
                        return

                # 포지션 사이즈 계산
                if ENABLE_KELLY_SIZING:
                    risk_per_unit = abs(sig.entry_price - sig.stop_loss)
                    reward_per_unit = abs(sig.take_profit2 - sig.entry_price)
                    rr_ratio = reward_per_unit / risk_per_unit if risk_per_unit > 0 else 0

                    quantity = self._calculate_kelly_size(
                        symbol, current_price, sig.confidence, rr_ratio, sig.stop_loss)
                    logger.info(f"⚖️  Kelly Sizing 적용: {quantity} (Conf: {sig.confidence:.1%}, RR: {rr_ratio:.1f})")
                else:
                    quantity = self.fetcher.calculate_position_size(
                        symbol, current_price, sig.stop_loss, sig.leverage)

                quantity = self.fetcher._round_quantity(symbol, quantity)

                if quantity <= 0:
                    logger.warning(f"⚠️ {symbol}: 수량 계산 실패 (너무 작거나 정밀도 미달)")
                    return

                notional_value = quantity * current_price
                if notional_value < MIN_NOTIONAL_USDT:
                    logger.warning(f"⚠️ {symbol}: Notional ${notional_value:.2f} < ${MIN_NOTIONAL_USDT:.2f} - 고가자산으로 스킵")
                    return

                # ★ V7.1: 최종 증거금 체크
                balance_info = self.fetcher.get_account_balance()
                available = float(balance_info.get('USDT', {}).get('available', 0))
                margin_required = notional_value / sig.leverage

                if available < margin_required:
                    logger.warning(f"🚨 {symbol}: 증거금 부족 (필요: ${margin_required:.2f}, 가용: ${available:.2f}) - 진입 거부")
                    return

                # ★ V5.9.3: LIMIT vs MARKET 주문 실행
                side = 'BUY' if sig.direction == 'LONG' else 'SELL'
                if is_limit_entry:
                    order = self.fetcher.place_limit_order_with_fallback(
                        symbol, side, quantity, limit_price, timeout_sec=120)
                    logger.info(f"🎯 {symbol}: OB/FVG LIMIT 주문 등록 @ {limit_price:,.4f} (120초 대기)")
                else:
                    order = self.fetcher.place_limit_order_with_fallback(
                        symbol, side, quantity, current_price)

                # ★ V7.4: 시장가 폴백의 경우 'status'가 'NEW' 형태여도 실제로 포지션이 체결되었을 확률이 매우 높음
                if order and order.get('status') in ['FILLED', 'NEW']:
                    avg_price = float(order.get('avgPrice', 0) or 0)
                    # ★ V7.4 Fix: avg_price가 0인 경우(로깅 오류 등) 현재가로 대체하여 SL/TP 계산 보장
                    actual_entry = avg_price if avg_price > 0 else current_price
                    is_filled = True
                else:
                    status_str = order.get('status') if order else 'Failed/None'
                    logger.warning(f"⚠️ {symbol}: 주문 상태 미확인 ({status_str})")
                    return

                if is_filled:
                    executed_qty_raw = order.get('executedQty')
                    if executed_qty_raw and float(executed_qty_raw) > 0:
                        actual_qty = float(executed_qty_raw)
                    else:
                        actual_qty = quantity

                    # SL/TP 주문 (최대 3회 재시도)
                    success = False
                    sl_id = None
                    for attempt in range(3):
                        sl_order, tp_orders = self.fetcher.place_sl_tp_orders(
                            symbol, sig.direction, actual_qty, sig.stop_loss,
                            sig.take_profit, sig.take_profit2, sig.tp1_ratio)

                        sl_id = sl_order.get('algoId') if isinstance(sl_order, dict) else None

                        if sl_order:
                            success = True
                            break
                        else:
                            logger.warning(f"⚠️ {symbol} SL 주문 실패 (시도 {attempt+1}/3)... 2초 후 재시도")
                            time.sleep(2)

                    if not success:
                        logger.error(f"🚨 {symbol} SL 3회 실패 → 포지션 즉시 강제 청산!")
                        close_side = 'SELL' if sig.direction == 'LONG' else 'BUY'

                        try:
                            self.fetcher.cancel_all_orders(symbol)
                            self.fetcher.cancel_all_algo_orders(symbol)
                            logger.info(f"✅ {symbol} TP/SL 주문 사전 취소 완료")
                        except Exception as cancel_err:
                            logger.warning(f"⚠️ {symbol} TP/SL 취소 실패: {cancel_err}")

                        try:
                            self.fetcher.place_order(symbol, close_side, quantity,
                                                     order_type='MARKET', reduce_only=True)
                            logger.info(f"✅ {symbol} SL 실패에 따른 강제 청산 완료")
                        except Exception as ce:
                            logger.error(f"🚨 {symbol} 강제 청산마저 실패: {ce}")

                        self._send_telegram(
                            f"🚨 <b>[긴급] {symbol} SL 설정 불가 → 강제 청산</b>\n"
                            f"SL 주문 3회 연속 실패로 포지션을 즉시 청산했습니다.\n"
                            f"API 상태 또는 잔고를 확인하세요."
                        )
                        self.open_positions.pop(symbol, None)
                        return

                    # 포지션 기록
                    rr_ratio = abs(sig.take_profit2 - actual_entry) / abs(actual_entry - sig.stop_loss) if abs(actual_entry - sig.stop_loss) > 0 else 0
                    self.open_positions[symbol] = {
                        'symbol': symbol,
                        'direction': sig.direction,
                        'entry_price': actual_entry,
                        'stop_loss': sig.stop_loss,
                        'take_profit': sig.take_profit,
                        'take_profit2': sig.take_profit2,
                        'quantity': actual_qty,
                        'leverage': sig.leverage,
                        'confidence': sig.confidence,
                        'rr_ratio': rr_ratio,
                        'entry_time': datetime.utcnow().isoformat(),
                        'order_id': order.get('orderId'),
                        'sl_id': sl_id,
                        'reasons': sig.reasons,
                        'mode': sig.mode
                    }

                    self.trade_manager.record_trade_entry(
                        symbol=symbol,
                        direction=sig.direction,
                        entry_price=actual_entry,
                        quantity=actual_qty,
                        leverage=sig.leverage,
                        reasons=sig.reasons,
                        confidence_score=sig.confidence,
                        rr_ratio=rr_ratio,
                        stop_loss=sig.stop_loss,
                        take_profit=sig.take_profit,
                        take_profit2=sig.take_profit2,
                        sl_id=sl_id,
                        notify_telegram=False
                    )

                    rtp1 = abs(sig.take_profit - actual_entry) / abs(actual_entry - sig.stop_loss)
                    rtp2 = abs(sig.take_profit2 - actual_entry) / abs(actual_entry - sig.stop_loss)
                    logger.info(f"\n{'='*50}")
                    logger.info(f"✅ 거래 체결!")
                    logger.info(f"  심볼: {symbol}")
                    logger.info(f"  방향: {'📗 LONG' if sig.direction == 'LONG' else '📕 SHORT'}")
                    logger.info(f"  진입가: {actual_entry:.4f}")
                    logger.info(f"  SL: {sig.stop_loss:.4f}")
                    logger.info(f"  TP1 (50%): {sig.take_profit:.4f} (RR {rtp1:.1f})")
                    logger.info(f"  TP2 (50%): {sig.take_profit2:.4f} (RR {rtp2:.1f})")
                    logger.info(f"  레버리지: {sig.leverage}x")
                    logger.info(f"  수량(Actual): {actual_qty}")
                    logger.info(f"  신뢰도: {sig.confidence:.1%}")
                    logger.info(f"{'='*50}\n")

                    try:
                        balance_info = self.fetcher.get_account_balance()
                        wallet_bal = float(balance_info.get('USDT', {}).get('wallet', 0))
                    except Exception:
                        wallet_bal = 0

                    if sig.mode == "SNIPER":
                        mode_tag = "🚀 [SNIPER - x100]"
                    elif sig.mode == "SCALP":
                        mode_tag = "⚡ [SCALPING]"
                    else:
                        mode_tag = "📡 [NORMAL]"

                    direction_emoji = "📈 LONG" if sig.direction == 'LONG' else "📉 SHORT"

                    self._send_telegram(
                        f"🤖 <b>[AI 진입 성공 - {symbol}]</b>\n"
                        f"🧠 {mode_tag} (확신도 {sig.confidence:.0%})\n"
                        f"━━━━━━━━━━━━━━\n"
                        f"💰 <b>방향:</b> {direction_emoji}\n"
                        f"💵 <b>진입가:</b> {actual_entry:,.4f}\n"
                        f"⚖️  <b>레버리지:</b> {sig.leverage}x\n"
                        f"💳 <b>증거금(Margin):</b> {MIN_POSITION_USDT} USDT\n"
                        f"📊 <b>진입규모(Notional):</b> ${actual_qty * actual_entry:,.1f}\n"
                        f"🛑 <b>Stop Loss:</b> {sig.stop_loss:,.4f}\n"
                        f"🏁 <b>Take Profit:</b> {sig.take_profit:,.4f}\n"
                        f"📝 <b>근거:</b> {', '.join(sig.reasons[:2])}\n"
                        f"━━━━━━━━━━━━━━"
                    )

            except Exception as e:
                logger.error(f"❌ {symbol} 거래 실행 실패: {e}")

    def _calculate_kelly_size(self, symbol: str, current_price: float,
                              confidence: float, rr_ratio: float, 
                              sl_price: float = 0) -> float:
        """
        [V8.2] '복리의 마법' 엔진: Fixed Fractional Risk Sizing
        - 켈리 공식 비중(fractional_f)과 상시 리스크(RISK_PER_TRADE)를 결합하여 
          잔고 대비 정해진 리스크(예: 2%)만큼만 손실을 보도록 수량을 조절합니다.
        """
        try:
            # 1. 가용 잔고 조회
            balance_info = self.fetcher.get_account_balance()
            total_balance = float(balance_info.get('USDT', {}).get('total', 0))
            available_balance = float(balance_info.get('USDT', {}).get('available', 0))
            
            if total_balance <= 0:
                logger.warning(f"⚠️ {symbol}: 잔고 부족($0.0) - 진입 취소")
                return 0

            # 2. 거래당 리스크 금액 (복리 핵심)
            from config.config import RISK_PER_TRADE, KELLY_FRACTION
            risk_pct = RISK_PER_TRADE / 100.0
            risk_amount = total_balance * risk_pct
            
            # 3. 손절 거리 기반 수량 산출
            price_distance = abs(current_price - sl_price) if sl_price > 0 else (current_price * 0.02) # SL 없으면 2% 가정
            if price_distance <= 0:
                return 0
                
            # 기본 수량: 리스크 금액 / 손절 거리
            quantity = risk_amount / price_distance
            
            # 4. 켈리 가중치 적용 (신뢰도에 따른 비중 조절)
            p = confidence
            b = rr_ratio if rr_ratio > 0 else 2.0
            kelly_f = max(0, p - (1 - p) / b)
            
            # 켈리 분수(Fractional Kelly)를 통한 최종 수량 보정
            # 신뢰도가 낮으면 수량을 더 줄이고, 높으면 설정한 리스크 금액을 온전히 사용
            quantity *= (kelly_f / (1.0 - (1.0 - 0.5) / 2.0)) # 대략적 정규화 (Conf 0.5일 때 대비)
            # 안전을 위해 장부상 상한선 적용 (KELLY_FRACTION)
            quantity = min(quantity, (total_balance * 5.0) / current_price) # 최대 레버리지 5배 수준으로 명목가치 캡

            # 5. 가용 증거금 내 실행 가능 여부 체크
            notional_value = quantity * current_price
            if notional_value / 20 > available_balance: # 20배 레버리지 기준 증거금 부족 시
                quantity = (available_balance * 0.8 * 20) / current_price # 가용 증거금의 80%만 사용

            return quantity
            max_allowed = available_balance * (MAX_KELLY_SIZE_PCT / 100.0)
            notional_size = min(notional_size, max_allowed)

            # 동적 최소값
            dynamic_min = min(available_balance * 0.05, MIN_POSITION_USDT)
            if notional_size < dynamic_min:
                logger.debug(f"포지션 너무 작음: ${notional_size:.2f} < ${dynamic_min:.2f}")
                return 0

            if current_price <= 0:
                logger.error(f"❌ {symbol} 가격 오류: {current_price}")
                return 0

            return notional_size / current_price

        except Exception as e:
            logger.error(f"켈리 계산 오류: {e}")
            return 0

    def _update_positions(self):
        """포지션 상태 업데이트"""
        try:
            live_positions = self.fetcher.get_all_positions()
            live_symbols = {p['symbol'] for p in live_positions}

            # 청산된 포지션 처리
            closed_symbols = set(self.open_positions.keys()) - live_symbols
            for symbol in closed_symbols:
                # ★ FIX: last_exit_times는 루프 상단에서 1회만 설정 (기존: 하단에서 중복 설정)
                self.last_exit_times[symbol] = datetime.utcnow()

                # ★ V7.2: 포지션 종료 시 미체결 알고 주문 전체 취소
                try:
                    self.fetcher.cancel_all_algo_orders(symbol)
                    logger.info(f"🧹 {symbol}: 포지션 종료에 따른 TP/SL 알고 주문 정리 완료")
                except Exception as e:
                    logger.warning(f"⚠️ {symbol}: 알고 주문 정리 중 오류 (무시 가능): {e}")

                # ★ V7.4 FIX: 즉시 pop 하지 않고 참조만 유지. 도중에 예외 발생 시 메모리 증발 방지.
                pos = self.open_positions.get(symbol)
                if not pos:
                    continue
                    
                current_price = self.fetcher.get_price(symbol)

                entry_price = pos.get('entry_price', 0)
                if entry_price <= 0:
                    logger.error(f"❌ {symbol} 진입가 오류 (0 또는 None)")
                    pnl_pct = 0.0
                elif pos['direction'] == 'LONG':
                    pnl_pct = (current_price - entry_price) / entry_price * 100
                else:
                    pnl_pct = (entry_price - current_price) / entry_price * 100

                leverage = pos.get('leverage', DEFAULT_LEVERAGE)
                roe_pct = pnl_pct * leverage

                pnl_usdt = (pos['quantity'] * current_price - pos['quantity'] * pos['entry_price']) * (1 if pos['direction'] == 'LONG' else -1)
                duration_minutes = int((datetime.now() - datetime.fromisoformat(pos.get('entry_time', datetime.now().isoformat()))).total_seconds() / 60)

                if pnl_pct > 2:
                    exit_reason = "TP"
                elif pnl_pct < -2:
                    exit_reason = "SL"
                else:
                    exit_reason = "CLOSED"

                trade_data = {
                    'symbol': symbol,
                    'direction': pos['direction'],
                    'entry_price': pos['entry_price'],
                    'entry_time': pos.get('entry_time', datetime.now().isoformat()),
                    'exit_price': current_price,
                    'exit_time': datetime.now().isoformat(),
                    'exit_reason': exit_reason,
                    'quantity': pos['quantity'],
                    'pnl': pnl_usdt,
                    'pnl_pct': pnl_pct,
                    'stop_loss': pos.get('stop_loss', 0),
                    'take_profit1': pos.get('take_profit', 0),
                    'take_profit2': pos.get('take_profit2', 0),
                    'duration_minutes': duration_minutes,
                    'confidence': pos.get('confidence', 0),
                    'rr_ratio': pos.get('rr_ratio', 0),
                    'leverage': pos.get('leverage', DEFAULT_LEVERAGE),
                }
                self.trade_logger.log_trade_closed(trade_data)

                self.trade_manager.record_trade_exit(
                    symbol=symbol,
                    exit_price=current_price,
                    exit_type=exit_reason,
                    realized_pnl=pnl_usdt,
                    pnl_pct=pnl_pct,
                    notify_telegram=False
                )

                result_emoji = "✅" if pnl_pct > 0 else "❌"
                logger.info(f"{result_emoji} {symbol} 포지션 청산 | PnL: {pnl_usdt:+.2f} USDT (ROE {roe_pct:+.2f}%) | 사유: {exit_reason}")

                self._send_telegram(
                    f"{result_emoji} {symbol} 포지션 청산\n"
                    f"💰 PnL: {pnl_usdt:+.2f} USDT (ROE {roe_pct:+.2f}%)\n"
                    f"사유: {exit_reason}"
                )
                
                # ★ V7.4 FIX: 모든 처리와 알림이 끝난 후 최종적으로 메모리에서 제거
                self.open_positions.pop(symbol, None)
                # ★ FIX: 이중 할당 제거 (루프 상단에서 이미 설정됨)
                # self.last_exit_times[symbol] = datetime.utcnow()  ← 삭제됨

            # 현재 포지션 정보 업데이트
            for pos_info in live_positions:
                symbol = pos_info['symbol']
                if symbol in self.open_positions:
                    self.open_positions[symbol].update({
                        'unrealized_pnl': pos_info['unrealized_pnl'],
                        'mark_price': pos_info['mark_price']
                    })

        except Exception as e:
            logger.error(f"포지션 업데이트 실패: {e}")

    def _sync_with_exchange(self):
        """
        거래소에서 현재 포지션 정보를 읽어와 로컬 상태와 동기화 (재시작 대응)

        [BUG FIX V7.3]: 기존 코드에서 들여쓰기 오류로 인해
        `if symbol not in self.open_positions:` 조건이 누락되어 있었음.
        → 포지션이 이미 존재하더라도 무조건 덮어씌우는 버그 수정.
        """
        try:
            live_positions = self.fetcher.get_all_positions()
            for p in live_positions:
                symbol = p['symbol']
                # ★ V5.7: get_all_positions()은 'size'(abs) + 'side' 키 반환
                qty = float(p.get('size', 0))
                if qty > 0:
                    # ★ FIX: 봇이 이미 알고 있는 포지션이 아닌 경우에만 추가
                    if symbol not in self.open_positions:
                        direction = p.get('side', 'LONG')
                        entry_price = float(p.get('entry_price', p.get('entryPrice', 0)))

                        # ★ V6.1 Fix: 상태 동기화 중 기존 Algo 주문(SL/TP) 상태 복구
                        sl_price, tp_price, tp_price2 = 0.0, 0.0, 0.0
                        try:
                            open_algo = self.fetcher.get_all_open_algo_orders()
                            algo_sym = [o for o in open_algo if o.get('symbol') == symbol]

                            for o in algo_sym:
                                o_type = str(o.get('type', '')).upper()
                                trig_price = float(o.get('stopPrice') or o.get('triggerPrice') or o.get('price') or 0.0)
                                if trig_price <= 0:
                                    continue

                                if 'STOP' in o_type or 'LOSS' in o_type:
                                    if (direction == 'LONG' and trig_price < entry_price) or \
                                       (direction == 'SHORT' and trig_price > entry_price):
                                        sl_price = trig_price
                                elif 'TAKE_PROFIT' in o_type or 'PROFIT' in o_type:
                                    if tp_price == 0.0:
                                        tp_price = trig_price
                                    else:
                                        if direction == 'LONG':
                                            if trig_price > tp_price:
                                                tp_price2 = trig_price
                                            else:
                                                tp_price2, tp_price = tp_price, trig_price
                                        else:
                                            if trig_price < tp_price:
                                                tp_price2 = trig_price
                                            else:
                                                tp_price2, tp_price = tp_price, trig_price
                        except Exception as e:
                            logger.warning(f"⚠️ {symbol} SL/TP 복원 실패: {e}")

                        # ★ BUG FIX: 수동 포지션(알고리즘 SL/TP 없음) 완전 무시 ("내가 진입한 포지션 건들지마" 정책)
                        if sl_price == 0.0 and tp_price == 0.0:
                            logger.info(f"⏭️ {symbol} 수동 포지션 감지(알고리즘 SL/TP 없음) → 봇의 관리대상에서 제외합니다.")
                            continue

                        self.open_positions[symbol] = {
                            'symbol': symbol,
                            'direction': direction,
                            'entry_price': entry_price,
                            'quantity': qty,
                            'leverage': int(p.get('leverage', 10)),
                            'stop_loss': sl_price,
                            'take_profit': tp_price,
                            'take_profit2': tp_price2,
                            'entry_time': datetime.utcnow().isoformat(),
                            'reasons': ["상태 동기화 (재시작)"]
                        }
                        logger.info(f"🔄 {symbol} 기존 포지션 병합 복구: SL({sl_price}), TP({tp_price})")
        except Exception as e:
            logger.error(f"⚠️ 거래소 동기화 중 오류: {e}")

    def _monitor_position(self, symbol: str, pos: dict):
        """포지션 모니터링 + 동적 트레일링 스탑 (V5.5)"""
        try:
            current_price = self.fetcher.get_price(symbol)
            entry = pos['entry_price']
            sl = pos.get('stop_loss', 0)
            tp = pos.get('take_profit', 0)
            leverage = pos.get('leverage', DEFAULT_LEVERAGE)

            # ★ [Safety Shield V7.4]: SL/TP 누락 방지 및 자동 복구
            if sl == 0 or tp == 0:
                logger.warning(f"🛡️ {symbol}: SL/TP 누락 감지! 거래소 실제 주문 확인 중...")
                has_sl, has_tp = False, False
                try:
                    open_algos = self.fetcher.get_all_open_algo_orders()
                    algo_sym = [o for o in open_algos if o.get('symbol') == symbol]
                    for o in algo_sym:
                        o_type = str(o.get('type', '')).upper()
                        if 'STOP' in o_type: has_sl = True
                        if 'PROFIT' in o_type: has_tp = True
                    
                    if not has_sl or not has_tp:
                        logger.info(f"🔧 {symbol}: 누락된 주문 재설정 시도 (SL={has_sl}, TP={has_tp})")
                        self.fetcher.place_sl_tp_orders(
                            symbol, pos['direction'], pos['quantity'],
                            pos.get('stop_loss') or (entry * 0.98 if pos['direction'] == 'LONG' else entry * 1.02), # 비상용 2%
                            pos.get('take_profit') or (entry * 1.05 if pos['direction'] == 'LONG' else entry * 0.95),
                            pos.get('take_profit2'), 0.5
                        )
                        # 로컬 상태 업데이트
                        if not sl:
                            new_sl_val = entry * 0.98 if pos['direction'] == 'LONG' else entry * 1.02
                            pos['stop_loss'] = new_sl_val
                            self.open_positions[symbol]['stop_loss'] = new_sl_val  # ★ 원본 업데이트 (무한루프 방지)
                        if not tp:
                            new_tp_val = entry * 1.05 if pos['direction'] == 'LONG' else entry * 0.95
                            pos['take_profit'] = new_tp_val
                            self.open_positions[symbol]['take_profit'] = new_tp_val  # ★ 원본 업데이트 (무한루프 방지)
                except Exception as se:
                    logger.error(f"🛡️ {symbol}: Safety Shield 복구 실패: {se}")

            df_m = self.fetcher.get_klines(symbol, "15m", limit=50)
            from src.indicators import detect_market_structure
            ms = detect_market_structure(df_m)

            if pos['direction'] == 'LONG':
                current_pnl = (current_price - entry) / entry * 100 * leverage

                # [V8.0: Zero-Risk Transition]
                # TP1 도달(또는 80% 근접) 시 본절로 SL 이동하여 무위험 상태 확보 (Runner 전략)
                tp_dist = tp - entry
                curr_dist = current_price - entry
                if tp_dist > 0 and curr_dist >= tp_dist * 0.8 and not pos.get('trailing_active', False):
                    new_sl = entry * 1.0005  # 수수료 포함 본절가
                    self._move_sl_to_breakeven(symbol, pos, new_sl, tp)
                    # 별도 트레일링 스레드 불필요, 상태만 업데이트
                    self.open_positions[symbol]['trailing_active'] = True
                    self.open_positions[symbol]['stop_loss'] = new_sl
                    return
                    # 본절 약간 위에서 방어 (수수료 커버)
                    breakeven_sl = entry * 1.002
                    self._move_sl_to_breakeven(symbol, pos, breakeven_sl, tp)

                if current_pnl >= 15.0: # 수익 극대화를 위해 구조 기반 트레일링은 좀 더 늦게 시작
                    new_sl = ms.last_low * 0.999 if ms.last_low > entry else sl
                    if new_sl > sl * 1.001:
                        self._update_sl_tp(symbol, pos, new_sl, tp)
                        logger.info(f"🚀 {symbol} 구조 기반 SL 상승 이동 (HL 추격): {new_sl:,.4f}")

            else:  # SHORT
                current_pnl = (entry - current_price) / entry * 100 * leverage

                # [V8.0: Zero-Risk Transition for SHORT]
                tp_dist = entry - tp
                curr_dist = entry - current_price
                if tp_dist > 0 and curr_dist >= tp_dist * 0.8 and not pos.get('trailing_active', False):
                    new_sl = entry * 0.9995  # 수수료 포함 본절가
                    self._move_sl_to_breakeven(symbol, pos, new_sl, tp)
                    self.open_positions[symbol]['trailing_active'] = True
                    self.open_positions[symbol]['stop_loss'] = new_sl
                    return

                if current_pnl >= 15.0:
                    new_sl = ms.last_high * 1.001 if (ms.last_high < entry and ms.last_high > 0) else sl
                    if new_sl < sl * 0.999:
                        self._update_sl_tp(symbol, pos, new_sl, tp)
                        logger.info(f"🚀 {symbol} 구조 기반 SL 하강 이동 (LH 추격): {new_sl:,.4f}")

            progress = 0
            if pos['direction'] == 'LONG':
                progress = (current_price - entry) / (tp - entry) * 100 if tp > entry else 0
            else:
                progress = (entry - current_price) / (entry - tp) * 100 if entry > tp else 0

            logger.info(f"  📊 {symbol} 포지션: {pos['direction']} | "
                       f"현재가: {current_price:.4f} | "
                       f"PnL: {current_pnl:+.2f}% | "
                       f"TP 진행: {progress:.0f}%")

        except Exception as e:
            logger.debug(f"포지션 모니터링 실패 {symbol}: {e}")

    def _move_sl_to_breakeven(self, symbol: str, pos: dict, new_sl: float, tp: float):
        """본절가로 SL 이동 + 알림"""
        try:
            self.fetcher.cancel_all_orders(symbol)
            self.fetcher.cancel_all_algo_orders(symbol)
            self.fetcher.place_sl_tp_orders(
                symbol, pos['direction'], pos['quantity'],
                new_sl, tp, pos.get('take_profit2'), 0.5
            )
            with self._lock:
                self.open_positions[symbol]['stop_loss'] = new_sl
                self.open_positions[symbol]['trailing_active'] = True

            self._send_telegram(
                f"🛡️ <b>{symbol} 본절가 이동</b>\n"
                f"SL을 <b>{new_sl:,.4f}</b>로 이동하여 이제 무위험 포지션입니다."
            )
        except Exception as e:
            logger.warning(f"본절 이동 실패 {symbol}: {e}")

    def _update_sl_tp(self, symbol: str, pos: dict, new_sl: float, tp: float):
        """SL 또는 TP 값 거래소 업데이트"""
        try:
            self.fetcher.cancel_all_orders(symbol)
            self.fetcher.cancel_all_algo_orders(symbol)
            self.fetcher.place_sl_tp_orders(
                symbol, pos['direction'], pos['quantity'],
                new_sl, tp, pos.get('take_profit2'), 0.5
            )
            with self._lock:
                self.open_positions[symbol]['stop_loss'] = new_sl
        except Exception as e:
            logger.warning(f"SL/TP 업데이트 실패 {symbol}: {e}")

    def get_status(self) -> dict:
        """봇 현재 상태 반환"""
        try:
            balance = self.fetcher.get_account_balance()
            usdt = balance.get('USDT', {})
        except Exception:
            usdt = {}

        return {
            'is_running': self.is_running,
            'open_positions': len(self.open_positions),
            'positions': list(self.open_positions.values()),
            'wallet_balance': usdt.get('wallet', 0),
            'unrealized_pnl': usdt.get('unrealized_pnl', 0),
            'available': usdt.get('available', 0),
        }

    def _send_heartbeat(self):
        """정기 보고 - Holding Report 포함"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

            try:
                balance_info = self.fetcher.get_account_balance()
                wallet = float(balance_info.get('USDT', {}).get('wallet', 0))
                available = float(balance_info.get('USDT', {}).get('available', 0))
            except Exception:
                wallet, available = 0, 0

            positions_count = len(self.open_positions)

            if positions_count == 0:
                analysis_blocks = []
                for sym, ar in list(self.last_analysis.items())[:3]:
                    txt = getattr(ar, 'analysis_text', None)
                    if txt:
                        analysis_blocks.append(f"─────────────────────\n{txt}")

                analysis_section = ("\n\n" + "\n".join(analysis_blocks)) if analysis_blocks else ""

                msg = (
                    f"💓 <b>ChoiGPT Pulse</b>\n"
                    f"⏰ {timestamp}\n"
                    f"⚙️ {self.cycle_count} 사이클 완료\n"
                    f"💰 잔고: ${wallet:,.2f} USDT (가용: ${available:,.2f})\n"
                    f"📊 포지션 없음 - 신호 대기 중\n"
                    f"📡 시스템 정상 작동 중"
                    f"{analysis_section}"
                )
            else:
                pos_lines = []
                for sym, pos in list(self.open_positions.items()):
                    try:
                        curr = self.fetcher.get_price(sym)
                        entry = pos['entry_price']
                        lev = pos.get('leverage', DEFAULT_LEVERAGE)
                        direction = pos['direction']
                        if direction == 'LONG':
                            pnl = (curr - entry) / entry * 100 * lev
                        else:
                            pnl = (entry - curr) / entry * 100 * lev
                        pnl_emoji = "🟢" if pnl >= 0 else "🔴"
                        trailing = "🛡️ 본절 이동됨" if pos.get('trailing_active') else "⏳ 모니터링 중"
                        pos_lines.append(
                            f"  • {sym} {direction} {lev}x | "
                            f"현재 {pnl_emoji} {pnl:+.1f}% | {trailing}"
                        )
                    except Exception:
                        pos_lines.append(f"  • {sym} 데이터 조회 중...")

                msg = (
                    f"🛡️ <b>Holding Report</b>\n"
                    f"⏰ {timestamp}\n"
                    f"💰 잔고: ${wallet:,.2f} USDT\n"
                    f"📊 보유 포지션 {positions_count}개:\n"
                    + "\n".join(pos_lines) +
                    f"\n⚙️ {self.cycle_count} 사이클 완료 | 계속 모니터링 중..."
                )

            self._send_telegram(msg)
            logger.info("💓 Holding Report 전송 완료")
        except Exception as e:
            logger.error(f"하트비트 전송 실패: {e}")

    def _send_telegram(self, message: str):
        """텔레그램 알림 전송"""
        if not ENABLE_TELEGRAM or not TELEGRAM_BOT_TOKEN:
            return
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            resp = requests.post(url, json={
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'HTML'
            }, timeout=5)
            if resp.status_code != 200:
                logger.error(f"텔레그램 전송 실패: {resp.text}")
        except Exception as e:
            logger.error(f"텔레그램 통신 오류: {e}")


if __name__ == "__main__":
    trader = LiveTrader(
        api_key=API_KEY,
        api_secret=API_SECRET,
        use_testnet=USE_TESTNET
    )

    symbols = SYMBOLS if not USE_DYNAMIC_SYMBOLS else None
    trader.start(symbols=symbols)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("⛔ Live Trader 종료 중...")
        trader.stop()
        logger.info("Live Trader Stopped")