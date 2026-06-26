#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChoiGPT 방법론 바이낸스 선물 자동매매 봇
메인 실행 파일

사용법:
  백테스트:  python main.py --mode backtest --symbol BTCUSDT
  최적화:    python main.py --mode optimize --symbol BTCUSDT
  실전봇:    python main.py --mode live
  분석만:    python main.py --mode analyze --symbol BTCUSDT
"""

import argparse
import logging
import os
import sys
import io
import time
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# ★ V5.5: UTF-8 인코딩 설정 (이모지 출력 지원)
if sys.stdout.encoding != 'utf-8':
    if sys.platform == 'win32':
        import codecs
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 프로젝트 루트 디렉토리를 패스에 추가하여 어디서든 실행 가능하게 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# 내부 모듈 임포트 (변경된 구조 반영)
from config.config import *
from src.data_fetcher import BinanceFetcher
from src.strategy import ChoiGPTStrategy
from scripts.backtester import Backtester
from src.live_trader import LiveTrader


# ── 로깅 설정 ──
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


# ============================================================
# 백테스트 모드
# ============================================================

def run_backtest(symbol: str, start: str = None, end: str = None,
                 save_chart: bool = True):
    """백테스트 실행"""
    if start is None:
        start = BACKTEST_START
    if end is None:
        end = BACKTEST_END

    print(f"\n{'='*60}")
    print(f"📊 백테스트 모드")
    print(f"  심볼: {symbol} | 기간: {start} ~ {end}")
    print(f"  초기 자본: ${BACKTEST_INITIAL_CAPITAL:,}")
    print(f"{'='*60}")

    # 데이터 수집
    print("\n📥 바이낸스에서 과거 데이터 수집 중...")
    fetcher = BinanceFetcher()

    try:
        df = fetcher.get_historical_klines(symbol, ENTRY_TF, start, end)
    except Exception as e:
        print(f"❌ 데이터 수집 실패: {e}")
        print("💡 샘플 데이터로 대체하여 실행합니다...")
        df = generate_sample_data(start, end)

    if len(df) < 100:
        print("❌ 데이터가 충분하지 않습니다.")
        return None

    print(f"✅ 데이터 수집 완료: {len(df)}개 캔들 ({df.index[0]} ~ {df.index[-1]})")

    # 백테스트 실행
    print("\n⚙️  백테스트 실행 중...")
    backtester = Backtester(initial_capital=BACKTEST_INITIAL_CAPITAL)
    result = backtester.run(df, symbol)

    # 결과 출력
    backtester.print_results(result)

    # 차트 저장
    if save_chart and result.equity_curve is not None:
        save_backtest_chart(result, symbol, df)
        print(f"\n📈 차트 저장 완료: backtest_{symbol}.png")

    return result


def save_backtest_chart(result, symbol: str, df: pd.DataFrame):
    """백테스트 결과 차트 저장"""
    fig, axes = plt.subplots(3, 1, figsize=(16, 12))
    fig.suptitle(f'{symbol} ChoiGPT 방법론 백테스트 결과', fontsize=14, fontweight='bold')

    # 1. 가격 차트 + 거래 신호
    ax1 = axes[0]
    ax1.plot(df.index, df['close'], color='gray', linewidth=0.8, label='가격', alpha=0.7)

    wins = [t for t in result.trades if t.status == 'WIN']
    losses = [t for t in result.trades if t.status == 'LOSS']

    for t in wins:
        color = 'green' if t.direction == 'LONG' else 'blue'
        marker = '^' if t.direction == 'LONG' else 'v'
        ax1.scatter(t.entry_time, t.entry_price, color=color, marker=marker, s=80, zorder=5)
        if t.exit_time and t.exit_price:
            ax1.scatter(t.exit_time, t.exit_price, color='lime', marker='o', s=50, zorder=5)

    for t in losses:
        color = 'red' if t.direction == 'LONG' else 'orange'
        marker = '^' if t.direction == 'LONG' else 'v'
        ax1.scatter(t.entry_time, t.entry_price, color=color, marker=marker, s=80, zorder=5)
        if t.exit_time and t.exit_price:
            ax1.scatter(t.exit_time, t.exit_price, color='darkred', marker='o', s=50, zorder=5)

    ax1.set_ylabel('가격 (USDT)')
    ax1.legend(['가격', '승리(롱)', '승리(숏)', '패배'], loc='upper left', fontsize=8)
    ax1.grid(True, alpha=0.3)

    # 2. 자본 곡선
    ax2 = axes[1]
    ax2.plot(result.equity_curve.index, result.equity_curve.values,
             color='blue', linewidth=1.5)
    ax2.axhline(y=BACKTEST_INITIAL_CAPITAL, color='gray', linestyle='--', alpha=0.5)
    ax2.fill_between(result.equity_curve.index, BACKTEST_INITIAL_CAPITAL,
                     result.equity_curve.values,
                     where=result.equity_curve.values >= BACKTEST_INITIAL_CAPITAL,
                     color='green', alpha=0.2)
    ax2.fill_between(result.equity_curve.index, BACKTEST_INITIAL_CAPITAL,
                     result.equity_curve.values,
                     where=result.equity_curve.values < BACKTEST_INITIAL_CAPITAL,
                     color='red', alpha=0.2)
    ax2.set_ylabel('자본 (USDT)')
    ax2.set_title('자본 곡선')
    ax2.grid(True, alpha=0.3)

    # 3. 드로우다운
    ax3 = axes[2]
    eq = result.equity_curve
    rolling_max = eq.cummax()
    drawdown = (eq - rolling_max) / rolling_max * 100
    ax3.fill_between(drawdown.index, drawdown.values, 0, color='red', alpha=0.5)
    ax3.set_ylabel('낙폭 (%)')
    ax3.set_title('드로우다운')
    ax3.grid(True, alpha=0.3)

    # 성과 텍스트 박스
    metrics = result.metrics
    text = (f"총 거래: {metrics.get('총 거래 수', 0)}\n"
            f"승률: {metrics.get('승률', 'N/A')}\n"
            f"수익률: {metrics.get('총 수익률', 'N/A')}\n"
            f"MDD: {metrics.get('최대 낙폭 (MDD)', 'N/A')}\n"
            f"샤프: {metrics.get('샤프 비율', 'N/A')}\n"
            f"PF: {metrics.get('프로핏 팩터', 'N/A')}")

    ax1.text(0.02, 0.97, text, transform=ax1.transAxes,
             fontsize=8, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig(f'backtest_{symbol}.png', dpi=150, bbox_inches='tight')
    plt.close()


# ============================================================
# 최적화 모드
# ============================================================

def run_optimization(symbol: str):
    """파라미터 최적화"""
    print(f"\n{'='*60}")
    print(f"🔍 파라미터 최적화 모드: {symbol}")
    print(f"{'='*60}")

    fetcher = BinanceFetcher()

    try:
        df = fetcher.get_historical_klines(symbol, ENTRY_TF,
                                            BACKTEST_START, BACKTEST_END)
    except Exception as e:
        print(f"❌ 데이터 수집 실패: {e}")
        df = generate_sample_data(BACKTEST_START, BACKTEST_END)

    backtester = Backtester()

    # 파라미터 그리드
    param_grid = {
        'min_confidence': [0.55, 0.60, 0.65, 0.70, 0.75],
    }

    opt_results = backtester.optimize_parameters(df, symbol, param_grid)

    if len(opt_results) > 0:
        print("\n🏆 최적 파라미터 (상위 5개):")
        print(opt_results.head().to_string(index=False))

        best = opt_results.iloc[0]
        print(f"\n✨ 최적 설정:")
        print(f"   신뢰도 임계값: {best.get('min_confidence', 0.65)}")
        print(f"   예상 수익률: {best.get('total_return', 0):.2f}%")
        print(f"   예상 MDD: {best.get('max_drawdown', 0):.2f}%")
        print(f"   예상 승률: {best.get('win_rate', 0):.1%}")

    return opt_results


# ============================================================
# 실시간 분석 모드
# ============================================================

def run_analysis(symbol: str):
    """현재 시장 실시간 분석"""
    print(f"\n{'='*60}")
    print(f"📊 실시간 분석 모드: {symbol}")
    print(f"{'='*60}")

    fetcher = BinanceFetcher()
    strategy = ChoiGPTStrategy(min_confidence=AUTO_TRADE_MIN_CONFIDENCE)

    try:
        df_entry = fetcher.get_klines(symbol, ENTRY_TF, limit=200)
        df_higher = fetcher.get_klines(symbol, HIGHER_TF, limit=100)
        current_price = fetcher.get_price(symbol)

        print(f"\n💰 {symbol} 현재가: ${current_price:,.2f}")

        analysis = strategy.analyze(df_entry, symbol, df_higher)
        print(analysis.analysis_text)

    except Exception as e:
        print(f"❌ 분석 실패: {e}")
        print("💡 API 키를 config.py에 설정하세요.")


# ============================================================
# 실전 봇 모드
# ============================================================

def run_live(symbols: list = None):
    """실전 자동매매 봇 시작 (V3.6: 통합된 run_bot.py 사용을 권장합니다)"""
    print(f"\n{'='*60}")
    print("🚀 실전 자동매매 봇 모드")
    print("⚠️  V3.6부터는 텔레그램 봇과 통합된 'run_bot.py' 사용을 권장합니다.")
    print("   이 모드는 콘솔 전용이며 중복 실행 시 주문이 충돌할 수 있습니다.")
    print(f"{'='*60}")

    time.sleep(2)
    trader = LiveTrader(use_testnet=USE_TESTNET)
    
    current_symbols = symbols or SYMBOLS
    if USE_DYNAMIC_SYMBOLS:
        try:
            fetcher = BinanceFetcher()
            dynamic_list = fetcher.get_top_symbols(DYNAMIC_SYMBOL_COUNT)
            if dynamic_list:
                current_symbols = dynamic_list
                print(f"📊 거래량 상위 {len(current_symbols)}개 종목으로 시작합니다.")
        except Exception as e:
            print(f"⚠️ 동적 심볼 로드 실패: {e}")

    trader.start(current_symbols)


# ============================================================
# 샘플 데이터 생성 (API 없을 때)
# ============================================================

def generate_sample_data(start: str, end: str) -> pd.DataFrame:
    """API 없이 테스트용 샘플 데이터 생성"""
    import numpy as np

    dates = pd.date_range(start=start, end=end, freq='15min')
    n = len(dates)

    # 현실적인 BTC 가격 시뮬레이션
    np.random.seed(42)
    price = 40000.0
    prices = [price]

    for i in range(1, n):
        # 랜덤워크 + 약한 추세
        change = np.random.normal(0, 0.003) + 0.00005
        price = price * (1 + change)
        prices.append(price)

    prices = np.array(prices)

    # OHLCV 생성
    volatility = 0.002
    opens = prices * (1 + np.random.normal(0, volatility*0.3, n))
    highs = np.maximum(prices, opens) * (1 + abs(np.random.normal(0, volatility, n)))
    lows = np.minimum(prices, opens) * (1 - abs(np.random.normal(0, volatility, n)))
    closes = prices
    volumes = np.random.exponential(1000, n)

    df = pd.DataFrame({
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes,
        'volume': volumes
    }, index=dates)

    return df


# ============================================================
# 메인 진입점
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='ChoiGPT 방법론 바이낸스 선물 자동매매 봇')
    parser.add_argument('--mode', choices=['backtest', 'optimize', 'analyze', 'live'],
                       default='live', help='실행 모드')  # ★ V5.5: 기본값을 live로 변경
    parser.add_argument('--symbol', default='BTCUSDT', help='거래 심볼')
    parser.add_argument('--start', default=BACKTEST_START, help='백테스트 시작일 (YYYY-MM-DD)')
    parser.add_argument('--end', default=BACKTEST_END, help='백테스트 종료일 (YYYY-MM-DD)')
    parser.add_argument('--no-chart', action='store_true', help='차트 저장 안 함')

    args = parser.parse_args()

    print("\n" + "="*60)
    print("   [Chart] ChoiGPT Binance Auto Bot v1.0")
    print("   MSS | LRL | FVG | IFVG | BPR | OB | BB | DOL")
    print("="*60)

    if args.mode == 'backtest':
        run_backtest(args.symbol, args.start, args.end, not args.no_chart)

    elif args.mode == 'optimize':
        run_optimization(args.symbol)

    elif args.mode == 'analyze':
        run_analysis(args.symbol)

    elif args.mode == 'live':
        run_live()


if __name__ == "__main__":
    main()
