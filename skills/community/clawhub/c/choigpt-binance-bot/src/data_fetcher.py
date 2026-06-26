"""
바이낸스 선물 데이터 수집 모듈
"""

import time
import hmac
import hashlib
import requests
import pandas as pd
import numpy as np
import copy
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Optional
import logging

from config.config import *

logger = logging.getLogger(__name__)


class BinanceFetcher:
    """바이낸스 선물 데이터 수집"""

    INTERVAL_MAP = {
        '1m': 1, '3m': 3, '5m': 5, '15m': 15, '30m': 30,
        '1h': 60, '2h': 120, '4h': 240, '6h': 360, '8h': 480,
        '12h': 720, '1d': 1440, '3d': 4320, '1w': 10080
    }

    def __init__(self, api_key: str = API_KEY, api_secret: str = API_SECRET,
                 use_testnet: bool = USE_TESTNET):
        self.api_key = api_key
        self.api_secret = api_secret
        self.use_testnet = use_testnet
        self.base_url = "https://fapi.binance.com" if not use_testnet else "https://testnet.binancefuture.com"
        
        # V3.7: 심볼별 정밀도 및 필터 데이터 캐싱
        self.exchange_info = {}
        try:
            self.update_exchange_info()
        except Exception as e:
            logger.warning(f"Exchange info 초기 로드 실패: {e}")

        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/json'
        })
        self.time_offset = 0
        self.last_sync_time = 0
        self.time_sync_interval = 1800  # 30분마다 자동 동기화
        self._sync_time()

    def _sync_time(self):
        """서버 시간과 동기화"""
        try:
            res = requests.get(f"{self.base_url}/fapi/v1/time", timeout=5)
            server_time = res.json()['serverTime']
            local_time = int(time.time() * 1000)
            self.time_offset = server_time - local_time
            self.last_sync_time = time.time()
            logger.info(f"🕒 서버 시간 동기화 완료 (Offset: {self.time_offset}ms)")
        except Exception as e:
            logger.warning(f"⚠️ 서버 시간 동기화 실패: {e}")

    def normalize_symbol(self, symbol: str) -> Optional[str]:
        """심볼 포맷 정규화 (예: SOL -> SOLUSDT) - V3.1: 비표준 문자 스킵"""
        import re
        if not symbol or not isinstance(symbol, str):
            return None
            
        s = symbol.upper().strip()
        # 영문/숫자 외의 문자가 포함된 경우(중국어 등) 에러 대신 스킵(None)
        if not re.match(r'^[A-Z0-9]+$', s):
            logger.warning(f"⚠️ 비표준 심볼 감지 ({s}) - 브리핑 리스트에서 제외합니다.")
            return None
            
        if not s.endswith('USDT'):
            return f"{s}USDT"
        return s

    def _sign(self, params: dict) -> OrderedDict:
        """API 서명 (OrderedDict를 사용하여 순서 보장)"""
        p = OrderedDict()
        for k, v in params.items():
            p[k] = v
            
        # 가동 시간 체크하여 주기적 동기화
        if time.time() - self.last_sync_time > self.time_sync_interval:
            self._sync_time()
            
        p['timestamp'] = int(time.time() * 1000) + self.time_offset
        p['recvWindow'] = 10000
        
        query = '&'.join([f"{k}={v}" for k, v in p.items()])
        signature = hmac.new(
            self.api_secret.encode(), query.encode(), hashlib.sha256
        ).hexdigest()
        p['signature'] = signature
        return p

    def _get(self, endpoint: str, params: dict = None, signed: bool = False, timeout: int = 15, retry_count: int = 0):
        """GET 요청"""
        # 원본 보존을 위해 딥카피 사용
        req_params = copy.deepcopy(params) if params else {}
        
        if signed:
            req_params = self._sign(req_params)
        
        response = None
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=req_params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout as e:
            logger.error(f"API GET 타임아웃 ({timeout}s): {endpoint}")
            raise
        except requests.exceptions.HTTPError as e:
            if response is not None:
                try:
                    error_body = response.json()
                    # V5.1.5: 시간 오차 에러(-1021) 발생 시 즉시 동기화 후 재시도
                    if error_body.get('code') == -1021 and retry_count < 2:
                        logger.warning(f"🕒 시간 오차 감지 (-1021) -> 복구 중... (시도 {retry_count+1}/2)")
                        self._sync_time()
                        return self._get(endpoint, params, signed, timeout, retry_count + 1)
                    
                    # -4046 같은 예상된 에러는 WARNING으로 처리
                    if error_body.get('code') == -4046:
                        logger.debug(f"ℹ️ {endpoint}: {error_body.get('msg')}")
                    else:
                        logger.error(f"API GET 실패 ({response.status_code}): {error_body}")
                except (ValueError, AttributeError):
                    logger.error(f"API GET 실패 ({response.status_code}): {response.text}")
            else:
                logger.error(f"API GET 실패: {e}")
            raise
        except Exception as e:
            logger.error(f"API GET 예상 외 오류: {e}")
            raise

    def _post(self, endpoint: str, params: dict = None, timeout: int = 20, retry_count: int = 0):
        """POST 요청"""
        req_params = copy.deepcopy(params) if params else {}
        req_params = self._sign(req_params)
        
        response = None
        try:
            response = self.session.post(f"{self.base_url}{endpoint}", data=req_params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout as e:
            logger.error(f"API POST 타임아웃 ({timeout}s): {endpoint}")
            raise
        except requests.exceptions.HTTPError as e:
            if response is not None:
                try:
                    error_body = response.json()
                    if error_body.get('code') == -1021 and retry_count < 2:
                        logger.warning(f"🕒 시간 오차 감지 (-1021) -> 복구 중... (시도 {retry_count+1}/2)")
                        self._sync_time()
                        return self._post(endpoint, params, timeout, retry_count + 1)
                    
                    # -4046 (마진 타입 이미 설정됨) 등은 무시
                    if error_body.get('code') == -4046:
                        logger.debug(f"ℹ️ {endpoint}: {error_body.get('msg')}")
                    else:
                        logger.error(f"API POST 실패 ({response.status_code}): {error_body}")
                except (ValueError, AttributeError):
                    logger.error(f"API POST 실패 ({response.status_code}): {response.text}")
            else:
                logger.error(f"API POST 실패: {e}")
            raise
        except Exception as e:
            logger.error(f"API POST 예상 외 오류: {e}")
            raise

    def _delete(self, endpoint: str, params: dict = None, timeout: int = 20):
        """DELETE 요청 (V3.8 추가)"""
        if params is None:
            params = {}
        params = self._sign(params)
        response = None
        try:
            # DELETE는 종종 쿼리 스트링으로 파라미터를 보냄
            response = self.session.delete(f"{self.base_url}{endpoint}", params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response is not None:
                try:
                    error_body = response.json()
                    logger.error(f"API DELETE 실패 ({response.status_code}): {error_body}")
                except:
                    logger.error(f"API DELETE 실패 ({response.status_code}): {response.text}")
            else:
                logger.error(f"API DELETE 실패: {e}")
            raise
        except Exception as e:
            logger.error(f"API DELETE 요청 중 오류: {e}")
            raise

    # ──────────────────────────────────────────────
    # 마켓 정보 및 정밀도 관리 (V3.7)
    # ──────────────────────────────────────────────

    def update_exchange_info(self):
        """바이낸스 선물 마켓 정보(정밀도, 필터 등) 업데이트"""
        try:
            url = f"{self.base_url}/fapi/v1/exchangeInfo"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            for s in data['symbols']:
                symbol = s['symbol']
                # LOT_SIZE 필터에서 stepSize 추출
                lot_size_filter = next((f for f in s['filters'] if f['filterType'] == 'LOT_SIZE'), None)
                # PRICE_FILTER 필터에서 tickSize 추출
                price_filter = next((f for f in s['filters'] if f['filterType'] == 'PRICE_FILTER'), None)
                
                self.exchange_info[symbol] = {
                    'status': s['status'],
                    'baseAsset': s['baseAsset'],
                    'quantityPrecision': s['quantityPrecision'],
                    'pricePrecision': s['pricePrecision'],
                    'tickSize': float(price_filter['tickSize']) if price_filter else 0.0,
                    'stepSize': float(lot_size_filter['stepSize']) if lot_size_filter else 1.0,
                    'minQty': float(lot_size_filter['minQty']) if lot_size_filter else 0.0,
                }
            logger.info(f"✅ Exchange Info 업데이트 완료 ({len(self.exchange_info)}개 심볼)")
        except Exception as e:
            logger.error(f"Exchange Info 업데이트 실패: {e}")

    def _round_quantity(self, symbol, quantity):
        """심볼별 stepSize에 맞춰 수량 반올림/버림"""
        try:
            import math
            if symbol not in self.exchange_info:
                # ★ V5.5: 원본 수량 반환 (int() 변환 제거 - 0으로 변환되는 버그 수정)
                logger.debug(f"⚠️ {symbol}: Exchange info 없음 - 원본 수량 반환 ({quantity})")
                return quantity

            info = self.exchange_info[symbol]
            step_size = info['stepSize']
            precision = info['quantityPrecision']

            # stepSize 기반 라운딩
            rounded_qty = math.floor(quantity / step_size) * step_size

            # 부동소수점 오차 방지
            fmt = f"{{:.{precision}f}}"
            return float(fmt.format(rounded_qty))
        except Exception as e:
            logger.error(f"수량 정밀도 계산 오류 ({symbol}): {e}")
            return round(quantity, 1)

    def _round_price(self, symbol, price):
        """심볼별 tickSize에 맞춰 가격 반올림 (V5.2.6: -4014 에러 방지)"""
        try:
            if symbol not in self.exchange_info:
                return round(price, 4)
            
            info = self.exchange_info[symbol]
            tick_size = info.get('tickSize', 0.0)
            precision = info.get('pricePrecision', 4)

            if tick_size > 0:
                # tickSize의 배수로 반올림
                rounded_price = round(price / tick_size) * tick_size
                # 부동소수점 오차 방지를 위해 precision만큼 포맷팅
                fmt = f"{{:.{precision}f}}"
                return float(fmt.format(rounded_price))
            else:
                return round(price, precision)
        except Exception as e:
            logger.error(f"가격 정밀도 계산 오류 ({symbol}): {e}")
            return round(price, 4)

    def get_klines(self, symbol: str, interval: str, limit: int = 500,
                   start_time: Optional[datetime] = None,
                   end_time: Optional[datetime] = None) -> pd.DataFrame:
        """캔들스틱 데이터 수집 - V3.1: 심볼 오류 시 빈 DF 반환"""
        symbol = self.normalize_symbol(symbol)
        if not symbol:
            return pd.DataFrame()
            
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        if start_time:
            params['startTime'] = int(start_time.timestamp() * 1000)
        if end_time:
            params['endTime'] = int(end_time.timestamp() * 1000)

        data = self._get('/fapi/v1/klines', params)

        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ])

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col])

        return df[['open', 'high', 'low', 'close', 'volume']]

    def get_historical_klines(self, symbol: str, interval: str,
                               start: str, end: str = None) -> pd.DataFrame:
        """대량 과거 데이터 수집 (백테스트용)"""
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end) if end else datetime.utcnow()

        all_data = []
        current_start = start_dt
        interval_minutes = self.INTERVAL_MAP.get(interval, 15)

        while current_start < end_dt:
            current_end = min(current_start + timedelta(minutes=interval_minutes * 1500), end_dt)

            try:
                df = self.get_klines(symbol, interval, limit=1500,
                                     start_time=current_start, end_time=current_end)
                if len(df) == 0:
                    break
                all_data.append(df)
                current_start = df.index[-1] + timedelta(minutes=interval_minutes)
                time.sleep(0.1)  # API 레이트 제한 방지
            except Exception as e:
                logger.error(f"데이터 수집 실패 {current_start}: {e}")
                time.sleep(1)
                continue

        if all_data:
            result = pd.concat(all_data)
            result = result[~result.index.duplicated(keep='first')]
            return result.sort_index()

        return pd.DataFrame()

    def get_account_balance(self) -> dict:
        """선물 계좌 잔고 조회"""
        data = self._get('/fapi/v2/account', signed=True)
        balances = {}
        for asset in data.get('assets', []):
            if float(asset['walletBalance']) > 0:
                balances[asset['asset']] = {
                    'wallet': float(asset['walletBalance']),
                    'unrealized_pnl': float(asset['unrealizedProfit']),
                    'available': float(asset['availableBalance'])
                }
        return balances

    def get_position(self, symbol: str) -> Optional[dict]:
        """현재 포지션 조회"""
        data = self._get('/fapi/v2/positionRisk', {'symbol': symbol}, signed=True)
        for pos in data:
            if pos['symbol'] == symbol and float(pos['positionAmt']) != 0:
                return {
                    'symbol': symbol,
                    'side': 'LONG' if float(pos['positionAmt']) > 0 else 'SHORT',
                    'size': abs(float(pos['positionAmt'])),
                    'entry_price': float(pos['entryPrice']),
                    'unrealized_pnl': float(pos['unRealizedProfit']),
                    'leverage': float(pos['leverage'])
                }
        return None

    def get_all_positions(self) -> list:
        """모든 오픈 포지션 조회"""
        data = self._get('/fapi/v2/positionRisk', signed=True)
        positions = []
        for pos in data:
            if float(pos['positionAmt']) != 0:
                positions.append({
                    'symbol': pos['symbol'],
                    'side': 'LONG' if float(pos['positionAmt']) > 0 else 'SHORT',
                    'size': abs(float(pos['positionAmt'])),
                    'entry_price': float(pos['entryPrice']),
                    'unrealized_pnl': float(pos['unRealizedProfit']),
                    'leverage': float(pos['leverage']),
                    'mark_price': float(pos['markPrice'])
                })
        return positions

    def set_leverage(self, symbol: str, leverage: int) -> dict:
        """레버리지 설정"""
        return self._post('/fapi/v1/leverage', {
            'symbol': symbol,
            'leverage': leverage
        })

    def set_margin_type(self, symbol: str, margin_type: str = 'ISOLATED') -> dict:
        """마진 모드 설정 (ISOLATED/CROSSED)"""
        symbol = self.normalize_symbol(symbol)
        params = {
            'symbol': symbol,
            'marginType': margin_type.upper()
        }
        try:
            res = self._post('/fapi/v1/marginType', params)
            return res
        except Exception as e:
            # ★ V3.3 FIX: "No need to change" 에러(400)는 에러가 아닌 정보성으로 처리
            err_msg = str(e).upper()
            if "NO NEED TO CHANGE" in err_msg or "-4046" in err_msg:
                logger.debug(f"ℹ️ {symbol}: 마진 모드가 이미 {margin_type}입니다.")
                return {"msg": "No need to change"}
            
            logger.error(f"❌ {symbol} 마진 모드 설정 실패: {e}")
            return {}

    def set_leverage(self, symbol: str, leverage: int) -> dict:
        """레버리지 설정"""
        symbol = self.normalize_symbol(symbol)
        params = {
            'symbol': symbol,
            'leverage': int(leverage)
        }
        try:
            return self._post('/fapi/v1/leverage', params)
        except Exception as e:
            logger.error(f"❌ {symbol} 레버리지 설정 실패: {e}")
            return {}


    def place_order(self, symbol: str, side: str, quantity: float,
                    order_type: str = 'MARKET', price: float = None,
                    stop_price: float = None, reduce_only: bool = False) -> dict:
        """주문 실행"""
        # ★ 수량을 심볼별 정밀도에 맞춰 반올림 (V3.8: Precision Fix)
        quantity = self._round_quantity(symbol, quantity)
        logger.debug(f"📊 {symbol} 수량 정밀도 적용: {quantity}")

        # ★ V3.9: 과학 기호법 방지 (예: 1.23E-4 → 0.000123)
        qty_str = f"{quantity:.8f}".rstrip('0').rstrip('.')

        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': float(qty_str),  # 문자열을 다시 float로 변환 (Binance API 호환)
        }
        if price:
            params['price'] = price

        if stop_price:
            params['stopPrice'] = stop_price

        if reduce_only:
            params['reduceOnly'] = True  # Boolean, not string

        # ★ STOP/TAKE_PROFIT 주문에는 timeInForce 필수!
        if order_type in ['LIMIT', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET']:
            params['timeInForce'] = 'GTC'  # Good 'til Canceled

        return self._post('/fapi/v1/order', params)

    def place_limit_order_with_fallback(self, symbol: str, side: str, quantity: float,
                                        current_price: float, offset_pct: float = 0.03,
                                        timeout_sec: int = 8) -> dict:
        """지정가(Maker) 주문 후 미체결 시 시장가 폴백 (★ V5.5: 수수료 절감)

        - LONG(BUY):  현재가보다 offset_pct% 낮게 지정가 → Maker 수수료(-0.02%)
        - SHORT(SELL): 현재가보다 offset_pct% 높게 지정가 → Maker 수수료(-0.02%)
        - timeout_sec 내 미체결 → 취소 후 시장가(Taker 0.05%) 폴백
        """
        order_id = None
        try:
            # 지정가 계산
            if side == 'BUY':
                limit_price = current_price * (1 - offset_pct / 100)
            else:
                limit_price = current_price * (1 + offset_pct / 100)
            limit_price = self._round_price(symbol, limit_price)

            logger.info(f"📋 {symbol} 지정가 시도: {side} @ {limit_price:.6g} (현재가: {current_price:.6g}, offset: {offset_pct}%)")

            # 지정가 주문 실행
            limit_order = self.place_order(symbol, side, quantity,
                                           order_type='LIMIT', price=limit_price)

            if not limit_order or not limit_order.get('orderId'):
                logger.warning(f"⚠️ {symbol} 지정가 주문 실패 → 시장가 폴백")
                return self.place_order(symbol, side, quantity)

            order_id = limit_order['orderId']

            # 즉시 체결 확인 (LIMIT이 이미 채워진 경우)
            if limit_order.get('status') == 'FILLED':
                logger.info(f"✅ {symbol} 지정가 즉시 체결! (Maker) @ {limit_order.get('avgPrice', limit_price)}")
                return limit_order

            # 체결 대기 (polling)
            for i in range(timeout_sec):
                time.sleep(1)
                try:
                    status = self._get('/fapi/v1/order',
                                       {'symbol': symbol, 'orderId': order_id},
                                       signed=True)
                    order_status = status.get('status', '')

                    if order_status == 'FILLED':
                        logger.info(f"✅ {symbol} 지정가 체결! (Maker 수수료) @ {status.get('avgPrice', limit_price)}")
                        return status
                    elif order_status in ['CANCELED', 'EXPIRED', 'REJECTED']:
                        logger.warning(f"⚠️ {symbol} 지정가 주문 {order_status} → 시장가 폴백")
                        order_id = None
                        return self.place_order(symbol, side, quantity)

                    logger.debug(f"⏳ {symbol} 지정가 대기 중... ({i+1}s/{timeout_sec}s) 상태: {order_status}")
                except Exception as se:
                    logger.debug(f"주문 상태 조회 오류 (무시): {se}")

            # 타임아웃 → 취소 후 시장가 폴백
            logger.warning(f"⏰ {symbol} 지정가 {timeout_sec}초 미체결 → 취소 후 시장가 폴백")
            try:
                self._delete('/fapi/v1/order', {'symbol': symbol, 'orderId': order_id})
                order_id = None
                logger.info(f"🗑️ {symbol} 지정가 주문 취소 완료")
            except Exception as ce:
                logger.warning(f"지정가 취소 실패 (무시): {ce}")

            market_order = self.place_order(symbol, side, quantity)
            if market_order:
                status = market_order.get('status')
                if status:
                    logger.info(f"🔄 {symbol} 시장가 폴백 완료 @ {market_order.get('avgPrice', current_price)} (상태: {status})")
                else:
                    logger.info(f"🔄 {symbol} 시장가 폴백 응답 (status 누락됨) @ {current_price}")
                return market_order
            else:
                logger.error(f"❌ {symbol} 시장가 폴백 실패: place_order가 처리 가능한 응답을 반환하지 않음.")
                return None

        except Exception as e:
            logger.error(f"❌ {symbol} 지정가 주문 오류: {e} → 시장가 폴백 시도")
            # 미취소 주문이 남아있으면 정리 시도
            if order_id:
                try:
                    self._delete('/fapi/v1/order', {'symbol': symbol, 'orderId': order_id})
                except Exception:
                    pass
            fallback_order = self.place_order(symbol, side, quantity)
            if not fallback_order:
                logger.error(f"❌ {symbol} 2차 시장가 폴백마저 실패함.")
            return fallback_order

    def place_sl_tp_orders(self, symbol: str, position_side: str,
                           quantity: float, sl_price: float, tp_price: float,
                           tp_price2: float = None, tp1_ratio: float = 0.5):
        """스탑로스 + 테이크프로핏 (분할 가능) 설정

        ★ V4.5.7: Binance Algo Order API - 가격 정밀도 수정 (-1111 에러 방지)
        - 2025-12-09 Binance 마이그레이션: 조건부 주문 → Algo Service
        - 엔드포인트: /fapi/v1/algoOrder (단수! algoOrders 아님!)
        - algoType: 'CONDITIONAL' (V4.5.5에서 추가 완료)
        - triggerPrice: stopPrice 아님! (V4.5.6에서 수정 완료)
        - _round_price(): pricePrecision에 맞춰 가격 반올림 ← V4.5.7 핵심!
          예) DOGEUSDT TP2=0.09266542857142862 → 0.09267 (5자리)
        - Response: algoId (orderId 아님)
        - 포지션 진입 후 1초 지연 (포지션 완전 확립 대기)
        """
        import logging
        logger = logging.getLogger(__name__)

        # ★ SL/TP 수량도 정밀도에 맞춰 반올림 (V3.8)
        quantity = self._round_quantity(symbol, quantity)

        # ★ V4.5.7: 가격도 pricePrecision에 맞춰 반올림 (-1111 에러 방지)
        sl_price = self._round_price(symbol, sl_price)
        tp_price = self._round_price(symbol, tp_price)
        if tp_price2:
            tp_price2 = self._round_price(symbol, tp_price2)

        # ★ V6.1: TP/SL 가격 유효성 검증 (TP가 0이어도 SL은 등록하도록 수정)
        if position_side == 'LONG':
            if sl_price <= 0:
                logger.error(f"❌ {symbol} LONG: SL 오류 - SL={sl_price} 필수")
                return None, []
            if tp_price > 0 and tp_price <= sl_price:
                logger.warning(f"⚠️ {symbol} LONG: TP({tp_price})가 SL({sl_price})보다 낮아 TP 설정을 생략합니다.")
                tp_price, tp_price2 = 0.0, 0.0
            if tp_price2 > 0 and tp_price2 <= tp_price:
                tp_price2 = 0.0
        else:  # SHORT
            if sl_price <= 0:
                logger.error(f"❌ {symbol} SHORT: SL 오류 - SL={sl_price} 필수")
                return None, []
            if tp_price > 0 and tp_price >= sl_price:
                logger.warning(f"⚠️ {symbol} SHORT: TP({tp_price})가 SL({sl_price})보다 높아 TP 설정을 생략합니다.")
                tp_price, tp_price2 = 0.0, 0.0
            if tp_price2 > 0 and tp_price2 >= tp_price:
                tp_price2 = 0.0

        close_side = 'SELL' if position_side == 'LONG' else 'BUY'

        logger.info(f"🔧 {symbol} SL/TP 설정 시도 (Algo Order V5.4): SL={sl_price}, TP={tp_price}, TP2={tp_price2}")

        # ★ 포지션이 완전히 확립되도록 1초 대기
        time.sleep(1)

        # 1. 손절 (전량) - STOP_MARKET via Algo Order API
        sl_order = None
        try:
            params = {
                'symbol': symbol,
                'side': close_side,
                'algoType': 'CONDITIONAL',         # ★ 조건부 주문 타입
                'type': 'STOP_MARKET',             # ★ 주문 타입
                'triggerPrice': sl_price,           # ★ V4.5.6: stopPrice → triggerPrice!
                'quantity': quantity,               # ★ 전체 수량
                'reduceOnly': 'true',              # ★ 포지션 청산 전용
            }
            sl_response = self._post('/fapi/v1/algoOrder', params)  # ★ 단수형! (algoOrders 아님)
            if sl_response and (sl_response.get('algoId') or sl_response.get('orderId')):
                algo_id = sl_response.get('algoId') or sl_response.get('orderId')
                logger.info(f"✅ {symbol} 손절 주문 성공: AlgoID={algo_id}, Price={sl_price:.4f}")
                sl_order = sl_response
            else:
                logger.error(f"❌ {symbol} 손절 주문 응답 오류: {sl_response}")
                sl_order = None
        except Exception as e:
            logger.error(f"❌ {symbol} 손절 주문 실패: {e}")
            sl_order = None

        tp_orders = []
        if tp_price2:
            # 2. 1차 익절 - TAKE_PROFIT_MARKET via Algo Order API
            qty1 = self._round_quantity(symbol, quantity * tp1_ratio)
            try:
                params = {
                    'symbol': symbol,
                    'side': close_side,
                    'algoType': 'CONDITIONAL',         # ★ 조건부 주문 타입
                    'type': 'TAKE_PROFIT_MARKET',      # ★ 주문 타입
                    'triggerPrice': tp_price,           # ★ V4.5.6: stopPrice → triggerPrice!
                    'quantity': qty1,                   # ★ 1차 익절 수량
                    'reduceOnly': 'true',              # ★ 포지션 청산 전용
                }
                tp_response1 = self._post('/fapi/v1/algoOrder', params)  # ★ 단수형!
                if tp_response1 and (tp_response1.get('algoId') or tp_response1.get('orderId')):
                    algo_id = tp_response1.get('algoId') or tp_response1.get('orderId')
                    logger.info(f"✅ {symbol} 익절1 주문 성공: AlgoID={algo_id}, Price={tp_price:.4f}, Qty={qty1}")
                    tp_orders.append(tp_response1)
                else:
                    logger.error(f"❌ {symbol} 익절1 주문 응답 오류: {tp_response1}")
            except Exception as e:
                logger.error(f"❌ {symbol} 익절1 주문 실패: {e}")

            # 3. 2차 익절 (잔량) - TAKE_PROFIT_MARKET via Algo Order API
            # ★ V5.9.4 버그 픽스: qty1을 반올림한 후 남은 수량이 전체 quantity를 초과하지 않도록 철저히 보완
            qty2_raw = quantity - qty1
            qty2 = self._round_quantity(symbol, qty2_raw)
            # 만약 반올림 오차로 인해 qty1 + qty2 가 원래 quantity를 초과하면 qty2를 조정
            if qty1 + qty2 > quantity:
                qty2 = self._round_quantity(symbol, quantity - qty1 - 0.001) # 안전하게 한틱 차감 (또는 재계산)
            
            # 최종 수량이 0보다 작거나 같으면 2차 익절은 스킵 (먼지 수량 방지)
            if qty2 > 0:
                try:
                    params = {
                        'symbol': symbol,
                        'side': close_side,
                        'algoType': 'CONDITIONAL',         # ★ 조건부 주문 타입
                        'type': 'TAKE_PROFIT_MARKET',      # ★ 주문 타입
                        'triggerPrice': tp_price2,          # ★ V4.5.6: stopPrice → triggerPrice!
                        'quantity': qty2,                   # ★ 2차 익절 수량
                        'reduceOnly': 'true',              # ★ 포지션 청산 전용
                    }
                    tp_response2 = self._post('/fapi/v1/algoOrder', params)  # ★ 단수형!
                    if tp_response2 and (tp_response2.get('algoId') or tp_response2.get('orderId')):
                        algo_id = tp_response2.get('algoId') or tp_response2.get('orderId')
                        logger.info(f"✅ {symbol} 익절2 주문 성공: AlgoID={algo_id}, Price={tp_price2:.4f}, Qty={qty2}")
                        tp_orders.append(tp_response2)
                    else:
                        logger.error(f"❌ {symbol} 익절2 주문 응답 오류: {tp_response2}")
                except Exception as e:
                    logger.error(f"❌ {symbol} 익절2 주문 실패: {e}")
            else:
                logger.warning(f"⚠️ {symbol} 익절2 스킵: 남은 수량(qty2)이 0 이하임 ({qty2})")
        else:
            # 단일 익절 - TAKE_PROFIT_MARKET via Algo Order API
            try:
                params = {
                    'symbol': symbol,
                    'side': close_side,
                    'algoType': 'CONDITIONAL',         # ★ 조건부 주문 타입
                    'type': 'TAKE_PROFIT_MARKET',      # ★ 주문 타입
                    'triggerPrice': tp_price,           # ★ V4.5.6: stopPrice → triggerPrice!
                    'quantity': quantity,               # ★ 전체 수량
                    'reduceOnly': 'true',              # ★ 포지션 청산 전용
                }
                tp_response = self._post('/fapi/v1/algoOrder', params)  # ★ 단수형!
                if tp_response and (tp_response.get('algoId') or tp_response.get('orderId')):
                    algo_id = tp_response.get('algoId') or tp_response.get('orderId')
                    logger.info(f"✅ {symbol} 익절 주문 성공: AlgoID={algo_id}, Price={tp_price:.4f}, Qty={quantity}")
                    tp_orders.append(tp_response)
                else:
                    logger.error(f"❌ {symbol} 익절 주문 응답 오류: {tp_response}")
            except Exception as e:
                logger.error(f"❌ {symbol} 익절 주문 실패: {e}")

        return sl_order, tp_orders

    def cancel_all_orders(self, symbol: str) -> dict:
        """모든 미체결 일반 주문 취소"""
        return self._delete('/fapi/v1/allOpenOrders', {'symbol': symbol})

    def cancel_all_algo_orders(self, symbol: str) -> dict:
        """모든 미체결 알고 주문(TP/SL) 취소 (V5.1: API 호환성 수정)"""
        try:
            # 1. 해당 심볼의 모든 오픈 알고 주문 조회
            open_algos = self.get_all_open_algo_orders()
            symbol_algos = [o for o in open_algos if o['symbol'] == symbol]
            
            if not symbol_algos:
                return {"msg": "No open algo orders for symbol"}

            # 2. 각 주문별로 DELETE 호출
            results = []
            for algo in symbol_algos:
                res = self._delete('/fapi/v1/algoOrder', {
                    'symbol': symbol,
                    'algoId': algo['algoId']
                })
                results.append(res)
            
            return {"status": "success", "cancelled_count": len(results), "details": results}
        except Exception as e:
            logger.warning(f"⚠️ {symbol} 알고 주문 취소 실패: {e}")
            return {}

    def get_all_open_orders(self) -> list:
        """계정의 모든 미체결 일반 주문 조회"""
        return self._get('/fapi/v1/openOrders', {}, signed=True)

    def get_all_open_algo_orders(self) -> list:
        """계정의 모든 미체결 알고 주문(TP/SL) 조회"""
        data = self._get('/fapi/v1/openAlgoOrders', {}, signed=True)
        # ★ 바이낸스 응답이 {"algoOrders": [...]} 형태로 래핑된 경우 처리
        if isinstance(data, dict):
            return data.get('algoOrders', [])
        if isinstance(data, list):
            return data
        return []

    def get_user_trades(self, symbol: str, limit: int = 10) -> list:
        """특정 종목의 사용자 거래 이력 조회"""
        symbol = self.normalize_symbol(symbol)
        return self._get('/fapi/v1/userTrades', {'symbol': symbol, 'limit': limit}, signed=True)

    def get_income_history(self, symbol: str = None, income_type: str = "REALIZED_PNL", limit: int = 10) -> list:
        """계정 수익 이력 조회 (기본값: 실현 손익)"""
        params = {'incomeType': income_type, 'limit': limit}
        if symbol:
            params['symbol'] = self.normalize_symbol(symbol)
        return self._get('/fapi/v1/income', params, signed=True)

    def get_ticker(self, symbol: str) -> dict:
        """심볼의 24시간 티커 정보 조회 - V3.1: 심볼 오류 시 빈 dict 반환"""
        symbol = self.normalize_symbol(symbol)
        if not symbol:
            return {}
        return self._get('/fapi/v1/ticker/24hr', {'symbol': symbol})

    def get_price(self, symbol: str) -> float:
        """현재가 조회"""
        symbol = self.normalize_symbol(symbol)
        if not symbol:
            return 0.0
        data = self._get('/fapi/v1/ticker/price', {'symbol': symbol})
        return float(data['price'])

    def calculate_position_size(self, symbol: str, entry_price: float,
                                 stop_loss: float, leverage: int,
                                 risk_pct: float = RISK_PER_TRADE) -> float:
        """포지션 사이즈 계산 (V6.2 - 고정 증거금 50 USDT 방식)"""
        try:
            # ★ V5.5: 심볼 정규화 추가 (exchange_info 매칭 보장)
            symbol = self.normalize_symbol(symbol)

            # 실제 잔고 조회 (안전 장치용)
            try:
                balance_info = self.get_account_balance()
                usdt_balance = float(balance_info.get('USDT', {}).get('wallet', 50.0))
                if usdt_balance <= 0:
                    usdt_balance = 50.0
            except Exception:
                usdt_balance = 50.0

            # ★ V6.2: 고정 증거금(Margin) 방식
            # 진입 시 무조건 50 USDT를 증거금으로 사용
            usdt_margin = float(MIN_POSITION_USDT)
            
            # 포지션 크기 (Notional) = 증거금 * 레버리지
            notional_size = usdt_margin * leverage

            # 수량 = Notional / 현재가
            quantity = notional_size / entry_price

            # 최대 포지션 제한 적용 (설정값이 0보다 클 때만)
            if MAX_POSITION_SIZE > 0:
                max_notional = usdt_balance * leverage * (MAX_POSITION_SIZE / 100)
                max_quantity = max_notional / entry_price
                quantity = min(quantity, max_quantity)

            # 정밀도 반올림
            quantity = self._round_quantity(symbol, quantity)

            # 최소 수량 필터 및 보강 (V5.2.3: -4003 에러 방지)
            if symbol in self.exchange_info:
                min_qty = self.exchange_info[symbol]['minQty']
                if quantity < min_qty:
                    # 계산 수량이 최소 미만이면, 최소 수량(min_qty)으로 주문 시 위험도 체크
                    new_notional = min_qty * entry_price
                    # ★ V5.4: 허용 비중을 30%로 낮춤
                    max_allowed_notional = usdt_balance * leverage * 0.30
                    if new_notional <= max_allowed_notional:
                        logger.info(f"🔄 {symbol}: 수량 상향 ({quantity:.8f} -> {min_qty:.8f}) - 최소 단위 준수")
                        quantity = min_qty
                    else:
                        # 최소 수량도 안 되면, 절반 비중으로라도 주문
                        fallback_quantity = (usdt_balance * leverage * 0.15) / entry_price
                        fallback_quantity = self._round_quantity(symbol, fallback_quantity)
                        if fallback_quantity >= min_qty:
                            logger.info(f"🔄 {symbol}: 수량 재조정 ({min_qty:.8f} → {fallback_quantity:.8f}, notional 15%)")
                            quantity = fallback_quantity
                        else:
                            logger.warning(f"⚠️ {symbol}: 최소 수량 불가능 - 계산된 수량={quantity:.8f}, 최소={min_qty:.8f}")
                            return 0

            logger.info(f"📐 {symbol} 포지션 사이즈: {leverage}x, Margin={usdt_margin}$, Notional={quantity*entry_price:.1f}$, qty={quantity}")
            return quantity

        except Exception as e:
            logger.error(f"포지션 사이즈 계산 실패: {e}")
            return 0
    def get_top_symbols(self, limit: int = 50) -> list:
        """거래량 기준 상위 심볼 조회"""
        try:
            url = f"{self.base_url}/fapi/v1/ticker/24hr"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()

            df = pd.DataFrame(data)
            df['quoteVolume'] = pd.to_numeric(df['quoteVolume'])

            # 거래 가능(TRADING) 상태인 USDT 쌍만 필터링
            df = df[df['symbol'].str.endswith('USDT')]

            # ★ V4.2: 제외 목록 필터링
            from config.config import EXCLUDED_SYMBOLS, MIN_24H_VOLUME_USDT
            if EXCLUDED_SYMBOLS:
                df = df[~df['symbol'].isin(EXCLUDED_SYMBOLS)]

            # ★ V6.2: 거래량 최소값 필터 (저유동성 종목 차단)
            df = df[df['quoteVolume'] >= MIN_24H_VOLUME_USDT]

            # 캐싱된 정보가 있다면 TRADING 상태 체크
            if self.exchange_info:
                df = df[df['symbol'].map(lambda x: self.exchange_info.get(x, {}).get('status') == 'TRADING')]

            # 거래량 순 정렬
            top_df = df.sort_values(by='quoteVolume', ascending=False).head(limit)
            return top_df['symbol'].tolist()
        except Exception as e:
            logger.error(f"상위 심볼 조회 실패: {e}")
            return SYMBOLS # 실패 시 기본 고정 리스트 반환

    def get_order_book(self, symbol: str, limit: int = 50) -> dict:
        """
        ★ V7.7: 호가창(Level 2) 데이터 조회 및 불균형(Imbalance) 계산
        - 반환값: {'imbalance_ratio': float, 'bids_vol': float, 'asks_vol': float}
        - imbalance_ratio > 1.0 : 매수 극우위
        - imbalance_ratio < 1.0 : 매도 극우위
        """
        try:
            symbol = self.normalize_symbol(symbol)
            data = self._get('/fapi/v1/depth', {'symbol': symbol, 'limit': limit})
            
            bids = data.get('bids', [])
            asks = data.get('asks', [])
            
            # 수량(Qty) 기준 총합 계산
            bids_vol = sum(float(qty) for _, qty in bids)
            asks_vol = sum(float(qty) for _, qty in asks)
            
            imbalance = bids_vol / max(asks_vol, 1e-8)
            
            return {
                'imbalance_ratio': imbalance,
                'bids_vol': bids_vol,
                'asks_vol': asks_vol
            }
        except Exception as e:
            logger.error(f"호가창 조회 실패 ({symbol}): {e}")
            return {'imbalance_ratio': 1.0, 'bids_vol': 0.0, 'asks_vol': 0.0}
