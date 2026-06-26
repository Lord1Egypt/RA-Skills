#!/usr/bin/env python3
"""
亚马逊品牌加速器 - Level 2
Amazon Brand Accelerator

功能：
- score: 品牌加速评分（品牌注册/Brand Store/A+内容/品牌广告/透明计划 5维）
- roadmap: 品牌建设路线图
- budget: 预算建议

Author: Amazon Brand Team
Version: 1.0.0
"""

import sys
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class BrandLevel(Enum):
    """品牌等级"""
    PREMIUM = "Premium品牌"
    ADVANCED = "Advanced品牌"
    DEVELOPING = "Developing品牌"
    BASIC = "Basic品牌"
    NONE = "未建立品牌"


@dataclass
class BrandDimension:
    """品牌维度"""
    dimension: str
    score: float
    status: str
    completed_features: List[str] = field(default_factory=list)
    pending_features: List[str] = field(default_factory=list)
    impact_score: float = 0  # 对品牌建设的贡献度


@dataclass
class BrandReport:
    """品牌报告"""
    overall_score: float
    brand_level: BrandLevel
    dimensions: List[BrandDimension]
    roadmap: List[Dict]
    budget_plan: Dict[str, Any]
    recommendations: List[str]


class BrandAccelerator:
    """品牌加速器"""
    
    DIMENSIONS = [
        {"id": "brand_registry", "name": "品牌注册", "weight": 0.15, "essential": True},
        {"id": "brand_store", "name": "Brand Store", "weight": 0.20, "essential": True},
        {"id": "aplus_content", "name": "A+内容", "weight": 0.20, "essential": True},
        {"id": "brand_ads", "name": "品牌广告", "weight": 0.25, "essential": True},
        {"id": "transparency", "name": "透明计划", "weight": 0.20, "essential": False}
    ]
    
    FEATURES = {
        "brand_registry": [
            "TM标注册",
            "R标完成",
            "品牌描述完善",
            "品牌故事完整"
        ],
        "brand_store": [
            "Store创建",
            "店铺装修",
            "品牌首页",
            "子页面配置",
            "品牌Banner"
        ],
        "aplus_content": [
            "基础A+",
            "Premium A+",
            "品牌故事模块",
            "对比图表",
            "FAQ模块"
        ],
        "brand_ads": [
            "品牌视频广告",
            "品牌展示广告",
            "品牌推广(SB)",
            "品牌推广视频(SDV)"
        ],
        "transparency": [
            "透明计划注册",
            "产品贴标",
            "防伪包装",
            "消费者验证"
        ]
    }
    
    def __init__(self):
        self.current_report: Optional[BrandReport] = None
    
    def assess_dimension(self, dim_id: str, features: List[str]) -> BrandDimension:
        """评估单个维度"""
        dim_config = next((d for d in self.DIMENSIONS if d["id"] == dim_id), None)
        if not dim_config:
            return BrandDimension(dimension=dim_id, score=0, status="not_started")
        
        dim_name = dim_config["name"]
        all_features = self.FEATURES.get(dim_id, [])
        
        completed = [f for f in features if f in all_features]
        pending = [f for f in all_features if f not in features]
        
        # 计算分数
        completion_rate = len(completed) / len(all_features) if all_features else 0
        
        # 基础分
        if len(completed) == 0:
            base_score = 0
            status = "not_started"
        elif len(completed) == len(all_features):
            base_score = 100
            status = "complete"
        else:
            base_score = completion_rate * 80 + 10  # 最多90分
            status = "in_progress"
        
        # 关键功能加成
        key_features = {
            "brand_registry": ["R标完成"],
            "brand_store": ["Store创建", "店铺装修"],
            "aplus_content": ["基础A+"],
            "brand_ads": ["品牌推广(SB)"],
            "transparency": ["透明计划注册"]
        }
        
        key_feature_bonus = 10 if any(kf in completed for kf in key_features.get(dim_id, [])) else 0
        score = min(100, base_score + key_feature_bonus)
        
        # 计算影响分
        impact = {
            "brand_registry": 1.5,   # 基础必备
            "brand_store": 2.0,      # 高转化
            "aplus_content": 1.8,    # 高转化
            "brand_ads": 2.5,        # 流量引擎
            "transparency": 1.2       # 信任背书
        }.get(dim_id, 1.0)
        
        return BrandDimension(
            dimension=dim_name,
            score=round(score, 1),
            status=status,
            completed_features=completed,
            pending_features=pending[:3],
            impact_score=impact
        )
    
    def calculate_overall_score(self, dimensions: List[BrandDimension]) -> float:
        """计算综合评分"""
        total = 0
        for dim in dimensions:
            dim_config = next((d for d in self.DIMENSIONS if d["name"] == dim.dimension), None)
            weight = dim_config["weight"] if dim_config else 0.2
            total += dim.score * weight
        return round(total, 1)
    
    def get_brand_level(self, score: float) -> BrandLevel:
        """确定品牌等级"""
        if score >= 90:
            return BrandLevel.PREMIUM
        elif score >= 70:
            return BrandLevel.ADVANCED
        elif score >= 50:
            return BrandLevel.DEVELOPING
        elif score >= 25:
            return BrandLevel.BASIC
        else:
            return BrandLevel.NONE
    
    def score(self, features_data: Dict[str, List[str]]) -> BrandReport:
        """执行完整评分"""
        dimensions = []
        
        for dim_config in self.DIMENSIONS:
            features = features_data.get(dim_config["id"], [])
            dim = self.assess_dimension(dim_config["id"], features)
            dimensions.append(dim)
        
        overall_score = self.calculate_overall_score(dimensions)
        brand_level = self.get_brand_level(overall_score)
        
        # 生成路线图
        roadmap = self.generate_roadmap(dimensions, brand_level)
        
        # 生成预算计划
        budget_plan = self.generate_budget_plan(dimensions, brand_level)
        
        # 生成建议
        recommendations = self.generate_recommendations(dimensions, brand_level)
        
        self.current_report = BrandReport(
            overall_score=overall_score,
            brand_level=brand_level,
            dimensions=dimensions,
            roadmap=roadmap,
            budget_plan=budget_plan,
            recommendations=recommendations
        )
        
        return self.current_report
    
    def generate_roadmap(self, dimensions: List[BrandDimension], 
                        current_level: BrandLevel) -> List[Dict]:
        """生成品牌建设路线图"""
        roadmap = []
        
        # 第一阶段：基础建设（0-3月）
        roadmap.append({
            "phase": "1.基础建设期",
            "duration": "0-3个月",
            "focus": "品牌注册和基础搭建",
            "milestones": [
                "完成TM标/R标注册",
                "开通Brand Store",
                "完成基础A+内容"
            ],
            "kpis": ["品牌注册完成", "Store上线", "A+覆盖率≥50%"]
        })
        
        # 第二阶段：品牌推广（4-6月）
        roadmap.append({
            "phase": "2.品牌推广期",
            "duration": "4-6个月",
            "focus": "品牌广告和内容升级",
            "milestones": [
                "开启品牌广告投放",
                "升级Premium A+",
                "Store深度装修"
            ],
            "kpis": ["品牌广告ACOS≤30%", "A+覆盖率100%", "品牌搜索量+50%"]
        })
        
        # 第三阶段：品牌深化（7-12月）
        roadmap.append({
            "phase": "3.品牌深化期",
            "duration": "7-12个月",
            "focus": "品牌资产积累",
            "milestones": [
                "加入透明计划",
                "建立品牌社区",
                "品牌忠诚度提升"
            ],
            "kpis": ["品牌复购率≥15%", "品牌评分≥4.8", "透明计划覆盖率100%"]
        })
        
        return roadmap
    
    def generate_budget_plan(self, dimensions: List[BrandDimension],
                           level: BrandLevel) -> Dict[str, Any]:
        """生成预算计划"""
        # 基础预算
        base_budget = {
            BrandLevel.NONE: 5000,
            BrandLevel.BASIC: 30000,
            BrandLevel.DEVELOPING: 80000,
            BrandLevel.ADVANCED: 150000,
            BrandLevel.PREMIUM: 300000
        }.get(level, 80000)
        
        # 分配比例
        allocation = {
            "brand_ads": 0.50,      # 品牌广告占50%
            "content_creation": 0.25, # 内容创作25%
            "store_building": 0.15,  # Store建设15%
            "transparency": 0.10     # 透明计划10%
        }
        
        breakdown = {}
        for category, ratio in allocation.items():
            breakdown[category] = {
                "amount": round(base_budget * ratio, 2),
                "percentage": f"{ratio*100:.0f}%"
            }
        
        return {
            "total_annual_budget": base_budget,
            "monthly_budget": round(base_budget / 12, 2),
            "breakdown": breakdown,
            "roi_expectation": {
                "brand_search_increase": "+30-50%",
                "conversion_rate_increase": "+15-25%",
                "brand_premium_pricing": "+10-20%"
            }
        }
    
    def generate_recommendations(self, dimensions: List[BrandDimension],
                               level: BrandLevel) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 找出短板
        low_dims = sorted(dimensions, key=lambda x: x.score)[:2]
        
        for dim in low_dims:
            if dim.score < 70:
                if dim.completed_features:
                    recommendations.append(f"完成{dim.pending_features[0]}以提升{dim.dimension}覆盖")
                else:
                    recommendations.append(f"优先建设{dim.dimension}基础")
        
        # 等级特定建议
        if level == BrandLevel.NONE:
            recommendations.append("品牌注册是第一步，必须尽快完成")
            recommendations.append("建议3个月内完成TM标注册")
        elif level == BrandLevel.BASIC:
            recommendations.append("从Brand Store建设开始提升品牌力")
            recommendations.append("开始尝试品牌广告测试")
        elif level == BrandLevel.DEVELOPING:
            recommendations.append("加大品牌广告投入，追求规模效应")
            recommendations.append("考虑加入透明计划建立信任")
        elif level == BrandLevel.ADVANCED:
            recommendations.append("优化品牌广告效率，降低ACOS")
            recommendations.append("建立品牌内容矩阵")
        elif level == BrandLevel.PREMIUM:
            recommendations.append("保持领先，持续优化和创新")
            recommendations.append("考虑跨平台品牌扩展")
        
        return recommendations[:5]
    
    def format_report(self, report: BrandReport) -> str:
        """格式化报告"""
        output = []
        output.append("=" * 70)
        output.append("亚马逊品牌建设评分报告")
        output.append("=" * 70)
        
        output.append(f"\n【综合评分】{report.overall_score}分")
        output.append(f"【品牌等级】{report.brand_level.value}")
        
        output.append(f"\n【各维度评分】")
        for dim in report.dimensions:
            bar = "█" * int(dim.score/5) + "░" * (20 - int(dim.score/5))
            status_icon = "✅" if dim.status == "complete" else "🔄" if dim.status == "in_progress" else "❌"
            output.append(f"\n  {status_icon} {dim.dimension}: [{bar}] {dim.score}分")
            if dim.completed_features:
                output.append(f"     已完成: {', '.join(dim.completed_features[:2])}")
        
        output.append(f"\n【品牌建设路线图】")
        for phase in report.roadmap:
            output.append(f"\n  📌 {phase['phase']} ({phase['duration']})")
            output.append(f"     重点: {phase['focus']}")
        
        output.append(f"\n【预算规划】")
        bp = report.budget_plan
        output.append(f"  年度总预算: ¥{bp['total_annual_budget']:,.0f}")
        output.append(f"  月度预算: ¥{bp['monthly_budget']:,.0f}")
        
        output.append("\n" + "=" * 70)
        return "\n".join(output)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python brand-accelerator.py <command> [args]")
        print("命令:")
        print("  score     - 品牌评分")
        print("  roadmap   - 品牌路线图")
        print("  budget    - 预算建议")
        return
    
    command = sys.argv[1]
    accelerator = BrandAccelerator()
    
    # 示例数据
    sample_features = {
        "brand_registry": ["TM标注册", "R标完成", "品牌描述完善"],
        "brand_store": ["Store创建", "店铺装修"],
        "aplus_content": ["基础A+", "品牌故事模块"],
        "brand_ads": ["品牌推广(SB)"],
        "transparency": []
    }
    
    if command == "score":
        report = accelerator.score(sample_features)
        print(accelerator.format_report(report))
        
    elif command == "roadmap":
        accelerator.score(sample_features)
        roadmap = accelerator.current_report.roadmap
        
        print("=" * 70)
        print("品牌建设路线图")
        print("=" * 70)
        
        for phase in roadmap:
            print(f"\n📌 {phase['phase']} ({phase['duration']})")
            print(f"   重点: {phase['focus']}")
            print("   里程碑:")
            for m in phase["milestones"]:
                print(f"     ✓ {m}")
            print("   KPI:")
            for kpi in phase["kpis"]:
                print(f"     → {kpi}")
    
    elif command == "budget":
        accelerator.score(sample_features)
        budget = accelerator.current_report.budget_plan
        
        print("=" * 70)
        print("品牌建设预算方案")
        print("=" * 70)
        
        print(f"\n💰 年度总预算: ¥{budget['total_annual_budget']:,.0f}")
        print(f"   月度预算: ¥{budget['monthly_budget']:,.0f}")
        
        print(f"\n【预算分配】")
        for cat, info in budget["breakdown"].items():
            print(f"  {cat}: ¥{info['amount']:,.0f} ({info['percentage']})")
        
        print(f"\n【预期收益】")
        for metric, value in budget["roi_expectation"].items():
            print(f"  {metric}: {value}")
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
