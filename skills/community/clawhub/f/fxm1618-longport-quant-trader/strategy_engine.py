#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化策略引擎 v2.0
整合：技术指标 + 新闻舆情 + 大单监控 + 策略指标
"""

from datetime import datetime
from typing import Dict, List, Optional
import json

# 导入各模块
from hk_stock_strategies import get_stock_quotes, momentum_strategy, mean_reversion_strategy, submit_order
from news_monitor import fetch_news, fetch_stock_news, generate_news_signals, analyze_sentiment
from block_trade_monitor import RealTimeMonitor, detect_block_trade
from strategy_metrics import StrategyHealth, calculate_sharpe_ratio, calculate_max_drawdown
from logger import log_trade, log_signal, log_daily_snapshot
from feishu_push import notify_trade, notify_signal, notify_daily_report

# ============ 配置 ============

STRATEGY_CONFIG = {
    "momentum": {
        "enabled": True,
        "auto_trade": False,
        "min_change_rate": 0.02,
        "position_size": 100,
        "stop_loss": -0.05,
        "take_profit": 0.10,
    },
    "mean_reversion": {
        "enabled": True,
        "auto_trade": True,  # 开启自动交易
        "max_change_rate": -0.03,
        "position_size": 200,
        "stop_loss": -0.03,
        "take_profit": 0.05,
    },
    "news_driven": {
        "enabled": True,
        "auto_trade": False,
        "min_sentiment_score": 0.5,
        "position_size": 100,
    },
    "block_trade_follow": {
        "enabled": True,
        "auto_trade": False,
        "follow_delay_seconds": 5,
        "position_size": 100,
    }
}

WATCHLIST = [
    "700.HK",      # 腾讯
    "9988.HK",     # 阿里
    "3690.HK",     # 美团
    "1211.HK",     # 比亚迪
    "AAPL.US",     # 苹果
    "NVDA.US",     # 英伟达
]

# ============ 策略引擎 ============

class QuantStrategyEngine:
    """量化策略引擎"""
    
    def __init__(self):
        self.strategy_health = {}  # 各策略健康度
        self.positions = {}        # 持仓
        self.trades = []           # 交易记录
        self.signals = []          # 信号
        self.news_cache = {}       # 新闻缓存
        self.block_trade_alerts = []  # 大单提醒
        
        # 初始化策略健康追踪
        for strategy_name in STRATEGY_CONFIG:
            self.strategy_health[strategy_name] = StrategyHealth(strategy_name)
    
    def run_full_analysis(self) -> Dict:
        """运行完整分析"""
        print()
        print("=" * 80)
        print("🤖 量化策略引擎 v2.0 - 完整分析")
        print("=" * 80)
        print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"监控股票：{len(WATCHLIST)} 只")
        print("=" * 80)
        print()
        
        # 1. 获取行情
        print("📊 步骤 1: 获取实时行情")
        print("-" * 80)
        quotes = get_stock_quotes()
        for q in quotes:
            flag = "📈" if q["change_rate"] > 0.02 else "📉" if q["change_rate"] < -0.02 else "➖"
            print(f"{flag} {q['symbol']:12} {q['name']:10} | {q['price']:8.2f} | {q['change_rate']:6.2%}")
        print()
        
        # 2. 技术指标策略
        print("📈 步骤 2: 技术指标策略")
        print("-" * 80)
        tech_signals = self.run_technical_strategies(quotes)
        print(f"生成 {len(tech_signals)} 个技术信号")
        print()
        
        # 3. 新闻舆情分析
        print("📰 步骤 3: 新闻舆情分析")
        print("-" * 80)
        news_signals = self.run_news_analysis()
        print(f"生成 {len(news_signals)} 个新闻信号")
        print()
        
        # 4. 大单监控
        print("💰 步骤 4: 大单监控")
        print("-" * 80)
        block_signals = self.check_block_trades()
        print(f"检测到 {len(block_signals)} 笔大单")
        print()
        
        # 5. 信号汇总与决策
        print("🎯 步骤 5: 信号汇总与决策")
        print("-" * 80)
        all_signals = tech_signals + news_signals + block_signals
        final_signals = self.consolidate_signals(all_signals)
        
        for sig in final_signals:
            emoji = "🟢" if sig['action'] == 'Buy' else "🔴" if sig['action'] == 'Sell' else "⚪"
            print(f"{emoji} {sig['symbol']}: {sig['action']} - {sig['reason'][:50]}...")
        print()
        
        # 6. 执行交易
        print("📤 步骤 6: 执行交易")
        print("-" * 80)
        executed_trades = self.execute_signals(final_signals)
        print(f"执行 {len(executed_trades)} 笔交易")
        print()
        
        # 7. 策略健康度
        print("📊 步骤 7: 策略健康度")
        print("-" * 80)
        health_report = self.get_health_report()
        for strategy_name, health in health_report.items():
            emoji = health.get('status_emoji', '⚪')
            score = health.get('health_score', 0)
            status = health.get('health_status', 'unknown')
            print(f"{emoji} {strategy_name}: {score}分 ({status})")
        print()
        
        print("=" * 80)
        print("✅ 分析完成")
        print("=" * 80)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "quotes": quotes,
            "tech_signals": tech_signals,
            "news_signals": news_signals,
            "block_signals": block_signals,
            "final_signals": final_signals,
            "executed_trades": executed_trades,
            "health_report": health_report
        }
    
    def run_technical_strategies(self, quotes: List[Dict]) -> List[Dict]:
        """运行技术指标策略"""
        signals = []
        
        # 动量策略
        if STRATEGY_CONFIG["momentum"]["enabled"]:
            momentum_stocks = momentum_strategy(quotes)
            for s in momentum_stocks:
                signals.append({
                    "type": "technical",
                    "strategy": "momentum",
                    "symbol": s["symbol"],
                    "action": "Buy",
                    "price": s["price"],
                    "reason": f"动量策略：涨幅{s['change_rate']:.2%}"
                })
        
        # 均值回归
        if STRATEGY_CONFIG["mean_reversion"]["enabled"]:
            mr_stocks = mean_reversion_strategy(quotes)
            for s in mr_stocks:
                signals.append({
                    "type": "technical",
                    "strategy": "mean_reversion",
                    "symbol": s["symbol"],
                    "action": "Buy",
                    "price": s["price"],
                    "reason": f"均值回归：跌幅{s['change_rate']:.2%}"
                })
        
        return signals
    
    def run_news_analysis(self) -> List[Dict]:
        """运行新闻舆情分析"""
        if not STRATEGY_CONFIG["news_driven"]["enabled"]:
            return []
        
        # 抓取股票新闻
        symbols = [s.split(".")[0] for s in WATCHLIST if ".US" in s or ".HK" in s]
        stock_news = fetch_stock_news(symbols, hours=24)
        
        signals = []
        for symbol, news_list in stock_news.items():
            if not news_list:
                continue
            
            # 生成新闻信号
            news_signals = generate_news_signals(news_list)
            for sig in news_signals:
                signals.append({
                    "type": "news",
                    "strategy": "news_driven",
                    "symbol": f"{symbol}.US" if ".US" not in symbol else symbol,
                    "action": sig.get("action", "watch"),
                    "reason": sig.get("reason", ""),
                    "news_count": sig.get("news_count", 0)
                })
        
        return signals
    
    def check_block_trades(self) -> List[Dict]:
        """检查大单"""
        if not STRATEGY_CONFIG["block_trade_follow"]["enabled"]:
            return []
        
        # 简化实现：返回空列表
        # 实际需要实时行情推送
        return self.block_trade_alerts
    
    def consolidate_signals(self, signals: List[Dict]) -> List[Dict]:
        """信号汇总与决策"""
        if not signals:
            return []
        
        # 按股票分组
        from collections import defaultdict
        grouped = defaultdict(list)
        for sig in signals:
            grouped[sig['symbol']].append(sig)
        
        final_signals = []
        for symbol, symbol_signals in grouped.items():
            # 统计买卖信号
            buy_signals = [s for s in symbol_signals if s['action'] == 'Buy']
            sell_signals = [s for s in symbol_signals if s['action'] == 'Sell']
            
            # 多数决
            if len(buy_signals) >= 2:
                final_signals.append({
                    "symbol": symbol,
                    "action": "Buy",
                    "confidence": len(buy_signals) / len(symbol_signals),
                    "reason": f"{len(buy_signals)}个信号看涨",
                    "signals": symbol_signals
                })
            elif len(sell_signals) >= 2:
                final_signals.append({
                    "symbol": symbol,
                    "action": "Sell",
                    "confidence": len(sell_signals) / len(symbol_signals),
                    "reason": f"{len(sell_signals)}个信号看跌",
                    "signals": symbol_signals
                })
        
        return final_signals
    
    def execute_signals(self, signals: List[Dict]) -> List[Dict]:
        """执行信号"""
        executed = []
        
        for signal in signals:
            strategy = signal.get('strategy', 'unknown')
            config = STRATEGY_CONFIG.get(strategy, {})
            
            if not config.get("enabled", False) or not config.get("auto_trade", False):
                continue
            
            # 执行交易
            result = submit_order(
                symbol=signal['symbol'],
                side=signal['action'],
                price=signal.get('price', 0),
                quantity=config.get('position_size', 100),
                strategy=strategy
            )
            
            if result['success']:
                # 记录交易
                trade_record = {
                    "timestamp": datetime.now().isoformat(),
                    "symbol": signal['symbol'],
                    "side": signal['action'],
                    "quantity": config.get('position_size', 100),
                    "price": result['price'],
                    "strategy": strategy,
                    "order_id": result['order_id']
                }
                
                self.trades.append(trade_record)
                log_trade(trade_record)
                executed.append(trade_record)
                
                # 更新策略健康度
                self.strategy_health[strategy].add_trade(trade_record)
        
        return executed
    
    def get_health_report(self) -> Dict:
        """获取策略健康报告"""
        report = {}
        for name, health in self.strategy_health.items():
            report[name] = health.get_health_report()
        return report

# ============ 主函数 ============

if __name__ == "__main__":
    engine = QuantStrategyEngine()
    result = engine.run_full_analysis()
    
    # 保存结果
    with open("strategy_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    
    print()
    print("📁 分析结果已保存至 strategy_result.json")
