"""
메인 전략 (15m/4h) 자동 거래 핸들러
스캘핑과 별개로 동시에 작동
"""

import time
import logging
from datetime import datetime
from config.config import TELEGRAM_CHAT_ID, AUTO_TRADE_MIN_CONFIDENCE, MAX_LEVERAGE, MIN_LEVERAGE

logger = logging.getLogger(__name__)


class MainStrategyAutoTrader:
    """메인 전략(15m/4h) 자동 거래 담당"""
    
    def __init__(self, telegram_api, fetcher, strategy):
        self.tg = telegram_api
        self.fetcher = fetcher
        self.strategy = strategy
        self.last_scan_time = 0
        self.scan_interval = 900  # 15분마다 스캔
        
    def scan_main_signals(self, symbols):
        """메인 전략 신호 스캔 (15분마다)"""
        try:
            now = time.time()
            if now - self.last_scan_time < self.scan_interval:
                return
            
            self.last_scan_time = now
            
            for symbol in symbols[:10]:  # 상위 10개만 스캔
                try:
                    # 메인 데이터 수집 (15m/4h/1d)
                    df_entry = self.fetcher.get_klines(symbol, "15m", limit=100)
                    df_higher = self.fetcher.get_klines(symbol, "4h", limit=50)
                    df_daily = self.fetcher.get_klines(symbol, "1d", limit=100)
                    
                    if len(df_entry) < 50:
                        continue
                    
                    # 메인 전략 분석 (Sweepzone V1 포함)
                    analysis = self.strategy.analyze(df_entry, symbol, df_higher, df_1d=df_daily)
                    
                    if (analysis and analysis.signal and 
                        analysis.signal.confidence >= AUTO_TRADE_MIN_CONFIDENCE and
                        symbol not in self._get_active_positions()):
                        
                        logger.info(f"🎯 메인 신호 감지: {symbol} (신뢰도: {analysis.signal.confidence:.0%})")
                        return (symbol, analysis)
                        
                except Exception as e:
                    logger.debug(f"메인 신호 분석 오류 {symbol}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"메인 신호 스캔 오류: {e}")
        
        return None
    
    def _get_active_positions(self):
        """현재 오픈된 포지션 조회"""
        try:
            positions = self.fetcher.get_all_positions()
            return {p['symbol'] for p in positions}
        except:
            return set()


def execute_main_trade(bot, chat_id, symbol, analysis):
    """메인 전략 거래 실행"""
    signal = analysis.signal
    
    try:
        # 포지션 체크
        all_positions = bot.fetcher.get_all_positions()
        if len(all_positions) >= 2:  # 최대 2개 (메인 1 + 스캘핑 1)
            logger.warning(f"⚠️ 최대 포지션 도달")
            return
        
        # 레버리지 설정
        leverage = min(signal.leverage, MAX_LEVERAGE)
        bot.fetcher.set_leverage(symbol, leverage)
        bot.fetcher.set_margin_type(symbol, 'ISOLATED')
        
        # 수량 계산
        current_price = bot.fetcher.get_price(symbol)
        quantity = bot.fetcher.calculate_position_size(
            symbol, current_price, signal.stop_loss, leverage)
        
        if quantity <= 0:
            logger.warning(f"❌ {symbol} 수량 계산 실패")
            return
        
        # 주문 실행
        side = 'BUY' if signal.direction == 'LONG' else 'SELL'
        order = bot.fetcher.place_order(symbol, side, quantity)
        
        if order.get('orderId'):
            actual_entry = float(order.get('avgPrice', current_price) or current_price)
            # 신호 기반 SL/TP 설정
            bot.fetcher.place_stop_loss(symbol, side, signal.stop_loss, quantity)
            bot.fetcher.place_take_profit(symbol, side, signal.take_profit, quantity)
            
            # 메시지 전송
            msg = f"🚀 <b>메인 전략 진입: {symbol}</b>\n"
            msg += f"방향: {signal.direction}\n"
            msg += f"가격: {actual_entry:,.2f}\n"
            msg += f"SL: {signal.stop_loss:,.2f} | TP: {signal.take_profit:,.2f}"
            bot.tg.send_message(chat_id, msg)
            
    except Exception as e:
        logger.error(f"❌ 메인 거래 실행 오류: {e}")
