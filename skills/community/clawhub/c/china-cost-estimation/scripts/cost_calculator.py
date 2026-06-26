#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国建设工程快速估算计算器
基于最新国家标准和地方规定
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
from enum import Enum

class ProjectType(Enum):
    """项目类型"""
    RESIDENTIAL_MULTI = "多层住宅"
    RESIDENTIAL_HIGH = "高层住宅"
    COMMERCIAL = "商业建筑"
    OFFICE = "办公建筑"
    EDUCATION_KINDERGARTEN = "教育建筑-幼儿园"
    EDUCATION_SCHOOL = "教育建筑-中小学"
    EDUCATION_UNIVERSITY = "教育建筑-大学"
    MEDICAL_GENERAL = "医疗建筑-综合医院"
    MEDICAL_SPECIALIZED = "医疗建筑-专科医院"
    INDUSTRIAL_LIGHT = "工业厂房-轻钢"
    INDUSTRIAL_CONCRETE = "工业厂房-混凝土"
    WAREHOUSE = "仓储物流"
    UNDERGROUND_PARKING = "地下车库"

class RegionType(Enum):
    """地区类型"""
    TIER1 = "一线城市"
    TIER2 = "二线城市"
    TIER3 = "三四线城市"

class DecorationLevel(Enum):
    """装修标准"""
    ROUGH = "毛坯"
    STANDARD = "普通"
    DECORATED = "精装"
    LUXURY = "豪装"

@dataclass
class CostEstimateResult:
    """估算结果"""
    project_type: str
    building_area: float
    unit_cost_low: float
    unit_cost_mid: float
    unit_cost_high: float
    total_cost_low: float
    total_cost_mid: float
    total_cost_high: float
    cost_breakdown: Dict[str, float]
    other_costs: Dict[str, float]
    contingency: Dict[str, float]
    total_investment: Dict[str, float]

class ChinaCostEstimator:
    """中国建设工程估算器"""
    
    def __init__(self, database_dir: Optional[str] = None):
        """初始化估算器"""
        if database_dir is None:
            skill_dir = Path(__file__).parent.parent
            database_dir = skill_dir / "references"
        
        self.database_dir = Path(database_dir)
        self.load_databases()
    
    def load_databases(self):
        """加载数据库"""
        # 加载估算指标
        indices_path = self.database_dir / "estimation-indices.json"
        with open(indices_path, 'r', encoding='utf-8') as f:
            self.indices = json.load(f)
        
        # 加载费用组成规则
        rules_path = self.database_dir / "cost-composition-rules.json"
        with open(rules_path, 'r', encoding='utf-8') as f:
            self.rules = json.load(f)
    
    def estimate_investment(
        self,
        project_type: str,
        building_area: float,
        region: str = "二线城市",
        decoration: str = "普通",
        other_cost_rate: float = 0.18,
        contingency_rate: float = 0.06
    ) -> CostEstimateResult:
        """
        进行投资估算
        
        Args:
            project_type: 项目类型代码或名称
            building_area: 建筑面积(㎡)
            region: 地区类型
            decoration: 装修标准
            other_cost_rate: 工程建设其他费率
            contingency_rate: 预备费率
        """
        
        # 获取估算指标
        unit_cost_low, unit_cost_mid, unit_cost_high = self._get_unit_cost(
            project_type, region, decoration
        )
        
        # 计算工程费用
        project_cost_low = unit_cost_low * building_area / 10000  # 万元
        project_cost_mid = unit_cost_mid * building_area / 10000
        project_cost_high = unit_cost_high * building_area / 10000
        
        # 计算造价构成
        cost_breakdown = self._calculate_cost_breakdown(project_cost_mid)
        
        # 计算工程建设其他费
        other_costs = {
            "建设管理费": project_cost_mid * 0.015,
            "可行性研究费": project_cost_mid * 0.005,
            "勘察设计费": project_cost_mid * 0.030,
            "工程监理费": project_cost_mid * 0.020,
            "招标代理费": project_cost_mid * 0.005,
            "造价咨询费": project_cost_mid * 0.008,
            "环境影响评价费": project_cost_mid * 0.003,
            "其他费用": project_cost_mid * 0.094
        }
        other_cost_total = sum(other_costs.values())
        
        # 计算预备费
        contingency_base = project_cost_mid + other_cost_total
        contingency = {
            "基本预备费": contingency_base * contingency_rate,
            "价差预备费": 0  # 简化计算
        }
        contingency_total = sum(contingency.values())
        
        # 计算建设投资
        total_investment = {
            "工程费用": project_cost_mid,
            "工程建设其他费": other_cost_total,
            "预备费": contingency_total,
            "建设投资合计": project_cost_mid + other_cost_total + contingency_total
        }
        
        return CostEstimateResult(
            project_type=project_type,
            building_area=building_area,
            unit_cost_low=unit_cost_low,
            unit_cost_mid=unit_cost_mid,
            unit_cost_high=unit_cost_high,
            total_cost_low=project_cost_low * (1 + other_cost_rate + contingency_rate),
            total_cost_mid=project_cost_mid * (1 + other_cost_rate + contingency_rate),
            total_cost_high=project_cost_high * (1 + other_cost_rate + contingency_rate),
            cost_breakdown=cost_breakdown,
            other_costs=other_costs,
            contingency=contingency,
            total_investment=total_investment
        )
    
    def _get_unit_cost(self, project_type: str, region: str, decoration: str) -> Tuple[float, float, float]:
        """获取估算指标"""
        # 在房屋建筑类中查找
        building_categories = self.indices.get("building_construction", {}).get("categories", [])
        
        for category in building_categories:
            if project_type in [category.get("code"), category.get("name")]:
                low = category.get("unit_cost_low", 3000)
                mid = category.get("unit_cost_mid", 3500)
                high = category.get("unit_cost_high", 4000)
                
                # 应用地区调整系数
                region_factors = {"一线城市": 1.2, "二线城市": 1.0, "三四线城市": 0.85}
                region_factor = region_factors.get(region, 1.0)
                
                # 应用装修调整系数
                decoration_factors = {"毛坯": 0.85, "普通": 1.0, "精装": 1.25, "豪装": 1.6}
                decoration_factor = decoration_factors.get(decoration, 1.0)
                
                # 计算调整后的指标
                low = low * region_factor * decoration_factor
                mid = mid * region_factor * decoration_factor
                high = high * region_factor * decoration_factor
                
                return low, mid, high
        
        # 默认返回
        return 3000, 3500, 4000
    
    def _calculate_cost_breakdown(self, project_cost: float) -> Dict[str, float]:
        """计算造价构成"""
        proportions = self.indices.get("cost_proportions", {}).get("building_construction", {})
        
        return {
            "人工费": project_cost * proportions.get("labor_cost", {}).get("proportion_max", 20) / 100,
            "材料费": project_cost * proportions.get("material_cost", {}).get("proportion_max", 55) / 100,
            "机械费": project_cost * proportions.get("equipment_cost", {}).get("proportion_max", 5) / 100,
            "企业管理费": project_cost * proportions.get("management_cost", {}).get("proportion_max", 6) / 100,
            "利润": project_cost * proportions.get("profit", {}).get("proportion_max", 4) / 100,
            "规费": project_cost * proportions.get("fees", {}).get("proportion_max", 4) / 100,
            "税金": project_cost * 0.09 / 1.09  # 增值税9%
        }
    
    def calculate_construction_cost(
        self,
        divisional_works_cost: float,
        project_category: str = "建筑工程"
    ) -> Dict[str, float]:
        """
        计算建筑安装工程造价
        
        Args:
            divisional_works_cost: 分部分项工程费
            project_category: 工程类别
        """
        # 获取费率
        rates = self.rules.get("construction_cost_elements", {}).get("elements", [])
        
        # 措施项目费 (按分部分项工程费的10%估算)
        measures_cost = divisional_works_cost * 0.10
        
        # 其他项目费 (按分部分项工程费的3%估算)
        other_items_cost = divisional_works_cost * 0.03
        
        # 税前造价
        pre_tax_cost = divisional_works_cost + measures_cost + other_items_cost
        
        # 规费 (按税前造价的4%估算)
        fees = pre_tax_cost * 0.04
        
        # 税金 (增值税9%)
        tax_base = pre_tax_cost + fees
        tax = tax_base * 0.09
        
        # 工程造价
        total_cost = tax_base + tax
        
        return {
            "分部分项工程费": divisional_works_cost,
            "措施项目费": measures_cost,
            "其他项目费": other_items_cost,
            "税前造价": pre_tax_cost,
            "规费": fees,
            "税金": tax,
            "工程造价": total_cost
        }
    
    def print_estimate_report(self, result: CostEstimateResult):
        """打印估算报告"""
        print("\n" + "=" * 70)
        print("中国建设工程投资估算报告")
        print("=" * 70)
        
        print(f"\n【项目信息】")
        print(f"  项目类型: {result.project_type}")
        print(f"  建筑面积: {result.building_area:,.2f} ㎡")
        
        print(f"\n【估算指标】")
        print(f"  低限: {result.unit_cost_low:,.2f} 元/㎡")
        print(f"  中值: {result.unit_cost_mid:,.2f} 元/㎡")
        print(f"  高限: {result.unit_cost_high:,.2f} 元/㎡")
        
        print(f"\n【投资估算】（万元）")
        print(f"  低限: {result.total_cost_low:,.2f} 万元")
        print(f"  中值: {result.total_cost_mid:,.2f} 万元")
        print(f"  高限: {result.total_cost_high:,.2f} 万元")
        
        print(f"\n【造价构成】（中值）")
        for item, cost in result.cost_breakdown.items():
            proportion = cost / result.total_investment["工程费用"] * 100
            print(f"  {item}: {cost:,.2f} 万元 ({proportion:.1f}%)")
        
        print(f"\n【工程建设其他费】")
        for item, cost in result.other_costs.items():
            print(f"  {item}: {cost:,.2f} 万元")
        print(f"  小计: {sum(result.other_costs.values()):,.2f} 万元")
        
        print(f"\n【预备费】")
        for item, cost in result.contingency.items():
            print(f"  {item}: {cost:,.2f} 万元")
        print(f"  小计: {sum(result.contingency.values()):,.2f} 万元")
        
        print(f"\n【建设投资汇总】")
        for item, cost in result.total_investment.items():
            print(f"  {item}: {cost:,.2f} 万元")
        
        print("\n" + "=" * 70)
        print("编制依据:")
        print("  - GB/T 50500-2024《建设工程工程量清单计价标准》")
        print("  - 建标[2013]44号《建筑安装工程费用项目组成》")
        print("  - 江苏省建设工程费用定额(2024)")
        print("=" * 70)


def interactive_estimate():
    """交互式估算"""
    print("\n" + "=" * 70)
    print("中国建设工程快速估算系统")
    print("=" * 70)
    
    estimator = ChinaCostEstimator()
    
    # 项目类型选择
    print("\n请选择项目类型:")
    project_types = [
        ("1", "多层住宅"),
        ("2", "高层住宅"),
        ("3", "商业建筑"),
        ("4", "办公建筑"),
        ("5", "教育建筑-幼儿园"),
        ("6", "教育建筑-中小学"),
        ("7", "教育建筑-大学"),
        ("8", "医疗建筑-综合医院"),
        ("9", "医疗建筑-专科医院"),
        ("10", "工业厂房-轻钢"),
        ("11", "工业厂房-混凝土"),
        ("12", "仓储物流"),
        ("13", "地下车库")
    ]
    
    for code, name in project_types:
        print(f"  {code}. {name}")
    
    choice = input("\n请输入选项编号: ").strip()
    project_type_map = dict(project_types)
    project_type = project_type_map.get(choice, "多层住宅")
    
    # 建筑面积
    building_area = float(input("请输入建筑面积(㎡): ").strip() or "10000")
    
    # 地区
    print("\n请选择地区:")
    print("  1. 一线城市")
    print("  2. 二线城市")
    print("  3. 三四线城市")
    region_choice = input("请输入选项编号: ").strip()
    regions = {"1": "一线城市", "2": "二线城市", "3": "三四线城市"}
    region = regions.get(region_choice, "二线城市")
    
    # 装修标准
    print("\n请选择装修标准:")
    print("  1. 毛坯")
    print("  2. 普通")
    print("  3. 精装")
    print("  4. 豪装")
    decoration_choice = input("请输入选项编号: ").strip()
    decorations = {"1": "毛坯", "2": "普通", "3": "精装", "4": "豪装"}
    decoration = decorations.get(decoration_choice, "普通")
    
    # 计算
    result = estimator.estimate_investment(
        project_type=project_type,
        building_area=building_area,
        region=region,
        decoration=decoration
    )
    
    estimator.print_estimate_report(result)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_estimate()
    else:
        # 演示模式
        estimator = ChinaCostEstimator()
        
        # 示例1: 二线城市高层住宅
        print("\n【示例1: 二线城市高层住宅项目】")
        result1 = estimator.estimate_investment(
            project_type="高层住宅",
            building_area=50000,
            region="二线城市",
            decoration="普通"
        )
        estimator.print_estimate_report(result1)
        
        # 示例2: 一线城市医疗建筑
        print("\n【示例2: 一线城市综合医院项目】")
        result2 = estimator.estimate_investment(
            project_type="医疗建筑-综合医院",
            building_area=30000,
            region="一线城市",
            decoration="精装"
        )
        estimator.print_estimate_report(result2)
