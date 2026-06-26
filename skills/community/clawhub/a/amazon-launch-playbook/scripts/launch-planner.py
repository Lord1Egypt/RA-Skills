#!/usr/bin/env python3
"""
亚马逊新品上架评分器 - Level 2
Amazon New Product Launch Planner

功能：
- score: 新品上架评分（市场验证/Listing质量/广告准备/库存/评论策略 5维）
- schedule: 上架日程生成
- risk-check: 风险检查清单

Author: Amazon Launch Team
Version: 1.0.0
"""

import sys
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class LaunchScore(Enum):
    """上架评分"""
    EXCELLENT = "A级-强烈推荐上架"
    GOOD = "B级-建议上架"
    AVERAGE = "C级-谨慎上架"
    POOR = "D级-不建议上架"


@dataclass
class LaunchDimension:
    """上架维度"""
    dimension: str
    score: float
    status: str  # ready, partial, not_ready
    findings: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class LaunchReport:
    """上架报告"""
    overall_score: float
    launch_level: LaunchScore
    dimensions: List[LaunchDimension]
    schedule: List[Dict]
    risk_items: List[Dict]
    pre_launch_checklist: List[str]


class LaunchPlanner:
    """新品上架规划器"""
    
    DIMENSIONS = [
        {"id": "market_validation", "name": "市场验证", "weight": 0.25},
        {"id": "listing_quality", "name": "Listing质量", "weight": 0.25},
        {"id": "ad_preparation", "name": "广告准备", "weight": 0.20},
        {"id": "inventory", "name": "库存准备", "weight": 0.15},
        {"id": "review_strategy", "name": "评论策略", "weight": 0.15}
    ]
    
    def __init__(self):
        self.current_report: Optional[LaunchReport] = None
    
    def assess_dimension(self, dim_id: str, data: Dict) -> LaunchDimension:
        """评估单个维度"""
        dim_config = next((d for d in self.DIMENSIONS if d["id"] == dim_id), None)
        if not dim_config:
            return LaunchDimension(dimension=dim_id, score=0, status="not_ready")
        
        dim_name = dim_config["name"]
        
        if dim_id == "market_validation":
            return self._assess_market_validation(data)
        elif dim_id == "listing_quality":
            return self._assess_listing_quality(data)
        elif dim_id == "ad_preparation":
            return self._assess_ad_preparation(data)
        elif dim_id == "inventory":
            return self._assess_inventory(data)
        elif dim_id == "review_strategy":
            return self._assess_review_strategy(data)
        
        return LaunchDimension(dimension=dim_name, score=50, status="not_ready")
    
    def _assess_market_validation(self, data: Dict) -> LaunchDimension:
        """评估市场验证维度"""
        findings = []
        issues = []
        recommendations = []
        score = 50
        
        # 市场需求
        demand_score = data.get("monthly_sales", 0) / 100 * 50 if data.get("monthly_sales") else 25
        if demand_score >= 40:
            findings.append(f"市场需求强劲，月销{data.get('monthly_sales', 0)}单")
        elif demand_score >= 20:
            findings.append("市场需求一般")
        else:
            issues.append("市场需求较弱")
        
        # 竞争度
        competition = data.get("competition_level", "high")
        if competition == "low":
            score += 20
            findings.append("竞争程度低，蓝海市场")
        elif competition == "medium":
            score += 10
            findings.append("竞争程度适中")
        else:
            issues.append("市场竞争激烈")
        
        # 季节性
        if data.get("seasonal_risk"):
            issues.append("存在季节性风险")
            score -= 10
        
        # 差异化
        if data.get("differentiation"):
            score += 15
            findings.append("具有差异化卖点")
        
        score = max(0, min(100, score))
        
        if score < 50:
            recommendations.append("建议重新评估市场机会")
        elif score < 75:
            recommendations.append("需要强化差异化竞争")
        
        return LaunchDimension(
            dimension="市场验证",
            score=score,
            status="ready" if score >= 60 else "partial",
            findings=findings[:3],
            issues=issues[:2],
            recommendations=recommendations[:2]
        )
    
    def _assess_listing_quality(self, data: Dict) -> LaunchDimension:
        """评估Listing质量"""
        findings = []
        issues = []
        recommendations = []
        score = 0
        
        # 标题
        title = data.get("title", "")
        if len(title) >= 80 and len(title) <= 200:
            score += 20
            findings.append("标题长度合适")
        elif len(title) >= 50:
            score += 10
            findings.append("标题基本达标")
        else:
            issues.append("标题长度不足")
        
        # 图片
        main_image = data.get("main_image_quality", "poor")
        image_count = data.get("image_count", 0)
        if main_image == "excellent" and image_count >= 7:
            score += 25
            findings.append("主图质量优秀，图片齐全")
        elif main_image == "good" and image_count >= 5:
            score += 15
            findings.append("图片基本到位")
        else:
            issues.append("图片质量或数量不足")
        
        # 描述
        if data.get("description_complete"):
            score += 15
            findings.append("描述完整")
        else:
            issues.append("描述不完整")
        
        # A+内容
        if data.get("has_aplus"):
            score += 15
            findings.append("已有A+内容")
        elif data.get("has_aplus") is False:
            issues.append("缺少A+内容")
        
        # 要点
        bullet_count = data.get("bullet_count", 0)
        if bullet_count >= 5:
            score += 10
        elif bullet_count >= 3:
            score += 5
        else:
            issues.append("产品要点不足")
        
        score = max(0, min(100, score))
        
        if score < 60:
            recommendations.append("优先完善图片和标题")
        
        return LaunchDimension(
            dimension="Listing质量",
            score=score,
            status="ready" if score >= 70 else "partial" if score >= 50 else "not_ready",
            findings=findings[:3],
            issues=issues[:2],
            recommendations=recommendations[:2]
        )
    
    def _assess_ad_preparation(self, data: Dict) -> LaunchDimension:
        """评估广告准备"""
        findings = []
        issues = []
        recommendations = []
        score = 0
        
        # 关键词
        keyword_count = data.get("keyword_count", 0)
        if keyword_count >= 30:
            score += 30
            findings.append(f"已准备{keyword_count}个关键词")
        elif keyword_count >= 10:
            score += 15
            findings.append("关键词基本覆盖")
        else:
            issues.append("关键词准备不足")
        
        # 广告结构
        if data.get("campaign_structure"):
            score += 25
            findings.append("广告结构设计完成")
        else:
            issues.append("广告结构未规划")
        
        # 预算
        daily_budget = data.get("daily_budget", 0)
        min_budget = 50  # 最低日预算
        if daily_budget >= min_budget:
            score += 20
            findings.append(f"日预算${daily_budget}已设置")
        elif daily_budget >= min_budget * 0.5:
            score += 10
            recommendations.append("预算偏低，建议增加")
        else:
            issues.append("预算设置不足")
        
        # 竞价策略
        if data.get("bidding_strategy"):
            score += 15
            findings.append("竞价策略已制定")
        
        score = max(0, min(100, score))
        
        if score < 60:
            recommendations.append("至少准备10个核心关键词")
        
        return LaunchDimension(
            dimension="广告准备",
            score=score,
            status="ready" if score >= 70 else "partial" if score >= 40 else "not_ready",
            findings=findings[:3],
            issues=issues[:2],
            recommendations=recommendations[:2]
        )
    
    def _assess_inventory(self, data: Dict) -> LaunchDimension:
        """评估库存准备"""
        findings = []
        issues = []
        recommendations = []
        score = 0
        
        # 库存数量
        stock = data.get("fba_stock", 0)
        target_stock = data.get("target_monthly_sales", 300)
        
        if stock >= target_stock * 2:
            score += 35
            findings.append(f"库存充足({stock}件)")
        elif stock >= target_stock:
            score += 25
            findings.append("库存基本够用")
        else:
            issues.append(f"库存不足，目标需{target_stock}件")
            score += 10
        
        # 入仓时间
        if data.get("warehouse_ready"):
            score += 30
            findings.append("仓库已就绪")
        else:
            issues.append("仓库尚未就绪")
        
        # 补货计划
        if data.get("replenishment_plan"):
            score += 20
            findings.append("有补货计划")
        elif stock < target_stock:
            recommendations.append("建议制定补货计划")
        
        # 安全库存
        if data.get("safety_stock_days", 0) >= 14:
            score += 15
            findings.append("安全库存设置合理")
        
        score = max(0, min(100, score))
        
        return LaunchDimension(
            dimension="库存准备",
            score=score,
            status="ready" if score >= 70 else "partial",
            findings=findings[:3],
            issues=issues[:2],
            recommendations=recommendations[:2]
        )
    
    def _assess_review_strategy(self, data: Dict) -> LaunchDimension:
        """评估评论策略"""
        findings = []
        issues = []
        recommendations = []
        score = 0
        
        # Vine计划
        if data.get("vine_enrolled"):
            score += 30
            findings.append("已注册Vine计划")
        else:
            recommendations.append("建议注册Vine计划获取早期评价")
        
        # 评价请求
        if data.get("review_request_enabled"):
            score += 25
            findings.append("自动评价请求已开启")
        else:
            issues.append("未开启评价请求")
        
        # 产品包装
        if data.get("packaging_includes_request"):
            score += 20
            findings.append("包装含评价请求卡")
        else:
            recommendations.append("考虑在包装中添加评价请求")
        
        # 评论目标
        target_reviews = data.get("target_reviews", 0)
        if target_reviews >= 30:
            score += 15
            findings.append(f"目标获取{target_reviews}条评价")
        elif target_reviews >= 10:
            score += 10
        else:
            recommendations.append("设定明确的评价数量目标")
        
        # 合规性
        if data.get("compliant_review_methods"):
            score += 10
            findings.append("使用合规的评论获取方式")
        else:
            issues.append("存在不合规风险")
        
        score = max(0, min(100, score))
        
        return LaunchDimension(
            dimension="评论策略",
            score=score,
            status="ready" if score >= 70 else "partial",
            findings=findings[:3],
            issues=issues[:2],
            recommendations=recommendations[:2]
        )
    
    def calculate_overall_score(self, dimensions: List[LaunchDimension]) -> float:
        """计算综合评分"""
        total = 0
        for dim in dimensions:
            dim_config = next((d for d in self.DIMENSIONS if d["name"] == dim.dimension), None)
            weight = dim_config["weight"] if dim_config else 0.2
            total += dim.score * weight
        return round(total, 1)
    
    def get_launch_level(self, score: float) -> LaunchScore:
        """确定上架等级"""
        if score >= 85:
            return LaunchScore.EXCELLENT
        elif score >= 70:
            return LaunchScore.GOOD
        elif score >= 50:
            return LaunchScore.AVERAGE
        else:
            return LaunchScore.POOR
    
    def score(self, product_data: Dict) -> LaunchReport:
        """执行完整评分"""
        dimensions = []
        
        for dim_config in self.DIMENSIONS:
            data = product_data.get(dim_config["id"], {})
            dim = self.assess_dimension(dim_config["id"], data)
            dimensions.append(dim)
        
        overall_score = self.calculate_overall_score(dimensions)
        launch_level = self.get_launch_level(overall_score)
        
        # 生成日程
        schedule = self.generate_schedule(dimensions)
        
        # 风险检查
        risk_items = self.check_risks(dimensions)
        
        # 上架前检查清单
        checklist = self.generate_prelaunch_checklist(dimensions)
        
        self.current_report = LaunchReport(
            overall_score=overall_score,
            launch_level=launch_level,
            dimensions=dimensions,
            schedule=schedule,
            risk_items=risk_items,
            pre_launch_checklist=checklist
        )
        
        return self.current_report
    
    def generate_schedule(self, dimensions: List[LaunchDimension]) -> List[Dict]:
        """生成上架日程"""
        schedule = []
        
        # D-30: 提前30天
        schedule.append({
            "day": "D-30",
            "task": "市场验证完成",
            "status": "done" if next((d for d in dimensions if d.dimension == "市场验证"), None).score >= 60 else "pending"
        })
        
        # D-21: 三周前
        schedule.append({
            "day": "D-21",
            "task": "Listing初稿完成",
            "status": "pending"
        })
        
        # D-14: 两周前
        schedule.append({
            "day": "D-14",
            "task": "图片和A+内容完成",
            "status": "pending"
        })
        
        # D-7: 一周前
        schedule.append({
            "day": "D-7",
            "task": "广告计划和关键词准备",
            "status": "pending"
        })
        
        # D-3: 三天前
        schedule.append({
            "day": "D-3",
            "task": "FBA库存入仓",
            "status": "pending"
        })
        
        # D-1: 前一天
        schedule.append({
            "day": "D-1",
            "task": "最终Listing检查",
            "status": "pending"
        })
        
        # D-Day: 上架日
        schedule.append({
            "day": "D-Day",
            "task": "正式上架+广告启动",
            "status": "pending"
        })
        
        # D+7: 一周后
        schedule.append({
            "day": "D+7",
            "task": "数据分析与调整",
            "status": "pending"
        })
        
        # D+30: 一个月后
        schedule.append({
            "day": "D+30",
            "task": "首月复盘",
            "status": "pending"
        })
        
        return schedule
    
    def check_risks(self, dimensions: List[LaunchDimension]) -> List[Dict]:
        """风险检查"""
        risks = []
        
        for dim in dimensions:
            if dim.issues:
                for issue in dim.issues:
                    risks.append({
                        "dimension": dim.dimension,
                        "issue": issue,
                        "severity": "high" if dim.score < 50 else "medium"
                    })
        
        # 特定风险
        market_dim = next((d for d in dimensions if d.dimension == "市场验证"), None)
        if market_dim and market_dim.score < 40:
            risks.append({
                "dimension": "市场验证",
                "issue": "市场需求不足，上架风险极高",
                "severity": "critical"
            })
        
        return risks
    
    def generate_prelaunch_checklist(self, dimensions: List[LaunchDimension]) -> List[str]:
        """生成上架前检查清单"""
        checklist = []
        
        checklist.append("✅ 标题包含核心关键词且符合规范")
        checklist.append("✅ 主图符合亚马逊要求（白底、无水印）")
        checklist.append("✅ 至少5张高质量图片")
        checklist.append("✅ 5个产品要点清晰展示卖点")
        checklist.append("✅ 详细描述完整且专业")
        checklist.append("✅ 关键词研究完成（≥20个）")
        checklist.append("✅ 广告结构设计完成")
        checklist.append("✅ 日预算设置≥$50")
        checklist.append("✅ FBA库存已入仓")
        checklist.append("✅ Vine计划已注册（如适用）")
        checklist.append("✅ 评价请求功能已开启")
        checklist.append("✅ 同行关注已设置")
        
        return checklist
    
    def format_report(self, report: LaunchReport) -> str:
        """格式化报告"""
        output = []
        output.append("=" * 70)
        output.append("亚马逊新品上架评分报告")
        output.append("=" * 70)
        
        output.append(f"\n【综合评分】{report.overall_score}分 ({report.launch_level.value})")
        
        output.append(f"\n【各维度评分】")
        for dim in report.dimensions:
            bar = "█" * int(dim.score/5) + "░" * (20 - int(dim.score/5))
            output.append(f"\n  {dim.dimension}: [{bar}] {dim.score}分")
            if dim.findings:
                output.append(f"     ✓ {dim.findings[0]}")
            if dim.issues:
                output.append(f"     ⚠ {dim.issues[0]}")
        
        if report.risk_items:
            output.append(f"\n【风险提示】")
            for risk in report.risk_items[:3]:
                output.append(f"  ⚠ [{risk['severity'].upper()}] {risk['dimension']}: {risk['issue']}")
        
        output.append(f"\n【上架日程】")
        for s in report.schedule[:5]:
            icon = "✅" if s["status"] == "done" else "☐"
            output.append(f"  {icon} {s['day']}: {s['task']}")
        
        output.append("\n" + "=" * 70)
        return "\n".join(output)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python launch-planner.py <command> [args]")
        print("命令:")
        print("  score        - 上架评分")
        print("  schedule     - 上架日程")
        print("  risk-check   - 风险检查")
        return
    
    command = sys.argv[1]
    planner = LaunchPlanner()
    
    # 示例数据
    sample_data = {
        "market_validation": {
            "monthly_sales": 200,
            "competition_level": "medium",
            "seasonal_risk": False,
            "differentiation": True
        },
        "listing_quality": {
            "title": "Wireless Bluetooth Earbuds, Active Noise Cancelling, 40H Battery Life with Charging Case",
            "main_image_quality": "excellent",
            "image_count": 7,
            "description_complete": True,
            "has_aplus": True,
            "bullet_count": 5
        },
        "ad_preparation": {
            "keyword_count": 25,
            "campaign_structure": True,
            "daily_budget": 80,
            "bidding_strategy": "dynamic-bids-down"
        },
        "inventory": {
            "fba_stock": 500,
            "target_monthly_sales": 300,
            "warehouse_ready": True,
            "replenishment_plan": True,
            "safety_stock_days": 21
        },
        "review_strategy": {
            "vine_enrolled": True,
            "review_request_enabled": True,
            "packaging_includes_request": True,
            "target_reviews": 30,
            "compliant_review_methods": True
        }
    }
    
    if command == "score":
        report = planner.score(sample_data)
        print(planner.format_report(report))
        
    elif command == "schedule":
        planner.score(sample_data)
        schedule = planner.current_report.schedule
        
        print("=" * 70)
        print("新品上架日程")
        print("=" * 70)
        
        for s in schedule:
            icon = "✅" if s["status"] == "done" else "☐"
            print(f"\n{icon} {s['day']}")
            print(f"   任务: {s['task']}")
        
    elif command == "risk-check":
        planner.score(sample_data)
        risks = planner.current_report.risk_items
        
        print("=" * 70)
        print("风险检查报告")
        print("=" * 70)
        
        if not risks:
            print("\n✅ 未发现重大风险")
        else:
            for risk in risks:
                severity_icon = "🔴" if risk["severity"] == "critical" else "🟠" if risk["severity"] == "high" else "🟡"
                print(f"\n{severity_icon} [{risk['severity'].upper()}] {risk['dimension']}")
                print(f"   问题: {risk['issue']}")
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
