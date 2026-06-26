"""
加密货币跨交易所套利监控器
Crypto Arbitrage Monitor - 跨交易所价格差异监控
作者: 小琳 (SmartChain Capital)
"""

import ccxt
import time
import json
import requests
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('arb_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Config:
    """监控配置"""
    EXCHANGES = ['binance', 'okx', 'bybit']
    SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'DOGE/USDT']
    MIN_SPREAD_PERCENT = 0.5  # 最小价差百分比
    TRADING_FEE_PERCENT = 0.1  # 单边手续费
    CHECK_INTERVAL = 60  # 检查间隔(秒)
    
    # 飞书Webhook (需要用户配置)
    FEISHU_WEBHOOK = ""
    
    # Telegram配置 (需要用户配置)
    TELEGRAM_BOT_TOKEN = ""
    TELEGRAM_CHAT_ID = ""


class ExchangeManager:
    """交易所管理器"""
    
    def __init__(self, exchange_ids: List[str]):
        self.exchanges = {}
        for eid in exchange_ids:
            try:
                exchange_class = getattr(ccxt, eid)
                self.exchanges[eid] = exchange_class({
                    'enableRateLimit': True,
                    'timeout': 10000,
                })
                logger.info(f"✅ 交易所 {eid} 初始化成功")
            except Exception as e:
                logger.error(f"❌ 交易所 {eid} 初始化失败: {e}")
    
    def get_ticker(self, exchange_id: str, symbol: str) -> Optional[Dict]:
        """获取交易对行情"""
        try:
            exchange = self.exchanges.get(exchange_id)
            if not exchange:
                return None
            ticker = exchange.fetch_ticker(symbol)
            return {
                'exchange': exchange_id,
                'symbol': symbol,
                'bid': ticker.get('bid'),  # 买一价
                'ask': ticker.get('ask'),  # 卖一价
                'last': ticker.get('last'),  # 最新价
                'volume': ticker.get('baseVolume'),  # 24h成交量
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.warning(f"获取 {exchange_id} {symbol} 行情失败: {e}")
            return None


class ArbitrageAnalyzer:
    """套利分析器"""
    
    def __init__(self, trading_fee: float, min_spread: float):
        self.trading_fee = trading_fee / 100  # 转换为小数
        self.min_spread = min_spread / 100
    
    def find_opportunities(self, tickers: List[Dict]) -> List[Dict]:
        """查找套利机会"""
        opportunities = []
        
        # 按交易对分组
        by_symbol = {}
        for t in tickers:
            if t and t.get('bid') and t.get('ask'):
                sym = t['symbol']
                if sym not in by_symbol:
                    by_symbol[sym] = []
                by_symbol[sym].append(t)
        
        for symbol, exchange_tickers in by_symbol.items():
            if len(exchange_tickers) < 2:
                continue
            
            # 找最低买入价和最高卖出价
            for i, buy_exchange in enumerate(exchange_tickers):
                for j, sell_exchange in enumerate(exchange_tickers):
                    if i >= j:
                        continue
                    
                    buy_price = buy_exchange['ask']  # 在buy_exchange买入
                    sell_price = sell_exchange['bid']  # 在sell_exchange卖出
                    
                    if not buy_price or not sell_price or buy_price <= 0:
                        continue
                    
                    # 计算毛利润率
                    gross_profit = (sell_price - buy_price) / buy_price
                    # 扣除双边手续费
                    net_profit = gross_profit - 2 * self.trading_fee
                    net_profit_percent = net_profit * 100
                    
                    if net_profit_percent >= self.min_spread * 100:
                        opportunity = {
                            'symbol': symbol,
                            'buy_exchange': buy_exchange['exchange'],
                            'sell_exchange': sell_exchange['exchange'],
                            'buy_price': buy_price,
                            'sell_price': sell_price,
                            'spread': sell_price - buy_price,
                            'spread_percent': round(net_profit_percent, 3),
                            'gross_profit_percent': round(gross_profit * 100, 3),
                            'buy_volume': buy_exchange.get('volume'),
                            'sell_volume': sell_exchange.get('volume'),
                            'timestamp': datetime.now().isoformat()
                        }
                        opportunities.append(opportunity)
        
        # 按利润率排序
        opportunities.sort(key=lambda x: x['spread_percent'], reverse=True)
        return opportunities


class AlertSender:
    """预警推送"""
    
    @staticmethod
    def send_feishu(webhook_url: str, opportunities: List[Dict]):
        """发送飞书预警"""
        if not webhook_url:
            return
        
        for opp in opportunities:
            message = {
                "msg_type": "interactive",
                "card": {
                    "header": {
                        "title": {"tag": "plain_text", "content": f"💰 套利机会: {opp['symbol']}"},
                        "template": "green"
                    },
                    "elements": [
                        {
                            "tag": "div",
                            "text": {
                                "tag": "lark_md",
                                "content": (
                                    f"**买入交易所**: {opp['buy_exchange']}\n"
                                    f"**买入价格**: {opp['buy_price']:.2f} USDT\n"
                                    f"**卖出交易所**: {opp['sell_exchange']}\n"
                                    f"**卖出价格**: {opp['sell_price']:.2f} USDT\n"
                                    f"**价差**: {opp['spread']:.2f} USDT\n"
                                    f"**净利润率**: {opp['spread_percent']:.3f}%\n"
                                    f"**时间**: {opp['timestamp']}"
                                )
                            }
                        }
                    ]
                }
            }
            try:
                requests.post(webhook_url, json=message, timeout=5)
                logger.info(f"✅ 飞书预警发送成功: {opp['symbol']}")
            except Exception as e:
                logger.error(f"❌ 飞书预警发送失败: {e}")
    
    @staticmethod
    def send_telegram(bot_token: str, chat_id: str, opportunities: List[Dict]):
        """发送Telegram预警"""
        if not bot_token or not chat_id:
            return
        
        for opp in opportunities:
            text = (
                f"💰 *套利机会*: `{opp['symbol']}`\n\n"
                f"📥 买入: {opp['buy_exchange']} @ {opp['buy_price']:.2f}\n"
                f"📤 卖出: {opp['sell_exchange']} @ {opp['sell_price']:.2f}\n"
                f"📊 净利润率: *{opp['spread_percent']:.3f}%*\n"
                f"⏰ {opp['timestamp']}"
            )
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            try:
                requests.post(url, json={
                    'chat_id': chat_id,
                    'text': text,
                    'parse_mode': 'Markdown'
                }, timeout=5)
                logger.info(f"✅ Telegram预警发送成功: {opp['symbol']}")
            except Exception as e:
                logger.error(f"❌ Telegram预警发送失败: {e}")


class ArbitrageMonitor:
    """套利监控主程序"""
    
    def __init__(self):
        self.exchange_manager = ExchangeManager(Config.EXCHANGES)
        self.analyzer = ArbitrageAnalyzer(Config.TRADING_FEE_PERCENT, Config.MIN_SPREAD_PERCENT)
        self.alert_sender = AlertSender()
        self.opportunities_log = []
    
    def run_once(self) -> List[Dict]:
        """执行一次监控"""
        logger.info("🔍 开始扫描套利机会...")
        
        # 获取所有交易所的所有交易对行情
        all_tickers = []
        for exchange_id in self.exchange_manager.exchanges:
            for symbol in Config.SYMBOLS:
                ticker = self.exchange_manager.get_ticker(exchange_id, symbol)
                if ticker:
                    all_tickers.append(ticker)
                time.sleep(0.1)  # 限速
        
        # 分析套利机会
        opportunities = self.analyzer.find_opportunities(all_tickers)
        
        if opportunities:
            logger.info(f"🎯 发现 {len(opportunities)} 个套利机会!")
            for opp in opportunities:
                logger.info(
                    f"  {opp['symbol']}: {opp['buy_exchange']}({opp['buy_price']:.2f}) → "
                    f"{opp['sell_exchange']}({opp['sell_price']:.2f}) "
                    f"净利润: {opp['spread_percent']:.3f}%"
                )
            
            # 发送预警
            self.alert_sender.send_feishu(Config.FEISHU_WEBHOOK, opportunities)
            self.alert_sender.send_telegram(Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_CHAT_ID, opportunities)
            
            # 记录日志
            self.opportunities_log.extend(opportunities)
        else:
            logger.info("😴 暂无套利机会")
        
        return opportunities
    
    def run_forever(self):
        """持续监控"""
        logger.info("=" * 50)
        logger.info("🚀 加密货币套利监控器启动")
        logger.info(f"📊 监控交易所: {', '.join(Config.EXCHANGES)}")
        logger.info(f"💰 监控币种: {', '.join(Config.SYMBOLS)}")
        logger.info(f"📈 最小价差: {Config.MIN_SPREAD_PERCENT}%")
        logger.info(f"💸 手续费: {Config.TRADING_FEE_PERCENT}%")
        logger.info(f"⏱️ 检查间隔: {Config.CHECK_INTERVAL}秒")
        logger.info("=" * 50)
        
        while True:
            try:
                self.run_once()
                time.sleep(Config.CHECK_INTERVAL)
            except KeyboardInterrupt:
                logger.info("⏹️ 监控已停止")
                break
            except Exception as e:
                logger.error(f"❌ 监控异常: {e}")
                time.sleep(10)


def main():
    """主函数"""
    monitor = ArbitrageMonitor()
    monitor.run_forever()


if __name__ == "__main__":
    main()
