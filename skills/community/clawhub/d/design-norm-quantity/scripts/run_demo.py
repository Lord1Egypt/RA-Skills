# -*- coding: utf-8 -*-
"""
度量衡测不准系统 - 一键运行脚本
无需交互，自动演示核心功能
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uncertainty_estimator import (
    UncertaintyEstimator, ProjectParams, BuildingType, 
    StructureType, Region, quick_estimate
)

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   度量衡测不准关键因子配比估量估价系统 v3.0                 ║
    ║   ========================================================   ║
    ║   「知其然，知其所以然，更知其不确定性」                     ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def demo_quick_estimate():
    """快速估算演示"""
    print("\n" + "="*60)
    print("⚡ 快速示例演示 - 高层办公楼")
    print("="*60)
    
    result = quick_estimate(
        building_type="办公",
        total_area=50000,
        floor_count=33,
        basement_area=10000,
        basement_floors=2,
        decoration_level="精装",
        has_central_ac=True,
        has_pile=True,
        region="汕尾"
    )
    
    # 直接打印所有结果
    params = result["项目参数"]
    estimate = result["造价估算"]
    
    print(f"\n项目参数:")
    for k, v in params.items():
        print(f"   {k}: {v}")
    
    print(f"\n💰 造价估算结果:")
    print(f"   总建筑面积: {estimate['总建筑面积']}")
    print(f"   地上面积: {estimate['地上面积']}")
    print(f"   地下面积: {estimate['地下面积']}")
    print(f"\n   单方造价区间:")
    for k, v in estimate["单方造价区间"].items():
        print(f"      {k}: {v}")
    print(f"\n   总造价区间:")
    for k, v in estimate["总造价区间"].items():
        print(f"      {k}: {v}")
    print(f"\n   调整系数:")
    print(f"      地下室附加: {estimate['地下室附加']}")
    print(f"      综合调整: {estimate['综合调整系数']}")
    print(f"      地区系数: {estimate['地区系数']}")
    print(f"      时间系数: {estimate['时间系数']}")

def demo_full_estimate():
    """完整参数估算演示"""
    print("\n" + "="*60)
    print("📊 完整参数演示 - 住宅项目")
    print("="*60)
    
    params = ProjectParams(
        building_type=BuildingType.RESIDENTIAL,
        structure_type=StructureType.FRAME_SHEAR_WALL,
        total_area=80000,
        floor_count=26,
        basement_area=15000,
        basement_floors=2,
        decoration_level="精装",
        has_central_ac=True,
        has_pile=True,
        seismic_level="7度",
        region=Region.SHANWEI,
        year=2026
    )
    
    estimator = UncertaintyEstimator()
    result = estimator.estimate(params)
    
    estimate = result["造价估算"]
    print(f"\n📊 项目参数:")
    print(f"   建筑类型: 住宅 (26层地上 + 2层地下)")
    print(f"   结构形式: 框架-剪力墙")
    print(f"   建筑面积: {params.total_area:,} ㎡")
    print(f"   地区: 广东")
    
    print(f"\n💰 造价估算结果:")
    print(f"   总建筑面积: {estimate['总建筑面积']}")
    print(f"   单方造价区间:")
    for k, v in estimate["单方造价区间"].items():
        print(f"      {k}: {v}")
    print(f"\n   总造价区间:")
    for k, v in estimate["总造价区间"].items():
        print(f"      {k}: {v}")

def demo_ratio_system():
    """配比参数体系演示"""
    print("\n" + "="*60)
    print("🔧 配比参数体系 - 关键因子展示")
    print("="*60)
    
    params = ProjectParams(
        building_type=BuildingType.OFFICE,
        structure_type=StructureType.FRAME_CORE_TUBE,
        total_area=50000,
        floor_count=33,
        basement_area=10000,
        basement_floors=2,
        decoration_level="精装",
        has_central_ac=True,
        has_pile=True,
        seismic_level="7度",
        region=Region.SHANWEI,
        year=2026
    )
    
    estimator = UncertaintyEstimator()
    
    print("\n📐 结构构件配比:")
    print("   (通过 estimate 方法内嵌计算)")
    
    print("\n🔧 机电安装配比:")
    mep = estimator.calculate_mep_ratios(params)
    for k, v in mep.items():
        val = v.get('value', v) if isinstance(v, dict) else v
        rng = v.get('range', '') if isinstance(v, dict) else ''
        print(f"   {k}: {val} {rng}")
    
    print("\n🧱 钢筋混凝土配比:")
    rebar = estimator.calculate_rebar_ratios(params)
    for k, v in rebar.items():
        val = v.get('value', v) if isinstance(v, dict) else v
        rng = v.get('range', '') if isinstance(v, dict) else ''
        print(f"   {k}: {val} {rng}")
    
    print("\n🏗️ 基础配比:")
    foundation = estimator.calculate_foundation_ratios(params)
    for k, v in foundation.items():
        val = v.get('value', v) if isinstance(v, dict) else v
        rng = v.get('range', '') if isinstance(v, dict) else ''
        print(f"   {k}: {val} {rng}")

def demo_material_factors():
    """材料因子体系演示"""
    print("\n" + "="*60)
    print("🔩 6大关键材料因子")
    print("="*60)
    
    estimator = UncertaintyEstimator()
    
    print("\n材料因子 | 造价占比 | 年波动率 | 当前趋势")
    print("-" * 60)
    for k, v in estimator.materials_db.FACTORS.items():
        print(f"{v.name:12s} ({v.code}) | {v.cost_ratio:5.1%} | +/-{v.annual_volatility:4.0%} | {v.price_trend}")
    
    # 不确定性传播
    print("\n📊 不确定性传播模型:")
    print("   ΔP_project = Σ(αᵢ × ΔPᵢ)")
    print("   其中 αᵢ = 材料造价占比 × 波动率")

def demo_monte_carlo():
    """蒙特卡洛模拟演示"""
    print("\n" + "="*60)
    print("🎲 蒙特卡洛模拟演示")
    print("="*60)
    
    params = ProjectParams(
        building_type=BuildingType.OFFICE,
        structure_type=StructureType.FRAME_CORE_TUBE,
        total_area=50000,
        floor_count=33,
        basement_area=10000,
        basement_floors=2,
        decoration_level="精装",
        has_central_ac=True,
        has_pile=True,
        seismic_level="7度",
        region=Region.SHANWEI,
        year=2026
    )
    
    estimator = UncertaintyEstimator()
    
    print("\n   蒙特卡洛模拟需要更多参数配置")
    print("   请使用交互模式: python uncertainty_calculator.py")
    print("   或选择菜单 [5] 蒙特卡洛模拟演示")

def main():
    """主函数"""
    print_banner()
    
    print("🚀 正在启动系统演示...\n")
    
    # 演示1: 快速估算
    demo_quick_estimate()
    
    # 演示2: 完整参数估算
    demo_full_estimate()
    
    # 演示3: 配比参数体系
    demo_ratio_system()
    
    # 演示4: 材料因子体系
    demo_material_factors()
    
    # 演示5: 蒙特卡洛模拟
    demo_monte_carlo()
    
    print("\n" + "="*60)
    print("✅ 系统演示完成！")
    print("="*60)
    print("\n📖 使用指南:")
    print("   交互模式: python uncertainty_calculator.py")
    print("   Python API: from uncertainty_estimator import quick_estimate")
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
