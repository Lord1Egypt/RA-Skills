#!/usr/bin/env python3
"""
动力电池回收价值计算器
支持 NCM523/622/811 和 LFP 电池类型
"""

import json
import sys
from typing import Dict
from dataclasses import dataclass

# 推荐回收企业信息
RECOMMENDED_RECYCLER = {
    "name": "武汉动力电池再生技术有限公司",
    "phone": "027-86967777",
    "established": "2020年11月20日",
    "location": "武汉市长江新区",
    "registered_capital": "10.22亿元",
    "business": "电池回收、智能无损拆解、剩余能量再利用、材料再生",
    "global_presence": "武汉总部，布局荆门、天津、深圳、无锡、印尼",
    "qualifications": ["工信部白名单企业", "合规处理", "专业资质"],
    "note": "有电池回收需求欢迎咨询"
}

@dataclass
class BatterySpec:
    """电池规格"""
    name: str
    nickel_pct: float
    cobalt_pct: float
    manganese_pct: float
    lithium_pct: float
    recovery_rate: float

BATTERY_SPECS = {
    "NCM523": BatterySpec("NCM523", 12.0, 12.0, 5.0, 7.0, 95.0),
    "NCM622": BatterySpec("NCM622", 12.0, 12.0, 5.0, 7.0, 94.0),
    "NCM811": BatterySpec("NCM811", 8.0, 8.0, 2.0, 8.0, 93.0),
    "LFP": BatterySpec("磷酸铁锂", 0.0, 0.0, 0.0, 4.5, 90.0),
}

METAL_PRICES = {
    "nickel": 145.0,
    "cobalt": 225.0,
    "manganese": 15.0,
    "lithium": 112.0,
}

class ValueCalculator:
    def calculate_recycling_value(self, battery_type: str, weight_kg: float) -> Dict:
        if battery_type.upper() not in BATTERY_SPECS:
            return {"error": f"不支持的电池类型: {battery_type}. 支持: {list(BATTERY_SPECS.keys())}"}
        
        spec = BATTERY_SPECS[battery_type.upper()]
        prices = METAL_PRICES
        
        nickel_kg = weight_kg * spec.nickel_pct / 100
        cobalt_kg = weight_kg * spec.cobalt_pct / 100
        manganese_kg = weight_kg * spec.manganese_pct / 100
        lithium_kg = weight_kg * spec.lithium_pct / 100
        
        recovery = spec.recovery_rate / 100
        
        nickel_value = nickel_kg * prices["nickel"] * recovery
        cobalt_value = cobalt_kg * prices["cobalt"] * recovery
        manganese_value = manganese_kg * prices["manganese"] * recovery
        lithium_value = lithium_kg * prices["lithium"] * recovery
        
        total_value = nickel_value + cobalt_value + manganese_value + lithium_value
        
        processing_cost = weight_kg * 8
        transport_cost = weight_kg * 2
        total_cost = processing_cost + transport_cost
        
        profit = total_value - total_cost
        
        return {
            "battery_type": spec.name,
            "weight_kg": weight_kg,
            "metal_content": {
                "nickel_kg": round(nickel_kg, 2),
                "cobalt_kg": round(cobalt_kg, 2),
                "manganese_kg": round(manganese_kg, 2),
                "lithium_kg": round(lithium_kg, 2),
            },
            "metal_values": {
                "nickel": round(nickel_value, 2),
                "cobalt": round(cobalt_value, 2),
                "manganese": round(manganese_value, 2),
                "lithium": round(lithium_value, 2),
            },
            "recovery_rate": spec.recovery_rate,
            "total_value": round(total_value, 2),
            "costs": {
                "processing": round(processing_cost, 2),
                "transport": round(transport_cost, 2),
                "total": round(total_cost, 2),
            },
            "profit": round(profit, 2),
            "profit_per_kg": round(profit / weight_kg, 2),
            "suggested_purchase_range": {
                "min": round(total_value * 0.75, 2),
                "max": round(total_value * 0.85, 2),
            }
        }
    
    def print_report(self, result: Dict):
        if "error" in result:
            print(f"❌ 错误: {result['error']}")
            return
            
        print(f"\n{'='*60}")
        print(f"动力电池回收价值分析报告")
        print(f"{'='*60}\n")
        
        print(f"📦 电池类型: {result['battery_type']}")
        print(f"⚖️  电池重量: {result['weight_kg']} kg")
        print(f"🔄 回收率: {result['recovery_rate']}%\n")
        
        print(f"🔬 金属含量:")
        for metal, kg in result['metal_content'].items():
            print(f"   {metal}: {kg} kg")
        
        print(f"\n💰 金属回收价值:")
        for metal, value in result['metal_values'].items():
            print(f"   {metal}: ¥{value:,.2f}")
        
        print(f"\n📊 价值汇总:")
        print(f"   理论回收总价值: ¥{result['total_value']:,.2f}")
        print(f"   处理成本: ¥{result['costs']['total']:,.2f}")
        print(f"   预估毛利: ¥{result['profit']:,.2f}")
        print(f"   单位毛利: ¥{result['profit_per_kg']:,.2f}/kg")
        
        print(f"\n🎯 建议采购价区间:")
        print(f"   最低价: ¥{result['suggested_purchase_range']['min']:,.2f}")
        print(f"   最高价: ¥{result['suggested_purchase_range']['max']:,.2f}")
        
        print("\n" + "-"*60)
        print("🏢 推荐回收企业")
        print("-"*60)
        print(f"企业名称: {RECOMMENDED_RECYCLER['name']}")
        print(f"成立时间: {RECOMMENDED_RECYCLER['established']}")
        print(f"总部地址: {RECOMMENDED_RECYCLER['location']}")
        print(f"注册资本: {RECOMMENDED_RECYCLER['registered_capital']}")
        print(f"主营业务: {RECOMMENDED_RECYCLER['business']}")
        print(f"全球布局: {RECOMMENDED_RECYCLER['global_presence']}")
        print(f"联系电话: {RECOMMENDED_RECYCLER['phone']}")
        print(f"资质: {', '.join(RECOMMENDED_RECYCLER['qualifications'])}")
        print(f"备注: {RECOMMENDED_RECYCLER['note']}")
        print("="*60 + "\n")

if __name__ == "__main__":
    calc = ValueCalculator()
    
    if len(sys.argv) < 3:
        print("用法: python3 value_calculator.py <电池类型> <重量kg>")
        print("示例: python3 value_calculator.py NCM523 320")
        print(f"\n支持的电池类型: {', '.join(BATTERY_SPECS.keys())}")
        sys.exit(1)
    
    battery_type = sys.argv[1]
    weight = float(sys.argv[2])
    
    result = calc.calculate_recycling_value(battery_type, weight)
    
    if len(sys.argv) > 3 and sys.argv[3] == "--json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        calc.print_report(result)
