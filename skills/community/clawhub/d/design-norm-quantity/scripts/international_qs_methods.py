# -*- coding: utf-8 -*-
"""
度量衡智库 · 国际QS方法论整合器 v1.0
=====================================

整合RICS NRM、Arcadis、利比、元素估量法等国际QS最佳实践
融合中国特色的测不准系统

核心整合内容：
1. RICS NRM 元素编码体系
2. Arcadis 区域化成本手册方法
3. Elemental Estimating 元素估量法
4. Whole Life Costing 全生命周期成本
5. 中国特色工程量清单计价标准

作者：度量衡智库
版本：1.0.0
日期：2026-04-03
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import os

# ============================================================
# 第一部分：RICS NRM 元素编码体系
# ============================================================

class RICSElementCode:
    """
    RICS NRM 元素分类编码体系
    
    基于RICS New Rules of Measurement标准
    """
    # 元素编码定义
    CODES = {
        "0xx": {"name": "场地准备", "en": "Site Preparation", "typical_pct": 3.0},
        "1xx": {"name": "基础工程", "en": "Foundation", "typical_pct": 10.0},
        "2xx": {"name": "结构框架", "en": "Structure Frame", "typical_pct": 18.0},
        "3xx": {"name": "楼板系统", "en": "Floors", "typical_pct": 12.0},
        "4xx": {"name": "屋面系统", "en": "Roof", "typical_pct": 4.0},
        "5xx": {"name": "外墙系统", "en": "External Walls", "typical_pct": 15.0},
        "6xx": {"name": "外窗系统", "en": "Windows", "typical_pct": 10.0},
        "7xx": {"name": "外门系统", "en": "External Doors", "typical_pct": 2.0},
        "8xx": {"name": "内墙系统", "en": "Internal Walls", "typical_pct": 5.0},
        "9xx": {"name": "内门系统", "en": "Internal Doors", "typical_pct": 3.0},
        "10xx": {"name": "墙面装修", "en": "Wall Finishes", "typical_pct": 6.0},
        "11xx": {"name": "楼地面装修", "en": "Floor Finishes", "typical_pct": 7.0},
        "12xx": {"name": "顶棚装修", "en": "Ceiling Finishes", "typical_pct": 4.0},
        "13xx": {"name": "给排水", "en": "Plumbing", "typical_pct": 8.0},
        "14xx": {"name": "电气系统", "en": "Electrical", "typical_pct": 10.0},
        "15xx": {"name": "暖通空调", "en": "HVAC", "typical_pct": 12.0},
        "16xx": {"name": "电梯系统", "en": "Lifts", "typical_pct": 5.0},
        "17xx": {"name": "消防系统", "en": "Fire Protection", "typical_pct": 4.0},
        "18xx": {"name": "设备系统", "en": "Equipment", "typical_pct": 3.0},
        "19xx": {"name": "家具软装", "en": "Furniture", "typical_pct": 2.0},
        "20xx": {"name": "特殊系统", "en": "Special Systems", "typical_pct": 3.0},
        "21xx": {"name": "外部工程", "en": "External Works", "typical_pct": 5.0},
    }

# ============================================================
# 第二部分：国际QS公司方法论
# ============================================================

class InternationalQSMethods:
    """
    国际QS公司方法论整合器
    
    整合：
    - Arcadis: 区域化成本手册
    - RLB: 元素估量法
    - Davis Langdon: 基准成本法
    - Tishman Speyer: 全生命周期成本
    """
    
    # Arcadis城市成本指数 (以深圳为基准)
    ARCADIS_CITY_INDEX = {
        "深圳": 1.12, "香港": 1.35, "广州": 1.10, "上海": 1.15,
        "北京": 1.18, "苏州": 1.08, "珠海": 1.08, "汕尾": 1.03,
        "东莞": 1.05, "佛山": 1.06
    }
    
    # RLB建筑类型调整系数
    RLB_BUILDING_ADJUSTMENT = {
        "住宅": 1.00, "办公": 1.15, "商业": 1.25, "酒店": 1.35,
        "医院": 1.45, "学校": 1.05, "工业": 0.85
    }
    
    # Davis Langdon结构类型调整
    DAVIS_STRUCTURE_ADJUSTMENT = {
        "框架结构": 1.00, "框架-剪力墙": 1.10, "剪力墙结构": 1.15,
        "框架-核心筒": 1.25, "钢结构": 1.30
    }
    
    # 质量等级系数
    QUALITY_MULTIPLIER = {
        "economy": 0.85, "standard": 1.00, "high": 1.20, "luxury": 1.50
    }
    
    @classmethod
    def arcadis_estimate(cls, base_cost: float, city: str, quality: str = "standard") -> Dict:
        """Arcadis方法论：区域化成本估算"""
        city_idx = cls.ARCADIS_CITY_INDEX.get(city, 1.0)
        quality_mult = cls.QUALITY_MULTIPLIER.get(quality, 1.0)
        return {
            "method": "Arcadis Regional Index",
            "city_index": city_idx,
            "quality_mult": quality_mult,
            "unit_cost": base_cost * city_idx * quality_mult
        }
    
    @classmethod
    def rlb_estimate(cls, total_area: float, building_type: str, structure: str, floors: int) -> Dict:
        """RLB方法论：元素估量法"""
        bld_adj = cls.RLB_BUILDING_ADJUSTMENT.get(building_type, 1.0)
        str_adj = cls.DAVIS_STRUCTURE_ADJUSTMENT.get(structure, 1.0)
        height_adj = 1.0 + max(0, floors - 30) * 0.01
        base_unit = 3500
        unit_cost = base_unit * bld_adj * str_adj * height_adj
        return {
            "method": "RLB Elemental Estimating",
            "building_adj": bld_adj,
            "structure_adj": str_adj,
            "height_adj": height_adj,
            "unit_cost": unit_cost,
            "total_cost": unit_cost * total_area
        }
    
    @classmethod
    def davis_estimate(cls, total_area: float, building_type: str, structure: str, 
                       location_factor: float = 0.85) -> Dict:
        """Davis Langdon方法论：基准成本法"""
        # 香港基准 (HKD/m² -> CNY)
        benchmark = {
            "住宅": 10500, "办公": 15000, "商业": 13000,
            "酒店": 17000, "医院": 18000, "学校": 10000
        }
        base = benchmark.get(building_type, 10500) * 0.85  # 汇率调整
        str_adj = cls.DAVIS_STRUCTURE_ADJUSTMENT.get(structure, 1.0)
        unit_cost = base * str_adj * location_factor
        return {
            "method": "Davis Langdon Benchmark",
            "benchmark": base,
            "location_factor": location_factor,
            "unit_cost": unit_cost,
            "total_cost": unit_cost * total_area,
            "range": {
                "low": unit_cost * 0.80,
                "mid": unit_cost,
                "high": unit_cost * 1.20
            }
        }
    
    @classmethod
    def whole_life_cost(cls, construction_cost: float, life_years: int = 50, 
                        discount_rate: float = 0.05) -> Dict:
        """Tishman方法论：全生命周期成本"""
        annual_om = construction_cost * 0.015  # 1.5% 运营维护
        annual_energy = construction_cost * 0.010  # 1.0% 能耗
        n_years = life_years
        r = discount_rate
        
        # 折现因子
        if r > 0:
            pv_factor = (1 - (1 + r) ** (-n_years)) / r
        else:
            pv_factor = n_years
            
        npv_om = (annual_om + annual_energy) * pv_factor
        residual = construction_cost * 0.10  # 10%残值
        
        total_lcc = construction_cost + npv_om - residual
        
        return {
            "method": "Tishman Whole Life Costing",
            "construction_cost": construction_cost,
            "annual_om": annual_om,
            "annual_energy": annual_energy,
            "npv_om_cost": npv_om,
            "residual_value": residual,
            "total_lcc": total_lcc,
            "lcc_ratio": total_lcc / construction_cost
        }

# ============================================================
# 第三部分：中国特色元素成本数据库
# ============================================================

CHINESE_ELEMENT_COSTS = {
    # 结构工程 (2xx-3xx)
    "2xx": {"name": "结构框架", "unit_cost_range": (600, 800, 1200), "typical_pct": 18},
    "3xx": {"name": "楼板系统", "unit_cost_range": (400, 550, 750), "typical_pct": 12},
    
    # 外墙围护 (5xx-7xx)
    "5xx": {"name": "外墙系统", "unit_cost_range": (450, 650, 900), "typical_pct": 15},
    "6xx": {"name": "外窗幕墙", "unit_cost_range": (350, 500, 800), "typical_pct": 10},
    
    # 内部装修 (10xx-12xx)
    "10xx": {"name": "墙面装修", "unit_cost_range": (150, 220, 350), "typical_pct": 6},
    "11xx": {"name": "楼地面装修", "unit_cost_range": (180, 280, 450), "typical_pct": 7},
    "12xx": {"name": "顶棚装修", "unit_cost_range": (100, 150, 250), "typical_pct": 4},
    
    # 机电安装 (13xx-17xx)
    "13xx": {"name": "给排水", "unit_cost_range": (200, 300, 450), "typical_pct": 8},
    "14xx": {"name": "电气系统", "unit_cost_range": (280, 400, 600), "typical_pct": 10},
    "15xx": {"name": "暖通空调", "unit_cost_range": (350, 500, 750), "typical_pct": 12},
    "16xx": {"name": "电梯系统", "unit_cost_range": (80, 150, 300), "typical_pct": 5},
    "17xx": {"name": "消防系统", "unit_cost_range": (100, 150, 250), "typical_pct": 4},
    
    # 基础工程 (0xx-1xx)
    "0xx": {"name": "场地准备", "unit_cost_range": (50, 80, 150), "typical_pct": 3},
    "1xx": {"name": "基础工程", "unit_cost_range": (300, 450, 700), "typical_pct": 10},
}

# ============================================================
# 第四部分：快速使用接口
# ============================================================

def quick_qs_estimate(
    total_area: float,
    building_type: str,
    structure_type: str,
    city: str,
    floor_count: int = 18,
    quality_level: str = "standard"
) -> Dict:
    """
    快速国际QS整合估算
    
    综合运用Arcadis、RLB、Davis Langdon方法论
    
    Args:
        total_area: 总建筑面积 (m²)
        building_type: 建筑类型
        structure_type: 结构类型
        city: 城市
        floor_count: 层数
        quality_level: 质量等级
    
    Returns:
        综合估算结果
    """
    # 1. Arcadis估算
    arcadis = InternationalQSMethods.arcadis_estimate(
        base_cost=5000, city=city, quality=quality_level
    )
    
    # 2. RLB估算
    rlb = InternationalQSMethods.rlb_estimate(
        total_area=total_area,
        building_type=building_type,
        structure=structure_type,
        floors=floor_count
    )
    
    # 3. Davis Langdon估算
    location_factors = {
        "深圳": 0.85, "广州": 0.80, "上海": 0.85, 
        "香港": 1.00, "北京": 0.90, "苏州": 0.75
    }
    davis = InternationalQSMethods.davis_estimate(
        total_area=total_area,
        building_type=building_type,
        structure=structure_type,
        location_factor=location_factors.get(city, 0.80)
    )
    
    # 4. 融合估算 (国际方法30% + 国内方法70%)
    intl_avg = (arcadis["unit_cost"] + rlb["unit_cost"] + davis["unit_cost"]) / 3
    chinese_base = 4500  # 国内基础值
    fused = intl_avg * 0.30 + chinese_base * 0.70
    
    # 5. 全生命周期成本
    construction_cost = fused * total_area
    life_cycle = InternationalQSMethods.whole_life_cost(construction_cost)
    
    # 6. 元素分解
    breakdown = generate_elemental_breakdown(total_area, fused)
    
    return {
        "project_info": {
            "total_area": total_area,
            "building_type": building_type,
            "structure_type": structure_type,
            "city": city,
            "floor_count": floor_count,
            "quality_level": quality_level
        },
        "method_estimates": {
            "arcadis": arcadis,
            "rlb": rlb,
            "davis_langdon": davis
        },
        "fused_estimate": {
            "unit_cost": fused,
            "total_cost": fused * total_area,
            "range": {
                "low": fused * 0.85,
                "mid": fused,
                "high": fused * 1.15
            }
        },
        "whole_life_cost": life_cycle,
        "elemental_breakdown": breakdown
    }

def generate_elemental_breakdown(total_area: float, unit_cost: float) -> Dict:
    """生成RICS元素成本分解表"""
    breakdown = []
    total_pct = 0
    
    for code, data in CHINESE_ELEMENT_COSTS.items():
        low, mid, high = data["unit_cost_range"]
        pct = data["typical_pct"]
        subtotal = unit_cost * total_area * pct / 100
        
        breakdown.append({
            "code": code,
            "name": data["name"],
            "unit_cost_range": f"{low:,.0f}~{high:,.0f}",
            "percentage": pct,
            "subtotal": subtotal,
            "subtotal_wan": f"{subtotal/10000:,.1f}万"
        })
        total_pct += pct
    
    return {
        "items": breakdown,
        "total_pct": total_pct,
        "note": "RICS NRM Elemental Cost Breakdown - 度量衡智库"
    }

# ============================================================
# 测试入口
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DLHZ International QS Integration v1.0")
    print("International QS + Chinese Uncertainty System")
    print("=" * 60)
    
    result = quick_qs_estimate(
        total_area=50000,
        building_type="办公",
        structure_type="框架-核心筒",
        city="深圳",
        floor_count=30,
        quality_level="high"
    )
    
    p = result["project_info"]
    print(f"\n[Project Info]")
    print(f"  Type: {p['building_type']} | Structure: {p['structure_type']}")
    print(f"  City: {p['city']} | Area: {p['total_area']:,} m2 | Floors: {p['floor_count']}")
    
    print(f"\n[International QS Estimates]")
    for method, res in result["method_estimates"].items():
        print(f"  {method}: {res['unit_cost']:,.0f} CNY/m2")
    
    f = result["fused_estimate"]
    print(f"\n[Fused Estimate]")
    print(f"  Unit Cost: {f['unit_cost']:,.0f} CNY/m2")
    print(f"  Total Cost: {f['total_cost']/10000:,.0f} 10k CNY")
    print(f"  Range: {f['range']['low']:,.0f} ~ {f['range']['high']:,.0f} CNY/m2")
    
    w = result["whole_life_cost"]
    print(f"\n[Whole Life Cost (50yr)]")
    print(f"  Construction: {w['construction_cost']/10000:,.0f} 10k CNY")
    print(f"  Total LCC: {w['total_lcc']/10000:,.0f} 10k CNY")
    print(f"  LCC Ratio: {w['lcc_ratio']:.2f}")
    
    print(f"\n[RICS Elemental Cost Breakdown]")
    for item in result["elemental_breakdown"]["items"][:6]:
        print(f"  {item['code']} {item['name']}: {item['subtotal_wan']} ({item['percentage']}%)")
    
    print("\n" + "=" * 60)
    print("Uncertainty = International Wisdom + Chinese Characteristics")
    print("=" * 60)
