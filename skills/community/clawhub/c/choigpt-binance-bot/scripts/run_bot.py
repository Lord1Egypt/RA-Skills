"""
봇 실행 진입점
python run_bot.py 로 실행하세요
- 봇이 예외로 종료되어도 자동으로 재시작됩니다
"""

import os
import sys
import time
import logging
import traceback

# 프로젝트 루트 경로 계산
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
PID_FILE = os.path.join(LOG_DIR, "bot.pid")

# ★ 중복 실행 방지 (NAS + PC 동시 실행 시 포지션 2배 손실 방지)

def check_single_instance():
    os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                old_pid = int(f.read().strip())
            import psutil
            if psutil.pid_exists(old_pid):
                print(f"[ERROR] 봇이 이미 실행 중입니다! PID: {old_pid}")
                print(f"[ERROR] 중복 실행은 포지션 2배 노출로 큰 손실을 유발합니다.")
                print(f"[ERROR] 기존 프로세스를 종료 후 다시 실행하세요.")
                sys.exit(1)
        except (ValueError, ImportError):
            pass  # psutil 없거나 PID 파일 손상 → 계속 진행
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

def remove_pid():
    try:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
    except Exception:
        pass

# 경로 추가 (src 디렉토리를 패스에 추가하여 모듈 임포트 가능하게 함)
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# 로그 디렉토리 생성
os.makedirs(LOG_DIR, exist_ok=True)

# 로깅 설정 (DEBUG로 상세 로그 출력)
log_file = os.path.join(LOG_DIR, 'choigpt_bot.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, encoding='utf-8', mode='a')
    ]
)
logger = logging.getLogger(__name__)


def main():
    print("=" * 60)
    print("   ChoiGPT Binance Auto Bot")
    print("   ChoiGPT Methodology - Smart Money - ICT")
    print("=" * 60)
    print()
    print("[*] Starting bot initialization...")

    # API 키 확인
    try:
        from config import (API_KEY, API_SECRET, TELEGRAM_BOT_TOKEN,
                            ALLOWED_CHAT_IDS, USE_TESTNET)
        print("[OK] Config loaded successfully")
    except Exception as e:
        print(f"[ERROR] Failed to load config: {e}")
        print(traceback.format_exc())
        sys.exit(1)

    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        print("[ERROR] Binance API key not set in config.py")
        sys.exit(1)
    print("[OK] Binance API key loaded")

    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN":
        print("[ERROR] Telegram bot token not set in config.py")
        sys.exit(1)
    print("[OK] Telegram bot token loaded")

    mode = "LIVE" if not USE_TESTNET else "TESTNET"
    print()
    print(f"[*] Mode: {mode}")
    print(f"[*] Allowed Chat IDs: {ALLOWED_CHAT_IDS}")
    print(f"[*] Bot Token: ...{TELEGRAM_BOT_TOKEN[-10:]}")
    print()

    # ★ V7.7: SIGTERM → Exception 변환 (텔레그램 /reboot 명령 지원)
    # SIGTERM을 받으면 재시작 루프가 Exception을 캐치하여 자동 재시작이 일어남
    import signal
    class RequestedRestart(Exception):
        pass
    def _sigterm_handler(signum, frame):
        logger.warning("⚡ SIGTERM 수신 → 봇 재시작 루프 활성화")
        raise RequestedRestart("SIGTERM에 의한 재시작")
    signal.signal(signal.SIGTERM, _sigterm_handler)

    # 봇 자동 재시작 루프
    restart_count = 0
    while True:
        try:
            print("[*] Importing telegram bot module...")
            from telegram_bot import ChoiGPTBot
            print("[OK] Bot module imported")

            if restart_count > 0:
                print(f"\n[RESTART] Restarting bot... (attempt #{restart_count})")
                logger.info(f"Bot restart #{restart_count}")
            else:
                print("[*] Initializing bot...")

            bot = ChoiGPTBot()
            print("[OK] Bot initialized")
            print("[*] Starting polling loop...")
            bot.start()

        except KeyboardInterrupt:
            print("\n\n[STOP] Bot terminated by user (Ctrl+C)")
            logger.info("User terminated bot")
            sys.exit(0)
        except RequestedRestart:
            # /reboot 명령에 의한 의도적 재시작 - 짧게 대기 후 바로 재시작
            restart_count += 1
            logger.info(f"🔄 /reboot 요청에 의한 재기동 ({restart_count}회차) - 5초 후 재시작")
            print(f"\n[REBOOT] Bot restarting in 5 seconds... (#{restart_count})")
            time.sleep(5)
        except Exception as e:
            restart_count += 1
            wait = min(60, 10 * restart_count)
            tb_str = traceback.format_exc()
            logger.error(f"Bot crash (#{restart_count}): {e}\n{tb_str}")
            print(f"\n[ERROR] Bot crashed: {e}")
            print(f"[INFO] Restarting in {wait} seconds... (Press Ctrl+C to stop)")
            print(tb_str)
            time.sleep(wait)


if __name__ == "__main__":
    check_single_instance()
    try:
        main()
    finally:
        remove_pid()
