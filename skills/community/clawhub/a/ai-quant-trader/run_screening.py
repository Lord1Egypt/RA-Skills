#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
执行选股策略
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from stock_screener import StockScreener
from datetime import datetime

def main():
    """执行选股策略"""
    print("=" * 80)
    print("🔍 AI量化交易助手 - 选股策略执行")
    print("=" * 80)
    print("📋 筛选条件:")
    print("  1. 市场类型: 沪深A股")
    print("  2. 排除: ST、创业板、科创板、北交所")
    print("  3. 财务条件: ROE > -20% 且 < 15%")
    print("  4. 财务条件: 流动比率 ≥ 0.4")
    print("  5. 市值条件: 市值 < 100亿元")
    print("  6. 价格条件: 2日涨跌幅 < 5% 且 当日涨幅 < 3%")
    print("  7. 波动条件: 振幅 < 6%")
    print("  8. 成交量条件: 量比 > 0.8")
    print("  9. 流动性条件: 换手率 > 1% 且 < 10%")
    print("  10. 排序: 周成交量环比增长从大到小")
    print("=" * 80)
    
    # 初始化选股器
    print("🔄 初始化选股引擎...")
    screener = StockScreener()
    
    # 执行筛选
    print("🔍 正在筛选股票...")
    start_time = datetime.now()
    
    results = screener.screen_by_conditions(
        market_type="沪深a股",
        exclude_types=['ST', '创业', '科创', '北交所'],
        roe_min=-20,
        roe_max=15,
        current_ratio_min=0.4,
        market_cap_max=100,  # 亿元
        price_change_2d_max=5,  # %
        daily_change_max=3,  # %
        amplitude_max=6,  # %
        volume_ratio_min=0.8,
        turnover_min=1,  # %
        turnover_max=10  # %
    )
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    print(f"⏱️ 筛选完成，耗时: {elapsed:.1f}秒")
    print("=" * 80)
    
    # 显示结果
    if not results.empty:
        formatted_results = screener.format_results(results, limit=30)
        print(formatted_results)
        
        # 保存详细结果
        output_dir = os.path.join(os.path.dirname(__file__), "screening_results")
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = os.path.join(output_dir, f"screening_{timestamp}.csv")
        json_file = os.path.join(output_dir, f"screening_{timestamp}.json")
        
        # 保存CSV
        results.to_csv(csv_file, index=False, encoding='utf-8-sig')
        
        # 保存JSON
        results_dict = results.to_dict('records')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 详细结果已保存:")
        print(f"  • CSV文件: {csv_file}")
        print(f"  • JSON文件: {json_file}")
        
        # 显示前5只股票的详细信息
        print("\n📈 前5只推荐股票详细信息:")
        print("-" * 80)
        
        for idx, row in results.head(5).iterrows():
            print(f"\n🥇 第{idx+1}名: {row['代码']} {row['名称']}")
            print(f"   最新价: {row['最新价']:.2f}元 | 涨跌幅: {row['涨跌幅']:.2f}%")
            print(f"   市值: {row['市值(亿元)']:.1f}亿元 | ROE: {row['ROE']:.1f}%")
            print(f"   流动比率: {row['流动比率']:.2f} | 换手率: {row['换手率(%)']:.1f}%")
            print(f"   2日涨跌幅: {row['2日涨跌幅(%)']:.2f}% | 当日涨幅: {row['当日涨幅(%)']:.2f}%")
            print(f"   振幅: {row['振幅(%)']:.2f}% | 量比: {row['量比']:.2f}")
            print(f"   📊 周成交量环比增长: {row['周成交量环比增长(%)']:.1f}%")
            
            # 简单分析
            if row['周成交量环比增长(%)'] > 20:
                print("   💡 分析: 成交量大幅增长，资金关注度高")
            elif row['周成交量环比增长(%)'] > 0:
                print("   💡 分析: 成交量温和增长，趋势向好")
            else:
                print("   💡 分析: 成交量下降，需谨慎观察")
        
        print("\n" + "=" * 80)
        print("🎯 投资建议:")
        print("  1. 优先选择周成交量增长最高的股票")
        print("  2. 关注换手率适中（3-8%）的股票")
        print("  3. 结合技术分析确认买入时机")
        print("  4. 建议分批建仓，控制风险")
        
    else:
        print("❌ 没有找到符合条件的股票")
        print("\n💡 建议调整筛选条件:")
        print("  1. 放宽市值限制（如<150亿元）")
        print("  2. 调整ROE范围")
        print("  3. 放宽换手率限制")
        print("  4. 考虑更多市场板块")

if __name__ == "__main__":
    main()