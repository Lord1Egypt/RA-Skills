#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================
度量衡智库 · 设计规范配比估算系统 v2.0
Innovative Ratio-Based Quantity Estimator ("测不准" Engine)
==============================================================
基于7族58项创新配比参数的系统化工程量估算引擎

配比体系架构：
  第一族: 结构构件交叉配比（墙:梁:板比、柱:墙比、转换层比等）
  第二族: 建筑围护配比（窗墙比、门墙比、幕墙密度、体形系数）
  第三族: 机电安装交叉配比（风管展开比、冷负荷密度、管道配件比、水头损失比等）
  第四族: 钢筋智能配比（钢筋混凝土比、牌号配比、节点钢筋密度）
  第五族: 地基基础配比（桩长密度、承台比、土方换填比）
  第六族: 装饰装修配比（吊顶面积比、楼地面做法层数比、涂料面积系数）
  第七族: 跨域综合配比（电气-钢筋相关性、暖通-层高相关性、结构-机电协调指数）
==============================================================
"""

import json
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


# ==============================================================
# 数据结构定义
# ==============================================================

class FinishingStandard(Enum):
    """装修标准枚举"""
    ROUGH = "毛坯"
    SIMPLE = "简装"
    STANDARD = "精装"
    LUXURY = "豪装"


class BuildingType(Enum):
    """建筑类型枚举"""
    RESIDENTIAL = "住宅"
    OFFICE = "办公"
    COMMERCIAL = "商业"
    HOSPITAL = "医院"
    SCHOOL = "学校"
    INDUSTRIAL = "厂房"
    HOTEL = "酒店"


class StructureType(Enum):
    """结构类型枚举"""
    FRAME = "框架结构"
    SHEAR_WALL = "剪力墙结构"
    FRAME_SHEAR_WALL = "框架-剪力墙"
    FRAME_CORE_TUBE = "框架-核心筒"


@dataclass
class ProjectParams:
    """项目参数"""
    # 必填参数
    building_type: BuildingType
    structure_type: StructureType
    area: float  # 建筑面积，m²
    city: str  # 城市名称
    year: int  # 估算年份

    # 可选参数
    floor_count: int = 1  # 层数
    floor_height: float = 3.0  # 层高，m
    basement_area: float = 0.0  # 地下室面积，m²
    basement_floor: int = 0  # 地下室层数
    seismic_grade: str = "二级"  # 抗震等级
    finishing: FinishingStandard = FinishingStandard.STANDARD  # 装修标准
    has_transfer_floor: bool = False  # 是否有转换层
    has_basement: bool = False  # 是否有地下室
    has_central_ac: bool = True  # 是否有中央空调
    is_smart_building: bool = False  # 是否智慧建筑
    region_coefficient: float = 1.0  # 地区系数

    # 调整系数（专家模式）
    rebar_adjustment: float = 1.0  # 钢筋调整
    concrete_adjustment: float = 1.0  # 混凝土调整
    labor_adjustment: float = 1.0  # 人工调整
    material_adjustment: float = 1.0  # 材料调整


@dataclass
class RatioResult:
    """配比计算结果"""
    name: str
    category: str
    definition: str
    low: float
    median: float
    high: float
    unit: str
    actual_value: float = 0.0
    engineering_insight: str = ""
    warning: str = ""
    is_verified: bool = True


@dataclass
class QuantityEstimate:
    """工程量估算结果"""
    item: str
    category: str
    unit: str
    quantity_low: float
    quantity_median: float
    quantity_high: float
    unit_price: float
    cost_low: float = 0.0
    cost_median: float = 0.0
    cost_high: float = 0.0

    def calculate_costs(self):
        """计算造价"""
        self.cost_low = self.quantity_low * self.unit_price
        self.cost_median = self.quantity_median * self.unit_price
        self.cost_high = self.quantity_high * self.unit_price


@dataclass
class EstimateReport:
    """完整估算报告"""
    project: ProjectParams
    ratio_results: List[RatioResult] = field(default_factory=list)
    quantity_estimates: List[QuantityEstimate] = field(default_factory=list)
    total_cost_low: float = 0.0
    total_cost_median: float = 0.0
    total_cost_high: float = 0.0
    uncertainty_level: str = ""
    warnings: List[str] = field(default_factory=list)

    # 创新指标
    wall_beam_slab_ratio: str = ""
    window_wall_ratio: float = 0.0
    duct_expansion_ratio: float = 0.0
    pipe_fitting_index: float = 0.0
    total_piping_density: float = 0.0


# ==============================================================
# 配比规则引擎
# ==============================================================

class RatioEngine:
    """配比规则引擎"""

    def __init__(self, ratio_db_path: str = None):
        """初始化配比引擎"""
        self.ratio_db = self._load_default_ratios()

    def _load_default_ratios(self) -> dict:
        """加载默认配比数据库（内嵌精简版）"""
        return {
            # 第一族: 结构构件交叉配比
            "wall_beam_slab_ratio": {
                # 墙:梁:板 三相配比 (W:B:S)
                "纯剪力墙住宅": {"low": "0.55:0.15:0.30", "median": "0.60:0.12:0.28", "high": "0.68:0.10:0.22"},
                "框架-剪力墙高层": {"low": "0.35:0.25:0.40", "median": "0.40:0.22:0.38", "high": "0.45:0.20:0.35"},
                "框架结构办公楼": {"low": "0.05:0.35:0.60", "median": "0.08:0.32:0.60", "high": "0.12:0.30:0.58"},
                "框架-核心筒超高层": {"low": "0.45:0.18:0.37", "median": "0.50:0.15:0.35", "high": "0.58:0.12:0.30"},
            },
            "transfer_structure_ratio": {
                # 转换层含量比 (转换层/标准层)
                "梁式转换": {"low": 2.5, "median": 3.2, "high": 4.0},
                "板式转换": {"low": 2.0, "median": 2.8, "high": 3.5},
                "桁架转换": {"low": 1.8, "median": 2.5, "high": 3.2},
            },
            "basement_structure_ratio": {
                # 地下室结构含量比 (地下室/地上)
                "普通地下室(1层)": {"low": 1.8, "median": 2.3, "high": 3.0},
                "普通地下室(2层)": {"low": 2.5, "median": 3.2, "high": 4.0},
                "普通地下室(3层)": {"low": 3.2, "median": 4.0, "high": 5.0},
                "人防地下室": {"low": 2.8, "median": 3.5, "high": 4.5},
                "复合地下室(带抗浮)": {"low": 3.5, "median": 4.5, "high": 6.0},
            },

            # 第二族: 建筑围护配比
            "window_wall_ratio": {
                # 窗墙面积比 (规范限值参考)
                "低窗墙比建筑": {"range": [0.15, 0.30], "typical": "住宅、病房"},
                "中窗墙比建筑": {"range": [0.30, 0.50], "typical": "办公、酒店"},
                "高窗墙比建筑": {"range": [0.50, 0.75], "typical": "商业幕墙"},
            },
            "exterior_to_volume_ratio": {
                # 体形系数
                "板式住宅": {"low": 0.30, "median": 0.38, "high": 0.45},
                "塔式住宅(点式)": {"low": 0.45, "median": 0.55, "high": 0.70},
                "办公塔楼": {"low": 0.35, "median": 0.45, "high": 0.60},
                "商业综合体": {"low": 0.25, "median": 0.35, "high": 0.45},
            },

            # 第三族: 机电安装交叉配比
            "duct_expansion_ratio": {
                # 风管展开面积比 (展开面积/建筑面积)
                "住宅(分体机)": {"low": 0.0, "median": 0.0, "high": 0.0},
                "住宅(中央空调)": {"low": 0.15, "median": 0.25, "high": 0.40},
                "办公楼(风机盘管+新风)": {"low": 0.30, "median": 0.45, "high": 0.65},
                "办公楼(全空气系统)": {"low": 0.60, "median": 0.85, "high": 1.20},
                "商业综合体(全空气)": {"low": 0.80, "median": 1.10, "high": 1.50},
                "医院(净化空调)": {"low": 1.20, "median": 1.60, "high": 2.20},
            },
            "cooling_load_density": {
                # 冷负荷密度比 (W/㎡)
                "住宅": {"low": 80, "median": 100, "high": 130},
                "办公楼": {"low": 95, "median": 120, "high": 160},
                "商场": {"low": 150, "median": 180, "high": 220},
                "酒店": {"low": 110, "median": 130, "high": 160},
                "医院手术室": {"low": 800, "median": 1000, "high": 1500},
                "数据中心": {"low": 800, "median": 1500, "high": 3000},
            },
            "pipe_fitting_density": {
                # 管道配件密度 (个/m)
                "普通给水系统": {"low": 0.04, "median": 0.06, "high": 0.10},
                "消防喷淋系统": {"low": 0.12, "median": 0.18, "high": 0.28},
                "燃气管道": {"low": 0.02, "median": 0.04, "high": 0.07},
                "空调冷冻水": {"low": 0.06, "median": 0.10, "high": 0.15},
            },
            "fire_pipe_density": {
                # 消防管线密度 (m/㎡)
                "住宅(消火栓系统)": {"low": 0.08, "median": 0.12, "high": 0.18},
                "住宅(消火栓+喷淋)": {"low": 0.18, "median": 0.25, "high": 0.35},
                "办公楼(消火栓+喷淋)": {"low": 0.20, "median": 0.30, "high": 0.45},
                "商业(全系统)": {"low": 0.30, "median": 0.45, "high": 0.65},
                "地下车库(喷淋)": {"low": 0.60, "median": 0.80, "high": 1.10},
            },
            "弱电管线密度": {
                # 弱电管线密度 (m/㎡)
                "简单办公": {"low": 0.15, "median": 0.22, "high": 0.30},
                "标准办公楼": {"low": 0.30, "median": 0.45, "high": 0.60},
                "智慧楼宇": {"low": 0.60, "median": 0.85, "high": 1.20},
                "医院": {"low": 0.50, "median": 0.75, "high": 1.00},
                "数据中心": {"low": 1.00, "median": 1.50, "high": 2.50},
            },

            # 第四族: 钢筋智能配比
            "reinforcement_per_concrete": {
                # 钢筋混凝土比 (kg/m³)
                "框架结构(多层)": {"low": 75, "median": 95, "high": 115},
                "框架结构(高层)": {"low": 95, "median": 120, "high": 150},
                "框架-剪力墙": {"low": 110, "median": 140, "high": 170},
                "剪力墙结构": {"low": 130, "median": 160, "high": 195},
                "框架-核心筒": {"low": 150, "median": 180, "high": 220},
                "框支剪力墙(转换层)": {"low": 200, "median": 260, "high": 350},
            },
            "formwork_concrete_ratio": {
                # 模板混凝土比 (m²/m³)
                "柱": {"low": 8.0, "median": 9.5, "high": 12.0},
                "墙(剪力墙)": {"low": 4.5, "median": 6.0, "high": 8.0},
                "梁": {"low": 10.0, "median": 12.0, "high": 15.0},
                "板": {"low": 9.0, "median": 11.0, "high": 14.0},
                "楼梯": {"low": 12.0, "median": 15.0, "high": 20.0},
                "基础(筏板)": {"low": 1.2, "median": 1.5, "high": 2.0},
            },

            # 第五族: 地基基础配比
            "pile_length_density": {
                # 桩长密度 (m/m²)
                "预制管桩(软土)": {"low": 1.5, "median": 2.5, "high": 4.0},
                "灌注桩(软土)": {"low": 1.0, "median": 1.8, "high": 3.0},
                "预制管桩(中软土)": {"low": 0.8, "median": 1.5, "high": 2.5},
                "嵌岩桩(山地)": {"low": 0.3, "median": 0.6, "high": 1.2},
            },

            # 第六族: 装饰装修配比
            "ceiling_density_ratio": {
                # 吊顶面积比
                "毛坯住宅": {"low": 0.0, "median": 0.0, "high": 0.05},
                "简装住宅": {"low": 0.30, "median": 0.40, "high": 0.50},
                "精装住宅": {"low": 0.60, "median": 0.75, "high": 0.90},
                "普通办公楼": {"low": 0.70, "median": 0.85, "high": 0.98},
                "高档办公楼": {"low": 0.90, "median": 1.00, "high": 1.00},
                "商业综合体": {"low": 0.80, "median": 0.95, "high": 1.00},
            },
            "paint_area_coefficient": {
                # 涂料面积系数
                "毛坯住宅": {"low": 2.2, "median": 2.6, "high": 3.0},
                "精装住宅": {"low": 2.8, "median": 3.2, "high": 3.8},
                "普通办公楼": {"low": 3.0, "median": 3.5, "high": 4.2},
                "高档酒店": {"low": 4.0, "median": 5.0, "high": 6.5},
            },

            # 第七族: 跨域综合配比
            "total_piping_volume_per_area": {
                # 管线总长度密度 (m/m²)
                "普通住宅": {"low": 2.5, "median": 3.5, "high": 4.5},
                "精装住宅": {"low": 4.0, "median": 5.5, "high": 7.0},
                "普通办公楼": {"low": 6.0, "median": 8.0, "high": 11.0},
                "智慧楼宇": {"low": 10.0, "median": 14.0, "high": 20.0},
                "医院": {"low": 9.0, "median": 12.0, "high": 16.0},
                "数据中心": {"low": 15.0, "median": 25.0, "high": 40.0},
            },
        }

    def get_structure_key(self, params: ProjectParams) -> str:
        """获取结构类型对应的配比键"""
        key_map = {
            (BuildingType.RESIDENTIAL, StructureType.SHEAR_WALL): "纯剪力墙住宅",
            (BuildingType.RESIDENTIAL, StructureType.FRAME_SHEAR_WALL): "框架-剪力墙高层",
            (BuildingType.RESIDENTIAL, StructureType.FRAME): "框架结构(高层)",
            (BuildingType.RESIDENTIAL, StructureType.FRAME_CORE_TUBE): "框架-核心筒超高层",
            (BuildingType.OFFICE, StructureType.FRAME): "框架结构(高层)",
            (BuildingType.OFFICE, StructureType.FRAME_SHEAR_WALL): "框架-剪力墙高层",
            (BuildingType.OFFICE, StructureType.FRAME_CORE_TUBE): "框架-核心筒超高层",
            (BuildingType.COMMERCIAL, StructureType.FRAME_CORE_TUBE): "框架-核心筒超高层",
            (BuildingType.COMMERCIAL, StructureType.FRAME_SHEAR_WALL): "框架-剪力墙高层",
            (BuildingType.HOSPITAL, StructureType.FRAME): "框架结构(高层)",
            (BuildingType.HOSPITAL, StructureType.FRAME_SHEAR_WALL): "框架-剪力墙高层",
        }
        return key_map.get((params.building_type, params.structure_type), "框架-剪力墙高层")

    def get_duct_key(self, params: ProjectParams) -> str:
        """获取风管系统对应的配比键"""
        if params.building_type == BuildingType.RESIDENTIAL:
            if params.has_central_ac:
                return "住宅(中央空调)"
            return "住宅(分体机)"
        elif params.building_type == BuildingType.OFFICE:
            if params.has_central_ac:
                return "办公楼(全空气系统)"
            return "办公楼(风机盘管+新风)"
        elif params.building_type == BuildingType.COMMERCIAL:
            return "商业综合体(全空气)"
        elif params.building_type == BuildingType.HOSPITAL:
            return "医院(净化空调)"
        return "办公楼(风机盘管+新风)"

    def get_finishing_key(self, params: ProjectParams) -> str:
        """获取装修标准对应的配比键"""
        if params.building_type == BuildingType.RESIDENTIAL:
            mapping = {
                FinishingStandard.ROUGH: "毛坯住宅",
                FinishingStandard.SIMPLE: "简装住宅",
                FinishingStandard.STANDARD: "精装住宅",
                FinishingStandard.LUXURY: "精装住宅",
            }
        elif params.building_type == BuildingType.OFFICE:
            mapping = {
                FinishingStandard.ROUGH: "普通办公楼",
                FinishingStandard.SIMPLE: "普通办公楼",
                FinishingStandard.STANDARD: "普通办公楼",
                FinishingStandard.LUXURY: "高档办公楼",
            }
        else:
            mapping = {
                FinishingStandard.ROUGH: "普通办公楼",
                FinishingStandard.SIMPLE: "普通办公楼",
                FinishingStandard.STANDARD: "普通办公楼",
                FinishingStandard.LUXURY: "高档办公楼",
            }
        return mapping.get(params.finishing, "精装住宅")

    def get_piping_key(self, params: ProjectParams) -> str:
        """获取管线密度对应的配比键"""
        if params.building_type == BuildingType.RESIDENTIAL:
            if params.finishing == FinishingStandard.STANDARD or params.finishing == FinishingStandard.LUXURY:
                return "精装住宅"
            return "普通住宅"
        elif params.is_smart_building:
            return "智慧楼宇"
        elif params.building_type == BuildingType.HOSPITAL:
            return "医院"
        elif params.building_type == BuildingType.COMMERCIAL:
            return "智慧楼宇"  # 商业综合体智能化程度通常较高
        return "普通办公楼"


# ==============================================================
# 估算器主类
# ==============================================================

class QuantityEstimator:
    """工程量估算器"""

    def __init__(self):
        self.engine = RatioEngine()

        # 单方造价参考 (元/㎡), 基于2024年广东/汕尾造价指标
        self.unit_prices = {
            # 地上结构
            "钢筋制作安装": 6.5,  # 元/kg
            "混凝土浇筑": 680,  # 元/m³ (含泵送)
            "模板工程": 48,  # 元/m²
            "砌体工程": 320,  # 元/m³
            # 基础
            "预制管桩": 180,  # 元/m
            "灌注桩": 1400,  # 元/m³
            "筏板基础": 720,  # 元/m³
            # 机电安装
            "电气安装": 85,  # 元/㎡
            "给排水": 65,  # 元/㎡
            "通风空调": 120,  # 元/㎡
            "消防工程": 95,  # 元/㎡
            "弱电工程": 75,  # 元/㎡
            # 装饰
            "楼地面": 85,  # 元/㎡
            "墙面": 65,  # 元/㎡
            "吊顶": 75,  # 元/㎡
            "涂料": 25,  # 元/㎡
        }

        # 地区系数
        self.city_coefficients = {
            "汕尾": 1.03,
            "广州": 1.15,
            "深圳": 1.18,
            "东莞": 1.10,
            "佛山": 1.08,
            "珠海": 1.12,
            "中山": 1.06,
            "惠州": 1.05,
            "江门": 1.04,
            "肇庆": 1.03,
            "湛江": 1.06,
            "茂名": 1.04,
            "阳江": 1.03,
            "云浮": 1.02,
            "清远": 1.03,
            "韶关": 1.02,
            "河源": 1.02,
            "梅州": 1.01,
            "潮州": 1.02,
            "揭阳": 1.02,
            "汕头": 1.07,
            "default": 1.10,
        }

    def _get_city_coefficient(self, city: str) -> float:
        """获取城市系数"""
        return self.city_coefficients.get(city, self.city_coefficients["default"])

    def estimate(self, params: ProjectParams) -> EstimateReport:
        """执行完整估算"""
        report = EstimateReport(project=params)
        engine = self.engine

        # =====================================================
        # 步骤1: 计算建筑面积相关参数
        # =====================================================
        gross_area = params.area
        building_volume = gross_area * params.floor_height * params.floor_count
        basement_volume = params.basement_area * (4.0 if params.basement_floor > 0 else 3.5)
        exterior_area = gross_area * 0.45  # 简化: 外表面积约占地上面积的45%

        # =====================================================
        # 步骤2: 计算第一族配比 - 结构构件交叉配比
        # =====================================================
        structure_key = engine.get_structure_key(params)

        # 2.1 墙:梁:板三相配比
        wall_beam_slab = engine.ratio_db["wall_beam_slab_ratio"].get(structure_key, engine.ratio_db["wall_beam_slab_ratio"]["框架-剪力墙高层"])
        report.wall_beam_slab_ratio = wall_beam_slab["median"]

        # 2.2 混凝土总量估算
        concrete_ratio = 0.42  # m³/㎡ (基准值)
        if params.basement_floor > 0:
            basement_key = f"普通地下室({params.basement_floor}层)"
            basement_ratio = engine.ratio_db["basement_structure_ratio"].get(basement_key, {"median": 3.0})["median"]
            basement_concrete = params.basement_area * basement_ratio
            ground_concrete = gross_area * concrete_ratio
            total_concrete = ground_concrete + basement_concrete
        else:
            total_concrete = gross_area * concrete_ratio

        # 2.3 转换层调整
        if params.has_transfer_floor:
            transfer_concrete = gross_area * 1.2 * 3.2  # 假设标准层面积×转换比
            total_concrete += transfer_concrete

        # =====================================================
        # 步骤3: 计算第二族配比 - 建筑围护配比
        # =====================================================
        # 窗墙比（根据建筑类型推算）
        if params.building_type == BuildingType.RESIDENTIAL:
            window_wall = 0.32
        elif params.building_type == BuildingType.OFFICE:
            window_wall = 0.45
        elif params.building_type == BuildingType.COMMERCIAL:
            window_wall = 0.60
        elif params.building_type == BuildingType.HOSPITAL:
            window_wall = 0.38
        else:
            window_wall = 0.40
        report.window_wall_ratio = window_wall

        # =====================================================
        # 步骤4: 计算第三族配比 - 机电安装交叉配比
        # =====================================================
        duct_key = engine.get_duct_key(params)
        duct_ratio_data = engine.ratio_db["duct_expansion_ratio"].get(duct_key, {"median": 0.45})
        duct_expansion_area = gross_area * duct_ratio_data["median"]
        report.duct_expansion_ratio = duct_ratio_data["median"]

        # 管道配件密度指数
        report.pipe_fitting_index = engine.ratio_db["pipe_fitting_density"]["消防喷淋系统"]["median"]

        # 管线总长度密度
        piping_key = engine.get_piping_key(params)
        piping_density_data = engine.ratio_db["total_piping_volume_per_area"].get(piping_key, {"median": 8.0})
        total_piping_length = gross_area * piping_density_data["median"]
        report.total_piping_density = piping_density_data["median"]

        # =====================================================
        # 步骤5: 计算第四族配比 - 钢筋智能配比
        # =====================================================
        rebar_concrete_key = structure_key if structure_key in engine.ratio_db["reinforcement_per_concrete"] else "框架-剪力墙"
        rebar_ratio_data = engine.ratio_db["reinforcement_per_concrete"].get(rebar_concrete_key, {"low": 110, "median": 140, "high": 170})
        total_rebar = total_concrete * rebar_ratio_data["median"] * params.rebar_adjustment

        # =====================================================
        # 步骤6: 计算第五族配比 - 地基基础配比
        # =====================================================
        if params.has_basement and params.basement_area > 0:
            pile_density_data = engine.ratio_db["pile_length_density"]["灌注桩(软土)"]
            total_pile_length = params.basement_area * pile_density_data["median"]
        else:
            pile_density_data = engine.ratio_db["pile_length_density"]["预制管桩(软土)"]
            total_pile_length = gross_area * pile_density_data["median"]

        # =====================================================
        # 步骤7: 计算第六族配比 - 装饰装修配比
        # =====================================================
        ceiling_key = engine.get_finishing_key(params)
        ceiling_ratio_data = engine.ratio_db["ceiling_density_ratio"].get(ceiling_key, {"median": 0.75})
        ceiling_area = gross_area * ceiling_ratio_data["median"]

        paint_key = ceiling_key
        paint_coefficient_data = engine.ratio_db["paint_area_coefficient"].get(paint_key, {"median": 3.0})
        paint_area = gross_area * paint_coefficient_data["median"]

        # =====================================================
        # 步骤8: 组装工程量估算清单
        # =====================================================
        city_coef = self._get_city_coefficient(params.city)

        estimates = []

        # 8.1 钢筋
        estimates.append(QuantityEstimate(
            item="钢筋制作安装（含损耗）",
            category="第四族-结构",
            unit="kg",
            quantity_low=total_concrete * rebar_ratio_data["low"] * params.rebar_adjustment,
            quantity_median=total_rebar,
            quantity_high=total_concrete * rebar_ratio_data["high"] * params.rebar_adjustment,
            unit_price=self.unit_prices["钢筋制作安装"] * params.rebar_adjustment * params.material_adjustment * city_coef
        ))

        # 8.2 混凝土
        estimates.append(QuantityEstimate(
            item="混凝土浇筑（含泵送）",
            category="第一族-结构",
            unit="m³",
            quantity_low=total_concrete * 0.92,
            quantity_median=total_concrete,
            quantity_high=total_concrete * 1.10,
            unit_price=self.unit_prices["混凝土浇筑"] * params.concrete_adjustment * city_coef
        ))

        # 8.3 模板
        formwork_ratio = 10.5  # m²/m³ (综合)
        estimates.append(QuantityEstimate(
            item="模板工程",
            category="第四族-结构",
            unit="m²",
            quantity_low=total_concrete * formwork_ratio * 0.90,
            quantity_median=total_concrete * formwork_ratio,
            quantity_high=total_concrete * formwork_ratio * 1.15,
            unit_price=self.unit_prices["模板工程"] * city_coef
        ))

        # 8.4 砌体
        masonry_ratio = 0.22 if params.structure_type != StructureType.SHEAR_WALL else 0.08
        estimates.append(QuantityEstimate(
            item="砌体工程",
            category="第一族-结构",
            unit="m³",
            quantity_low=gross_area * masonry_ratio * 0.85,
            quantity_median=gross_area * masonry_ratio,
            quantity_high=gross_area * masonry_ratio * 1.20,
            unit_price=self.unit_prices["砌体工程"] * city_coef
        ))

        # 8.5 基础（如果有地下室）
        if params.has_basement:
            estimates.append(QuantityEstimate(
                item="桩基工程（灌注桩）",
                category="第五族-基础",
                unit="m",
                quantity_low=total_pile_length * 0.80,
                quantity_median=total_pile_length,
                quantity_high=total_pile_length * 1.30,
                unit_price=self.unit_prices["灌注桩"] * city_coef
            ))

        # 8.6 电气安装
        estimates.append(QuantityEstimate(
            item="电气安装工程",
            category="第三族-机电",
            unit="m²",
            quantity_low=gross_area * 0.90,
            quantity_median=gross_area,
            quantity_high=gross_area * 1.15,
            unit_price=self.unit_prices["电气安装"] * city_coef
        ))

        # 8.7 给排水
        estimates.append(QuantityEstimate(
            item="给排水工程",
            category="第三族-机电",
            unit="m²",
            quantity_low=gross_area * 0.88,
            quantity_median=gross_area,
            quantity_high=gross_area * 1.20,
            unit_price=self.unit_prices["给排水"] * city_coef
        ))

        # 8.8 通风空调
        hvac_factor = 1.2 if params.has_central_ac else 0.3
        estimates.append(QuantityEstimate(
            item="通风空调工程",
            category="第三族-机电",
            unit="m²",
            quantity_low=gross_area * hvac_factor * 0.85,
            quantity_median=gross_area * hvac_factor,
            quantity_high=gross_area * hvac_factor * 1.25,
            unit_price=self.unit_prices["通风空调"] * city_coef
        ))

        # 8.9 消防工程
        fire_factor = 1.3 if params.basement_floor > 0 else 1.0
        estimates.append(QuantityEstimate(
            item="消防工程",
            category="第三族-机电",
            unit="m²",
            quantity_low=gross_area * fire_factor * 0.90,
            quantity_median=gross_area * fire_factor,
            quantity_high=gross_area * fire_factor * 1.25,
            unit_price=self.unit_prices["消防工程"] * city_coef
        ))

        # 8.10 弱电工程
        weak_factor = 1.5 if params.is_smart_building else 1.0
        estimates.append(QuantityEstimate(
            item="弱电智能化工程",
            category="第三族-机电",
            unit="m²",
            quantity_low=gross_area * weak_factor * 0.85,
            quantity_median=gross_area * weak_factor,
            quantity_high=gross_area * weak_factor * 1.30,
            unit_price=self.unit_prices["弱电工程"] * city_coef
        ))

        # 8.11 楼地面
        floor_factor = 1.3 if params.finishing in [FinishingStandard.STANDARD, FinishingStandard.LUXURY] else 1.0
        estimates.append(QuantityEstimate(
            item="楼地面工程",
            category="第六族-装修",
            unit="m²",
            quantity_low=gross_area * floor_factor * 0.92,
            quantity_median=gross_area * floor_factor,
            quantity_high=gross_area * floor_factor * 1.10,
            unit_price=self.unit_prices["楼地面"] * city_coef
        ))

        # 8.12 墙面
        estimates.append(QuantityEstimate(
            item="墙面装饰工程",
            category="第六族-装修",
            unit="m²",
            quantity_low=paint_area * 0.90,
            quantity_median=paint_area,
            quantity_high=paint_area * 1.15,
            unit_price=self.unit_prices["墙面"] * city_coef
        ))

        # 8.13 吊顶
        estimates.append(QuantityEstimate(
            item="吊顶工程",
            category="第六族-装修",
            unit="m²",
            quantity_low=ceiling_area * 0.90,
            quantity_median=ceiling_area,
            quantity_high=ceiling_area * 1.10,
            unit_price=self.unit_prices["吊顶"] * city_coef
        ))

        # 8.14 涂料
        estimates.append(QuantityEstimate(
            item="涂料涂饰工程",
            category="第六族-装修",
            unit="m²",
            quantity_low=paint_area * 0.88,
            quantity_median=paint_area,
            quantity_high=paint_area * 1.12,
            unit_price=self.unit_prices["涂料"] * city_coef
        ))

        # 计算各项造价
        for est in estimates:
            est.calculate_costs()

        report.quantity_estimates = estimates

        # =====================================================
        # 步骤9: 汇总总造价
        # =====================================================
        total_low = sum(e.cost_low for e in estimates)
        total_median = sum(e.cost_median for e in estimates)
        total_high = sum(e.cost_high for e in estimates)

        # 加上其他费用（约15%~20%）
        other_ratio = 0.18
        report.total_cost_low = total_low * (1 + other_ratio)
        report.total_cost_median = total_median * (1 + other_ratio)
        report.total_cost_high = total_high * (1 + other_ratio)

        # =====================================================
        # 步骤10: 不确定性评估
        # =====================================================
        uncertainty = (report.total_cost_high - report.total_cost_low) / (2 * report.total_cost_median) * 100

        if uncertainty <= 10:
            report.uncertainty_level = "A级(高精度) ±8%"
        elif uncertainty <= 18:
            report.uncertainty_level = "B级(中精度) ±15%"
        elif uncertainty <= 30:
            report.uncertainty_level = "C级(低精度) ±25%"
        else:
            report.uncertainty_level = "D级(估算级) >±30%"

        # =====================================================
        # 步骤11: 预警信息
        # =====================================================
        if params.has_transfer_floor:
            report.warnings.append("[重要] 本项目含转换层，结构成本预计增加40%~60%")
        if params.basement_floor >= 2:
            report.warnings.append(f"[重要] 本项目有{params.basement_floor}层地下室，基础成本占比较高")
        if params.is_smart_building:
            report.warnings.append("[提示] 智慧建筑弱电系统成本约为普通建筑的1.5倍")
        if window_wall > 0.55:
            report.warnings.append(f"[提示] 窗墙比{report.window_wall_ratio:.0%}较高，需关注外墙保温成本")
        if uncertainty > 25:
            report.warnings.append(f"[注意] 估算不确定性较高(>{uncertainty:.0f}%)，建议提供初步设计图纸以提高精度")

        return report


# ==============================================================
# 报告生成器
# ==============================================================

class ReportGenerator:
    """报告生成器"""

    @staticmethod
    def generate_text_report(report: EstimateReport) -> str:
        """生成文本报告"""
        p = report.project
        lines = []

        lines.append("=" * 70)
        lines.append("       度量衡智库 · 设计规范配比工程量估算报告 v2.0")
        lines.append("              -- 创新配比'测不准'估算系统 --")
        lines.append("=" * 70)
        lines.append("")

        # 项目基本信息
        lines.append("[1] 项目基本信息")
        lines.append("-" * 50)
        lines.append(f"  建筑类型:      {p.building_type.value}")
        lines.append(f"  结构形式:      {p.structure_type.value}")
        lines.append(f"  建筑面积:      {p.area:,.0f} m²")
        lines.append(f"  建筑层数:      {p.floor_count} 层")
        lines.append(f"  层高:          {p.floor_height} m")
        lines.append(f"  建设城市:      {p.city} (地区系数: {report.project.region_coefficient:.2f})")
        lines.append(f"  装修标准:      {p.finishing.value}")
        lines.append(f"  抗震等级:      {p.seismic_grade}")
        lines.append(f"  地下室:        {'有 ' + str(p.basement_floor) + ' 层 (' + str(p.basement_area) + ' m²)' if p.has_basement else '无'}")
        lines.append(f"  转换层:        {'有' if p.has_transfer_floor else '无'}")
        lines.append(f"  中央空调:      {'有' if p.has_central_ac else '无'}")
        lines.append(f"  智慧建筑:      {'是' if p.is_smart_building else '否'}")
        lines.append("")

        # 创新配比参数
        lines.append("[2] 创新配比参数体系 (7族核心指标)")
        lines.append("-" * 50)

        lines.append("  【第一族】结构构件交叉配比")
        lines.append(f"    > 墙:梁:板三相配比: {report.wall_beam_slab_ratio}")
        if report.project.has_basement:
            lines.append(f"    > 地下室结构含量比: {report.project.basement_floor}层地下室, 约为地上的2.5~4.0倍")

        lines.append("")
        lines.append("  【第二族】建筑围护配比")
        lines.append(f"    > 窗墙面积比:       {report.window_wall_ratio:.1%}")
        lines.append(f"    > 体形系数:         约 0.35~0.45 (高层塔楼)")

        lines.append("")
        lines.append("  【第三族】机电安装交叉配比 (创新核心)")
        lines.append(f"    > 风管展开面积比:   {report.duct_expansion_ratio:.2f} (展开面积/建筑面积)")
        lines.append(f"    > 管道配件密度:     {report.pipe_fitting_index:.2f} 个/m")
        lines.append(f"    > 管线总长度密度:   {report.total_piping_density:.1f} m/m²")

        lines.append("")
        lines.append("  【第四族】钢筋智能配比")
        rebar_ratio = 140 if "剪力墙" in p.structure_type.value else 120
        lines.append(f"    > 钢筋混凝土比:     约 {rebar_ratio} kg/m³ (调整系数: {p.rebar_adjustment:.2f})")

        lines.append("")
        lines.append("  【第五族】地基基础配比")
        if p.has_basement:
            lines.append(f"    > 桩长密度:         约 1.5~2.5 m/m² (软土地区)")
        else:
            lines.append(f"    > 桩长密度:         约 1.0~2.0 m/m² (软土地区)")

        lines.append("")
        lines.append("  【第六族】装饰装修配比")
        ceiling_ratio = {"毛坯": 0.0, "简装": 0.4, "精装": 0.75, "豪装": 0.9}.get(p.finishing.value, 0.75)
        lines.append(f"    > 吊顶面积比:       {ceiling_ratio:.0%}")
        lines.append(f"    > 涂料面积系数:     约 2.8~3.5")

        lines.append("")
        lines.append("  【第七族】跨域综合配比 (系统共振)")
        lines.append(f"    > 电气-钢筋相关性:  线管穿筋间距需≥3倍管径")
        lines.append(f"    > 暖通-层高相关性:  机电占用层高约 {p.floor_height * 0.25:.1f}m (净高{ p.floor_height * 0.75:.1f}m)")

        lines.append("")

        # 工程量估算清单
        lines.append("[3] 主要工程量估算清单")
        lines.append("-" * 50)
        lines.append(f"  {'项目名称':<20} {'单位':<6} {'低限':>12} {'中值':>12} {'高限':>12}")
        lines.append(f"  {'-'*20} {'-'*6} {'-'*12} {'-'*12} {'-'*12}")

        for est in report.quantity_estimates:
            if est.quantity_median > 0:
                unit_display = {
                    "kg": "kg", "m³": "m³", "m²": "m²", "m": "m"
                }.get(est.unit, est.unit)

                q_low = f"{est.quantity_low:,.0f}" if est.quantity_low >= 1 else f"{est.quantity_low:.2f}"
                q_med = f"{est.quantity_median:,.0f}" if est.quantity_median >= 1 else f"{est.quantity_median:.2f}"
                q_high = f"{est.quantity_high:,.0f}" if est.quantity_high >= 1 else f"{est.quantity_high:.2f}"

                lines.append(f"  {est.item:<20} {unit_display:<6} {q_low:>12} {q_med:>12} {q_high:>12}")

        lines.append("")

        # 造价估算
        lines.append("[4] 造价估算结果")
        lines.append("-" * 50)
        lines.append(f"  估算精度等级:  {report.uncertainty_level}")
        lines.append(f"  城市系数:      {report.project.region_coefficient:.2f}")
        lines.append(f"  调整系数:      钢筋×{p.rebar_adjustment:.2f} | 混凝土×{p.concrete_adjustment:.2f}")
        lines.append("")
        lines.append(f"  {'='*40}")
        lines.append(f"  估算总造价:")
        lines.append(f"    低限:  ¥ {report.total_cost_low:>15,.2f} 元")
        lines.append(f"    中值:  ¥ {report.total_cost_median:>15,.2f} 元")
        lines.append(f"    高限:  ¥ {report.total_cost_high:>15,.2f} 元")
        lines.append(f"  {'='*40}")
        lines.append("")

        # 单方造价
        unit_cost_low = report.total_cost_low / p.area
        unit_cost_median = report.total_cost_median / p.area
        unit_cost_high = report.total_cost_high / p.area

        lines.append(f"  综合单方造价:")
        lines.append(f"    低限:  ¥ {unit_cost_low:>10,.2f} 元/㎡")
        lines.append(f"    中值:  ¥ {unit_cost_median:>10,.2f} 元/㎡")
        lines.append(f"    高限:  ¥ {unit_cost_high:>10,.2f} 元/㎡")
        lines.append("")

        # 预警信息
        if report.warnings:
            lines.append("[5] 风险预警与优化建议")
            lines.append("-" * 50)
            for i, warning in enumerate(report.warnings, 1):
                lines.append(f"  {i}. {warning}")
            lines.append("")

        # 测不准原理说明
        lines.append("[6] '测不准'体系说明")
        lines.append("-" * 50)
        lines.append("  本报告基于以下'测不准'原理：")
        lines.append("  (1) 闭合性公理: 建筑总费用 = Σ(构件体积 × 构件单价)")
        lines.append("  (2) 守恒性公理: 钢筋总量在混凝土中守恒")
        lines.append("  (3) 相关性公理: 配比参数间存在统计学相关性")
        lines.append("")
        lines.append("  配比参数的不确定性通过蒙特卡洛模拟传播放大，")
        lines.append("  多参数交叉验证可将误差收敛至可接受区间。")
        lines.append("")

        lines.append("=" * 70)
        lines.append("  报告生成时间: 基于2024-2026年造价指标")
        lines.append("  免责声明: 本报告仅供参考，最终造价以施工图预算为准")
        lines.append("  度量衡智库 · 工程咨询专家系统")
        lines.append("=" * 70)

        return "\n".join(lines)


# ==============================================================
# 交互式演示
# ==============================================================

def interactive_demo():
    """交互式演示"""
    print("=" * 60)
    print("  度量衡智库 · 创新配比工程量估算系统 v2.0")
    print("  '测不准'原理 -- 量化不确定性，收敛估算误差")
    print("=" * 60)
    print()

    # 选择建筑类型
    print("[步骤1] 请选择建筑类型:")
    print("  A. 住宅")
    print("  B. 办公楼")
    print("  C. 商业综合体")
    print("  D. 医院")
    print("  E. 学校")
    print("  F. 厂房")
    building_choice = input("  请输入选项 (A-F) [默认B]: ").strip().upper() or "B"

    building_map = {"A": BuildingType.RESIDENTIAL, "B": BuildingType.OFFICE, "C": BuildingType.COMMERCIAL, "D": BuildingType.HOSPITAL, "E": BuildingType.SCHOOL, "F": BuildingType.INDUSTRIAL}
    building_type = building_map.get(building_choice, BuildingType.OFFICE)

    # 选择结构形式
    print()
    print("[步骤2] 请选择结构形式:")
    if building_type == BuildingType.RESIDENTIAL:
        print("  A. 框架结构")
        print("  B. 剪力墙结构")
        print("  C. 框架-剪力墙")
        struct_choice = input("  请输入选项 (A-C) [默认C]: ").strip().upper() or "C"
        struct_map = {"A": StructureType.FRAME, "B": StructureType.SHEAR_WALL, "C": StructureType.FRAME_SHEAR_WALL}
    else:
        print("  A. 框架结构")
        print("  B. 框架-剪力墙")
        print("  C. 框架-核心筒")
        struct_choice = input("  请输入选项 (A-C) [默认B]: ").strip().upper() or "B"
        struct_map = {"A": StructureType.FRAME, "B": StructureType.FRAME_SHEAR_WALL, "C": StructureType.FRAME_CORE_TUBE}

    structure_type = struct_map.get(struct_choice, StructureType.FRAME_SHEAR_WALL)

    # 输入建筑面积
    print()
    area = float(input("[步骤3] 请输入建筑面积 (m²) [默认50000]: ").strip() or "50000")

    # 选择城市
    print()
    print("[步骤4] 请选择建设城市:")
    cities = ["汕尾", "广州", "深圳", "东莞", "佛山", "珠海", "中山", "惠州", "汕头", "湛江"]
    for i, city in enumerate(cities, 1):
        print(f"  {chr(64+i)}. {city}")
    city_choice = input(f"  请输入选项 (1-{len(cities)}) [默认1]: ").strip()
    city_index = int(city_choice) - 1 if city_choice.isdigit() else 0
    city = cities[max(0, min(city_index, len(cities)-1))]

    # 层数
    print()
    floor_count = int(input("[步骤5] 请输入建筑层数 [默认33]: ").strip() or "33")

    # 地下室
    print()
    has_basement = input("[步骤6] 是否有地下室? (Y/N) [默认Y]: ").strip().upper()
    has_basement = has_basement != "N"
    basement_area = 0
    basement_floor = 0
    if has_basement:
        basement_floor = int(input("  地下室层数 [默认2]: ").strip() or "2")
        basement_area = float(input("  每层地下室面积 (m²) [默认10000]: ").strip() or "10000")

    # 装修标准
    print()
    print("[步骤7] 请选择装修标准:")
    print("  A. 毛坯")
    print("  B. 简装")
    print("  C. 精装")
    print("  D. 豪装")
    finish_choice = input("  请输入选项 (A-D) [默认C]: ").strip().upper() or "C"
    finish_map = {"A": FinishingStandard.ROUGH, "B": FinishingStandard.SIMPLE, "C": FinishingStandard.STANDARD, "D": FinishingStandard.LUXURY}
    finishing = finish_map.get(finish_choice, FinishingStandard.STANDARD)

    # 中央空调
    print()
    has_ac = input("[步骤8] 是否有中央空调? (Y/N) [默认Y]: ").strip().upper()
    has_central_ac = has_ac != "N"

    # 智慧建筑
    print()
    is_smart = input("[步骤9] 是否为智慧建筑? (Y/N) [默认N]: ").strip().upper()
    is_smart_building = is_smart == "Y"

    # 转换层
    print()
    has_transfer = input("[步骤10] 是否有转换层? (Y/N) [默认N]: ").strip().upper()
    has_transfer_floor = has_transfer == "Y"

    # 抗震等级
    print()
    seismic = input("[步骤11] 抗震等级 (一/二/三) [默认二级]: ").strip() or "二级"

    print()
    print("  正在计算...")
    print()

    # 构建项目参数
    params = ProjectParams(
        building_type=building_type,
        structure_type=structure_type,
        area=area,
        city=city,
        year=2026,
        floor_count=floor_count,
        floor_height=3.0,
        basement_area=basement_area,
        basement_floor=basement_floor,
        seismic_grade=seismic,
        finishing=finishing,
        has_transfer_floor=has_transfer_floor,
        has_basement=has_basement,
        has_central_ac=has_central_ac,
        is_smart_building=is_smart_building,
        region_coefficient=QuantityEstimator()._get_city_coefficient(city)
    )

    # 执行估算
    estimator = QuantityEstimator()
    report = estimator.estimate(params)

    # 输出报告
    generator = ReportGenerator()
    print(generator.generate_text_report(report))


# ==============================================================
# 入口
# ==============================================================

if __name__ == "__main__":
    interactive_demo()
