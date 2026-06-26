import requests
import logging

logger = logging.getLogger(__name__)

def get_exchange_rate():
    """실시간 USD/KRW 환율 가져오기 (Fallback 포함)"""
    try:
        # 1. Yahoo Finance 또는 공공 API 시도 (여기서는 간편한 인베스팅/야후 스타일 API 사용처 가정)
        # 무료 API인 ExchangeRate-API 등 사용 가능하나, 안정성을 위해 여러 곳 시도 가능
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json().get('rates', {}).get('KRW', 1400.0)
    except Exception as e:
        logger.error(f"환율 정보 가져오기 실패: {e}")
    
    return 1400.0 # 기본값 (최근 추세 반영)

def get_upbit_price(symbol: str):
    """업비트 실시간 시세 (KRW-BTC 방식)"""
    try:
        # symbol: BTCUSDT -> BTC
        coin = symbol.replace('USDT', '')
        url = f"https://api.upbit.com/v1/ticker?markets=KRW-{coin}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data:
                return float(data[0]['trade_price'])
    except Exception as e:
        logger.error(f"업비트 시세 조회 실패 ({symbol}): {e}")
    return None

def get_bithumb_price(symbol: str):
    """빗썸 실시간 시세 (BTC_KRW 방식)"""
    try:
        coin = symbol.replace('USDT', '')
        url = f"https://api.bithumb.com/public/ticker/{coin}_KRW"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') == '0000':
                return float(data['data']['closing_price'])
    except Exception as e:
        logger.error(f"빗썸 시세 조회 실패 ({symbol}): {e}")
    return None

def calculate_kimchi_premium(symbol: str, binance_price_usdt: float):
    """김치 프리미엄 계산 (%)"""
    ex_rate = get_exchange_rate()
    upbit = get_upbit_price(symbol)
    bithumb = get_bithumb_price(symbol)
    
    # 두 거래소 중 데이터가 있는 곳의 평균 또는 업비트 우선
    krw_price = upbit or bithumb
    if not krw_price or binance_price_usdt <= 0:
        return 0.0, ex_rate
    
    base_krw = binance_price_usdt * ex_rate
    premium_pct = (krw_price / base_krw - 1) * 100
    return premium_pct, ex_rate

def convert_krw_to_usdt(krw_amount: float, premium_pct: float, ex_rate: float):
    """국내 평단(KRW)을 김프 제외한 바이낸스 가격(USDT)으로 변환"""
    # krw = usdt * ex_rate * (1 + premium/100)
    # usdt = krw / (ex_rate * (1 + premium/100))
    if ex_rate <= 0: return 0
    return krw_amount / (ex_rate * (1 + premium_pct / 100))

def convert_usdt_to_krw(usdt_amount: float, premium_pct: float, ex_rate: float):
    """바이낸스 목표가(USDT)를 김프 반영한 국내 가격(KRW)으로 변환"""
    return usdt_amount * ex_rate * (1 + premium_pct / 100)

def get_open_positions():
    """현재 열린 포지션 조회 (Binance Futures API)"""
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()

        import ccxt

        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')

        if not api_key or not api_secret:
            logger.error("Binance API 키가 없습니다")
            return []

        # CCXT 바이낸스 선물 클라이언트
        exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })

        # 포지션 정보 조회
        positions = exchange.fetch_positions()

        # 포지션 크기가 0이 아닌 것만 필터링
        open_positions = [p for p in positions if float(p.get('contracts', 0)) != 0]

        return open_positions

    except ImportError:
        logger.error("ccxt 라이브러리 필요: pip install ccxt")
        # Fallback: 거래 기록에서 포지션 추정
        return get_open_positions_from_trades()
    except Exception as e:
        logger.error(f"포지션 조회 실패: {e}")
        return get_open_positions_from_trades()

def get_open_positions_from_trades():
    """거래 기록 파일에서 현재 포지션 추정"""
    try:
        import json

        # completed_trades.json 읽기
        trade_file = 'data/journal/completed_trades.json'
        if not os.path.exists(trade_file):
            return []

        with open(trade_file, 'r', encoding='utf-8') as f:
            trades = json.load(f)

        # exit_type이 없거나 HOLD 상태인 거래 찾기
        open_trades = [t for t in trades if t.get('exit_type') is None]

        positions = []
        for trade in open_trades:
            pos = {
                'symbol': trade.get('symbol', 'UNKNOWN'),
                'positionSide': 'LONG' if trade.get('direction') == 'LONG' else 'SHORT',
                'positionAmt': trade.get('quantity', 0),
                'entryPrice': trade.get('entry_price', 0),
                'markPrice': trade.get('entry_price', 0),  # 정확한 현재가는 API 필요
                'unrealizedProfit': 0,  # 계산 불가
            }
            positions.append(pos)

        return positions

    except Exception as e:
        logger.error(f"거래 기록 파일 읽기 실패: {e}")
        return []
