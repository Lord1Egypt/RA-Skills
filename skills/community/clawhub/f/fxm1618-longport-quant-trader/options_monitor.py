#!/usr/bin/env python3
"""
长桥期权信号监控 v1.0
获取美股期权链数据，生成买卖信号
"""
from longport.openapi import QuoteContext, Config, SubType, PushQuote, OptionType
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time

load_dotenv()

# 监控标的
UNDERLYINGS = ["QQQ.US", "NVDA.US", "AAPL.US", "TSLA.US", "MSFT.US"]

# 策略配置
STRATEGY = {
    "news_threshold": 0.7,      # 新闻情绪阈值
    "big_order_threshold": 200000,  # 大单阈值（美元）
    "stop_loss": -0.20,         # 止损 -20%
    "take_profit": 0.50,        # 止盈 +50%
}

def get_option_chain(symbol: str, ctx: QuoteContext):
    """获取期权链"""
    print(f"\n📊 {symbol} 期权链")
    print("=" * 80)
    
    # 获取到期日
    # 注意：长桥 API 获取期权链的具体方法需要查阅文档
    # 这里先测试基础行情
    
    try:
        # 订阅标的行情
        ctx.subscribe([symbol], [SubType.Quote])
        print(f"✅ 已订阅 {symbol}")
    except Exception as e:
        print(f"❌ 订阅失败：{e}")

def analyze_options(symbol: str, underlying_price: float):
    """分析期权信号"""
    print(f"\n🎯 {symbol} 期权信号分析")
    print("-" * 60)
    
    # 模拟信号（实际需要从 API 获取期权数据）
    signals = []
    
    # 示例：基于标的价格的简单策略
    if symbol == "QQQ.US":
        # 关键价位
        support = 605
        resistance = 610
        
        if underlying_price < support:
            signals.append({
                "type": "Put",
                "strike": 600,
                "expiry": "2026-03-06",
                "reason": f"价格低于支撑位 ${support}",
                "strength": 8
            })
        elif underlying_price > resistance:
            signals.append({
                "type": "Call",
                "strike": 615,
                "expiry": "2026-03-06",
                "reason": f"价格突破阻力位 ${resistance}",
                "strength": 8
            })
        else:
            signals.append({
                "type": "观望",
                "reason": f"价格在 ${support}-${resistance} 区间内",
                "strength": 5
            })
    
    # 输出信号
    for sig in signals:
        print(f"  信号：{sig['type']}")
        if sig['type'] != "观望":
            print(f"    行权价：${sig['strike']}")
            print(f"    到期日：{sig['expiry']}")
        print(f"    理由：{sig['reason']}")
        print(f"    强度：{sig['strength']}/10")
    
    return signals

def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("🚀 长桥期权信号监控系统 v1.0")
    print("=" * 80)
    print(f"启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"监控标的：{', '.join(UNDERLYINGS)}")
    print(f"策略配置：新闻阈值={STRATEGY['news_threshold']}, "
          f"大单阈值=${STRATEGY['big_order_threshold']:,}")
    print("=" * 80)
    
    # 创建行情上下文
    config = Config.from_env()
    ctx = QuoteContext(config)
    
    # 存储最新价格
    latest_prices = {}
    
    def on_quote(symbol: str, quote: PushQuote):
        latest_prices[symbol] = quote.last_done
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {symbol:10} ${quote.last_done:.2f}")
    
    ctx.set_on_quote(on_quote)
    
    # 订阅所有标的
    print("\n📡 正在订阅行情...")
    ctx.subscribe(UNDERLYINGS, [SubType.Quote])
    print("✅ 订阅成功")
    
    # 等待数据
    print("\n等待行情数据...")
    time.sleep(5)
    
    # 分析每个标的
    print("\n" + "=" * 80)
    print("📈 开始期权信号分析")
    print("=" * 80)
    
    all_signals = {}
    for symbol in UNDERLYINGS:
        if symbol in latest_prices:
            signals = analyze_options(symbol, latest_prices[symbol])
            all_signals[symbol] = {
                "price": latest_prices[symbol],
                "signals": signals
            }
        else:
            print(f"⚠️ {symbol}: 无价格数据")
    
    # 汇总最强信号
    print("\n" + "=" * 80)
    print("🎯 最强信号汇总")
    print("=" * 80)
    
    best_signals = []
    for symbol, data in all_signals.items():
        for sig in data["signals"]:
            if sig["type"] != "观望":
                best_signals.append({
                    "symbol": symbol,
                    "price": data["price"],
                    **sig
                })
    
    # 按强度排序
    best_signals.sort(key=lambda x: x["strength"], reverse=True)
    
    if best_signals:
        print("\n推荐交易（按信号强度排序）：")
        for i, sig in enumerate(best_signals[:5], 1):
            print(f"\n{i}. {sig['symbol']} {sig['type']}")
            print(f"   标的价格：${sig['price']:.2f}")
            print(f"   行权价：${sig['strike']}")
            print(f"   到期日：{sig['expiry']}")
            print(f"   信号强度：{'⭐' * sig['strength']} ({sig['strength']}/10)")
            print(f"   理由：{sig['reason']}")
    else:
        print("\n⚠️ 暂无强烈推荐，保持观望")
    
    print("\n" + "=" * 80)
    print("✅ 分析完成")
    print("=" * 80)
    
    return all_signals

if __name__ == "__main__":
    main()
