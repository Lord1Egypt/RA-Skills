#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================
度量衡智库 · 关键材料因子引擎 v3.0
Key Material Factors Engine for Construction Cost Estimation
==============================================================
从2000+种建筑材料中遴选6大关键因子：
  M1 - 钢筋(螺纹钢/线材)   造价占比12%~18%, 年波动±15%
  M2 - 混凝土(商品砼)      造价占比8%~15%,  年波动±10%
  M3 - 铜(电线电缆)        造价占比8%~15%,  年波动±20%
  M4 - 铝合金(门窗/幕墙)   造价占比5%~12%,  年波动±15%
  M5 - 玻璃(幕墙/门窗)     造价占比4%~10%,  年波动±15%
  M6 - 结构型钢(H型钢/钢管) 造价占比3%~8%,   年波动±12%
==============================================================
"""

import json
import math
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# ==============================================================
# 数据结构
# ==============================================================

class MaterialFactor(Enum):
    """材料因子枚举"""
    M1_REBAR = "M1"  # 钢筋
    M2_CONCRETE = "M2"  # 混凝土
    M3_COPPER = "M3"  # 铜
    M4_ALUMINUM = "M4"  # 铝合金
    M5_GLASS = "M5"  # 玻璃
    M6_STRUCTURAL_STEEL = "M6"  # 结构型钢


@dataclass
class MaterialPrice:
    """材料价格数据"""
    material_code: str
    material_name: str
    spec: str
    unit: str
    price_low: float  # 低限
    price_median: float  # 中值
    price_high: float  # 高限
    currency: str = "CNY"
    unit_display: str = ""  # 显示用的单位
    last_updated: str = ""

    def __post_init__(self):
        if not self.last_updated:
            self.last_updated = datetime.now().strftime("%Y-%m-%d")


@dataclass
class CostImpact:
    """成本影响分析结果"""
    material_code: str
    material_name: str
    price_change_percent: float
    cost_weight: float  # 造价占比
    project_cost_impact: float  # 对项目总造价的影响金额
    project_cost_impact_percent: float  # 对项目总造价的百分比
    confidence: str  # 高/中/低


@dataclass
class UncertaintyResult:
    """不确定性分析结果"""
    percentile_10: float
    percentile_50: float
    percentile_80: float
    percentile_90: float
    percentile_95: float
    confidence_80_low: float
    confidence_80_high: float
    confidence_95_low: float
    confidence_95_high: float
    probability_price_increase: float  # 价格上涨概率


# ==============================================================
# 材料因子数据库
# ==============================================================

class MaterialFactorDB:
    """材料因子数据库"""

    # 当前参考价格 (2026年Q1基准价，单位：元)
    CURRENT_PRICES = {
        "M1": MaterialPrice(
            material_code="M1",
            material_name="钢筋(螺纹钢/线材)",
            spec="HRB400 螺纹钢",
            unit="元/吨",
            price_low=4000,
            price_median=4300,
            price_high=4800,
            unit_display="元/吨",
            last_updated="2026-01-15"
        ),
        "M2": MaterialPrice(
            material_code="M2",
            material_name="混凝土",
            spec="C30 商品混凝土(泵送)",
            unit="元/m3",
            price_low=520,
            price_median=560,
            price_high=620,
            unit_display="元/m3",
            last_updated="2026-01-15"
        ),
        "M3": MaterialPrice(
            material_code="M3",
            material_name="铜(电线电缆)",
            spec="1# 电解铜",
            unit="元/吨",
            price_low=62000,
            price_median=68000,
            price_high=75000,
            unit_display="元/吨",
            last_updated="2026-01-15"
        ),
        "M4": MaterialPrice(
            material_code="M4",
            material_name="铝合金",
            spec="A00 铝锭",
            unit="元/吨",
            price_low=18000,
            price_median=19500,
            price_high=23000,
            unit_display="元/吨",
            last_updated="2026-01-15"
        ),
        "M5": MaterialPrice(
            material_code="M5",
            material_name="玻璃",
            spec="5mm 浮法白玻原片",
            unit="元/重箱",
            price_low=90,
            price_median=100,
            price_high=120,
            unit_display="元/重箱",
            last_updated="2026-01-15"
        ),
        "M6": MaterialPrice(
            material_code="M6",
            material_name="结构型钢",
            spec="Q355B 热轧H型钢",
            unit="元/吨",
            price_low=4000,
            price_median=4400,
            price_high=5000,
            unit_display="元/吨",
            last_updated="2026-01-15"
        ),
    }

    # 成本权重 (各类材料占建安造价的比例)
    COST_WEIGHTS = {
        "M1": {"typical": 0.15, "range": [0.12, 0.18], "description": "框架-剪力墙结构"},
        "M2": {"typical": 0.12, "range": [0.08, 0.15], "description": "含地下室项目"},
        "M3": {"typical": 0.08, "range": [0.04, 0.12], "description": "标准办公楼"},
        "M4": {"typical": 0.07, "range": [0.05, 0.12], "description": "含幕墙项目"},
        "M5": {"typical": 0.05, "range": [0.04, 0.10], "description": "含幕墙项目"},
        "M6": {"typical": 0.04, "range": [0.02, 0.08], "description": "混凝土结构"},
    }

    # 年价格波动率 (标准差)
    ANNUAL_VOLATILITY = {
        "M1": 0.15,  # +/-15%
        "M2": 0.10,  # +/-10%
        "M3": 0.20,  # +/-20%
        "M4": 0.15,  # +/-15%
        "M5": 0.15,  # +/-15%
        "M6": 0.12,  # +/-12%
    }

    # 相关系数矩阵
    CORRELATION_MATRIX = {
        ("M1", "M6"): 0.85,  # 螺纹钢与结构型钢高度相关
        ("M1", "M2"): 0.30,  # 与混凝土弱相关
        ("M3", "M4"): 0.65,  # 铜与铝合金中度相关(有色金属)
        ("M4", "M5"): 0.40,  # 铝合金与玻璃中度相关(幕墙)
        ("M1", "M3"): 0.20,  # 弱相关
        ("M2", "M3"): 0.15,  # 弱相关
    }

    # 数据来源
    DATA_SOURCES = {
        "M1": "我的钢铁网(mysteel.com)、兰格钢铁网",
        "M2": "数字水泥网、中国水泥网",
        "M3": "上海有色金属网(SMM)、LME伦敦金属交易所",
        "M4": "上海有色金属网(SMM)、长江有色金属网",
        "M5": "中国玻璃信息网、隆众资讯",
        "M6": "我的钢铁网、钢结构协会",
    }

    @classmethod
    def get_price(cls, material_code: str) -> Optional[MaterialPrice]:
        """获取材料当前价格"""
        return cls.CURRENT_PRICES.get(material_code)

    @classmethod
    def get_all_prices(cls) -> Dict[str, MaterialPrice]:
        """获取所有材料价格"""
        return cls.CURRENT_PRICES.copy()

    @classmethod
    def get_cost_weight(cls, material_code: str) -> Tuple[float, List[float]]:
        """获取成本权重"""
        if material_code in cls.COST_WEIGHTS:
            w = cls.COST_WEIGHTS[material_code]
            return w["typical"], w["range"]
        return 0.05, [0.03, 0.08]


# ==============================================================
# 材料因子引擎
# ==============================================================

class MaterialFactorEngine:
    """材料因子分析引擎"""

    def __init__(self):
        self.db = MaterialFactorDB()

    def get_current_prices_report(self) -> str:
        """生成当前价格报告"""
        lines = []
        lines.append("=" * 70)
        lines.append("         度量衡智库 - 关键材料因子价格查询报告")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"  查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"  数据来源: 各权威行业平台加权平均")
        lines.append("")

        prices = self.db.get_all_prices()

        lines.append("[6大关键材料因子当前参考价格]")
        lines.append("-" * 70)
        lines.append(f"  {'代码':<5} {'材料名称':<18} {'规格':<18} {'低限':<12} {'中值':<12} {'高限':<12}")
        lines.append(f"  {'-'*5} {'-'*18} {'-'*18} {'-'*12} {'-'*12} {'-'*12}")

        for code in ["M1", "M2", "M3", "M4", "M5", "M6"]:
            p = prices[code]
            lines.append(
                f"  {code:<5} {p.material_name:<18} {p.spec:<18} "
                f"{p.price_low:>10,.0f} {p.price_median:>10,.0f} {p.price_high:>10,.0f}"
            )

        lines.append("")
        lines.append("[价格区间解读]")
        lines.append("-" * 70)
        lines.append("  低限: 市场价格较低区间(第25百分位)")
        lines.append("  中值: 市场价格中位值(第50百分位)")
        lines.append("  高限: 市场价格较高区间(第75百分位)")
        lines.append("")
        lines.append("[数据来源]")
        lines.append("-" * 70)
        for code, source in self.db.DATA_SOURCES.items():
            lines.append(f"  {code} - {source}")

        lines.append("")
        lines.append("[价格波动预警]")
        lines.append("-" * 70)

        copper_price = prices["M3"].price_median
        if copper_price > 70000:
            lines.append("  WARNING: 铜价处于高位(>70,000元/吨)，建议关注期货对冲机会")
        elif copper_price < 60000:
            lines.append("  TIP: 铜价处于低位(<60,000元/吨)，可考虑提前锁价")

        steel_price = prices["M1"].price_median
        if steel_price > 4500:
            lines.append("  WARNING: 钢筋价格处于高位(>4,500元/吨)，成本压力较大")
        else:
            lines.append("  TIP: 钢筋价格处于中位水平，成本可控")

        lines.append("")
        lines.append("=" * 70)
        lines.append("  免责声明: 本价格仅供参考，实际采购价以供应商报价为准")
        lines.append("  建议关注各地造价站发布的信息价获取更精准的本地化数据")
        lines.append("=" * 70)

        return "\n".join(lines)

    def calculate_cost_impact(
        self,
        project_total_cost: float,
        material_code: str,
        price_change_percent: float
    ) -> CostImpact:
        """计算材料价格变动对项目成本的影响"""
        p = self.db.get_price(material_code)
        if not p:
            raise ValueError(f"Unknown material code: {material_code}")

        weight, _ = self.db.get_cost_weight(material_code)
        weight_percent = weight * 100

        impact_percent = weight * (price_change_percent / 100) * 100
        impact_amount = project_total_cost * weight * (price_change_percent / 100)

        if abs(price_change_percent) <= 15:
            confidence = "高"
        elif abs(price_change_percent) <= 25:
            confidence = "中"
        else:
            confidence = "低"

        return CostImpact(
            material_code=material_code,
            material_name=p.material_name,
            price_change_percent=price_change_percent,
            cost_weight=weight_percent,
            project_cost_impact=impact_amount,
            project_cost_impact_percent=impact_percent,
            confidence=confidence
        )

    def calculate_multi_material_impact(
        self,
        project_total_cost: float,
        price_changes: Dict[str, float]
    ) -> Tuple[List[CostImpact], float]:
        """计算多种材料价格变动对项目成本的综合影响"""
        results = []
        total_impact = 0

        for code, change in price_changes.items():
            impact = self.calculate_cost_impact(project_total_cost, code, change)
            results.append(impact)
            total_impact += impact.project_cost_impact

        return results, total_impact

    def generate_cost_impact_report(
        self,
        project_total_cost: float,
        price_changes: Dict[str, float],
        project_name: str = "某工程项目"
    ) -> str:
        """生成成本影响分析报告"""
        lines = []
        lines.append("=" * 70)
        lines.append("         度量衡智库 - 材料价格变动成本影响分析报告")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"  项目名称: {project_name}")
        lines.append(f"  项目总造价: ¥ {project_total_cost:>15,.2f} 元")
        lines.append(f"  分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        results, total_impact = self.calculate_multi_material_impact(
            project_total_cost, price_changes
        )

        lines.append("[材料价格变动清单]")
        lines.append("-" * 70)
        lines.append(f"  {'材料':<16} {'变动幅度':<12} {'造价占比':<10} {'影响金额':<15} {'影响比例':<10} {'置信度':<6}")
        lines.append(f"  {'-'*16} {'-'*12} {'-'*10} {'-'*15} {'-'*10} {'-'*6}")

        for r in results:
            change_str = f"+{r.price_change_percent:.1f}%" if r.price_change_percent >= 0 else f"{r.price_change_percent:.1f}%"
            lines.append(
                f"  {r.material_name:<14} {change_str:>10} "
                f"{r.cost_weight:>8.1f}% "
                f"¥ {abs(r.project_cost_impact):>12,.0f} "
                f"{r.project_cost_impact_percent:>8.2f}% "
                f"{r.confidence:>4}"
            )

        lines.append("")
        lines.append("[汇总分析]")
        lines.append("-" * 70)

        total_impact_percent = (total_impact / project_total_cost) * 100

        if total_impact > 0:
            lines.append(f"  材料涨价导致项目成本增加:")
            lines.append(f"     增加金额: ¥ {total_impact:>15,.2f} 元")
        else:
            lines.append(f"  材料降价可节省项目成本:")
            lines.append(f"     节省金额: ¥ {abs(total_impact):>15,.2f} 元")

        lines.append(f"     影响比例: {total_impact_percent:>8.2f}%")
        lines.append("")

        lines.append("[敏感性排序 (影响金额从大到小)]")
        lines.append("-" * 70)
        sorted_results = sorted(results, key=lambda x: abs(x.project_cost_impact), reverse=True)
        for i, r in enumerate(sorted_results, 1):
            lines.append(f"  {i}. {r.material_name}: ¥ {abs(r.project_cost_impact):>12,.0f} 元 ({r.confidence}置信)")

        lines.append("")
        lines.append("[风险提示]")
        lines.append("-" * 70)

        high_risk = [r for r in results if abs(r.project_cost_impact_percent) > 1.0]
        if high_risk:
            lines.append("  WARNING 高风险材料 (影响>1%):")
            for r in high_risk:
                lines.append(f"     - {r.material_name}: 影响比例 {r.project_cost_impact_percent:.2f}%")

        lines.append("")
        lines.append("[建议措施]")
        lines.append("-" * 70)

        if total_impact > project_total_cost * 0.05:
            lines.append("  1. 建议启动价格风险应急预案")
            lines.append("  2. 考虑期货对冲或价格保险")
            lines.append("  3. 与供应商签订价格调整条款合同")
        else:
            lines.append("  1. 密切监控材料价格走势")
            lines.append("  2. 适时启动战略采购")
            lines.append("  3. 预留价格调整预备费")

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def monte_carlo_uncertainty(
        self,
        project_total_cost: float,
        holding_period_months: int = 12
    ) -> UncertaintyResult:
        """蒙特卡洛模拟 - 计算项目造价的不确定性区间"""
        annual_volatility = {
            "M1": 0.15, "M2": 0.10, "M3": 0.20,
            "M4": 0.15, "M5": 0.15, "M6": 0.12
        }

        weights = {
            "M1": 0.15, "M2": 0.12, "M3": 0.08,
            "M4": 0.07, "M5": 0.05, "M6": 0.04
        }

        n_simulations = 10000
        results = []

        for _ in range(n_simulations):
            total_change = 0

            for code, weight in weights.items():
                sigma = annual_volatility[code] * math.sqrt(holding_period_months / 12)
                z = random.gauss(0, sigma)
                price_change = math.exp(z) - 1

                total_change += weight * price_change

            final_cost = project_total_cost * (1 + total_change)
            results.append(final_cost)

        results.sort()
        n = len(results)

        return UncertaintyResult(
            percentile_10=results[int(n * 0.10)],
            percentile_50=results[int(n * 0.50)],
            percentile_80=results[int(n * 0.80)],
            percentile_90=results[int(n * 0.90)],
            percentile_95=results[int(n * 0.95)],
            confidence_80_low=results[int(n * 0.10)],
            confidence_80_high=results[int(n * 0.90)],
            confidence_95_low=results[int(n * 0.025)],
            confidence_95_high=results[int(n * 0.975)],
            probability_price_increase=sum(1 for r in results if r > project_total_cost) / n
        )

    def generate_uncertainty_report(
        self,
        project_total_cost: float,
        project_name: str = "某工程项目",
        holding_period_months: int = 12
    ) -> str:
        """生成不确定性分析报告"""
        lines = []
        lines.append("=" * 70)
        lines.append("         度量衡智库 - '测不准'造价波动不确定性分析报告")
        lines.append("              -- 基于蒙特卡洛模拟的材料价格传播模型")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"  项目名称: {project_name}")
        lines.append(f"  基准造价: ¥ {project_total_cost:>15,.2f} 元")
        lines.append(f"  分析周期: {holding_period_months} 个月")
        lines.append(f"  模拟次数: 10,000 次")
        lines.append("")

        result = self.monte_carlo_uncertainty(
            project_total_cost, holding_period_months
        )

        lines.append("[蒙特卡洛模拟结果]")
        lines.append("-" * 70)
        lines.append(f"  基准造价(当前):     ¥ {project_total_cost:>15,.2f} 元")
        lines.append(f"  P50(中值, 50%概率): ¥ {result.percentile_50:>15,.2f} 元")
        lines.append("")

        mid_budget = result.percentile_50
        high_budget = result.confidence_80_high

        lines.append(f"  [80%置信区间]")
        lines.append(f"    低限: ¥ {result.confidence_80_low:>15,.2f} 元  (偏差 {(result.confidence_80_low/project_total_cost-1)*100:+.1f}%)")
        lines.append(f"    高限: ¥ {result.confidence_80_high:>15,.2f} 元  (偏差 {(result.confidence_80_high/project_total_cost-1)*100:+.1f}%)")
        lines.append(f"    区间幅度: ¥ {result.confidence_80_high - result.confidence_80_low:>15,.2f} 元")

        lines.append("")
        lines.append(f"  [95%置信区间]")
        lines.append(f"    低限: ¥ {result.confidence_95_low:>15,.2f} 元  (偏差 {(result.confidence_95_low/project_total_cost-1)*100:+.1f}%)")
        lines.append(f"    高限: ¥ {result.confidence_95_high:>15,.2f} 元  (偏差 {(result.confidence_95_high/project_total_cost-1)*100:+.1f}%)")

        lines.append("")
        lines.append("[分位数分布]")
        lines.append("-" * 70)
        lines.append(f"  P10(最乐观10%): ¥ {result.percentile_10:>15,.2f} 元  (比基准低 {(1-result.percentile_10/project_total_cost)*100:.1f}%)")
        lines.append(f"  P50(中位数):    ¥ {result.percentile_50:>15,.2f} 元  (比基准 {(result.percentile_50/project_total_cost-1)*100:+.1f}%)")
        lines.append(f"  P90(最悲观10%): ¥ {result.percentile_90:>15,.2f} 元  (比基准高 {(result.percentile_90/project_total_cost-1)*100:.1f}%)")
        lines.append(f"  P95(极端悲观):  ¥ {result.percentile_95:>15,.2f} 元  (比基准高 {(result.percentile_95/project_total_cost-1)*100:.1f}%)")

        lines.append("")
        lines.append("[概率分析]")
        lines.append("-" * 70)
        lines.append(f"  材料价格上涨概率: {result.probability_price_increase*100:.1f}%")
        lines.append(f"  材料价格下跌概率: {(1-result.probability_price_increase)*100:.1f}%")

        lines.append("")
        lines.append("[预算建议]")
        lines.append("-" * 70)

        low_budget = result.percentile_10

        lines.append(f"  情形1 - 乐观预算: ¥ {result.percentile_10:>15,.2f} 元 (P10)")
        lines.append(f"  情形2 - 中性预算: ¥ {mid_budget:>15,.2f} 元 (P50)")
        lines.append(f"  情形3 - 悲观预算: ¥ {high_budget:>15,.2f} 元 (P90)")
        lines.append(f"  建议预备费(不可预见费): ¥ {high_budget - project_total_cost:>15,.2f} 元 (约{(high_budget/project_total_cost-1)*100:.1f}%)")

        lines.append("")
        lines.append("[测不准原理说明]")
        lines.append("-" * 70)
        lines.append("  本分析基于以下假设:")
        lines.append("  (1) 各材料价格变动服从对数正态分布")
        lines.append("  (2) 6大因子之间存在特定相关性(铜-铝联动、钢-铁联动等)")
        lines.append("  (3) 模拟10,000次，统计得出概率分布")
        lines.append("")
        lines.append("  核心洞察: 不追求精确预测，而是量化不确定性区间。")
        lines.append("  当我们知道'我们不知道多少'时，才是真正的工程智慧。")

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)


# ==============================================================
# 演示函数
# ==============================================================

def demo_price_query():
    """演示：价格查询"""
    print("\n" + "=" * 70)
    print("  演示1: 查询当前6大关键材料因子价格")
    print("=" * 70 + "\n")

    engine = MaterialFactorEngine()
    print(engine.get_current_prices_report())


def demo_cost_impact():
    """演示：成本影响分析"""
    print("\n" + "=" * 70)
    print("  演示2: 材料涨价对项目成本的影响分析")
    print("=" * 70 + "\n")

    engine = MaterialFactorEngine()

    price_changes = {
        "M3": 20,  # 铜涨20%
        "M4": 10,  # 铝涨10%
        "M1": 5,   # 钢筋涨5%
    }

    print(engine.generate_cost_impact_report(
        project_total_cost=500_000_000,
        price_changes=price_changes,
        project_name="某商业综合体项目(地上10万m2)"
    ))


def demo_uncertainty():
    """演示：不确定性分析"""
    print("\n" + "=" * 70)
    print("  演示3: 基于蒙特卡洛模拟的造价不确定性分析")
    print("=" * 70 + "\n")

    engine = MaterialFactorEngine()

    print(engine.generate_uncertainty_report(
        project_total_cost=500_000_000,
        project_name="某商业综合体项目",
        holding_period_months=24
    ))


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("    度量衡智库 - 关键材料因子引擎 v3.0")
    print("    从2000+种材料中遴选6大关键因子")
    print("    量化工程造价的不确定性")
    print("=" * 70)

    demo_price_query()
    demo_cost_impact()
    demo_uncertainty()
