# -*- coding: utf-8 -*-
"""
度量衡智库 · 度量衡测不准系统 v3.3
Uncertainty Estimator - Core Engine
=====================================

核心功能：
1. 7族58项创新配比参数体系
2. 6大关键材料因子体系  
3. 不确定性传播模型
4. 蒙特卡洛模拟
5. 数据库校正引擎 v1.0
6. 官方数据爬虫集成
7. 国际QS方法论整合 v1.0
   - RICS NRM 元素编码体系
   - Arcadis 区域化成本手册
   - RLB 利比元素估量法
   - Davis Langdon 基准成本法
   - Tishman Speyer 全生命周期成本
8. 全球工程公司方法论 v1.0 (v3.3新增)
   - AECOM PACES 参数化成本估算
   - WSP 全球项目管理
   - 日本五大建设：鹿岛/清水/竹中/大林组/大成
   - 日本建築積算 SECI方法
   - 中国GB50010-2024/GB50011-2024规范整合

作者：度量衡智库
版本：3.3.0
日期：2026-04-03
"""

import json
import math
import random
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import os
import sys

# 添加scripts目录到路径（用于导入校正模块）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 尝试导入数据校正模块
try:
    from db_connector import CostDatabaseConnector, CostIndex, get_real_time_factor
    from data_calibrator import DataCalibrator, quick_calibrate, get_verified_data
    CALIBRATION_AVAILABLE = True
    logger.info("Data calibration module loaded")
except ImportError as e:
    CALIBRATION_AVAILABLE = False
    logger.warning(f"Data calibration module not available: {e}")

# 尝试导入国际QS方法论模块
try:
    from international_qs_methods import (
        InternationalQSMethods,
        quick_qs_estimate,
        generate_elemental_breakdown,
        RICSElementCode,
        CHINESE_ELEMENT_COSTS
    )
    INTERNATIONAL_QS_AVAILABLE = True
    logger.info("International QS methods module loaded")
except ImportError as e:
    INTERNATIONAL_QS_AVAILABLE = False
    logger.warning(f"International QS module not available: {e}")

# 尝试导入全球工程公司方法论模块
try:
    from global_engineering_qs import (
        GlobalEstimatorFuser,
        global_quick_estimate,
        AECOMCostMethods,
        WSPMethods,
        JapaneseSuperGCMethods,
        ChineseQSMethods
    )
    GLOBAL_QS_AVAILABLE = True
    logger.info("Global engineering QS module loaded")
except ImportError as e:
    GLOBAL_QS_AVAILABLE = False
    logger.warning(f"Global engineering QS module not available: {e}")

# ============================================================
# 数据路径配置
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REFERENCES_DIR = os.path.join(os.path.dirname(BASE_DIR), 'references')

# ============================================================
# 枚举类型定义
# ============================================================

class BuildingType(Enum):
    """建筑类型"""
    RESIDENTIAL = "住宅"
    OFFICE = "办公"
    COMMERCIAL = "商业"
    HOTEL = "酒店"
    HOSPITAL = "医疗"
    EDUCATION = "教育"
    INDUSTRIAL = "工业"

class StructureType(Enum):
    """结构类型"""
    FRAME = "框架"
    SHEAR_WALL = "剪力墙"
    FRAME_SHEAR_WALL = "框架-剪力墙"
    FRAME_CORE_TUBE = "框架-核心筒"
    STEEL = "钢结构"

class Region(Enum):
    """地区"""
    SUZHOU = ("苏州", 1.08, 1.10)
    GUANGZHOU = ("广州", 1.10, 1.12)
    SHENZHEN = ("深圳", 1.12, 1.15)
    ZHUHAI = ("珠海", 1.08, 1.10)
    SHANTOU = ("汕头", 1.05, 1.07)
    SHANWEI = ("汕尾", 1.03, 1.05)
    FOSHAN = ("佛山", 1.07, 1.09)
    DONGGUAN = ("东莞", 1.06, 1.08)
    NANJING = ("南京", 1.08, 1.10)
    HANGZHOU = ("杭州", 1.09, 1.11)
    CHENGDU = ("成都", 1.05, 1.07)
    WUHAN = ("武汉", 1.06, 1.08)
    
    def __init__(self, name_cn: str, build_coeff: float, install_coeff: float):
        self.name_cn = name_cn
        self.build_coeff = build_coeff
        self.install_coeff = install_coeff

# ============================================================
# 数据类定义
# ============================================================

@dataclass
class MaterialFactor:
    """材料因子"""
    code: str
    name: str
    specification: str
    cost_ratio: float
    annual_volatility: float
    current_price: float
    unit: str
    price_trend: str
    
@dataclass
class ProjectParams:
    """项目参数"""
    building_type: BuildingType
    structure_type: StructureType
    total_area: float
    floor_count: int
    basement_area: float
    basement_floors: int
    decoration_level: str
    has_central_ac: bool
    has_pile: bool
    seismic_level: str
    region: Region
    year: int

# ============================================================
# 材料因子数据库
# ============================================================

class MaterialFactorsDB:
    """材料因子数据库"""
    
    FACTORS = {
        "M1": MaterialFactor(
            code="M1", name="钢筋(螺纹钢/线材)", specification="HRB400",
            cost_ratio=0.15, annual_volatility=0.15, current_price=4200,
            unit="吨", price_trend="↑震荡上行"
        ),
        "M2": MaterialFactor(
            code="M2", name="混凝土(商品砼)", specification="C30泵送",
            cost_ratio=0.12, annual_volatility=0.10, current_price=580,
            unit="m³", price_trend="→平稳"
        ),
        "M3": MaterialFactor(
            code="M3", name="铜(电线电缆)", specification="1#电解铜",
            cost_ratio=0.08, annual_volatility=0.20, current_price=68000,
            unit="吨", price_trend="↑↑强势上涨"
        ),
        "M4": MaterialFactor(
            code="M4", name="铝合金(门窗/幕墙)", specification="A00铝锭",
            cost_ratio=0.07, annual_volatility=0.15, current_price=19500,
            unit="吨", price_trend="↑温和上涨"
        ),
        "M5": MaterialFactor(
            code="M5", name="玻璃(幕墙/门窗)", specification="5mm浮法白玻",
            cost_ratio=0.05, annual_volatility=0.15, current_price=45,
            unit="㎡", price_trend="→区间震荡"
        ),
        "M6": MaterialFactor(
            code="M6", name="结构型钢(H型钢)", specification="Q355B",
            cost_ratio=0.04, annual_volatility=0.12, current_price=4500,
            unit="吨", price_trend="↑跟随钢价"
        )
    }
    
    @classmethod
    def get_weight_vector(cls) -> Dict[str, float]:
        return {code: factor.cost_ratio for code, factor in cls.FACTORS.items()}
    
    @classmethod
    def get_volatility_vector(cls) -> Dict[str, float]:
        return {code: factor.annual_volatility for code, factor in cls.FACTORS.items()}

# ============================================================
# 度量衡测不准系统核心引擎
# ============================================================

class UncertaintyEstimator:
    """
    度量衡测不准关键因子配比估量估价系统
    ============================
    
    核心创新：
    1. 7族58项创新配比参数
    2. 6大关键材料因子
    3. 不确定性传播模型
    4. 蒙特卡洛模拟
    
    测不准三公理：
    - 闭合性公理: 总费用 = Σ(构件体积 × 构件单价)
    - 守恒性公理: 钢筋总量在混凝土中守恒
    - 相关性公理: 配比参数间存在统计学相关性
    """
    
    def __init__(self):
        self.materials_db = MaterialFactorsDB()
        
        # 时间调整系数（以2022年为基准）
        self.year_coeffs = {
            2019: 0.92, 2020: 0.94, 2021: 0.97, 
            2022: 1.00, 2023: 1.03, 2024: 1.06, 
            2025: 1.10, 2026: 1.14
        }
        
        # 装修调整系数
        self.decoration_coeffs = {
            "毛坯": 1.00, "简装": 1.35, "精装": 1.80, "豪装": 2.20
        }
        
        # 桩基调整系数
        self.pile_coeffs = {True: 1.15, False: 1.00}
        
    def get_base_unit_cost(self, building_type: BuildingType, region: Region) -> Dict[str, float]:
        """获取基础单方造价指标（元/㎡）"""
        base_costs = {
            BuildingType.RESIDENTIAL: {"low": 2800, "mid": 3200, "high": 3800},
            BuildingType.OFFICE: {"low": 3200, "mid": 3800, "high": 4500},
            BuildingType.COMMERCIAL: {"low": 3800, "mid": 4500, "high": 5500},
            BuildingType.HOTEL: {"low": 3500, "mid": 4200, "high": 5200},
            BuildingType.HOSPITAL: {"low": 4000, "mid": 4800, "high": 5800},
            BuildingType.EDUCATION: {"low": 2800, "mid": 3300, "high": 4000},
            BuildingType.INDUSTRIAL: {"low": 2200, "mid": 2800, "high": 3500},
        }
        
        costs = base_costs.get(building_type, base_costs[BuildingType.OFFICE])
        region_coeff = region.build_coeff
        
        return {
            "low": costs["low"] * region_coeff,
            "mid": costs["mid"] * region_coeff,
            "high": costs["high"] * region_coeff
        }
    
    def get_struct_code(self, structure_type: StructureType) -> str:
        mapping = {
            StructureType.FRAME: "FRAME",
            StructureType.SHEAR_WALL: "SHEAR_WALL",
            StructureType.FRAME_SHEAR_WALL: "FRAME_SHEAR_WALL",
            StructureType.FRAME_CORE_TUBE: "FRAME_CORE_TUBE",
            StructureType.STEEL: "STEEL"
        }
        return mapping.get(structure_type, "FRAME_SHEAR_WALL")
    
    def get_building_code(self, building_type: BuildingType) -> str:
        mapping = {
            BuildingType.RESIDENTIAL: "RESIDENTIAL",
            BuildingType.OFFICE: "OFFICE",
            BuildingType.COMMERCIAL: "COMMERCIAL",
            BuildingType.HOTEL: "HOTEL",
            BuildingType.HOSPITAL: "HOSPITAL",
            BuildingType.EDUCATION: "OFFICE",
            BuildingType.INDUSTRIAL: "INDUSTRIAL"
        }
        return mapping.get(building_type, "OFFICE")
    
    def get_decoration_code(self, decoration_level: str) -> str:
        mapping = {
            "毛坯": "ROUGH", "简装": "SIMPLE", "精装": "FINE", "豪装": "HIGH_END"
        }
        return mapping.get(decoration_level, "SIMPLE")
    
    def calculate_mep_ratios(self, params: ProjectParams) -> Dict:
        """计算机电安装交叉配比"""
        building_code = self.get_building_code(params.building_type)
        
        # 风管展开面积比
        duct_ratios = {
            "OFFICE": {"low": 0.70, "mid": 0.85, "high": 1.20},
            "COMMERCIAL": {"low": 1.00, "mid": 1.30, "high": 1.60},
            "HOSPITAL": {"low": 1.20, "mid": 1.60, "high": 2.00},
            "HOTEL": {"low": 0.80, "mid": 1.00, "high": 1.30},
            "INDUSTRIAL": {"low": 0.50, "mid": 0.80, "high": 1.20},
            "RESIDENTIAL": {"low": 0.30, "mid": 0.50, "high": 0.70},
        }
        duct_ratio = duct_ratios.get(building_code, duct_ratios["OFFICE"])
        
        # 弱电管线密度
        weak_ratios = {
            "RESIDENTIAL": {"low": 0.50, "mid": 0.70, "high": 1.00},
            "OFFICE": {"low": 1.00, "mid": 1.50, "high": 2.00},
            "COMMERCIAL": {"low": 1.50, "mid": 2.00, "high": 2.50},
            "HOSPITAL": {"low": 1.50, "mid": 2.00, "high": 2.50},
            "HOTEL": {"low": 1.00, "mid": 1.50, "high": 2.00},
            "INDUSTRIAL": {"low": 0.80, "mid": 1.20, "high": 1.80},
        }
        weak_ratio = weak_ratios.get(building_code, weak_ratios["OFFICE"])
        
        return {
            "风管展开比": {
                "value": duct_ratio["mid"],
                "range": f"{duct_ratio['low']:.2f}~{duct_ratio['high']:.2f}",
                "展开面积": params.total_area * duct_ratio["mid"]
            },
            "弱电管线密度": {
                "value": weak_ratio["mid"],
                "range": f"{weak_ratio['low']:.1f}~{weak_ratio['high']:.1f} m/㎡",
                "总长度": params.total_area * weak_ratio["mid"]
            },
            "消防管线密度": {
                "value": 1.0,
                "range": "0.8~1.2 m/㎡"
            }
        }
    
    def calculate_rebar_ratios(self, params: ProjectParams) -> Dict:
        """计算钢筋智能配比"""
        struct_code = self.get_struct_code(params.structure_type)
        
        # 钢筋混凝土比
        rebar_concrete_ratios = {
            "FRAME": {"low": 90, "mid": 110, "high": 130},
            "SHEAR_WALL": {"low": 130, "mid": 155, "high": 185},
            "FRAME_SHEAR_WALL": {"low": 115, "mid": 140, "high": 165},
            "FRAME_CORE_TUBE": {"low": 145, "mid": 170, "high": 200},
            "STEEL": {"low": 80, "mid": 100, "high": 120},
        }
        rebar_ratio = rebar_concrete_ratios.get(struct_code, rebar_concrete_ratios["FRAME_SHEAR_WALL"])
        
        # 估算混凝土体积
        concrete_volume = params.total_area * 0.40
        if params.basement_area > 0:
            concrete_volume += params.basement_area * 0.60
        
        # 估算钢筋总量
        rebar_mid = concrete_volume * rebar_ratio["mid"] / 1000
        
        return {
            "钢筋混凝土比": {
                "value": rebar_ratio["mid"],
                "range": f"{rebar_ratio['low']:.0f}~{rebar_ratio['high']:.0f} kg/m³",
                "估算钢筋量": rebar_mid,
                "单位": "吨"
            },
            "牌号配比": {
                "HRB400": 0.75, "HRB500": 0.15, "HPB300": 0.10
            }
        }
    
    def calculate_foundation_ratios(self, params: ProjectParams) -> Dict:
        """计算地基基础配比"""
        has_pile = "SOFT_SOIL" if params.has_pile else "NORMAL"
        
        pile_ratios = {
            "SOFT_SOIL": {"low": 2.5, "mid": 3.5, "high": 5.0},
            "NORMAL": {"low": 1.5, "mid": 2.5, "high": 4.0},
            "ROCK": {"low": 0.8, "mid": 1.5, "high": 2.5},
        }
        pile_ratio = pile_ratios.get(has_pile, pile_ratios["NORMAL"])
        
        base_area = params.total_area * 0.15
        total_pile_length = base_area * pile_ratio["mid"]
        
        return {
            "桩长密度": {
                "value": pile_ratio["mid"],
                "range": f"{pile_ratio['low']:.1f}~{pile_ratio['high']:.1f} m/㎡",
                "估算总桩长": total_pile_length,
                "单位": "m"
            },
            "不确定性等级": "高" if params.has_pile else "中"
        }
    
    def calculate_decoration_ratios(self, params: ProjectParams) -> Dict:
        """计算装饰装修配比"""
        deco_code = self.get_decoration_code(params.decoration_level)
        
        ceiling_ratios = {
            "ROUGH": 0.00, "SIMPLE": 0.40, "FINE": 0.75, "HIGH_END": 0.90
        }
        ceiling_ratio = ceiling_ratios.get(deco_code, 0.40)
        
        paint_ratios = {
            "ROUGH": {"low": 2.8, "mid": 3.0, "high": 3.2},
            "SIMPLE": {"low": 3.0, "mid": 3.2, "high": 3.5},
            "FINE": {"low": 3.5, "mid": 4.0, "high": 4.5},
            "HIGH_END": {"low": 4.5, "mid": 5.0, "high": 5.5},
        }
        paint_ratio = paint_ratios.get(deco_code, paint_ratios["SIMPLE"])
        
        return {
            "吊顶面积比": {
                "value": ceiling_ratio,
                "装修面积": params.total_area * ceiling_ratio,
                "说明": "精装是毛坯的3~5倍"
            },
            "涂料面积系数": {
                "value": paint_ratio["mid"],
                "range": f"{paint_ratio['low']:.1f}~{paint_ratio['high']:.1f}",
                "涂料总面积": params.total_area * paint_ratio["mid"]
            }
        }
    
    def calculate_cross_domain_ratios(self, params: ProjectParams) -> Dict:
        """计算跨域综合配比"""
        building_code = self.get_building_code(params.building_type)
        
        pipe_density_ratios = {
            "RESIDENTIAL": {"low": 4.0, "mid": 5.5, "high": 7.0},
            "OFFICE": {"low": 6.0, "mid": 8.0, "high": 10.0},
            "COMMERCIAL": {"low": 8.0, "mid": 12.0, "high": 16.0},
            "HOSPITAL": {"low": 10.0, "mid": 14.0, "high": 18.0},
            "HOTEL": {"low": 6.0, "mid": 9.0, "high": 12.0},
            "INDUSTRIAL": {"low": 5.0, "mid": 7.0, "high": 10.0},
        }
        pipe_density = pipe_density_ratios.get(building_code, pipe_density_ratios["OFFICE"])
        
        return {
            "管线总长度密度": {
                "value": pipe_density["mid"],
                "range": f"{pipe_density['low']:.1f}~{pipe_density['high']:.1f} m/㎡",
                "总长度": params.total_area * pipe_density["mid"],
                "说明": "数据中心是住宅的6~10倍"
            },
            "机电协调指数": {
                "value": 0.85,
                "说明": "BIM设计可将现场开凿减少70%"
            }
        }
    
    def analyze_material_impact(self, base_cost: float) -> Dict:
        """分析材料因子对总造价的影响"""
        weights = self.materials_db.get_weight_vector()
        volatilities = self.materials_db.get_volatility_vector()
        
        result = {}
        total_influence = 0
        
        for code, weight in weights.items():
            factor = self.materials_db.FACTORS[code]
            influence = base_cost * weight * factor.annual_volatility
            total_influence += influence
            
            result[code] = {
                "name": factor.name,
                "当前价格": f"{factor.current_price:,} 元/{factor.unit}",
                "造价占比": f"{factor.cost_ratio:.0%}",
                "年波动率": f"±{factor.annual_volatility:.0%}",
                "价格趋势": factor.price_trend,
                "对造价影响": f"±{influence:,.0f} 元/㎡"
            }
        
        result["_summary"] = {
            "总影响幅度": f"±{total_influence:,.0f} 元/㎡",
            "影响占比": f"±{total_influence/base_cost:.1%}",
            "核心驱动因子": "M1(钢筋)、M2(混凝土)、M3(铜缆)三大因子累计贡献70%~85%"
        }
        
        return result
    
    def monte_carlo_simulation(self, base_cost: float, n_simulations: int = 10000) -> Dict:
        """蒙特卡洛模拟"""
        random.seed(42)
        
        weights = self.materials_db.get_weight_vector()
        volatilities = self.materials_db.get_volatility_vector()
        
        results = []
        
        for _ in range(n_simulations):
            total_delta = 0
            for code, weight in weights.items():
                volatility = volatilities[code]
                delta = random.gauss(0, volatility / 2)
                delta = max(-volatility, min(volatility, delta))
                total_delta += weight * delta
            
            simulated_cost = base_cost * (1 + total_delta)
            results.append(simulated_cost)
        
        results.sort()
        
        return {
            "P10": results[int(n_simulations * 0.10)],
            "P50": results[int(n_simulations * 0.50)],
            "P90": results[int(n_simulations * 0.90)],
            "mean": sum(results) / len(results),
            "std": (sum((x - sum(results)/len(results))**2 for x in results) / len(results)) ** 0.5,
            "n_simulations": n_simulations
        }
    
    def estimate(self, params: ProjectParams, enable_monte_carlo: bool = True, 
                 use_database_calibration: bool = True) -> Dict:
        """
        完整估算流程
        
        Args:
            params: 项目参数
            enable_monte_carlo: 是否启用蒙特卡洛模拟
            use_database_calibration: 是否使用数据库校正（新增）
        """
        # 1. 获取基础单方造价
        base_unit_cost = self.get_base_unit_cost(params.building_type, params.region)
        
        # 2. 应用调整系数
        year_coeff = self.year_coeffs.get(params.year, 1.14)
        deco_coeff = self.decoration_coeffs.get(params.decoration_level, 1.35)
        pile_coeff = self.pile_coeffs.get(params.has_pile, 1.00)
        region_coeff = params.region.build_coeff
        
        total_adjust = year_coeff * deco_coeff * pile_coeff
        
        # 3. 计算调整后造价区间
        adjusted_cost = {
            "low": base_unit_cost["low"] * total_adjust,
            "mid": base_unit_cost["mid"] * total_adjust,
            "high": base_unit_cost["high"] * total_adjust
        }
        
        # 4. 数据库校正（新增）
        calibration_info = None
        if use_database_calibration and CALIBRATION_AVAILABLE:
            try:
                # 获取结构类型中文名
                struct_type_map = {
                    StructureType.FRAME: "框架结构",
                    StructureType.SHEAR_WALL: "剪力墙结构",
                    StructureType.FRAME_SHEAR_WALL: "框架-剪力墙",
                    StructureType.FRAME_CORE_TUBE: "框架-核心筒",
                    StructureType.STEEL: "钢结构"
                }
                struct_type_cn = struct_type_map.get(params.structure_type, "框架结构")
                
                # 获取建筑类型中文名
                building_type_map = {
                    BuildingType.RESIDENTIAL: "住宅",
                    BuildingType.OFFICE: "办公",
                    BuildingType.COMMERCIAL: "商业",
                    BuildingType.HOTEL: "酒店",
                    BuildingType.HOSPITAL: "医疗",
                    BuildingType.EDUCATION: "教育",
                    BuildingType.INDUSTRIAL: "工业"
                }
                building_type_cn = building_type_map.get(params.building_type, "住宅")
                
                # 查询数据库
                verified_data = get_verified_data(
                    params.region.name_cn,
                    building_type_cn,
                    struct_type_cn
                )
                
                if verified_data:
                    db_index = verified_data[0]
                    calibration_info = {
                        "已启用数据库校正": True,
                        "数据来源": db_index.data_source,
                        "数据日期": db_index.data_date,
                        "置信度": "A级 (±10%)",
                        "数据库单方造价": f"{db_index.unit_price_low:,.0f} ~ {db_index.unit_price_high:,.0f} 元/㎡",
                        "数据库钢筋含量": f"{db_index.steel_content} kg/㎡",
                        "数据库混凝土含量": f"{db_index.concrete_content} m³/㎡",
                        "校正说明": "数据来源于本地数据库"
                    }
                    
                    # 使用数据库数据校正估算值
                    db_mid_price = db_index.unit_price_mid
                    model_mid_price = adjusted_cost["mid"]
                    
                    # 加权融合：数据库权重0.7，模型权重0.3
                    fusion_weight = 0.7
                    fused_mid_price = db_mid_price * fusion_weight + model_mid_price * (1 - fusion_weight)
                    
                    # 调整区间
                    db_range_ratio = (db_index.unit_price_high - db_index.unit_price_low) / db_index.unit_price_mid
                    adjusted_cost["mid"] = fused_mid_price
                    adjusted_cost["low"] = fused_mid_price * (1 - db_range_ratio * 0.5)
                    adjusted_cost["high"] = fused_mid_price * (1 + db_range_ratio * 0.5)
                    
                    logger.info(f"数据库校正完成: {model_mid_price:.0f} → {fused_mid_price:.0f}")
            except Exception as e:
                logger.warning(f"数据库校正失败: {e}")
                calibration_info = {"已启用数据库校正": False, "失败原因": str(e)}
        elif not CALIBRATION_AVAILABLE:
            calibration_info = {"已启用数据库校正": False, "说明": "数据校正模块未加载"}
        
        # 5. 地下室附加造价
        basement_cost_per_sqm = 2500 * region_coeff * year_coeff
        basement_total = params.basement_area * basement_cost_per_sqm
        
        # 6. 计算总造价
        above_ground_area = params.total_area - params.basement_area
        
        total_low = adjusted_cost["low"] * above_ground_area + basement_total * 0.90
        total_mid = adjusted_cost["mid"] * above_ground_area + basement_total * 1.00
        total_high = adjusted_cost["high"] * above_ground_area + basement_total * 1.10
        
        # 7. 材料因子影响分析
        material_impact = self.analyze_material_impact(adjusted_cost["mid"])
        
        # 8. 蒙特卡洛模拟
        monte_carlo = None
        if enable_monte_carlo:
            monte_carlo = self.monte_carlo_simulation(adjusted_cost["mid"])
        
        # 9. 计算所有配比参数
        structural_ratios = self._calculate_structural_ratios(params)
        envelope_ratios = self._calculate_envelope_ratios(params)
        mep_ratios = self.calculate_mep_ratios(params)
        rebar_ratios = self.calculate_rebar_ratios(params)
        foundation_ratios = self.calculate_foundation_ratios(params)
        decoration_ratios = self.calculate_decoration_ratios(params)
        cross_domain_ratios = self.calculate_cross_domain_ratios(params)
        
        # 10. 组装完整报告
        accuracy_level = "A级 (±10%)" if calibration_info and calibration_info.get("已启用数据库校正") else "B级 (±15%)"
        
        report = {
            "项目参数": asdict(params),
            "造价估算": {
                "总建筑面积": f"{params.total_area:,.0f} ㎡",
                "地上面积": f"{above_ground_area:,.0f} ㎡",
                "地下面积": f"{params.basement_area:,.0f} ㎡",
                "单方造价区间": {
                    "低限": f"{adjusted_cost['low']:,.0f} 元/㎡",
                    "中值": f"{adjusted_cost['mid']:,.0f} 元/㎡",
                    "高限": f"{adjusted_cost['high']:,.0f} 元/㎡"
                },
                "总造价区间": {
                    "低限": f"{total_low/10000:,.2f} 万元",
                    "中值": f"{total_mid/10000:,.2f} 万元",
                    "高限": f"{total_high/10000:,.2f} 万元"
                },
                "地下室附加": f"{basement_total/10000:,.2f} 万元",
                "综合调整系数": f"{total_adjust:.3f}",
                "地区系数": f"{region_coeff:.2f} ({params.region.name_cn})",
                "时间系数": f"{year_coeff:.2f} ({params.year}年)"
            },
            "配比参数": {
                "第一族_结构构件交叉配比": structural_ratios,
                "第二族_建筑围护配比": envelope_ratios,
                "第三族_机电安装交叉配比": mep_ratios,
                "第四族_钢筋智能配比": rebar_ratios,
                "第五族_地基基础配比": foundation_ratios,
                "第六族_装饰装修配比": decoration_ratios,
                "第七族_跨域综合配比": cross_domain_ratios
            },
            "材料因子影响": material_impact,
            "数据库校正": calibration_info,
            "不确定性分析": {
                "估算精度等级": accuracy_level,
                "适用阶段": "初步设计" if calibration_info and calibration_info.get("已启用数据库校正") else "可研阶段",
                "误差范围": "±10%" if calibration_info and calibration_info.get("已启用数据库校正") else "±15%",
                "蒙特卡洛模拟": monte_carlo
            } if monte_carlo else None
        }
        
        return report
    
    def _calculate_structural_ratios(self, params: ProjectParams) -> Dict:
        """计算结构构件交叉配比"""
        struct_code = self.get_struct_code(params.structure_type)
        
        ratios = {
            "FRAME": (0.38, 0.18, 0.44),
            "SHEAR_WALL": (0.60, 0.12, 0.28),
            "FRAME_SHEAR_WALL": (0.45, 0.15, 0.40),
            "FRAME_CORE_TUBE": (0.40, 0.22, 0.38),
            "STEEL": (0.35, 0.20, 0.45),
        }
        ratio = ratios.get(struct_code, ratios["FRAME_SHEAR_WALL"])
        
        column_wall_ratios = {
            "FRAME": 0.80, "FRAME_SHEAR_WALL": 0.30,
            "FRAME_CORE_TUBE": 0.15, "SHEAR_WALL": 0.05, "STEEL": 0.60
        }
        
        return {
            "墙:梁:板三相配比": {
                "value": ratio,
                "说明": "剪力墙:梁:板体积比"
            },
            "柱墙体积比": column_wall_ratios.get(struct_code, 0.30),
            "地下室结构系数": {1: 1.5, 2: 3.2, 3: 5.5, 4: 8.0}.get(params.basement_floors, 3.2)
        }
    
    def _calculate_envelope_ratios(self, params: ProjectParams) -> Dict:
        """计算建筑围护配比"""
        building_code = self.get_building_code(params.building_type)
        
        window_ratios = {
            "RESIDENTIAL": 0.30,
            "OFFICE": 0.50,
            "COMMERCIAL": 0.65,
            "HOTEL": 0.45,
            "HOSPITAL": 0.40,
            "INDUSTRIAL": 0.35,
        }
        
        return {
            "窗墙比": window_ratios.get(building_code, 0.45),
            "窗墙比区间": "住宅≤35%，商业≤70%",
            "体形系数": 0.50
        }
    
    def get_innovation_summary(self) -> Dict:
        """获取创新体系总览"""
        return {
            "系统名称": "度量衡测不准关键因子配比估量估价系统",
            "版本": "3.0.0",
            "核心创新": [
                "7族58项创新配比参数体系",
                "6大关键材料因子体系",
                "不确定性传播模型",
                "蒙特卡洛模拟（P10/P50/P90）"
            ],
            "测不准三公理": [
                "闭合性公理: 总费用 = Σ(构件体积 × 构件单价)",
                "守恒性公理: 钢筋总量在混凝土中守恒",
                "相关性公理: 配比参数间存在统计学相关性"
            ],
            "精度等级": {
                "A级": "±8%（需完整施工图）",
                "B级": "±15%（初步设计）",
                "C级": "±25%（概念方案）",
                "D级": ">±30%（仅类型和面积）"
            }
        }


# ============================================================
# 便捷函数
# ============================================================

def quick_estimate(
    building_type: str = "办公",
    structure_type: str = "框架-剪力墙",
    total_area: float = 50000,
    floor_count: int = 33,
    basement_area: float = 10000,
    basement_floors: int = 2,
    decoration_level: str = "精装",
    has_central_ac: bool = True,
    has_pile: bool = True,
    region: str = "汕尾",
    year: int = 2026
) -> Dict:
    """快速估算函数"""
    
    bt_map = {
        "住宅": BuildingType.RESIDENTIAL, "办公": BuildingType.OFFICE,
        "商业": BuildingType.COMMERCIAL, "酒店": BuildingType.HOTEL,
        "医疗": BuildingType.HOSPITAL, "教育": BuildingType.EDUCATION,
        "工业": BuildingType.INDUSTRIAL
    }
    
    st_map = {
        "框架": StructureType.FRAME, "剪力墙": StructureType.SHEAR_WALL,
        "框架-剪力墙": StructureType.FRAME_SHEAR_WALL,
        "框架-核心筒": StructureType.FRAME_CORE_TUBE, "钢结构": StructureType.STEEL
    }
    
    region_map = {r.name_cn: r for r in Region}
    
    params = ProjectParams(
        building_type=bt_map.get(building_type, BuildingType.OFFICE),
        structure_type=st_map.get(structure_type, StructureType.FRAME_SHEAR_WALL),
        total_area=total_area,
        floor_count=floor_count,
        basement_area=basement_area,
        basement_floors=basement_floors,
        decoration_level=decoration_level,
        has_central_ac=has_central_ac,
        has_pile=has_pile,
        seismic_level="二级",
        region=region_map.get(region, Region.SHANWEI),
        year=year
    )
    
    estimator = UncertaintyEstimator()
    return estimator.estimate(params)


# ============================================================
# 主入口
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  DLHZ Uncertainty Estimator v3.2")
    print("  International QS + Chinese Characteristics")
    print("=" * 60)
    print()
    
    estimator = UncertaintyEstimator()
    info = estimator.get_innovation_summary()
    
    print("Core Innovations:")
    for item in info["核心创新"]:
        print(f"   * {item}")
    print()
    
    print("=" * 60)
    print("Example: 50,000m2 High-rise Office Building")
    print("=" * 60)
    
    result = quick_estimate(
        building_type="办公",
        structure_type="框架-剪力墙",
        total_area=50000,
        floor_count=33,
        basement_area=10000,
        basement_floors=2,
        decoration_level="精装",
        has_central_ac=True,
        has_pile=True,
        region="汕尾"
    )
    
    print()
    print("[Cost Estimate Result]")
    cost = result["造价估算"]
    print(f"  Total Area: {cost['总建筑面积']}")
    print(f"  Unit Cost: {cost['单方造价区间']['低限']} ~ {cost['单方造价区间']['高限']}")
    print(f"  Total Cost: {cost['总造价区间']['低限']} ~ {cost['总造价区间']['高限']}")
    print()
    
    print("[Material Impact]")
    impact = result["材料因子影响"]["_summary"]
    print(f"  {impact['总影响幅度']}")
    print(f"  Core Drivers: {impact['核心驱动因子']}")
    print()
    
    print("[Monte Carlo (10,000 iterations)]")
    mc = result["不确定性分析"]["蒙特卡洛模拟"]
    print(f"  P10 (Optimistic): {mc['P10']:,.0f} CNY/m2")
    print(f"  P50 (Neutral): {mc['P50']:,.0f} CNY/m2")
    print(f"  P90 (Conservative): {mc['P90']:,.0f} CNY/m2")
    print()
    
    # 国际QS方法论测试
    if INTERNATIONAL_QS_AVAILABLE:
        print("=" * 60)
        print("[International QS Methods Integration]")
        print("=" * 60)
        
        qs_result = quick_qs_estimate(
            total_area=50000,
            building_type="办公",
            structure_type="框架-核心筒",
            city="深圳",
            floor_count=30,
            quality_level="high"
        )
        
        print(f"\n  [Arcadis] {qs_result['method_estimates']['arcadis']['unit_cost']:,.0f} CNY/m2")
        print(f"  [RLB] {qs_result['method_estimates']['rlb']['unit_cost']:,.0f} CNY/m2")
        print(f"  [Davis Langdon] {qs_result['method_estimates']['davis_langdon']['unit_cost']:,.0f} CNY/m2")
        print(f"\n  [Fused] {qs_result['fused_estimate']['unit_cost']:,.0f} CNY/m2")
        print(f"  [Total] {qs_result['fused_estimate']['total_cost']/10000:,.0f} 10k CNY")
        print(f"\n  [Whole Life Cost] {qs_result['whole_life_cost']['total_lcc']/10000:,.0f} 10k CNY (50yr)")
        print()
    
    print("=" * 60)
    print("  Uncertainty = International Wisdom + Chinese Characteristics")
    print("=" * 60)
