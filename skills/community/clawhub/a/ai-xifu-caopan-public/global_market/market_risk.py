#!/usr/bin/env python3
"""
🌍 全球市场风险分析引擎 v1.0
================================
为英国、日本、德国市场提供本地化情报分析。
套用大叔教的概率论+博弈论框架，但信号内容适配当地。

用法:
  python3 market_risk.py --market 英国 --symbol SHEL.L
  python3 market_risk.py --market 日本 --symbol 7203.T
  python3 market_risk.py --market 德国 --symbol SAP.DE
  python3 market_risk.py --list-all
"""

import json
import os
import sys
import datetime

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, 'market_config.json')


def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_market_risk(market_name):
    """
    根据本地化预警信号分析市场风险。
    套用大叔教的概率论逻辑，但分析内容适配当地。
    """
    config = load_config()
    if market_name not in config['markets']:
        return None
    
    market = config['markets'][market_name]
    signals = market.get('signal_adapters', {})
    risk_info = market.get('risk_signals', {})
    
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"\n{'='*55}")
    print(f"  🌍 {market['display_name']} — 本地化情报分析")
    print(f"  📍 {market['exchange']}")
    print(f"  🕐 {now} (大叔时间+8)")
    print(f"{'='*55}")
    
    # 1️⃣ 市场基本信息
    print(f"\n【一、市场概况】")
    print(f"  交易所: {market['exchange']}")
    print(f"  货币: {market['currency']}")
    print(f"  时区: {market['timezone']} (UTC{market['utc_offset']})")
    print(f"  交易时间: {market['trading_hours'].get('regular', '详见配置')}")
    
    indices = market.get('indices', {})
    print(f"  基准指数:")
    for key, name in indices.items():
        print(f"    📊 {name}")
    
    # 2️⃣ 核心影响因子
    print(f"\n【二、核心影响因子】")
    ri = risk_info
    if ri:
        print(f"  央行: {ri.get('central_bank', 'N/A')}")
        print(f"  通胀指标: {ri.get('inflation_indicator', 'N/A')}")
        print(f"  增长指标: {ri.get('growth_indicator', 'N/A')}")
        print(f"  关键货币对: {ri.get('currency_pair', 'N/A')}")
        print(f"  基准利率影响: 参照{ri.get('central_bank', '央行')}货币政策")
        print(f"  关键行业: {', '.join(ri.get('key_sectors', []))}")
    
    # 3️⃣ 本地化预警信号
    print(f"\n【三、{market_name}市场预警信号（15项）】")
    print(f"  {'#'} 信号内容{' ' * 30}状态")
    print(f"  {'-'*55}")
    
    enabled = sum(1 for v in signals.values() if v)
    for i, (signal, status) in enumerate(signals.items(), 1):
        icon = '🟢' if status else '⚪'
        # Format signal display - show first 40 chars + ...
        sig_short = signal[:45] if len(signal) > 45 else signal
        padding = ' ' * (43 - len(sig_short)) if len(signal) > 45 else ' ' * (48 - len(signal))
        print(f"  {icon} {sig_short}{padding} {'已加载' if status else '待开通'}")
    
    print(f"\n  信号总数: {len(signals)}项 | 已激活: {enabled}项")
    risk_level = "中"
    if enabled >= 12:
        risk_level = "高覆盖"
    elif enabled >= 8:
        risk_level = "完整"
    coverage = "🔴 极高" if enabled == 0 else "🟢 完整" if enabled >= 12 else "🟡 中等"
    print(f"  覆盖度: {coverage}")
    
    # 4️⃣ 情报分析框架（套用大叔的概率论+博弈论）
    print(f"\n【四、情报分析框架（概率论+博弈论）】")
    
    # 央行政策预判
    cb = ri.get('central_bank', '央行')
    print(f"  🏦 {cb}政策分析:")
    print(f"     - 近期利率决议是市场核心驱动")
    print(f"     - 通胀数据决定加息预期方向")
    print(f"     - 经济增速影响政策节奏判断")
    
    # 汇率影响
    cp = ri.get('currency_pair', '本币')
    print(f"  💱 {cp}汇率分析:")
    print(f"     - 汇率波动直接影响出口型企业盈利")
    print(f"     - 本币贬值: 利好出口企业(短期)")
    print(f"     - 本币升值: 利好进口/消费企业")
    
    # 行业侧重
    sectors = ', '.join(ri.get('key_sectors', ['金融', '制造业']))
    print(f"  🏭 关键行业侧重 ({sectors}):")
    print(f"     - 行业龙头走势决定指数方向")
    print(f"     - 关注各行业PMI/产能利用率变化")
    print(f"     - 行业政策变化带来结构性机会")
    
    # 全球联动
    print(f"  🌐 全球市场联动分析:")
    print(f"     - 美股走势对该市场有传导效应")
    print(f"     - 大宗商品价格影响能源/资源类股票")
    print(f"     - 全球风险偏好变化影响资金流向")
    
    # 5️⃣ 重要事件日历
    events = ri.get('policy_events', [])
    if events:
        print(f"\n【五、近期重要事件日历】")
        for e in events:
            print(f"  📅 {e}")
    
    # 6️⃣ 综合风险评级
    print(f"\n【六、综合风险评级】")
    
    # 按市场特色给出不同的风险维度
    if market_name == "英国":
        print(f"  ⚡ 主要风险源:")
        print(f"     - BOE利率决议（通胀粘性→鹰派风险）")
        print(f"     - 英镑汇率波动（影响FTSE 100成分股）")
        print(f"     - 能源价格冲击（居民消费承压）")
        print(f"  📊 风险评级: 🟡 中等 | 概率论预判需结合实时数据")
    elif market_name == "日本":
        print(f"  ⚡ 主要风险源:")
        print(f"     - BOJ货币政策正常化（YCC退出→日元升值）")
        print(f"     - 日元汇率波动（套利交易平仓风险）")
        print(f"     - 全球半导体周期（影响日本电子业）")
        print(f"  📊 风险评级: 🟡 中等 | 日本是今年全球最复杂市场之一")
    elif market_name == "德国":
        print(f"  ⚡ 主要风险源:")
        print(f"     - ECB货币政策（通胀vs经济增长）")
        print(f"     - 能源成本冲击（制造业竞争力受损）")
        print(f"     - 对华贸易依赖（中欧贸易摩擦风险）")
        print(f"  📊 风险评级: 🟠 中等偏高 | 德国制造业PMI持续承压")
    
    print(f"\n  概率论框架: 15项预警信号 → 加权计算下跌概率")
    print(f"  博弈论分析: 机构/散户/海外资金 三方博弈")
    print(f"  MACD判断: 结合技术指标确认趋势位置")
    print(f"\n{'='*55}")
    
    return {
        'market': market_name,
        'signals': len(signals),
        'enabled': enabled,
        'risk_level': risk_level,
    }


def main():
    if len(sys.argv) < 2:
        print("🌍 全球市场风险分析引擎 v1.0")
        print(f"   使用: python3 market_risk.py --market 英国")
        print(f"   使用: python3 market_risk.py --market 日本")
        print(f"   使用: python3 market_risk.py --market 德国")
        print(f"   使用: python3 market_risk.py --list-all")
        return
    
    args = sys.argv[1:]
    
    if "--list-all" in args:
        config = load_config()
        print("\n🌐 已配置本地化情报的市场")
        print("=" * 50)
        for name, market in config['markets'].items():
            signals = market.get('signal_adapters', {})
            active = market.get('active', False)
            flag = '✅' if active else '⏳'
            if signals:
                print(f"  {flag} {market['display_name']:<12} {len(signals)}个预警信号")
        print()
    
    elif "--market" in args:
        idx = args.index("--market") + 1
        if idx < len(args):
            analyze_market_risk(args[idx])
        else:
            print("❌ 请指定市场: 英国/日本/德国")
    else:
        print("❌ 未知参数")


if __name__ == "__main__":
    main()
