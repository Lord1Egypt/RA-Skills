"""
텔레그램 봇 메인 핸들러
종목 질문 → 분석 차트 + 텍스트 → 자동매매 실행
python-telegram-bot 없이 raw requests로 구현
"""

import os
import sys
import time
import json
import logging
import threading
import traceback
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
import asyncio

# 현재 디렉토리를 패스에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config import *
from src.data_fetcher import BinanceFetcher
from src.strategy import ChoiGPTStrategy
from src.chart_generator import generate_analysis_chart, format_price, generate_analysis_explanation
from src.ai_analyzer import (format_telegram_message, classify_intent,
                         generate_chat_response, generate_contextual_chat_response,
                         clear_history, get_symbol_from_text,
                         generate_exit_strategy_analysis,
                         generate_trade_strategy_analysis)
from src.trade_logger import TradeLogger
from scripts.report_manager import ReportManager
import src.exchange_utils as exchange_utils

# 전문가 학습용 모듈 (D드라이브 전용)
from scripts.telegram_scraper import TelegramScraper
from src.ai_signal_parser import AISignalParser
from scripts.expert_comparator import ExpertComparator

from src.logger_utils import setup_rotating_logger
logger = setup_rotating_logger(__name__, 'logs/telegram_bot.log')

from scripts.market_scanner_service import MarketScannerService


# HTML 태그 제거용 정규식 (로그용)
def strip_html(text: str) -> str:
    if not text: return ""
    return re.sub(r'<[^>]*>', '', text)

# ============================================================
# 텔레그램 API 래퍼 (raw requests)
# ============================================================

class TelegramAPI:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"

    def _post(self, method: str, data: dict = None, files: dict = None,
              timeout: int = 30) -> dict:
        url = f"{self.base_url}/{method}"
        try:
            if files:
                response = requests.post(url, data=data, files=files, timeout=timeout)
            else:
                response = requests.post(url, json=data, timeout=timeout)
            
            res_json = response.json()
            if not res_json.get('ok'):
                logger.error(f"텔레그램 API 응답 오류 ({method}): {res_json}")
            return res_json
        except Exception as e:
            logger.error(f"텔레그램 API 오류 ({method}): {e}")
            return {}

    def get_updates(self, offset: int = 0, timeout: int = 30) -> list:
        result = self._post('getUpdates', {'offset': offset, 'timeout': timeout}, timeout=timeout+5)
        return result.get('result', [])

    def get_keyboard(self):
        """메인 메뉴 키보드"""
        return {
            "keyboard": [
                [{"text": "📊 현재 봇 상태"}, {"text": "💰 계좌 잔고"}],
                [{"text": "💼 보유 포지션"}, {"text": "📈 수익 통계"}],
                [{"text": "🚀 폭등 및 폭락 종목 선정"}],
                [{"text": "🤖 자동매매 ON/OFF"}, {"text": "❓ 도움말"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False
        }

    def send_message(self, chat_id: int, text: str,
                     parse_mode: str = 'HTML', # ★ Markdown -> HTML
                     reply_markup: dict = None) -> dict:
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
        }
        if reply_markup:
            data['reply_markup'] = json.dumps(reply_markup)
        
        # 로그에는 태그 없이 기록
        logger.info(f"📤 [TG] 메시지 전송 ({chat_id}):\n{strip_html(text)}")
        return self._post('sendMessage', data)

    def send_photo(self, chat_id: int, photo: bytes, caption: str = "",
                   parse_mode: str = 'HTML') -> dict: # ★ Markdown -> HTML
        data = {
            'chat_id': str(chat_id),
            'caption': caption,
            'parse_mode': parse_mode,
        }
        files = {'photo': ('chart.png', photo, 'image/png')}
        
        # 로그에는 태그 없이 기록
        if caption:
            logger.info(f"📤 [TG] 사진 전송 ({chat_id}) - 캡션:\n{strip_html(caption)}")
        
        return self._post('sendPhoto', data=data, files=files, timeout=60)

    def send_typing(self, chat_id: int):
        self._post('sendChatAction', {'chat_id': chat_id, 'action': 'typing'})

    def send_upload_photo(self, chat_id: int):
        self._post('sendChatAction', {'chat_id': chat_id, 'action': 'upload_photo'})

    def set_commands(self, commands: list) -> dict:
        return self._post('setMyCommands', {'commands': json.dumps(commands)})

class TelegramManager(TelegramAPI):
    """ExpertComparator 등에서 인자 없이 호출하기 위한 래퍼 클래스"""
    def __init__(self, token: str = None):
        from config.config import TELEGRAM_BOT_TOKEN
        super().__init__(token or TELEGRAM_BOT_TOKEN)


# ============================================================
# 봇 상태 관리
# ============================================================

class BotState:
    def __init__(self, state_file: str = "data/bot_state.json"):
        self.state_file = Path(state_file).absolute()
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        self.auto_trade = True
        self.monitoring = False
        self.active_positions = {}
        self.analysis_cache = {}  # 심볼: (결과, 타임스탬프)
        self.lock = threading.Lock()

        # ★ 누적 수익률 추적
        self.cumulative_returns = []  # [{symbol, pnl_pct, ...}, ...]
        self.cumulative_pnl = 0.0  # 누적 P&L (%)
        self.total_trades = 0  # 총 거래 수
        self.winning_trades = 0  # 수익 거래

        self.load_state()
        self.save_state()  # ★ V5.0: 초기 파일/디렉토리 생성 강제

    def save_state(self):
        """상태 저장 (V5.0)"""
        try:
            with self.lock:
                data = {
                    'auto_trade': self.auto_trade,
                    'active_positions': self.active_positions,
                    'cumulative_returns': self.cumulative_returns,
                    'cumulative_pnl': self.cumulative_pnl,
                    'total_trades': self.total_trades,
                    'winning_trades': self.winning_trades
                }
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("💾 봇 상태 저장 완료")
        except Exception as e:
            logger.error(f"봇 상태 저장 실패: {e}")

    def load_state(self):
        """상태 로드 (V5.0)"""
        if not self.state_file.exists():
            return
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.auto_trade = data.get('auto_trade', True)
                self.active_positions = data.get('active_positions', {})
                self.cumulative_returns = data.get('cumulative_returns', [])
                self.cumulative_pnl = data.get('cumulative_pnl', 0.0)
                self.total_trades = data.get('total_trades', 0)
                self.winning_trades = data.get('winning_trades', 0)
            logger.info(f"💾 봇 상태 로드 완료 (총 거래: {self.total_trades}개)")
        except Exception as e:
            logger.error(f"봇 상태 로드 실패: {e}")


# ============================================================
# 메인 봇 클래스
# ============================================================

class ChoiGPTBot:
    OFFSET_FILE  = "logs/telegram_offset.txt"
    LEADER_FILE  = "logs/bot_leader.json"   # ★ 다중 인스턴스 중복 방지 (NAS + PC)
    LEADER_TTL   = 45                       # 45초 이내 갱신 없으면 리더 교체

    def __init__(self):
        self.tg = TelegramAPI(TELEGRAM_BOT_TOKEN)
        self.fetcher = BinanceFetcher(API_KEY, API_SECRET, USE_TESTNET)
        # ★ config.py의 AUTO_TRADE_MIN_CONFIDENCE 값 사용
        self.strategy = ChoiGPTStrategy(min_confidence=AUTO_TRADE_MIN_CONFIDENCE)
        self.state = BotState()
        self.offset = self._load_offset()  # ★ 재시작 시 이전 offset 이어받기

        # 전문가 학습 엔진 초기화
        if ENABLE_EXPERT_LEARNING:
            self.scraper = TelegramScraper()
            self.parser = AISignalParser()
            self.comparator = ExpertComparator(bot=self)
        else:
            self.scraper = None
            self.parser = None
            self.comparator = None

        # 심볼 별명 매핑
        self.symbol_aliases = {
            'btc': 'BTCUSDT', 'bitcoin': 'BTCUSDT', '비트': 'BTCUSDT', '비트코인': 'BTCUSDT',
            'eth': 'ETHUSDT', 'ethereum': 'ETHUSDT', '이더': 'ETHUSDT', '이더리움': 'ETHUSDT',
            'sol': 'SOLUSDT', 'solana': 'SOLUSDT', '솔라나': 'SOLUSDT', '솔': 'SOLUSDT',
            'bnb': 'BNBUSDT', '비앤비': 'BNBUSDT',
            'xrp': 'XRPUSDT', '리플': 'XRPUSDT',
            'doge': 'DOGEUSDT', '도지': 'DOGEUSDT',
            'ada': 'ADAUSDT', '에이다': 'ADAUSDT',
            'avax': 'AVAXUSDT', '아발란체': 'AVAXUSDT',
            'link': 'LINKUSDT', '링크': 'LINKUSDT',
            'dot': 'DOTUSDT', '폴카닷': 'DOTUSDT',
            'ltc': 'LTCUSDT', '라이트코인': 'LTCUSDT',
            'matic': 'MATICUSDT', '폴리곤': 'MATICUSDT',
            'atom': 'ATOMUSDT', '코스모스': 'ATOMUSDT',
            'trx': 'TRXUSDT', '트론': 'TRXUSDT',
        }
        
        # ★ V5.0: 로거 및 레포트 매니저 초기화
        self.trade_logger = TradeLogger(log_dir="logs")
        self.report_manager = ReportManager(reports_dir="reports", logs_dir="logs")
        
        # 복기용 스케줄러 상태
        self.last_report_date = datetime.now().strftime('%Y%m%d')

        # ★ V5.2.2: 강력한 주문 잠금 (Race Condition 방지)
        self.trade_lock = threading.Lock()

        # ★ V5.2.2: 거래소와 포지션 상태 동기화 (재시작 대응 + 클리닝)
        self._sync_with_exchange()

    def _load_offset(self) -> int:
        """저장된 offset 파일에서 읽기 (재시작 시 중복 메시지 방지)"""
        try:
            os.makedirs('logs', exist_ok=True)
            if os.path.exists(self.OFFSET_FILE):
                with open(self.OFFSET_FILE, 'r') as f:
                    val = int(f.read().strip())
                    logger.info(f"📌 Telegram offset 복원: {val}")
                    return val
        except Exception:
            pass
        return 0

    def _save_offset(self, offset: int):
        """처리한 마지막 offset 파일에 저장"""
        try:
            with open(self.OFFSET_FILE, 'w') as f:
                f.write(str(offset))
        except Exception:
            pass

    # ──────────────────────────────────────────────
    # ★ 다중 인스턴스 리더 선출 (NAS + PC 중복 실행 대응)
    # ──────────────────────────────────────────────

    def _check_and_claim_leader(self) -> bool:
        """True = 이 인스턴스가 Telegram 메시지 처리 담당 (리더)
        파일 기반 하트비트로 NAS/PC 두 인스턴스 중 하나만 응답하도록 조정.
        """
        import socket
        hostname = socket.gethostname()
        pid = os.getpid()
        now = time.time()
        try:
            if os.path.exists(self.LEADER_FILE):
                with open(self.LEADER_FILE, 'r') as f:
                    data = json.load(f)
                cur_host = data.get('hostname', '')
                cur_pid  = data.get('pid', 0)
                last_ts  = data.get('timestamp', 0)
                # 내가 이미 리더 → 하트비트 갱신 후 True
                if cur_host == hostname and cur_pid == pid:
                    self._write_leader_file(hostname, pid, now)
                    return True
                # 다른 인스턴스가 살아있음 → 대기
                if now - last_ts < self.LEADER_TTL:
                    return False
                # 리더가 죽음(TTL 초과) → 교체
                logger.info(f"🏆 리더 교체: {cur_host}(PID:{cur_pid}) → {hostname}(PID:{pid})")
        except Exception:
            pass  # 파일 읽기 실패 시 리더로 동작
        self._write_leader_file(hostname, pid, now)
        return True

    def _write_leader_file(self, hostname: str, pid: int, ts: float):
        """리더 하트비트 파일 갱신"""
        try:
            os.makedirs('logs', exist_ok=True)
            with open(self.LEADER_FILE, 'w') as f:
                json.dump({'hostname': hostname, 'pid': pid, 'timestamp': ts}, f)
        except Exception as e:
            logger.debug(f"리더 파일 갱신 실패: {e}")

    # ──────────────────────────────────────────────
    # 봇 시작
    # ──────────────────────────────────────────────

    def start(self):
        """봇 시작"""
        logger.info("🚀 ChoiGPT Binance Auto Bot 시작!")

        # 봇 명령어 등록
        self.tg.set_commands([
            {"command": "start",     "description": "봇 시작 및 도움말"},
            {"command": "status",    "description": "현재 봇 상태"},
            {"command": "positions", "description": "오픈 포지션 확인"},
            {"command": "balance",   "description": "계좌 잔고 확인"},
            {"command": "stats",     "description": "누적 승률/수익률 통계"},
            {"command": "autotrade", "description": "자동매매 ON/OFF 토글"},
            {"command": "scan",      "description": "설정 종목 신호 스캔 (예: /scan 65)"},
            {"command": "fullscan",  "description": "바이낸스 전체 종목 스캔 (예: /fullscan 65)"},
            {"command": "report",    "description": "일일 전략 분석 리포트"},
            {"command": "ai",        "description": "AI 대화 모드 (예: /ai 솔라나 전망은?)"},
            {"command": "clear",     "description": "AI 대화 이력 초기화"},
            {"command": "help",      "description": "전체 명령어 도움말"},
        ])

        # 시작 알림 (★ 리더만 발송 - 팔로워는 Telegram 메시지 안 보냄)
        if self._check_and_claim_leader():
            self.send_startup_message()
        else:
            import socket
            logger.info(f"⏸️ [{socket.gethostname()}] 팔로워 모드 - 다른 인스턴스가 리더. 시작 알림 스킵.")

        # 메시지 폴링 루프
        self._polling_loop()

    def _polling_loop(self):
        """텔레그램 메시지 폴링 - 자동 재시작 포함"""
        logger.info("📡 폴링 시작...")
        consecutive_errors = 0
        _last_leader_log = 0  # 팔로워 로그 스팸 방지용
        import random
        while True:
            try:
                # ★ 리더 선출 체크 - NAS+PC 동시 실행 시 한 인스턴스만 응답
                is_leader = self._check_and_claim_leader()

                if not is_leader:
                    _now = time.time()
                    if _now - _last_leader_log > 300:
                        logger.info("⏸️ [팔로워] 다른 인스턴스가 리더 - 메시지 폴링 대기 중")
                        _last_leader_log = _now
                    time.sleep(15 + random.random() * 5)
                    continue

                time.sleep(1) 
                
                updates = self.tg.get_updates(offset=self.offset, timeout=30)
                consecutive_errors = 0
                for update in updates:
                    self.offset = update['update_id'] + 1
                    self._save_offset(self.offset)
                    self._handle_update(update)
            except KeyboardInterrupt:
                logger.info("⏹️ Ctrl+C 감지 - 종료합니다.")
                raise
            except requests.exceptions.ConnectionError as e:
                consecutive_errors += 1
                wait = min(30, 5 * consecutive_errors)
                logger.error(f"연결 오류 ({consecutive_errors}회): {e}")
                time.sleep(wait)
            except requests.exceptions.Timeout:
                continue
            except Exception as e:
                consecutive_errors += 1
                wait = min(30, 5 * consecutive_errors)
                if "409" in str(e) or "Conflict" in str(e):
                    import random
                    wait = 20 + random.random() * 10
                    logger.warning(f"⚠️ 텔레그램 중복 실행(409) 감지 - {wait:.1f}초 후 팔로워 모드 재시도")
                else:
                    logger.error(f"폴링 오류 ({consecutive_errors}회): {e}\n{traceback.format_exc()}")
                time.sleep(wait)

    def _handle_update(self, update: dict):
        """메시지 라우팅"""
        message = update.get('message', {})
        if not message:
            return

        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '').strip()

        if not chat_id or not text:
            return

        if ALLOWED_CHAT_IDS and chat_id not in ALLOWED_CHAT_IDS:
            self.tg.send_message(chat_id, "⛔ 접근 권한이 없습니다.")
            return

        username = message.get('from', {}).get('first_name', '사용자')
        logger.info(f"📩 메시지 수신 [{chat_id}] {username}: {text[:50]}")
        self.tg.send_typing(chat_id)

        thread = threading.Thread(
            target=self._process_message,
            args=(chat_id, text, username),
            daemon=True
        )
        thread.start()

    def _process_message(self, chat_id: int, text: str, username: str):
        """메시지 처리 (스레드에서 실행)"""
        try:
            text_lower = text.lower().strip()
            
            # 0. 텍스트 매칭 (버튼 메뉴 대응)
            if text == "🚀 폭등 및 폭락 종목 선정":
                threading.Thread(target=self._cmd_market_briefing_manual, args=(chat_id,), daemon=True).start()
                return
            elif text == "📊 현재 봇 상태":
                self._cmd_status(chat_id)
                return
            elif text == "💰 계좌 잔고":
                self._cmd_balance(chat_id)
                return
            elif text == "💼 보유 포지션":
                self._cmd_positions(chat_id)
                return
            elif text == "📈 수익 통계":
                self._cmd_stats(chat_id)
                return
            elif text == "🤖 자동매매 ON/OFF":
                self._cmd_toggle_autotrade(chat_id)
                return
            elif text == "❓ 도움말":
                self._cmd_help(chat_id)
                return
            
            # 1. 커맨드 처리 (시작이 / 로 시작하는 경우)
            if text.startswith('/'):
                cmd_parts = text.split()
                # @봇이름이 포함된 명령어도 처리 가능하도록 수정 (BOT_USERNAME 의존성 제거)
                full_cmd = cmd_parts[0].lower()
                cmd = full_cmd.split('@')[0] 
                args = cmd_parts[1:] if len(cmd_parts) > 1 else []

                if cmd == '/start':
                    self._cmd_start(chat_id, username)
                elif cmd == '/help':
                    self._cmd_help(chat_id)
                elif cmd == '/status':
                    self._cmd_status(chat_id)
                elif cmd == '/positions':
                    self._cmd_positions(chat_id)
                elif cmd == '/balance':
                    self._cmd_balance(chat_id)
                elif cmd == '/stats':
                    self._cmd_stats(chat_id)
                elif cmd == '/autotrade':
                    self._cmd_toggle_autotrade(chat_id)
                elif cmd == '/scan':
                    min_conf = float(args[0]) / 100 if args else 0.60
                    threading.Thread(target=self._cmd_scan_signals, args=(chat_id, min_conf), daemon=True).start()
                elif cmd == '/fullscan':
                    min_conf = float(args[0]) / 100 if args else 0.60
                    threading.Thread(target=self._cmd_fullscan_symbols, args=(chat_id, min_conf), daemon=True).start()
                elif cmd == '/report':
                    threading.Thread(target=self._cmd_report, args=(chat_id,), daemon=True).start()
                elif cmd == '/ai':
                    self._cmd_ai_chat(chat_id, " ".join(args))
                elif cmd == '/clear':
                    self._cmd_clear_chat(chat_id)
                elif cmd == '/clean':
                    self._cmd_clean(chat_id)
                elif cmd == '/reboot':
                    self._cmd_reboot(chat_id)
                elif cmd == '/learn':
                    self._cmd_manual_learn(chat_id)
                else:
                    self.tg.send_message(chat_id, f"❓ 알 수 없는 명령어입니다: {cmd}\n/help 를 입력해 명령어를 확인하세요.")
                return

            # 2. 일반 텍스트 분석 (NLP 인텐트 분류)
            intent_data = classify_intent(text)
            intent = intent_data.get('intent', 'CHAT')
            
            # ★ V6.8: 분석 키워드가 포함되어 있으면 ANALYSIS 인텐트가 아니더라도 강제로 분석 트리거
            # 사용자가 "포지션"이라는 단어를 섞더라도 "분석", "봐줘", "차트" 등이 있으면 기술 분석을 우선함
            analysis_keywords = ['분석', '봐줘', '차트', '어때', '전망', '해줘', '그려']
            is_analysis_requested = any(kw in text for kw in analysis_keywords)

            if intent == 'ANALYSIS' or is_analysis_requested:
                symbol = get_symbol_from_text(text)
                if symbol:
                    # 타임프레임 파싱 시도
                    _, tf = self._parse_symbol_and_timeframe(text)
                    logger.info(f"🎯 분석 요청 감지: {symbol} ({tf})")
                    self._analyze_and_respond(chat_id, symbol, tf)
                    return
                else:
                    # 심볼은 없는데 분석 요청인 경우 AI 챗으로 넘겨서 심볼을 묻도록 함
                    self._handle_normal_chat(chat_id, text)
                    return

            # 3. 기타 인텐트 처리
            if intent == 'EXIT_STRATEGY':
                self._handle_exit_strategy_request(chat_id, text)
                return
            elif intent == 'TRADE_STRATEGY':
                self._handle_trade_strategy_request(chat_id, text)
                return
            elif intent == 'STATUS':
                self._cmd_status(chat_id)
                return
            elif intent == 'TRADE_REVIEW':
                self._handle_trade_review_request(chat_id, text)
                return
            elif intent == 'LEARN_EXPERTS':
                threading.Thread(target=self._cmd_manual_learn, args=(chat_id,), daemon=True).start()
                return

            # 4. 기타 모든 일반 대화 (AI 챗)
            self._handle_normal_chat(chat_id, text)

        except Exception as e:
            logger.error(f"메시지 처리 오류: {e}\n{traceback.format_exc()}")
            self.tg.send_message(chat_id, f"❌ 처리 중 오류 발생: {str(e)[:100]}")

    # ──────────────────────────────────────────────
    # 핵심: 분석 및 응답
    # ──────────────────────────────────────────────

    def _analyze_and_respond(self, chat_id: int, symbol: str, timeframe: str = "1h"):
        """심볼 분석 → 차트 + 텍스트 전송 → 자동매매"""
        self.tg.send_typing(chat_id)
        self.tg.send_message(chat_id, f"🔍 *{symbol}* ({timeframe}) 분석 중...\n잠시 기다려주세요 ⏳", parse_mode='Markdown')

        try:
            # 데이터 수집
            df_entry = self.fetcher.get_klines(symbol, ENTRY_TF, limit=200)
            df_chart = self.fetcher.get_klines(symbol, timeframe, limit=150)
            df_higher = self.fetcher.get_klines(symbol, HIGHER_TF, limit=100)
            current_price = self.fetcher.get_price(symbol)

            if len(df_entry) < 50:
                self.tg.send_message(chat_id, f"❌ {symbol}: 데이터 부족")
                return

            df_1h = df_chart if timeframe == "1h" else self.fetcher.get_klines(symbol, "1h", limit=100)

            # 전략 분석
            analysis = self.strategy.analyze(df_entry, symbol, df_higher, df_1h=df_1h)
            
            if analysis is None:
                self.tg.send_message(chat_id, f"❌ {symbol} 분석 결과가 없습니다.")
                return

            # 차트 생성
            user_pos = self.fetcher.get_position(symbol)
            self.tg.send_upload_photo(chat_id)
            chart_bytes = generate_analysis_chart(
                df=df_chart,
                symbol=symbol,
                analysis_result=analysis,
                signal=analysis.signal if analysis else None,
                user_position=user_pos
            )

            # 분석 텍스트 생성
            message_text = format_telegram_message(
                analysis_result=analysis,
                symbol=symbol,
                current_price=current_price,
                timeframe=timeframe.upper()
            )

            # 전송
            if len(message_text) > 1000:
                self.tg.send_photo(chat_id=chat_id, photo=chart_bytes, caption=f"📊 {symbol} 차트")
                self.tg.send_message(chat_id, message_text, parse_mode='HTML')
            else:
                self.tg.send_photo(chat_id=chat_id, photo=chart_bytes, caption=message_text, parse_mode='HTML')

            # AI 설명 추가
            explanation = generate_analysis_explanation(analysis, analysis.signal)
            self.tg.send_message(chat_id, explanation, parse_mode='HTML')

            # 자동매매
            if self.state.auto_trade:
                if analysis.signal and analysis.signal.confidence >= AUTO_TRADE_MIN_CONFIDENCE:
                    self._execute_auto_trade(chat_id, symbol, analysis)

        except Exception as e:
            logger.error(f"분석 오류 {symbol}: {e}")
            self.tg.send_message(chat_id, f"❌ {symbol} 분석 실패: {str(e)[:200]}")

    def _execute_auto_trade(self, chat_id: int, symbol: str, analysis):
        """자동매매 실행 (V5.2.2)"""
        signal = analysis.signal
        with self.trade_lock:
            try:
                live_positions = self.fetcher.get_all_positions()
                if any(p['symbol'] == symbol for p in live_positions):
                    return

                if len(live_positions) >= MAX_OPEN_POSITIONS:
                    return

                self.fetcher.set_leverage(symbol, signal.leverage)
                self.fetcher.set_margin_type(symbol, 'ISOLATED')

                current_price = self.fetcher.get_price(symbol)
                quantity = self.fetcher.calculate_position_size(symbol, current_price, signal.stop_loss, signal.leverage)
                quantity = self.fetcher._round_quantity(symbol, quantity)

                if quantity <= 0: return

                side = 'BUY' if signal.direction == 'LONG' else 'SELL'
                order = self.fetcher.place_limit_order_with_fallback(symbol, side, quantity, current_price)

                if order.get('orderId'):
                    self.fetcher.place_sl_tp_orders(symbol, signal.direction, quantity, signal.stop_loss, signal.take_profit)
                    self.tg.send_message(chat_id, f"🤖 <b>[AI 진입 성공 - {symbol}]</b>\n{signal.direction} @ {current_price}", parse_mode='HTML')
                    
                    with self.state.lock:
                        self.state.active_positions[symbol] = {
                            'entry_price': current_price,
                            'quantity': quantity,
                            'direction': signal.direction,
                            'timestamp': time.time()
                        }
                    self.state.save_state()

            except Exception as e:
                logger.error(f"거래 오류 {symbol}: {e}")

    # ──────────────────────────────────────────────
    # 명령어 핸들러
    # ──────────────────────────────────────────────

    def _cmd_start(self, chat_id: int, username: str):
        msg = f"👋 안녕하세요, {username}님!\n<b>ChoiGPT Binance Auto Bot</b> v6.8 입니다.\n\n아래 메뉴 또는 /help 를 입력하여 사용법을 확인하세요."
        self.tg.send_message(chat_id, msg, parse_mode='HTML', reply_markup=self.tg.get_keyboard())

    def _cmd_help(self, chat_id: int):
        msg = (
            "🛠️ <b>주요 명령어 안내</b>\n\n"
            "📈 <b>분석 및 매매</b>\n"
            "• <code>/scan [신뢰도]</code>: 현재 후보 종목 스캔 (기본 60)\n"
            "• <code>/fullscan [신뢰도]</code>: 전 종목 정밀 스캔\n"
            "• <code>btc 1h</code>: 특정 종목 즉시 분석\n"
            "• '비트코인 어때?' : 자연어 질문 대응\n\n"
            "⚙️ <b>계정 및 상태</b>\n"
            "• <code>/status</code>: 봇 가동 상태 및 잔고\n"
            "• <code>/positions</code>: 현재 보유 포지션\n"
            "• <code>/balance</code>: 지갑 잔고 상세\n"
            "• <code>/stats</code>: 누적 수익 통계\n"
            "• <code>/autotrade</code>: 자동매매 ON/OFF 토글\n\n"
            "🧠 <b>AI 및 기타</b>\n"
            "• <code>/ai [질문]</code>: 일반 AI 대화\n"
            "• <code>/clear</code>: 대화 이력 초기화\n"
            "• <code>/report</code>: 일일 전략 리포트 생성"
        )
        self.tg.send_message(chat_id, msg, parse_mode='HTML')

        try:
            balance = self.fetcher.get_balance()
            positions = self.fetcher.get_all_positions()
            
            status_emoji = "🟢 RUNNING" if self.state.auto_trade else "🔴 PAUSED"
            msg = (
                f"📊 <b>Bot Status: {status_emoji}</b>\n"
                f"━━━━━━━━━━━━━━\n"
                f"💰 <b>Wallet Balance:</b> ${balance:,.2f}\n"
                f"📦 <b>Open Positions:</b> {len(positions)}개\n"
                f"🤖 <b>Auto Trade:</b> {'ON' if self.state.auto_trade else 'OFF'}\n"
                f"📡 <b>Instance:</b> {os.environ.get('COMPUTERNAME', 'Server')}\n"
                f"━━━━━━━━━━━━━━"
            )
            self.tg.send_message(chat_id, msg, parse_mode='HTML')
        except Exception as e:
            self.tg.send_message(chat_id, f"❌ 상태 확인 중 오류: {e}")

    def _cmd_status(self, chat_id: int):
        """현재 봇 상태 요약 보고"""
        try:
            balance_info = self.fetcher.get_account_balance()
            usdt_bal = balance_info.get('USDT', {})
            wallet = usdt_bal.get('wallet', 0.0)
            available = usdt_bal.get('available', 0.0)
            
            positions = self.fetcher.get_all_positions()
            status_emoji = "🟢 가동 중 (RUNNING)" if self.state.auto_trade else "🔴 정지 (PAUSED)"
            
            msg = (
                f"🤖 <b>ChoiGPT Bot 상태 브리핑</b>\n"
                f"━━━━━━━━━━━━━━\n"
                f"⚙️ <b>가동 모드:</b> {status_emoji}\n"
                f"💰 <b>USDT 잔고:</b> ${wallet:,.2f}\n"
                f"🔓 <b>가용 잔고:</b> ${available:,.2f}\n"
                f"📦 <b>오픈 포지션:</b> {len(positions)}개\n"
                f"📡 <b>서버:</b> {os.environ.get('COMPUTERNAME', 'Server')}\n"
                f"━━━━━━━━━━━━━━"
            )
            self.tg.send_message(chat_id, msg, parse_mode='HTML')
        except Exception as e:
            logger.error(f"상태 확인 오류: {e}")
            self.tg.send_message(chat_id, f"❌ 상태 조회 중 오류 발생: {str(e)[:100]}")

    def _cmd_balance(self, chat_id: int):
        """상세 계좌 잔고 확인"""
        try:
            balance_info = self.fetcher.get_account_balance()
            lines = ["💰 <b>상세 자산 현황</b>", "━━━━━━━━━━━━━━"]
            total_wallet = 0
            for asset, data in balance_info.items():
                w = data.get('wallet', 0)
                a = data.get('available', 0)
                u = data.get('unrealized_pnl', 0)
                lines.append(f"<b>[{asset}]</b> 자산")
                lines.append(f"• Wallet: ${w:,.2f}")
                lines.append(f"• Available: ${a:,.2f}")
                lines.append(f"• UnPnl: {u:+.2f} USDT\n")
                if asset == 'USDT': total_wallet = w
                
            lines.append("━━━━━━━━━━━━━━")
            self.tg.send_message(chat_id, "\n".join(lines), parse_mode='HTML')
        except Exception as e:
            self.tg.send_message(chat_id, f"❌ 잔고 조회 실패: {e}")

    def _cmd_positions(self, chat_id: int):
        """현재 보유 포지션 상세 확인"""
        try:
            positions = self.fetcher.get_all_positions()
            if not positions:
                self.tg.send_message(chat_id, "💼 <b>보유 중인 포지션이 없습니다.</b>", parse_mode='HTML')
                return

            lines = [f"💼 <b>오픈 포지션 내역 ({len(positions)}개)</b>", "━━━━━━━━━━━━━━"]
            for p in positions:
                sym = p['symbol']
                side = "🟢 LONG" if p['side'] == 'LONG' else "🔴 SHORT"
                pnl = p['unrealized_pnl']
                pnl_pct = (pnl / (p['entry_price'] * p['size'] / p['leverage']) * 100) if p['size'] > 0 else 0
                
                lines.append(f"<b>{sym}</b> {side} {p['leverage']}x")
                lines.append(f"• 수량: {p['size']} ({p['entry_price']:.4f})")
                lines.append(f"• 수익: {pnl:+.2f} USDT ({pnl_pct:+.1f}%)")
                lines.append(f"• 마크가: {p['mark_price']:.4f}\n")
            
            lines.append("━━━━━━━━━━━━━━")
            self.tg.send_message(chat_id, "\n".join(lines), parse_mode='HTML')
        except Exception as e:
            self.tg.send_message(chat_id, f"❌ 포지션 조회 실패: {e}")

    def _cmd_stats(self, chat_id: int):
        """누적 수익 통계 확인"""
        try:
            total = self.state.total_trades
            wins = self.state.winning_trades
            wr = (wins / total * 100) if total > 0 else 0
            pnl = self.state.cumulative_pnl
            
            msg = (
                f"📈 <b>누적 매매 성과 통계</b>\n"
                f"━━━━━━━━━━━━━━\n"
                f"📊 <b>총 거래 횟수:</b> {total}회\n"
                f"🎯 <b>승률:</b> {wr:.1f}% ({wins}승 {total-wins}패)\n"
                f"💰 <b>누적 수익률:</b> {pnl:+.2f}%\n"
                f"━━━━━━━━━━━━━━\n"
                f"<i>* 봇 가동 이후의 누적 데이터 기준입니다.</i>"
            )
            self.tg.send_message(chat_id, msg, parse_mode='HTML')
        except Exception as e:
            self.tg.send_message(chat_id, f"❌ 통계 조회 실패: {e}")

    def _cmd_toggle_autotrade(self, chat_id: int):
        """자동매매 ON/OFF 토글"""
        self.state.auto_trade = not self.state.auto_trade
        self.state.save_state()
        status = "가동(ON) ✅" if self.state.auto_trade else "중지(OFF) 🛑"
        self.tg.send_message(chat_id, f"🤖 <b>AI 자동매매 상태 변경</b>\n━━━━━━━━━━━━━━\n현재 상태: <b>{status}</b>")
        logger.info(f"⚙️ 자율 모드 수동 변경: {self.state.auto_trade}")

    def _cmd_scan_signals(self, chat_id: int, min_conf: float = 0.60):
        """후보 종목 신호 스캔"""
        self.tg.send_message(chat_id, f"📡 <b>후보 종목 스캔 시작...</b> (신뢰도 {min_conf:.0%}+)", parse_mode='HTML')
        from config.config import SYMBOLS
        found = 0
        for symbol in SYMBOLS:
            try:
                # 1h 분석 기준
                df_entry = self.fetcher.get_klines(symbol, "15m", limit=200)
                df_1h = self.fetcher.get_klines(symbol, "1h", limit=150)
                df_4h = self.fetcher.get_klines(symbol, "4h", limit=100)
                
                analysis = self.strategy.analyze(df_entry, symbol, df_4h, df_1h=df_1h, override_min_conf=min_conf)
                if analysis and analysis.signal:
                    found += 1
                    self._analyze_and_respond(chat_id, symbol, "1h")
                    time.sleep(1) # 전송 부하 방지
            except Exception as e:
                logger.error(f"Scan error for {symbol}: {e}")
        
        if found == 0:
            self.tg.send_message(chat_id, "🔍 감지된 유효 신호가 없습니다.")

    def _cmd_fullscan_symbols(self, chat_id: int, min_conf: float = 0.65):
        """바이낸스 전체 종목 스캔"""
        self.tg.send_message(chat_id, f"🌍 <b>전체 마켓 정밀 스캔 가동...</b>\n약 1~2분 소요됩니다.", parse_mode='HTML')
        try:
            # 거래량 상위 100개 추출
            resp = requests.get("https://fapi.binance.com/fapi/v1/ticker/24hr", timeout=10)
            tickers = resp.json()
            usdt_tickers = [t for t in tickers if t['symbol'].endswith('USDT') and t['symbol'] not in EXCLUDED_SYMBOLS]
            top_tickers = sorted(usdt_tickers, key=lambda x: float(x['quoteVolume']), reverse=True)[:60]
            
            found = 0
            for t in top_tickers:
                symbol = t['symbol']
                df_entry = self.fetcher.get_klines(symbol, "15m", limit=300)
                df_1h = self.fetcher.get_klines(symbol, "1h", limit=150)
                df_4h = self.fetcher.get_klines(symbol, "4h", limit=100)
                
                analysis = self.strategy.analyze(df_entry, symbol, df_4h, df_1h=df_1h, override_min_conf=min_conf)
                if analysis and analysis.signal:
                    found += 1
                    self._analyze_and_respond(chat_id, symbol, "1h")
                    time.sleep(1)
                if found >= 5: break # 너무 많으면 중단 (탑 5개만)
                
            if found == 0:
                self.tg.send_message(chat_id, "🔍 현재 전 종목 중 기준 충족 신호가 없습니다.")
            else:
                self.tg.send_message(chat_id, f"✅ 스캔 완료: 총 {found}개의 고신뢰도 신호 감지")
        except Exception as e:
            self.tg.send_message(chat_id, f"❌ 전체 스캔 오류: {e}")

    def _cmd_report(self, chat_id: int):
        """일일 전략 리포트 생성 및 발송"""
        self.tg.send_message(chat_id, "📊 <b>오늘의 매매 전략 리포트 생성 중...</b>", parse_mode='HTML')
        try:
            report_path = self.report_manager.generate_daily_report()
            if report_path and os.path.exists(report_path):
                with open(report_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # 텔레그램 메시지 길이 제한(4096) 대응
                if len(content) > 4000:
                    content = content[:3900] + "...(이하 생략)"
                self.tg.send_message(chat_id, content, parse_mode='HTML')
            else:
                self.tg.send_message(chat_id, "ℹ️ 오늘 처리된 거래 기록이 없어 리포트를 생성할 수 없습니다.")
        except Exception as e:
            self.tg.send_message(chat_id, f"❌ 리포트 생성 실패: {e}")

    def _cmd_ai_chat(self, chat_id: int, user_msg: str):
        """AI 상세 상담"""
        if not user_msg:
            self.tg.send_message(chat_id, "💡 <code>/ai 질문내용</code> 형식으로 입력해 주세요.")
            return
        self._handle_normal_chat(chat_id, user_msg)

    def _cmd_clear_chat(self, chat_id: int):
        """채팅 이력 초기화"""
        clear_history(chat_id)
        self.tg.send_message(chat_id, "🧹 <b>AI 대화 이력이 초기화되었습니다.</b>", parse_mode='HTML')

    def _cmd_clean(self, chat_id: int):
        """미체결 주문 및 좀비 포지션 정리"""
        self.tg.send_message(chat_id, "🧹 <b>미체결 주문 및 고립 포지션 정리 중...</b>", parse_mode='HTML')
        try:
            # 1. 모든 미체결 알고 주문 취소
            positions = self.fetcher.get_all_positions()
            pos_symbols = {p['symbol'] for p in positions}
            
            # 포지션이 없는 종목인데 주문이 걸려있는 경우 취소
            open_algos = self.fetcher.get_all_open_algo_orders()
            cleaned_orders = 0
            for o in open_algos:
                s = o['symbol']
                if s not in pos_symbols:
                    self.fetcher.cancel_all_algo_orders(s)
                    self.fetcher.cancel_all_orders(s)
                    cleaned_orders += 1
            
            self.tg.send_message(chat_id, f"✅ 정리 완료: {cleaned_orders}건의 고립 주문을 취소했습니다.")
            self._sync_with_exchange() # 상태 동기화
        except Exception as e:
            self.tg.send_message(chat_id, f"❌ 클리닝 중 오류: {e}")

    def _cmd_manual_learn(self, chat_id: int):
        """전문가 신호 수동 학습"""
        if not self.comparator:
            self.tg.send_message(chat_id, "⚠️ 학습 모듈이 비활성화 상태입니다.")
            return
        self.tg.send_message(chat_id, "🧠 <b>실시간 전문가 신호 수집 및 학습 시작...</b>", parse_mode='HTML')
        def run_learn():
            try:
                self.comparator.run_daily_comparison()
                self.tg.send_message(chat_id, "✅ 전문가 학습 및 전략 업데이트 완료!")
            except Exception as e:
                self.tg.send_message(chat_id, f"❌ 학습 오류: {e}")
        threading.Thread(target=run_learn, daemon=True).start()

    def _parse_symbol_and_timeframe(self, text: str):
        """텍스트에서 심볼과 타임프레임 파싱 (예: btc 1h)"""
        text = text.lower().strip()
        symbol = get_symbol_from_text(text)
        
        # 타임프레임 추출 (1m, 5m, 15m, 1h, 4h, 1d 등)
        tf_match = re.search(r'\b(1m|3m|5m|15m|30m|1h|2h|4h|6h|8h|12h|1d|1w)\b', text)
        timeframe = tf_match.group(1) if tf_match else "1h"
        
        return symbol, timeframe

    def send_startup_message(self):
        """봇 시작 알림 전송"""
        try:
            msg = (
                "🤖 <b>ChoiGPT Bot 가동 중</b>\n"
                f"━━━━━━━━━━━━━━\n"
                f"🕒 <b>시간:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"📡 <b>서버:</b> {os.environ.get('COMPUTERNAME', 'Server')}\n"
                f"⚙️ <b>자동매매:</b> {'ON' if self.state.auto_trade else 'OFF'}\n"
                f"━━━━━━━━━━━━━━\n"
                f"💡 /help 를 입력하여 사용법을 확인하세요."
            )
            # 설정된 관리자 Chat ID로 전송
            for cid in ALLOWED_CHAT_IDS:
                self.tg.send_message(cid, msg, parse_mode='HTML')
        except Exception as e:
            logger.error(f"시작 메시지 전송 실패: {e}")

    def _sync_with_exchange(self):
        """거래소와 로컬 상태 동기화 (V5.2.2)"""
        try:
            live_positions = self.fetcher.get_all_positions()
            live_symbols = {p['symbol'] for p in live_positions}
            
            with self.state.lock:
                # 1. 상태 파일엔 있는데 거래소엔 없는 종목 삭제
                obsolete = [s for s in self.state.active_positions if s not in live_symbols]
                for s in obsolete:
                    del self.state.active_positions[s]
                
                # 2. 거래소엔 있는데 상태 파일엔 없는 종목 추가 (기본값)
                for p in live_positions:
                    s = p['symbol']
                    if s not in self.state.active_positions:
                        self.state.active_positions[s] = {
                            'entry_price': float(p['entryPrice']),
                            'quantity': abs(float(p['positionAmt'])),
                            'direction': 'LONG' if float(p['positionAmt']) > 0 else 'SHORT',
                            'timestamp': time.time()
                        }
            self.state.save_state()
            logger.info("📡 포지션 동기화 완료")
        except Exception as e:
            logger.error(f"동기화 오류: {e}")

    def _cmd_reboot(self, chat_id: int):
        """봇 강제 재시작"""
        self.tg.send_message(chat_id, "🔄 봇 재시작 신호 전송 완료... (약 10초 소요)")
        os._exit(0)

    # ──────────────────────────────────────────────
    # 응답 핸들러 (NLP 연동)
    # ──────────────────────────────────────────────

    def _handle_normal_chat(self, chat_id: int, text: str):
        """일반 AI 대화 처리 (V6.0: 컨텍스트 주입 최적화)"""
        self.tg.send_typing(chat_id)
        try:
            # 계좌 컨텍스트 수집
            context = {}
            try:
                balance_info = self.fetcher.get_account_balance()
                usdt_bal = balance_info.get('USDT', {})
                positions = self.fetcher.get_all_positions()
                
                context = {
                    'balance': usdt_bal.get('wallet', 0.0),
                    'available': usdt_bal.get('available', 0.0),
                    'open_positions': [
                        {
                            'symbol': p['symbol'],
                            'direction': p['side'],
                            'pnl_pct': (p['unrealized_pnl'] / (p['entry_price'] * p['size'] / p['leverage']) * 100) if p['size'] > 0 else 0
                        } for p in positions
                    ],
                    'win_rate': (self.state.winning_trades / self.state.total_trades * 100) if self.state.total_trades > 0 else 0,
                    'total_trades': self.state.total_trades,
                    'cycle_count': getattr(self.state, 'cycle_count', 0)
                }
            except Exception as context_err:
                logger.debug(f"AI 컨텍스트 수집 실패 (무시): {context_err}")

            # 컨텍스트 포함 대화 생성 (V6.0: generate_contextual_chat_response 직접 사용)
            response = generate_contextual_chat_response(text, chat_id, account_context=context)
            
            if not response:
                response = "💡 죄송합니다. 지금은 분석에 집중하고 있어 대답하기 어렵습니다. 잠시 후 다시 물어봐 주세요."
                
            self.tg.send_message(chat_id, response, parse_mode='HTML')
        except Exception as e:
            logger.error(f"AI 대화 처리 오류: {e}")
            self.tg.send_message(chat_id, "💡 죄송합니다. 대답을 생성하는 중에 오류가 발생했습니다.")

    def _handle_exit_strategy_request(self, chat_id: int, text: str):
        """평단 기반 엑시트 전략 상담 (V5.7)"""
        self.tg.send_typing(chat_id)
        # NLP를 통해 심볼과 평단 추출 시도
        try:
            analysis_text = generate_exit_strategy_analysis(text)
            self.tg.send_message(chat_id, analysis_text, parse_mode='HTML')
        except Exception as e:
            self.tg.send_message(chat_id, "❌ 엑시트 전략 분석 중 오류가 발생했습니다.")

    def _handle_trade_strategy_request(self, chat_id: int, text: str):
        """진입 전략 상담 (V5.8)"""
        self.tg.send_typing(chat_id)
        try:
            analysis_text = generate_trade_strategy_analysis(text)
            self.tg.send_message(chat_id, analysis_text, parse_mode='HTML')
        except Exception as e:
            self.tg.send_message(chat_id, "❌ 매매 전략 분석 중 오류가 발생했습니다.")

    def _handle_trade_review_request(self, chat_id: int, text: str):
        """매매 복기 서비스 (V6.2)"""
        self.tg.send_message(chat_id, "📝 최근 매매 내역을 분석하여 복기 리포트를 작성 중입니다...")
        try:
            # [실제 리포트 매니저 연동]
            report = self.report_manager.get_last_trade_review()
            self.tg.send_message(chat_id, f"🧐 <b>최근 매매 복기 리포트</b>\n\n{report}", parse_mode='HTML')
        except Exception as e:
            self.tg.send_message(chat_id, "❌ 복기 데이터를 불러오지 못했습니다.")

    def _cmd_market_briefing_manual(self, chat_id: int):
        """수동 시장 브리핑 (폭등/폭락 종목 선정)"""
        self.tg.send_typing(chat_id)
        self.tg.send_message(chat_id, "🔍 <b>현재 시장의 폭등 및 폭락 종목을 선정 중입니다...</b>\nSMC 구조 분석과 차트 생성이 진행됩니다. (약 30초 소요)", parse_mode='HTML')
        
        try:
            # 브리핑 서비스 호출
            scanner = MarketScannerService()
            briefing_text, charts = scanner.get_top_opportunities()
            
            # 1. 브리핑 텍스트 발송
            self.tg.send_message(chat_id, briefing_text, parse_mode='HTML')
            
            # 2. 분석 차트 순차 발송
            if charts:
                self.tg.send_message(chat_id, "📊 <b>선정 종목 상세 분석 차트:</b>", parse_mode='HTML')
                for chart in charts:
                    self.tg.send_photo(
                        chat_id=chat_id, 
                        photo=chart['data'], 
                        caption=f"📈 <b>{chart['symbol']} SMC Analysis</b>", 
                        parse_mode='HTML'
                    )
                    time.sleep(0.5) # 전송 간격
                    
            logger.info(f"✅ 수동 브리핑 완료 (종목 {len(charts)}개)")
            
        except Exception as e:
            logger.error(f"수동 브리핑 오류: {e}\n{traceback.format_exc()}")
            self.tg.send_message(chat_id, f"❌ 브리핑 생성 도중 오류가 발생했습니다: {str(e)[:100]}")

if __name__ == "__main__":
    # 로깅 설정
    try:
        bot = ChoiGPTBot()
        bot.start()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        traceback.print_exc()