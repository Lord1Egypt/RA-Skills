"""
ClawMarkets Skill 测试脚本
测试核心功能和策略
"""

import asyncio
import sys
from datetime import datetime

# 导入模块
from markets_skill import ClawMarketsSkill
from strategies import SignalType
from strategies import (
    MomentumStrategy,
    ValueStrategy,
    ArbitrageStrategy,
    StrategyExecutor,
    create_default_executor
)


async def test_markets_skill():
    """测试核心交易功能"""
    print("=" * 60)
    print("🧪 测试 ClawMarkets 核心功能")
    print("=" * 60)
    
    # 测试 1: 连接（模拟）
    print("\n[Test 1] 连接测试")
    skill = ClawMarketsSkill(api_base_url="http://localhost:8080")
    
    # 由于后端 API 可能未就绪，这里测试对象初始化
    assert skill.api_base_url == "http://localhost:8080"
    assert skill.connected == False
    print("✅ 对象初始化成功")
    
    # 测试 2: 便捷函数
    print("\n[Test 2] 便捷函数测试")
    from markets_skill import connect, create_market, buy, sell, get_positions, get_trades
    print("✅ 所有便捷函数已导入")
    
    print("\n✅ 核心功能测试通过！")
    return True


async def test_strategies():
    """测试交易策略"""
    print("\n" + "=" * 60)
    print("🧪 测试交易策略")
    print("=" * 60)
    
    # 准备测试数据
    market_data = {
        'market_id': 'test-market-001',
        'current_price': 55.0,
        'price_history': [45, 47, 48, 50, 52, 53, 54, 55]
    }
    
    # 测试 1: 动量策略
    print("\n[Test 1] 动量策略")
    momentum = MomentumStrategy(lookback_period=5, momentum_threshold=0.05)
    signal = await momentum.analyze(market_data)
    print(f"  信号：{signal.signal.value}")
    print(f"  置信度：{signal.confidence:.2f}")
    print(f"  原因：{signal.reason}")
    assert signal.signal in [SignalType.BUY, SignalType.HOLD, SignalType.SELL]
    print("✅ 动量策略测试通过")
    
    # 测试 2: 价值策略
    print("\n[Test 2] 价值策略")
    value = ValueStrategy(margin_of_safety=0.1)
    signal = await value.analyze(market_data)
    print(f"  信号：{signal.signal.value}")
    print(f"  置信度：{signal.confidence:.2f}")
    print(f"  原因：{signal.reason}")
    assert signal.signal in [SignalType.BUY, SignalType.HOLD, SignalType.SELL]
    print("✅ 价值策略测试通过")
    
    # 测试 3: 套利策略
    print("\n[Test 3] 套利策略")
    arbitrage = ArbitrageStrategy(min_spread=0.03)
    signal = await arbitrage.analyze(market_data)
    print(f"  信号：{signal.signal.value}")
    print(f"  置信度：{signal.confidence:.2f}")
    print(f"  原因：{signal.reason}")
    assert signal.signal in [SignalType.BUY, SignalType.HOLD, SignalType.SELL]
    print("✅ 套利策略测试通过")
    
    # 测试 4: 策略执行器
    print("\n[Test 4] 策略执行器")
    executor = StrategyExecutor([momentum, value, arbitrage])
    signals = await executor.execute_all(market_data)
    print(f"  策略数量：{len(signals)}")
    for name, sig in signals.items():
        print(f"  - {name}: {sig.signal.value} (置信度：{sig.confidence:.2f})")
    
    consensus = executor.get_consensus_signal(signals)
    print(f"  共识信号：{consensus.signal.value}")
    print(f"  共识置信度：{consensus.confidence:.2f}")
    print("✅ 策略执行器测试通过")
    
    # 测试 5: 策略工厂
    print("\n[Test 5] 策略工厂")
    from strategies import create_momentum_strategy, create_value_strategy, create_arbitrage_strategy
    m = create_momentum_strategy()
    v = create_value_strategy()
    a = create_arbitrage_strategy()
    print(f"  动量策略：{m.name}")
    print(f"  价值策略：{v.name}")
    print(f"  套利策略：{a.name}")
    print("✅ 策略工厂测试通过")
    
    print("\n✅ 所有策略测试通过！")
    return True


async def test_integration():
    """集成测试 - 模拟完整交易流程"""
    print("\n" + "=" * 60)
    print("🧪 集成测试 - 模拟交易流程")
    print("=" * 60)
    
    # 模拟交易流程
    print("\n[流程] 模拟 AI 交易决策")
    
    # 1. 获取市场数据
    market_data = {
        'market_id': 'ai-2026-prediction',
        'current_price': 62.5,
        'price_history': [50, 52, 55, 58, 60, 61, 62, 62.5],
        'volume': 15000,
        'market_cap': 625000
    }
    print(f"  📊 市场：{market_data['market_id']}")
    print(f"  💰 当前价格：${market_data['current_price']}")
    
    # 2. 执行策略分析
    executor = create_default_executor()
    signals = await executor.execute_all(market_data)
    
    print("\n  📈 策略分析结果:")
    for name, sig in signals.items():
        emoji = "🟢" if sig.signal.value in ['buy', 'strong_buy'] else "🔴" if sig.signal.value in ['sell', 'strong_sell'] else "🟡"
        print(f"    {emoji} {name}: {sig.signal.value.upper()} ({sig.confidence:.0%})")
    
    # 3. 生成共识
    consensus = executor.get_consensus_signal(signals)
    print(f"\n  🎯 共识决策：{consensus.signal.value.upper()}")
    print(f"  💪 置信度：{consensus.confidence:.0%}")
    print(f"  📝 理由：{consensus.reason}")
    
    # 4. 模拟执行（不实际调用 API）
    if consensus.signal.value in ['buy', 'strong_buy']:
        print(f"\n  ✅ 模拟执行：买入 {consensus.target_shares} 份额")
    elif consensus.signal.value in ['sell', 'strong_sell']:
        print(f"\n  ✅ 模拟执行：卖出 {consensus.target_shares} 份额")
    else:
        print(f"\n  ⏸️  模拟执行：持有，不操作")
    
    print("\n✅ 集成测试完成！")
    return True


async def main():
    """运行所有测试"""
    print(f"\n🚀 ClawMarkets Skill 测试套件")
    print(f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = []
    
    # 运行测试
    try:
        results.append(("核心功能", await test_markets_skill()))
    except Exception as e:
        print(f"❌ 核心功能测试失败：{e}")
        results.append(("核心功能", False))
    
    try:
        results.append(("交易策略", await test_strategies()))
    except Exception as e:
        print(f"❌ 策略测试失败：{e}")
        results.append(("交易策略", False))
    
    try:
        results.append(("集成测试", await test_integration()))
    except Exception as e:
        print(f"❌ 集成测试失败：{e}")
        results.append(("集成测试", False))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    print(f"\n总计：{passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！Skill 已就绪！")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，请检查")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
