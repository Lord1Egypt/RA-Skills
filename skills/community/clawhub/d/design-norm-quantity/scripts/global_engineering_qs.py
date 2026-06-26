# -*- coding: utf-8 -*-
"""
度量衡智库 · 度量衡测不准系统 v3.3
Global Engineering Companies QS Methods Integration
=====================================================

整合全球顶级工程咨询公司的估量估价方法论：

1. AECOM - Parametric Automated Cost Engineering System (PACES)
2. WSP - Global Program & Construction Management
3. 日本五大建设：
   - 鹿島建設 (Kajima)
   - 清水建設 (Shimizu)
   - 竹中用工店 (Takenaka)
   - 大林組 (Obayashi)
   - 大成建設 (Taisei)
4. RIBS/BSIJ - 日本建築積算協会方法论
5. 中国本土方法论

作者：度量衡智库
版本：3.3.0
日期：2026-04-03
"""

import json
import math
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

# ==================== AECOM PACES 方法论 ====================

class AECOMEstimateLevel(Enum):
    """AECOM估算精度等级"""
    LEVEL_5_CONCEPT = {"name": "概念估算", "accuracy": "+/-50%", "phase": "可行性研究"}
    LEVEL_4_SCHEMATIC = {"name": "方案估算", "accuracy": "+/-30%", "phase": "方案设计"}
    LEVEL_3_DESIGN = {"name": "设计估算", "accuracy": "+/-15%", "phase": "初步设计"}
    LEVEL_2_DD = {"name": "详细估算", "accuracy": "+/-5%", "phase": "施工图设计"}
    LEVEL_1_BID = {"name": "投标估算", "accuracy": "+/-2%", "phase": "招投标"}


class AECOMCostMethods:
    """AECOM成本估算方法"""
    
    @staticmethod
    def parametric_estimate(
        base_cost: float,
        complexity_factor: float,
        location_factor: float,
        time_factor: float
    ) -> Dict[str, float]:
        """
        参数化估算
        
        参数:
        - base_cost: 基准成本
        - complexity_factor: 复杂度因子 (1.0-2.0)
        - location_factor: 地域因子 (0.8-1.5)
        - time_factor: 时间因子 (考虑通胀)
        """
        adjusted_cost = base_cost * complexity_factor * location_factor * time_factor
        return {
            "method": "Parametric (PACES)",
            "adjusted_cost": adjusted_cost,
            "breakdown": {
                "base": base_cost,
                "complexity": complexity_factor,
                "location": location_factor,
                "time": time_factor
            }
        }
    
    @staticmethod
    def assembly_model_estimate(
        assembly_items: List[Dict],
        location_factor: float = 1.0
    ) -> Dict[str, Any]:
        """
        组件模型估算 (Assembly Model)
        
        基于预定义组件的成本估算方法
        """
        total = 0
        assembly_details = []
        
        for item in assembly_items:
            quantity = item.get("quantity", 0)
            unit_cost = item.get("unit_cost", 0)
            subtotal = quantity * unit_cost * location_factor
            total += subtotal
            assembly_details.append({
                "assembly": item.get("name"),
                "quantity": quantity,
                "unit_cost": unit_cost,
                "subtotal": subtotal
            })
        
        return {
            "method": "Assembly Model",
            "total_cost": total,
            "location_adjusted": total * location_factor,
            "items": assembly_details
        }
    
    @staticmethod
    def monte_carlo_risk_estimate(
        base_cost: float,
        risk_factors: List[Dict[str, float]],
        iterations: int = 10000
    ) -> Dict[str, Any]:
        """
        蒙特卡洛风险估算
        
        风险因子格式: [{"name": "基础工程", "min": 0.9, "max": 1.2, "weight": 0.15}, ...]
        """
        import random
        random.seed(42)
        
        results = []
        for _ in range(iterations):
            adjustment = 1.0
            for rf in risk_factors:
                adjustment += (random.uniform(rf["min"], rf["max"]) - 1.0) * rf.get("weight", 0.1)
            results.append(base_cost * adjustment)
        
        results.sort()
        
        return {
            "method": "Monte Carlo Risk Analysis",
            "iterations": iterations,
            "p10": results[int(iterations * 0.1)],
            "p50": results[int(iterations * 0.5)],
            "p90": results[int(iterations * 0.9)],
            "mean": sum(results) / len(results),
            "std_dev": (sum((r - sum(results)/len(results))**2 for r in results) / len(results)) ** 0.5
        }


# ==================== WSP 方法论 ====================

class WSPMethods:
    """WSP全球项目管理与成本管理方法"""
    
    # WSP 成本估算分级
    ESTIMATE_CLASSIFICATIONS = {
        "CLASS_A": {
            "name": "Class A (批准预算)",
            "accuracy": "+/-5%",
            "method": "详细工程量清单 + 施工单位报价"
        },
        "CLASS_B": {
            "name": "Class B (控制预算)",
            "accuracy": "+/-10-15%",
            "method": "元素估量法 + 市场价格"
        },
        "CLASS_C": {
            "name": "Class C (指示性估算)",
            "accuracy": "+/-15-25%",
            "method": "单位成本法 + 面积指标"
        },
        "CLASS_D": {
            "name": "Class D (概念估算)",
            "accuracy": "+/-25-40%",
            "method": "类比估算法 + 经验数据"
        },
        "CLASS_E": {
            "name": "Class E (初步估算)",
            "accuracy": "+/-40-50%",
            "method": "参数模型 + 宏观指标"
        }
    }
    
    # WSP 地域调整因子
    LOCATION_FACTORS = {
        "上海": 1.15,
        "北京": 1.12,
        "深圳": 1.10,
        "广州": 1.08,
        "苏州": 1.05,
        "珠海": 1.05,
        "汕尾": 1.00,
        "二线城市": 0.95,
        "三线城市": 0.88
    }
    
    @staticmethod
    def generate_cost_plan(
        total_area: float,
        building_type: str,
        location: str,
        quality: str,
        estimate_class: str = "CLASS_C"
    ) -> Dict[str, Any]:
        """
        生成WSP风格的成本计划
        
        返回详细的成本分解结构
        """
        classification = WSPMethods.ESTIMATE_CLASSIFICATIONS.get(
            estimate_class, 
            WSPMethods.ESTIMATE_CLASSIFICATIONS["CLASS_C"]
        )
        
        # 基础单方造价
        base_unit_costs = {
            "办公": 4500,
            "住宅": 3200,
            "商业": 5500,
            "酒店": 6000,
            "医院": 6500,
            "学校": 3800,
            "工业": 2800
        }
        
        base = base_unit_costs.get(building_type, 4000)
        
        # 质量调整
        quality_adjustments = {
            "高档": 1.25,
            "中档": 1.0,
            "普通": 0.85
        }
        
        # 地域调整
        location_factor = WSPMethods.LOCATION_FACTORS.get(location, 1.0)
        quality_factor = quality_adjustments.get(quality, 1.0)
        
        unit_cost = base * location_factor * quality_factor
        total_cost = unit_cost * total_area
        
        # WSP成本分解
        elemental_breakdown = [
            {"element": "0xx - 场地准备", "percentage": 0.03, "subtotal": total_cost * 0.03},
            {"element": "1xx - 基础工程", "percentage": 0.10, "subtotal": total_cost * 0.10},
            {"element": "2xx - 结构框架", "percentage": 0.18, "subtotal": total_cost * 0.18},
            {"element": "3xx - 楼板系统", "percentage": 0.08, "subtotal": total_cost * 0.08},
            {"element": "4xx - 屋面系统", "percentage": 0.04, "subtotal": total_cost * 0.04},
            {"element": "5xx - 外墙系统", "percentage": 0.12, "subtotal": total_cost * 0.12},
            {"element": "6xx - 外窗幕墙", "percentage": 0.08, "subtotal": total_cost * 0.08},
            {"element": "10xx - 装修工程", "percentage": 0.15, "subtotal": total_cost * 0.15},
            {"element": "13xx-17xx - 机电安装", "percentage": 0.22, "subtotal": total_cost * 0.22}
        ]
        
        return {
            "method": "WSP Cost Planning",
            "classification": classification,
            "project_summary": {
                "building_type": building_type,
                "location": location,
                "quality": quality,
                "total_area": total_area
            },
            "cost_summary": {
                "unit_cost": unit_cost,
                "total_cost": total_cost,
                "location_factor": location_factor,
                "quality_factor": quality_factor
            },
            "elemental_breakdown": elemental_breakdown,
            "contingency": {
                "design": 0.10,
                "construction": 0.05,
                "market": 0.03
            }
        }


# ==================== 日本五大建设方法论 ====================

class JapaneseSuperGCMethods:
    """日本五大超级总承包商方法论"""
    
    # 日本建筑积算协会 (BSIJ) 标准歩掛
    STANDARD_HOURS = {
        "钢筋工程": {
            "普通钢筋": {"unit": "t", "standard_hours": 12.5, "note": "含加工、运输、绑扎"},
            "型鋼": {"unit": "t", "standard_hours": 15.0, "note": "含焊接、安装"},
            "鉄骨": {"unit": "t", "standard_hours": 20.0, "note": "高层钢结构"}
        },
        "混凝土工程": {
            "型枠": {"unit": "m2", "standard_hours": 0.8, "note": "墙/柱复合模板"},
            "コンクリート": {"unit": "m³", "standard_hours": 0.5, "note": "打设、养生"},
            "PC工事": {"unit": "件", "standard_hours": 8.0, "note": "预制构件安装"}
        },
        "装修工程": {
            "左官": {"unit": "m2", "standard_hours": 0.4, "note": "抹灰"},
            "内装": {"unit": "m2", "standard_hours": 0.6, "note": "室内装修"}
        }
    }
    
    # 日本SEC皮和方法 (Scope, Estimate, Control)
    SECI_METHOD = {
        "S_Scope": {
            "description": "范围管理 - WBS分解",
            "activities": [
                "设计意图确认",
                "数量调查",
                "施工方法検討",
                "工程表作成"
            ]
        },
        "E_Estimate": {
            "description": "成本估算 - 積算",
            "activities": [
                "標準歩掛適用",
                "市場単価調査",
                "経費計算",
                "利益管理"
            ]
        },
        "C_Control": {
            "description": "成本控制",
            "activities": [
                "実行予算管理",
                "進捗管理",
                "変更管理",
                "原価診断"
            ]
        }
    }
    
    # 鹿岛建设特色：预制化率调整
    KAJIMA_PREFAB_RATIOS = {
        "低预制": {"factor": 1.0, "range": "0-20%"},
        "中预制": {"factor": 0.95, "range": "20-50%"},
        "高预制": {"factor": 0.90, "range": "50-80%"},
        "单元预制": {"factor": 0.85, "range": "80%+"}
    }
    
    # 清水建设特色：CRM (Cost Risk Management)
    SHIMIZU_CRM = {
        "定性评价": [
            "设计深度不足",
            "地質リスク",
            " Market price volatility",
            "工期不确定性",
            "施工難易度"
        ],
        "定量评价": [
            "历史项目偏差分析",
            "蒙特卡洛シミュレーション",
            "贝叶斯更新"
        ],
        "应对策略": [
            "应急费 (5-15%)",
            "价格调整条款",
            "风险分担机制"
        ]
    }
    
    # 竹中用工店特色：精密度管理
    TAKENAKA_PRECISION = {
        "测量精度": "+/-1mm",
        "平整度管理": "3mm/10m",
        "高程管理": "+/-5mm",
        "轴线精度": "+/-2mm",
        "成本精度目标": "+/-3%以内"
    }
    
    @staticmethod
    def sekisan_estimate(
        structural_work: Dict[str, float],
        architectural_work: Dict[str, float],
        mep_work: Dict[str, float],
        overhead_rate: float = 0.18
    ) -> Dict[str, Any]:
        """
        日本積算式估算
        
        结构工程: {"RC": m³, "S": t, "SRC": m³}
        建筑装修: {"型枠": m2, "左官": m2, "内装": m2}
        机电: {" Plumbing": m2, "電気": m2, "的空": m2}
        """
        
        # 基准单价 (含管理费和利润)
        unit_prices = {
            "RC": 18000,  # 日元/m³
            "S": 95000,   # 日元/t
            "SRC": 22000, # 日元/m³
            "型枠": 6500,  # 日元/m2
            "左官": 4500,  # 日元/m2
            "内装": 12000, # 日元/m2
            " Plumbing": 8500,
            "電気": 15000,
            "的空": 22000
        }
        
        # 计算直接费
        structural_cost = sum(
            structural_work.get(work_type, 0) * unit_prices.get(work_type, 0)
            for work_type in structural_work
        )
        
        architectural_cost = sum(
            architectural_work.get(work_type, 0) * unit_prices.get(work_type, 0)
            for work_type in architectural_work
        )
        
        mep_cost = sum(
            mep_work.get(work_type, 0) * unit_prices.get(work_type, 0)
            for work_type in mep_work
        )
        
        direct_cost = structural_cost + architectural_cost + mep_cost
        
        # 経費 (间接费) 通常18-22%
        overhead = direct_cost * overhead_rate
        
        # 利润 通常3-5%
        profit = (direct_cost + overhead) * 0.04
        
        total_cost = direct_cost + overhead + profit
        
        return {
            "method": "日本積算法 (Sekisan)",
            "breakdown": {
                "構造工事": {"cost": structural_cost, "currency": "JPY"},
                "建築工事": {"cost": architectural_cost, "currency": "JPY"},
                "設備工事": {"cost": mep_cost, "currency": "JPY"},
                "直接費合計": direct_cost,
                "経費": overhead,
                "利潤": profit,
                "総合計": total_cost
            },
            "rate_analysis": {
                "経費率": overhead_rate,
                "利益率": 0.04,
                "間接費率": overhead_rate / (1 + overhead_rate)
            }
        }
    
    @staticmethod
    def get_sekisan_summary() -> Dict[str, Any]:
        """获取日本積算方法摘要"""
        return {
            "institutes": [
                {
                    "name": "日本建築積算協会 (BSIJ)",
                    "role": "建築積算士資格、制度確立"
                },
                {
                    "name": "(一財)建築コスト管理システム研究所 (RIBC)",
                    "role": "共通歩掛りデータベース"
                }
            ],
            "methods": [
                {
                    "name": "SEC皮和方法",
                    "description": "Scope-Estimate-Control lifecycle"
                },
                {
                    "name": "標準歩掛法",
                    "description": "基于标准人工定额的估算"
                },
                {
                    "name": "市場単価法",
                    "description": "基于市场单价的估算"
                }
            ],
            "standards": [
                "公共建築工事積算基準 (国交省)",
                "建築工程標準詳細書",
                "建設機械等損料算定基準"
            ]
        }


# ==================== 中国本土QS方法论 ====================

class ChineseQSMethods:
    """中国本土工料测量方法"""
    
    # GB/T 50500-2024 造价构成
    COST_COMPONENTS_GB50500 = {
        "建安工程费": {
            "的分": {
                "人工费": 0.15,
                "材料费": 0.55,
                "施工机具使用费": 0.08,
                "企业管理费": 0.12,
                "利润": 0.10
            }
        },
        "工程建设其他费": {
            "用地与工程准备费": 0.03,
            "技术服务费": 0.02,
            "工程建设其他费用": 0.05
        },
        "预备费": {
            "基本预备费": 0.05,
            "价差预备费": 0.03
        }
    }
    
    # 中国特色估算阶段
    ESTIMATION_STAGES = {
        "项目建议书": {
            "precision": "+/-30%",
            "method": "类似工程单方造价指标",
            "依据": "类似工程决算资料"
        },
        "可行性研究": {
            "precision": "+/-20%",
            "method": "单元估算法/概算指标",
            "依据": "概算定额/概算指标"
        },
        "初步设计": {
            "precision": "+/-10%",
            "method": "概算定额法",
            "依据": "概算定额/标准设计"
        },
        "施工图设计": {
            "precision": "+/-5%",
            "method": "预算定额法/工程量清单",
            "依据": "预算定额/工程量清单计价规范"
        }
    }
    
    # 中国规范体系
    DESIGN_NORMS_SYSTEM = {
        "结构设计": {
            "GB50010-2024": "混凝土结构设计标准",
            "GB50011-2024": "建筑抗震设计标准",
            "GB50017-2024": "钢结构设计标准",
            "GB50005-2023": "木结构设计标准"
        },
        "建筑设计": {
            "GB50016-2024": "建筑设计防火规范",
            "GB50352-2019": "民用建筑设计统一标准",
            "GB50189-2022": "公共建筑节能设计标准"
        },
        "机电设计": {
            "GB50015-2019": "建筑给水排水设计标准",
            "GB50052-2024": "供配电系统设计规范",
            "GB50736-2012": "民用建筑供暖通风与空气调节设计规范",
            "GB51309-2018": "消防应急照明和疏散指示系统技术标准"
        },
        "施工验收": {
            "GB50300-2013": "建筑工程施工质量验收统一标准",
            "GB50202-2018": "建筑地基基础工程施工质量验收标准",
            "GB50204-2015": "混凝土结构工程施工质量验收规范"
        }
    }
    
    @staticmethod
    def generate_cost_breakdown_gb50500(
        total_cost: float,
        breakdown_level: str = "detailed"
    ) -> Dict[str, Any]:
        """
        按GB/T 50500-2024生成造价构成
        
        breakdown_level: "summary" | "standard" | "detailed"
        """
        
        components = {
            "建安工程费": total_cost * 0.75,
            "工程建设其他费": total_cost * 0.10,
            "预备费": total_cost * 0.08,
            "建设期利息": total_cost * 0.05,
            "流动资金": total_cost * 0.02
        }
        
        if breakdown_level in ["standard", "detailed"]:
            # 详细分解建安工程费
            jian_an = components["建安工程费"]
            components["建安费_详细"] = {
                "分部工程": {
                    "土建工程": jian_an * 0.45,
                    "装饰装修": jian_an * 0.15,
                    "给排水": jian_an * 0.05,
                    "电气工程": jian_an * 0.08,
                    "通风空调": jian_an * 0.10,
                    "消防工程": jian_an * 0.05,
                    "电梯工程": jian_an * 0.04,
                    "弱电智能化": jian_an * 0.03,
                    "其他": jian_an * 0.05
                },
                "费用组成": {
                    "人工费": jian_an * 0.15,
                    "材料费": jian_an * 0.50,
                    "机械费": jian_an * 0.08,
                    "管理费": jian_an * 0.15,
                    "利润": jian_an * 0.08,
                    "规费": jian_an * 0.04
                }
            }
        
        return {
            "standard": "GB/T 50500-2024",
            "breakdown_level": breakdown_level,
            "components": components,
            "cost_per_sqm": {
                "建安工程费": components["建安工程费"] / 10000,
                "其他费用": (total_cost - components["建安工程费"]) / 10000
            }
        }


# ==================== 全局估算融合器 ====================

class GlobalEstimatorFuser:
    """全球方法论融合估算器"""
    
    def __init__(self):
        self.aecom = AECOMCostMethods()
        self.wsp = WSPMethods()
        self.japanese = JapaneseSuperGCMethods()
        self.chinese = ChineseQSMethods()
    
    def comprehensive_estimate(
        self,
        total_area: float,
        building_type: str,
        structure_type: str,
        city: str,
        quality: str = "中档",
        floor_count: int = 20
    ) -> Dict[str, Any]:
        """
        综合多方法论估算
        
        融合 AECOM / WSP / 日本五大建设 / 中国本土方法
        """
        
        # 1. WSP 单位成本法
        wsp_result = WSPMethods.generate_cost_plan(
            total_area=total_area,
            building_type=building_type,
            location=city,
            quality=quality
        )
        
        # 2. AECOM 参数化调整
        location_factor = wsp_result["cost_summary"]["location_factor"]
        complexity_factor = 1.0 + (floor_count - 10) * 0.02  # 楼层复杂度
        time_factor = 1.02  # 时间通胀因子
        
        aecom_adjusted = AECOMCostMethods.parametric_estimate(
            base_cost=wsp_result["cost_summary"]["unit_cost"],
            complexity_factor=complexity_factor,
            location_factor=location_factor,
            time_factor=time_factor
        )
        
        # 3. 蒙特卡洛风险分析 (AECOM方法)
        risk_factors = [
            {"name": "设计变更", "min": 0.95, "max": 1.10, "weight": 0.05},
            {"name": "材料价格", "min": 0.90, "max": 1.15, "weight": 0.10},
            {"name": "人工成本", "min": 0.95, "max": 1.08, "weight": 0.05},
            {"name": "工期延误", "min": 0.98, "max": 1.05, "weight": 0.03}
        ]
        
        base_estimate = wsp_result["cost_summary"]["total_cost"]
        monte_carlo = AECOMCostMethods.monte_carlo_risk_estimate(
            base_cost=base_estimate,
            risk_factors=risk_factors,
            iterations=10000
        )
        
        # 4. 中国GB50500造价构成
        chinese_breakdown = ChineseQSMethods.generate_cost_breakdown_gb50500(
            total_cost=monte_carlo["p50"],
            breakdown_level="standard"
        )
        
        # 5. 日本SECI方法摘要
        seci_summary = JapaneseSuperGCMethods.get_sekisan_summary()
        
        # 6. 融合估算
        # 加权平均：WSP(30%) + AECOM参数化(30%) + 蒙特卡洛P50(40%)
        fused_unit_cost = (
            wsp_result["cost_summary"]["unit_cost"] * 0.3 +
            aecom_adjusted["adjusted_cost"] * 0.3 +
            monte_carlo["p50"] / total_area * 0.4
        )
        
        return {
            "version": "v3.3 Global QS Integration",
            "project_info": {
                "building_type": building_type,
                "structure_type": structure_type,
                "city": city,
                "total_area": total_area,
                "floor_count": floor_count,
                "quality": quality
            },
            
            "method_results": {
                "wsp_unit_cost": {
                    "unit_cost": wsp_result["cost_summary"]["unit_cost"],
                    "total_cost": wsp_result["cost_summary"]["total_cost"],
                    "classification": wsp_result["classification"]["name"]
                },
                "aecom_parametric": {
                    "unit_cost": aecom_adjusted["adjusted_cost"],
                    "factors": aecom_adjusted["breakdown"]
                },
                "monte_carlo": {
                    "p10": monte_carlo["p10"] / total_area,
                    "p50": monte_carlo["p50"] / total_area,
                    "p90": monte_carlo["p90"] / total_area,
                    "confidence_range": f"+/-{((monte_carlo['p90'] - monte_carlo['p10']) / monte_carlo['p50'] / 2 * 100):.1f}%"
                }
            },
            
            "fused_estimate": {
                "unit_cost": fused_unit_cost,
                "total_cost": fused_unit_cost * total_area,
                "range": {
                    "low": monte_carlo["p10"] / total_area,
                    "high": monte_carlo["p90"] / total_area
                }
            },
            
            "chinese_gb50500": chinese_breakdown,
            
            "japanese_methods": seci_summary,
            
            "recommendations": {
                "pre_design": "建议采用WSP Class C估算作为初步参考",
                "design_stage": "建议采用AECOM参数化+蒙特卡洛P50作为设计概算",
                "tender_stage": "建议采用详细工程量清单+中国GB50500造价构成"
            }
        }


# ==================== 快速估算函数 ====================

def global_quick_estimate(
    total_area: float,
    building_type: str = "办公",
    structure_type: str = "框架-剪力墙",
    city: str = "深圳",
    quality: str = "中档",
    floor_count: int = 20
) -> Dict[str, Any]:
    """
    快速全球方法论综合估算
    
    使用示例:
    >>> result = global_quick_estimate(
    ...     total_area=50000,
    ...     building_type="办公",
    ...     city="深圳",
    ...     quality="高档",
    ...     floor_count=30
    ... )
    """
    fuser = GlobalEstimatorFuser()
    return fuser.comprehensive_estimate(
        total_area=total_area,
        building_type=building_type,
        structure_type=structure_type,
        city=city,
        quality=quality,
        floor_count=floor_count
    )


# ==================== 主测试 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("DLHZ Global QS Integration v3.3")
    print("Global Engineering Companies + Chinese Characteristics")
    print("=" * 60)
    
    # 测试综合估算
    result = global_quick_estimate(
        total_area=50000,
        building_type="办公",
        structure_type="框架-核心筒",
        city="深圳",
        quality="高档",
        floor_count=30
    )
    
    print(f"\n[Project] {result['project_info']['building_type']} | {result['project_info']['city']}")
    print(f"  Area: {result['project_info']['total_area']:,}m2 | Floors: {result['project_info']['floor_count']}")
    
    print(f"\n[Method Results]")
    print(f"  WSP: {result['method_results']['wsp_unit_cost']['unit_cost']:,.0f} CNY/m2")
    print(f"  AECOM: {result['method_results']['aecom_parametric']['unit_cost']:,.0f} CNY/m2")
    print(f"  Monte Carlo P50: {result['method_results']['monte_carlo']['p50']:,.0f} CNY/m2")
    
    print(f"\n[Fused Estimate]")
    fused = result['fused_estimate']
    print(f"  Unit Cost: {fused['unit_cost']:,.0f} CNY/m2")
    print(f"  Total Cost: {fused['total_cost']/10000:,.0f} 10k CNY")
    print(f"  Range: {fused['range']['low']:,.0f} ~ {fused['range']['high']:,.0f} CNY/m2")
    
    print(f"\n[Japanese SECI Methods]")
    for method in result['japanese_methods']['methods']:
        print(f"  - {method['name']}: {method['description']}")
    
    print(f"\n[Recommendations]")
    for stage, rec in result['recommendations'].items():
        print(f"  {stage}: {rec}")
    
    print("\n" + "=" * 60)
    print("Global QS + Japanese Precision + Chinese Standards = v3.3")
    print("=" * 60)
