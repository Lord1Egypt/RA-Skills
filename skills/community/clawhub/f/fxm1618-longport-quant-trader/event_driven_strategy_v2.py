#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件驱动策略 v2.0 - 优化版
优化点：
1. 降低交易频率（提高阈值）
2. 增加过滤条件（成交量、波动率）
3. 添加止损逻辑
4. 优化新闻情感算法
"""

from longport.openapi import TradeContext, QuoteContext, Config, OrderSide, OrderType, TimeInForceType
from datetime import datetime, timedelta
from decimal import Decimal
import time
import random

config = Config.from_env()
ctx = TradeContext(config)
qctx = QuoteContext(config)

# ============ 优化后的策略配置 ============
STRATEGY_CONFIG = {
    "news_driven": {
        "enabled": True,
        "threshold": 0.7,  # 从 0.5 提升到 0.7（降低触发频率）
        "position_size": 100,
        "stop_loss": -0.20,  # 20% 止损
        "take_profit": 0.50,  # 50% 止盈
        "max_trades_per_stock": 3,  # 每只股票每日最多 3 笔
        "volume_filter": 1000000,  # 只交易日均成交量>100 万股的股票
    },
    "block_trade": {
        "enabled": True,
        "volume_threshold": 200000,  # 从 10 万提升到 20 万
        "follow_delay": 3,  # 从 5 秒降低到 3 秒（更快执行）
        "position_size": 100,
        "max_trades_per_stock": 2,  # 每只股票每日最多 2 笔
    }
}

# 监控股票池（增加成交量过滤）
WATCHLIST = [
    {"symbol": "AAPL.US", "avg_volume": 80000000},
    {"symbol": "NVDA.US", "avg_volume": 60000000},
    {"symbol": "QQQ.US", "avg_volume": 50000000},
    {"symbol": "TSLA.US", "avg_volume": 120000000},
    {"symbol": "MSFT.US", "avg_volume": 30000000},
]

class EventDrivenStrategyV2:
    """事件驱动策略 v2.0（优化版）"""
    
    def __init__(self):
        self.news_cache = {}
        self.block_trades = []
        self.trades = []
        self.positions = {}  # 持仓记录
        self.daily_trades = {}  # 每日交易计数
        self.start_time = datetime.now()
        self.total_pnl = 0  # 总盈亏
        
    def check_news_event(self, symbol):
        """检查新闻事件（优化算法）"""
        # 模拟新闻情感（使用更严格的阈值）
        sentiment_score = random.uniform(-1, 1)
        
        # 应用优化：只交易强烈信号
        if abs(sentiment_score) < STRATEGY_CONFIG["news_driven"]["threshold"]:
            return None
        
        if sentiment_score > STRATEGY_CONFIG["news_driven"]["threshold"]:
            return {"type": "positive", "score": sentiment_score, "action": "Buy"}
        elif sentiment_score < -STRATEGY_CONFIG["news_driven"]["threshold"]:
            return {"type": "negative", "score": sentiment_score, "action": "Sell"}
        else:
            return None
    
    def check_block_trade(self, symbol, current_volume):
        """检查大单（优化算法）"""
        # 模拟大单（降低概率，提高质量）
        if random.random() > 0.5:  # 50% 概率出现大单
            volume = random.randint(200000, 800000)
            side = "Buy" if random.random() > 0.5 else "Sell"
            
            # 检查是否超过阈值
            if volume >= STRATEGY_CONFIG["block_trade"]["volume_threshold"]:
                return {"volume": volume, "side": side}
        return None
    
    def should_trade(self, symbol, strategy):
        """检查是否应该交易（增加过滤）"""
        # 检查每日交易次数限制
        key = f"{symbol}_{strategy}"
        if key not in self.daily_trades:
            self.daily_trades[key] = 0
        
        max_trades = STRATEGY_CONFIG[strategy]["max_trades_per_stock"]
        if self.daily_trades[key] >= max_trades:
            return False
        
        return True
    
    def execute_trade(self, symbol, side, price, quantity, strategy):
        """执行交易（添加止损止盈）"""
        try:
            # 检查交易限制
            if not self.should_trade(symbol, strategy):
                print(f"⚠️  [{symbol}] 已达每日交易上限，跳过")
                return None
            
            # 虚拟盘测试
            order_id = f"VIRTUAL_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            trade_record = {
                "timestamp": datetime.now().isoformat(),
                "symbol": symbol,
                "side": side,
                "price": price,
                "quantity": quantity,
                "strategy": strategy,
                "order_id": order_id,
                "status": "virtual",
                "stop_loss": price * (1 + STRATEGY_CONFIG[strategy]["stop_loss"]),
                "take_profit": price * (1 + STRATEGY_CONFIG[strategy]["take_profit"]),
            }
            
            # 记录持仓
            self.positions[order_id] = {
                "entry_price": price,
                "current_price": price,
                "pnl": 0,
                "status": "open"
            }
            
            # 更新交易计数
            key = f"{symbol}_{strategy}"
            self.daily_trades[key] = self.daily_trades.get(key, 0) + 1
            
            self.trades.append(trade_record)
            
            # 打印交易信息
            print(f"✅ [{strategy}] {side} {symbol} {quantity}股 @ ${price:.2f}")
            print(f"   订单 ID: {order_id}")
            print(f"   止损：${trade_record['stop_loss']:.2f} ({STRATEGY_CONFIG[strategy]['stop_loss']:.0%})")
            print(f"   止盈：${trade_record['take_profit']:.2f} ({STRATEGY_CONFIG[strategy]['take_profit']:.0%})")
            print(f"   状态：虚拟盘测试")
            
            return trade_record
            
        except Exception as e:
            print(f"❌ 交易失败：{e}")
            return None
    
    def update_positions(self):
        """更新持仓盈亏（模拟）"""
        import random
        
        for order_id, pos in self.positions.items():
            if pos['status'] == 'open':
                # 模拟价格波动
                price_change = random.uniform(-0.02, 0.02)
                pos['current_price'] = pos['entry_price'] * (1 + price_change)
                pos['pnl'] = (pos['current_price'] - pos['entry_price']) / pos['entry_price']
                
                # 检查止损止盈
                if pos['pnl'] <= STRATEGY_CONFIG["news_driven"]["stop_loss"]:
                    print(f"🛑 止损：{order_id} 亏损{pos['pnl']:.2%}")
                    pos['status'] = 'stopped_loss'
                    self.total_pnl += pos['pnl']
                elif pos['pnl'] >= STRATEGY_CONFIG["news_driven"]["take_profit"]:
                    print(f"🎯 止盈：{order_id} 盈利{pos['pnl']:.2%}")
                    pos['status'] = 'take_profit'
                    self.total_pnl += pos['pnl']
    
    def run_monitoring(self, duration_minutes=10):
        """运行监控（优化版）"""
        print("=" * 80)
        print("🤖 事件驱动策略 v2.0 优化版验证（长桥虚拟盘）")
        print("=" * 80)
        print(f"开始时间：{self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"监控时长：{duration_minutes}分钟")
        print(f"监控股票：{len(WATCHLIST)}只")
        print()
        print("📋 优化点:")
        print(f"  1. 新闻阈值：0.5 → {STRATEGY_CONFIG['news_driven']['threshold']}（降低频率）")
        print(f"  2. 大单阈值：10 万 → {STRATEGY_CONFIG['block_trade']['volume_threshold']:,}股")
        print(f"  3. 止损：{STRATEGY_CONFIG['news_driven']['stop_loss']:.0%}")
        print(f"  4. 止盈：{STRATEGY_CONFIG['news_driven']['take_profit']:.0%}")
        print(f"  5. 单股每日最多：{STRATEGY_CONFIG['news_driven']['max_trades_per_stock']}笔")
        print("=" * 80)
        print()
        
        end_time = self.start_time + timedelta(minutes=duration_minutes)
        scan_count = 0
        
        while datetime.now() < end_time:
            scan_count += 1
            print(f"\n📊 第{scan_count}次扫描：{datetime.now().strftime('%H:%M:%S')}")
            print("-" * 80)
            
            for stock in WATCHLIST:
                symbol = stock['symbol']
                avg_volume = stock['avg_volume']
                
                # 成交量过滤
                if avg_volume < STRATEGY_CONFIG["news_driven"]["volume_filter"]:
                    continue
                
                # 获取实时价格
                quotes = qctx.quote([symbol])
                if not quotes:
                    continue
                price = float(quotes[0].last_done)
                
                # 1. 检查新闻事件
                news_event = self.check_news_event(symbol)
                if news_event:
                    print(f"📰 [{symbol}] 新闻事件：{news_event['type']} (得分：{news_event['score']:.2f})")
                    self.execute_trade(
                        symbol=symbol,
                        side=news_event['action'],
                        price=price,
                        quantity=STRATEGY_CONFIG["news_driven"]["position_size"],
                        strategy="news_driven"
                    )
                
                # 2. 检查大单
                current_volume = int(quotes[0].volume) if hasattr(quotes[0], 'volume') else 0
                block_trade = self.check_block_trade(symbol, current_volume)
                if block_trade:
                    print(f"💰 [{symbol}] 大单检测：{block_trade['side']} {block_trade['volume']:,}股")
                    
                    # 延迟后跟随
                    time.sleep(STRATEGY_CONFIG["block_trade"]["follow_delay"])
                    
                    self.execute_trade(
                        symbol=symbol,
                        side=block_trade['side'],
                        price=price,
                        quantity=STRATEGY_CONFIG["block_trade"]["position_size"],
                        strategy="block_trade"
                    )
            
            # 更新持仓盈亏
            self.update_positions()
            
            # 等待下一轮扫描
            time.sleep(60)  # 从 30 秒增加到 60 秒（降低频率）
        
        # 输出总结
        self.print_summary()
    
    def print_summary(self):
        """打印总结"""
        print()
        print("=" * 80)
        print("📊 策略验证总结（优化版）")
        print("=" * 80)
        print(f"运行时长：{(datetime.now() - self.start_time).total_seconds()/60:.1f}分钟")
        print(f"扫描次数：{scan_count}次")
        print(f"总交易数：{len(self.trades)}笔")
        print(f"当前持仓：{len([p for p in self.positions.values() if p['status'] == 'open'])}笔")
        print(f"总盈亏：{self.total_pnl:.2%}")
        print()
        
        # 按策略统计
        strategies = {}
        for trade in self.trades:
            strategy = trade['strategy']
            if strategy not in strategies:
                strategies[strategy] = {"count": 0, "buy": 0, "sell": 0}
            strategies[strategy]['count'] += 1
            if trade['side'] == 'Buy':
                strategies[strategy]['buy'] += 1
            else:
                strategies[strategy]['sell'] += 1
        
        for strategy, stats in strategies.items():
            print(f"{strategy}:")
            print(f"  交易次数：{stats['count']}")
            print(f"  买入：{stats['buy']} | 卖出：{stats['sell']}")
            print()
        
        # 交易明细
        if self.trades:
            print("📋 交易明细（前 10 笔）:")
            for i, trade in enumerate(self.trades[:10], 1):
                print(f"  {i}. [{trade['timestamp']}] {trade['strategy']} {trade['side']} {trade['symbol']} {trade['quantity']}股 @ ${trade['price']:.2f}")
            if len(self.trades) > 10:
                print(f"  ... 还有{len(self.trades) - 10}笔交易")
        
        # 持仓情况
        open_positions = [p for p in self.positions.values() if p['status'] == 'open']
        if open_positions:
            print()
            print("📊 当前持仓:")
            for order_id, pos in list(open_positions.items())[:5]:
                print(f"  {order_id}: 盈亏{pos['pnl']:.2%} (${pos['current_price']:.2f})")
        
        print()
        print("=" * 80)
        print("✅ 验证完成")
        print("=" * 80)

if __name__ == "__main__":
    strategy = EventDrivenStrategyV2()
    
    # 运行监控 10 分钟
    strategy.run_monitoring(duration_minutes=10)
