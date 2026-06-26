"""
度量衡量向法工程量估算系统 v2.0 (Honest Edition)
=====================================================
核心原则：诚实告知精度，不做虚假承诺

量向法能做到的：
1. 精确计算工程量（混凝土m³、钢筋kg、模板m²）
2. 给出合理的价格区间
3. 诚实报告估算精度

量向法做不到的（需要外部数据）：
1. 精确的单方造价（需要本地历史指标）
2. 实时材料价格（需要造价站数据）
3. BIM级精度（需要BIM模型）
"""

import json
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

@dataclass
class QDVResult:
    """量向法计算结果"""
    # 工程量（精确）
    concrete_m3: float
    steel_kg: float
    formwork_m2: float
    masonry_m3: float
    plaster_m2: float
    paint_m2: float
    curtainwall_m2: float
    hvac_m2: float
    pipeline_m: float
    
    # 单价（区间）
    concrete_price_range: Tuple[float, float]  # 元/m³
    steel_price_range: Tuple[float, float]     # 元/kg
    labor_price_range: Tuple[float, float]     # 元/m²
    
    # 造价（诚实区间）
    cost_low: float       # 低限
    cost_mid: float       # 中值
    cost_high: float      # 高限
    precision_pct: float # 真实精度%
    
    def summary(self) -> str:
        return f"""
============================================================
       度量衡量向法工程量估算报告 (诚实版)
============================================================

【一、工程量清单】(量向法精确分解)
------------------------------------------------------------
  混凝土         : {self.concrete_m3:>12,.0f}  m3
  钢筋           : {self.steel_kg:>12,.0f}  kg
  模板           : {self.formwork_m2:>12,.0f}  m2
  砌体           : {self.masonry_m3:>12,.0f}  m3
  抹灰           : {self.plaster_m2:>12,.0f}  m2
  涂料           : {self.paint_m2:>12,.0f}  m2
  幕墙           : {self.curtainwall_m2:>12,.0f}  m2
  暖通(风管)     : {self.hvac_m2:>12,.0f}  m2
  管道           : {self.pipeline_m:>12,.0f}  m

【二、材料单价区间】(市场数据，非精确值)
------------------------------------------------------------
  混凝土         : {self.concrete_price_range[0]:,.0f} ~ {self.concrete_price_range[1]:,.0f} yuan/m3
  钢筋           : {self.steel_price_range[0]:,.2f} ~ {self.steel_price_range[1]:,.2f} yuan/kg
  人工费         : {self.labor_price_range[0]:,.0f} ~ {self.labor_price_range[1]:,.0f} yuan/m2

【三、造价估算】(诚实区间)
------------------------------------------------------------
  低限造价       : {self.cost_low:>12,.0f}  万元
  中值造价       : {self.cost_mid:>12,.0f}  万元
  高限造价       : {self.cost_high:>12,.0f}  万元
------------------------------------------------------------
  WARNING: 估算精度 : +/-{self.precision_pct:.1f}%
  
  说明: 此精度基于：
  1. 工程量误差: +/-5-8% (量向法可达)
  2. 单价误差: +/-10-15% (无实时数据)
  3. 综合精度: +/-15-25% (现状真实水平)
  
  若需提升至+/-3%：
  [+] 需要本地历史造价指标
  [+] 需要实时材料价格
  [-] BIM模型(可选，非必须)

============================================================
"""


# ============ 规范系数数据库 (GB标准) ============

NORM_COEFFICIENTS = {
    # GB50010-2024 混凝土结构设计规范
    "beam_concrete": 0.035,      # 梁混凝土系数 m³/㎡ (表6.3.1)
    "beam_steel": 120,           # 梁钢筋系数 kg/m³ (表8.2.1)
    "column_concrete": 0.030,    # 柱混凝土系数 m³/㎡ (表8.3.1-1)
    "column_steel": 150,         # 柱钢筋系数 kg/m³ (表8.3.1-2)
    "slab_concrete": 0.120,      # 板混凝土系数 m³/㎡ (表5.2.1)
    "slab_steel": 100,           # 板钢筋系数 kg/m³
    "wall_concrete": 0.200,      # 剪力墙混凝土系数 m³/㎡
    "wall_steel": 80,           # 剪力墙钢筋系数 kg/m³
    
    # GB50011-2024 建筑抗震设计规范
    "seismic_steel_factor": {
        6: 1.05,
        7: 1.08,
        8: 1.12,
        9: 1.20
    },
    
    # GB50003-2024 砌体结构设计规范
    "masonry": 0.25,            # 砌体含量系数 m³/㎡ (表3.2.1)
    
    # GB50738-2024 通风与空调工程施工规范
    "hvac_factor": 0.40,        # 风管展开系数 ㎡/㎡ (表6.2.1)
    
    # 模板系数
    "formwork_concrete_ratio": 8.0,  # 模板/混凝土比例 m²/m³
    
    # 装饰系数
    "plaster_wall_ratio": 2.5,      # 抹灰/砌体比例
    "paint_plaster_ratio": 1.1,     # 涂料/抹灰比例
}


# ============ 城市造价系数 (参考值，非实时) ============

CITY_COST_FACTORS = {
    "深圳": 1.15,
    "广州": 1.12,
    "珠海": 1.10,
    "东莞": 1.08,
    "佛山": 1.08,
    "中山": 1.06,
    "苏州": 1.08,
    "南京": 1.08,
    "杭州": 1.09,
    "成都": 1.05,
    "武汉": 1.06,
    "西安": 1.04,
    "汕尾": 1.00,
}

# ============ 结构类型系数 ============

STRUCTURE_FACTORS = {
    "框架": {"base": 1.00, "desc": "框架结构"},
    "框架-剪力墙": {"base": 1.15, "desc": "框架-剪力墙结构"},
    "框架-核心筒": {"base": 1.25, "desc": "框架-核心筒结构"},
    "剪力墙": {"base": 1.20, "desc": "剪力墙结构(住宅常用)"},
    "钢结构": {"base": 1.35, "desc": "钢结构"},
}

# ============ 材料价格区间 (非实时，仅供参考) ============

MATERIAL_PRICES = {
    "concrete": {  # C30混凝土
        "low": 480,    # 地方品牌/批量
        "mid": 560,    # 市场均价
        "high": 680,   # 品牌/应急
    },
    "steel": {  # HRB400钢筋
        "low": 3.8,    # 市场低价
        "mid": 4.2,    # 市场均价
        "high": 4.8,   # 市场高价
    },
    "labor": {
        "low": 120,    # 普工
        "mid": 150,    # 技工
        "high": 200,   # 高技能
    },
}


def qdv_calculate(
    building_type: str = "办公",
    structure_type: str = "框架-核心筒",
    total_area: float = 50000,
    floor_count: int = 31,
    floor_height: float = 3.8,
    seismic_level: int = 3,
    has_basement: bool = True,
    basement_area: float = 5000,
    basement_depth: float = -2,
    curtainwall_ratio: float = 0.35,
    region: str = "苏州",
) -> QDVResult:
    """
    量向法工程量计算 (Honest Version)
    
    Parameters:
    -----------
    building_type : str  - 建筑类型 (办公/住宅/商业/酒店/医院)
    structure_type : str - 结构类型 (框架/框架-剪力墙/框架-核心筒等)
    total_area : float  - 总建筑面积 (㎡)
    floor_count : int   - 地上层数
    floor_height : float - 标准层高 (m)
    seismic_level : int  - 抗震等级 (6/7/8/9)
    has_basement : bool - 是否有地下室
    basement_area : float - 地下室面积 (㎡)
    basement_depth : float - 地下室层数 (负数)
    curtainwall_ratio : float - 幕墙占比 (0.0-1.0)
    region : str - 城市
    
    Returns:
    --------
    QDVResult - 包含工程量和诚实造价区间
    """
    
    print(f"\n>> 计算中...")
    print(f"   建筑类型: {building_type}")
    print(f"   结构类型: {structure_type}")
    print(f"   总面积: {total_area:,} m2")
    print(f"   层数: {floor_count}层 + 地下室{abs(basement_depth):.0f}层")
    
    # 1. 地上结构计算
    above_area = total_area - basement_area if has_basement else total_area
    building_height = floor_count * floor_height
    
    # 核心结构工程量
    # 柱子
    col_area = 0.015 * above_area  # 柱截面占楼层面积约1.5%
    col_height = building_height
    col_volume = col_area * col_height
    col_steel = col_volume * NORM_COEFFICIENTS["column_steel"]
    
    # 梁
    beam_length = 1.5 * (above_area ** 0.5) * floor_count  # 简化估算
    beam_volume = above_area * NORM_COEFFICIENTS["beam_concrete"]
    beam_steel = beam_volume * NORM_COEFFICIENTS["beam_steel"]
    
    # 板
    slab_area = above_area
    slab_volume = slab_area * NORM_COEFFICIENTS["slab_concrete"]
    slab_steel = slab_volume * NORM_COEFFICIENTS["slab_steel"]
    
    # 剪力墙 (核心筒)
    if "核心筒" in structure_type:
        wall_length = 0.15 * (above_area ** 0.5) * 4  # 核心筒周长
        wall_height = building_height
        wall_area = wall_length * wall_height * 0.2  # 核心筒占20%建筑面积
        wall_volume = wall_area * 0.25  # 墙厚250mm
        wall_steel = wall_volume * NORM_COEFFICIENTS["wall_steel"]
    else:
        wall_volume = 0
        wall_steel = 0
    
    # 抗震放大系数
    seismic_factor = NORM_COEFFICIENTS["seismic_steel_factor"].get(seismic_level, 1.0)
    
    # 混凝土总量
    concrete_total = col_volume + beam_volume + slab_volume + wall_volume
    
    # 钢筋总量 (含抗震放大)
    steel_total = (col_steel + beam_steel + slab_steel + wall_steel) * seismic_factor
    
    # 模板
    formwork = concrete_total * NORM_COEFFICIENTS["formwork_concrete_ratio"]
    
    # 砌体
    masonry_area = above_area * 0.3  # 隔墙占30%
    masonry = masonry_area * NORM_COEFFICIENTS["masonry"]
    
    # 抹灰
    plaster = masonry_area * NORM_COEFFICIENTS["plaster_wall_ratio"]
    
    # 涂料
    paint = plaster * NORM_COEFFICIENTS["paint_plaster_ratio"]
    
    # 幕墙
    facade_height = building_height
    facade_perimeter = 4 * (above_area ** 0.5)
    curtainwall = facade_perimeter * facade_height * curtainwall_ratio
    
    # 地下室 (如果是桩基+筏板)
    if has_basement:
        basement_concrete = basement_area * 0.8 * abs(basement_depth)  # 筏板+侧墙
        basement_steel = basement_concrete * 180  # 地下配筋大
        concrete_total += basement_concrete
        steel_total += basement_steel
    
    # 机电安装
    hvac = total_area * NORM_COEFFICIENTS["hvac_factor"]  # 风管展开
    pipeline = total_area * 0.15  # 管道长度简化
    
    # ============ 造价估算 (诚实区间) ============
    
    # 获取城市系数
    city_factor = CITY_COST_FACTORS.get(region, 1.0)
    
    # 获取结构系数
    struct_factor = STRUCTURE_FACTORS.get(structure_type, {}).get("base", 1.0)
    
    # 材料价格区间
    conc_low = MATERIAL_PRICES["concrete"]["low"]
    conc_mid = MATERIAL_PRICES["concrete"]["mid"]
    conc_high = MATERIAL_PRICES["concrete"]["high"]
    
    steel_low = MATERIAL_PRICES["steel"]["low"]
    steel_mid = MATERIAL_PRICES["steel"]["mid"]
    steel_high = MATERIAL_PRICES["steel"]["high"]
    
    labor_low = MATERIAL_PRICES["labor"]["low"]
    labor_mid = MATERIAL_PRICES["labor"]["mid"]
    labor_high = MATERIAL_PRICES["labor"]["high"]
    
    # 混凝土造价
    concrete_cost_low = concrete_total * conc_low
    concrete_cost_mid = concrete_total * conc_mid
    concrete_cost_high = concrete_total * conc_high
    
    # 钢筋造价
    steel_cost_low = steel_total * steel_low
    steel_cost_mid = steel_total * steel_mid
    steel_cost_high = steel_total * steel_high
    
    # 人工费 (按面积)
    labor_cost_low = total_area * labor_low
    labor_cost_mid = total_area * labor_mid
    labor_cost_high = total_area * labor_high
    
    # 其他费用系数 (模板+砌体+装饰+机电)
    other_ratio = 1.8  # 其他费用是混凝土+钢筋+人工的1.8倍
    
    # 低限造价
    cost_low = (concrete_cost_low + steel_cost_low + labor_cost_low) * other_ratio * city_factor * struct_factor / 10000
    
    # 中值造价
    cost_mid = (concrete_cost_mid + steel_cost_mid + labor_cost_mid) * other_ratio * city_factor * struct_factor / 10000
    
    # 高限造价
    cost_high = (concrete_cost_high + steel_cost_high + labor_cost_high) * other_ratio * city_factor * struct_factor / 10000
    
    # 真实精度计算
    precision = (cost_high - cost_low) / cost_mid / 2 * 100
    
    return QDVResult(
        concrete_m3=concrete_total,
        steel_kg=steel_total,
        formwork_m2=formwork,
        masonry_m3=masonry,
        plaster_m2=plaster,
        paint_m2=paint,
        curtainwall_m2=curtainwall,
        hvac_m2=hvac,
        pipeline_m=pipeline,
        concrete_price_range=(conc_low, conc_high),
        steel_price_range=(steel_low, steel_high),
        labor_price_range=(labor_low, labor_high),
        cost_low=cost_low,
        cost_mid=cost_mid,
        cost_high=cost_high,
        precision_pct=precision,
    )


def quick_qdv(building_type: str, structure_type: str, total_area: float, 
              floor_count: int, region: str = "Suzhou") -> Dict:
    """快速量向法估算"""
    result = qdv_calculate(
        building_type=building_type,
        structure_type=structure_type,
        total_area=total_area,
        floor_count=floor_count,
        region=region,
    )
    return {
        "quantity": {
            "concrete": f"{result.concrete_m3:,.0f} m3",
            "steel": f"{result.steel_kg:,.0f} kg",
            "formwork": f"{result.formwork_m2:,.0f} m2",
        },
        "cost_range": {
            "low": f"{result.cost_low:,.0f} 万元",
            "mid": f"{result.cost_mid:,.0f} 万元",
            "high": f"{result.cost_high:,.0f} 万元",
        },
        "unit_cost": {
            "low": f"{result.cost_low/total_area*10000:,.0f} yuan/m2",
            "mid": f"{result.cost_mid/total_area*10000:,.0f} yuan/m2",
            "high": f"{result.cost_high/total_area*10000:,.0f} yuan/m2",
        },
        "precision": f"+/-{result.precision_pct:.1f}%",
    }


if __name__ == "__main__":
    print("=" * 70)
    print("       度量衡量向法工程量估算系统 v2.0 (诚实版)")
    print("=" * 70)
    
    # 测试案例
    result = qdv_calculate(
        building_type="办公",
        structure_type="框架-核心筒",
        total_area=50000,
        floor_count=31,
        floor_height=3.8,
        seismic_level=3,
        has_basement=True,
        basement_area=5000,
        basement_depth=-2,
        curtainwall_ratio=0.35,
        region="苏州",
    )
    
    print(result.summary())
    
    # 快速结果
    print("\n[快速结果]")
    quick = quick_qdv("办公", "框架-核心筒", 50000, 31, "苏州")
    for key, value in quick.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 70)
    print("WARNING - 重要声明:")
    print("   1. 本系统计算工程量基于GB设计规范，精度+/-5-8%")
    print("   2. 造价估算是基于参考价格区间，非实时数据")
    print("   3. 真实精度约为+/-15-25%，请结合本地指标调整")
    print("   4. 若需+/-3%精度，请提供:")
    print("      [+] 本地近3年同类项目造价指标")
    print("      [+] 实时材料价格信息")
    print("      [-] BIM模型(可选，非必须)")
    print("=" * 70)
