#!/usr/bin/env python3
"""
GEO运营多国风险分析器 - Level 2
GEO AgentOps Multi-Country Risk Analyzer

功能：
- risk-assess: 多国运营风险评估（法规/文化/支付/物流/语言5维）
- prioritize: 市场优先级排序
- localization-gap: 本地化差距分析

Author: GEO AgentOps Team
Version: 1.0.0
"""

import sys
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class MarketRegion(Enum):
    """市场区域"""
    NORTH_AMERICA = "北美"
    EUROPE = "欧洲"
    SOUTHEAST_ASIA = "东南亚"
    MIDDLE_EAST = "中东"
    LATIN_AMERICA = "拉美"
    EAST_ASIA = "东亚"


@dataclass
class RiskDimension:
    """风险维度"""
    name: str
    score: float  # 0-100，风险分数越高风险越大
    level: str
    details: List[str] = field(default_factory=list)
    mitigations: List[str] = field(default_factory=list)


@dataclass
class MarketAnalysis:
    """市场分析结果"""
    country: str
    region: str
    overall_risk: float
    risk_level: str
    dimensions: List[RiskDimension]
    opportunities: List[str]
    challenges: List[str]
    recommendations: List[str]


@dataclass
class LocalizationGap:
    """本地化差距"""
    aspect: str
    current_status: str
    target_status: str
    gap_level: str  # high, medium, low
    effort_required: str  # 高/中/低
    priority: int


class GeoOpsAnalyzer:
    """GEO运营分析器"""
    
    # 市场风险数据库（简化版）
    MARKET_RISK_DATA = {
        "美国": {
            "region": MarketRegion.NORTH_AMERICA,
            "regulatory": {"score": 45, "details": [" FTC合规", "CCPA隐私", "FDA认证（如适用）"]},
            "cultural": {"score": 25, "details": ["直接沟通风格", "重视隐私", "品牌忠诚度"]},
            "payment": {"score": 20, "details": ["信用卡普及", "PayPal流行", "BNPL兴起"]},
            "logistics": {"score": 30, "details": ["FBA体系成熟", "最后一公里发达", "退货率高"]},
            "language": {"score": 15, "details": ["英语为主", "西语需求增长"]}
        },
        "德国": {
            "region": MarketRegion.EUROPE,
            "regulatory": {"score": 65, "details": ["GDPR严格", "产品安全法", "包装法合规"]},
            "cultural": {"score": 35, "details": ["重视品质", "理性消费", "环保意识强"]},
            "payment": {"score": 40, "details": ["Klarna流行", "SEPA转账", "信用卡渗透一般"]},
            "logistics": {"score": 35, "details": ["DHL/FedEx发达", "CD不普及", "周日不派送"]},
            "language": {"score": 55, "details": ["德语必需", "英语接受度一般"]}
        },
        "英国": {
            "region": MarketRegion.EUROPE,
            "regulatory": {"score": 50, "details": ["UK GDPR", "消费者权益法", "VAT合规"]},
            "cultural": {"score": 20, "details": ["间接沟通", "礼貌用语", "幽默感重要"]},
            "payment": {"score": 25, "details": ["信用卡成熟", "Apple Pay普及", "Open Banking"]},
            "logistics": {"score": 25, "details": ["Royal Mail覆盖广", "次日达普遍"]},
            "language": {"score": 10, "details": ["英语为主要语言"]}
        },
        "日本": {
            "region": MarketRegion.EAST_ASIA,
            "regulatory": {"score": 55, "details": ["PSE认证", "JIS标准", "消费税合规"]},
            "cultural": {"score": 70, "details": ["高期望服务", "礼节复杂", "品牌忠诚度高", "季节感重要"]},
            "payment": {"score": 35, "details": ["现金仍流行", "便利店支付", "信用卡增长"]},
            "logistics": {"score": 40, "details": ["黑猫/佐川发达", "礼节要求高", "包装精美"]},
            "language": {"score": 85, "details": ["日语必需", "敬语复杂", "文化差异大"]}
        },
        "东南亚": {
            "region": MarketRegion.SOUTHEAST_ASIA,
            "regulatory": {"score": 60, "details": ["各国法规差异大", "泰国/越南/印尼各有要求"]},
            "cultural": {"score": 55, "details": ["多元文化", "社交电商重要", "价格敏感"]},
            "payment": {"score": 50, "details": ["电子支付增长", "银行渗透不均", "COD普遍"]},
            "logistics": {"score": 55, "details": ["基础设施不均", "岛屿配送挑战", "新兴物流"]},
            "language": {"score": 65, "details": ["多语言需求", "英语水平不一"]}
        },
        "中东": {
            "region": MarketRegion.MIDDLE_EAST,
            "regulatory": {"score": 70, "details": ["SASO认证", "Halal认证", "文化合规"]},
            "cultural": {"score": 60, "details": ["宗教节日重要", "性别区分服务", "VIP文化"]},
            "payment": {"score": 55, "details": ["CashU", "本地电子支付", "分期付款流行"]},
            "logistics": {"score": 65, "details": ["区域限制", "清关复杂", "最后一公里挑战"]},
            "language": {"score": 70, "details": ["阿拉伯语必需", "英语商业可用"]}
        }
    }
    
    def __init__(self):
        self.current_analysis: Optional[MarketAnalysis] = None
    
    def assess_risk(self, country: str, custom_data: Dict[str, Any] = None) -> MarketAnalysis:
        """
        评估市场风险
        
        Args:
            country: 国家/地区名称
            custom_data: 自定义数据（可选）
        
        Returns:
            市场分析结果
        """
        if country not in self.MARKET_RISK_DATA:
            # 生成默认分析
            return self._generate_default_analysis(country)
        
        market_data = self.MARKET_RISK_DATA[country]
        dimensions = []
        
        # 评估各维度风险
        dim_names = ["regulatory", "cultural", "payment", "logistics", "language"]
        dim_cn = {"regulatory": "法规合规", "cultural": "文化适配", 
                  "payment": "支付体系", "logistics": "物流配送", "language": "语言本地化"}
        
        for dim in dim_names:
            data = market_data.get(dim, {"score": 50, "details": []})
            score = data["score"]
            
            # 应用自定义调整
            if custom_data and dim in custom_data:
                score = (score + custom_data[dim]) / 2
            
            # 确定风险等级
            if score < 30:
                level = "低风险"
            elif score < 50:
                level = "中低风险"
            elif score < 65:
                level = "中等风险"
            elif score < 80:
                level = "中高风险"
            else:
                level = "高风险"
            
            # 生成缓解措施
            mitigations = self._generate_mitigations(dim, score)
            
            dimensions.append(RiskDimension(
                name=dim_cn[dim],
                score=score,
                level=level,
                details=data.get("details", []),
                mitigations=mitigations
            ))
        
        # 计算综合风险
        weights = {"regulatory": 0.30, "cultural": 0.20, "payment": 0.20, 
                   "logistics": 0.15, "language": 0.15}
        
        overall_risk = sum(
            market_data.get(dim, {"score": 50})["score"] * weights.get(dim, 0.2)
            for dim in dim_names
        )
        
        if overall_risk < 30:
            risk_level = "低风险"
        elif overall_risk < 50:
            risk_level = "中低风险"
        elif overall_risk < 65:
            risk_level = "中等风险"
        elif overall_risk < 80:
            risk_level = "中高风险"
        else:
            risk_level = "高风险"
        
        # 机会与挑战分析
        opportunities = self._generate_opportunities(country, dimensions)
        challenges = self._generate_challenges(country, dimensions)
        recommendations = self._generate_recommendations(country, dimensions)
        
        self.current_analysis = MarketAnalysis(
            country=country,
            region=market_data["region"].value,
            overall_risk=round(overall_risk, 1),
            risk_level=risk_level,
            dimensions=dimensions,
            opportunities=opportunities,
            challenges=challenges,
            recommendations=recommendations
        )
        
        return self.current_analysis
    
    def _generate_default_analysis(self, country: str) -> MarketAnalysis:
        """生成默认分析（未知市场）"""
        dimensions = [
            RiskDimension("法规合规", 50, "中等风险", ["需要深入调研当地法规"]),
            RiskDimension("文化适配", 50, "中等风险", ["建议进行文化调研"]),
            RiskDimension("支付体系", 50, "中等风险", ["需了解当地支付习惯"]),
            RiskDimension("物流配送", 50, "中等风险", ["物流基础设施待确认"]),
            RiskDimension("语言本地化", 50, "中等风险", ["语言需求待评估"])
        ]
        
        return MarketAnalysis(
            country=country,
            region="未知",
            overall_risk=50,
            risk_level="中等风险",
            dimensions=dimensions,
            opportunities=["市场潜力待挖掘"],
            challenges=["信息不足，需进一步调研"],
            recommendations=["建议进行全面的市场调研"]
        )
    
    def _generate_mitigations(self, dimension: str, score: float) -> List[str]:
        """生成风险缓解措施"""
        mitigations = {
            "regulatory": {
                "high": ["聘请当地法律顾问", "建立合规检查清单", "定期法规更新"],
                "medium": ["关注法规动态", "建立合规流程"],
                "low": ["持续关注即可"]
            },
            "cultural": {
                "high": ["聘请本地文化顾问", "进行用户调研", "建立文化适应指南"],
                "medium": ["培训团队文化意识", "参考同行经验"],
                "low": ["保持基本礼仪即可"]
            },
            "payment": {
                "high": ["接入主流支付方式", "考虑COD服务", "建立支付失败处理机制"],
                "medium": ["接入本地支付", "提供多种选择"],
                "low": ["保持主流支付接入"]
            },
            "logistics": {
                "high": ["选择可靠物流伙伴", "建立海外仓", "优化包装设计"],
                "medium": ["选择有保障的物流", "设置合理预期"],
                "low": ["标准物流方案即可"]
            },
            "language": {
                "high": ["专业本地化团队", "母语级翻译", "文化适配审核"],
                "medium": ["专业翻译服务", "本地化审核"],
                "low": ["基础翻译服务即可"]
            }
        }
        
        level = "high" if score >= 65 else "medium" if score >= 40 else "low"
        return mitigations.get(dimension, {}).get(level, [])
    
    def _generate_opportunities(self, country: str, dimensions: List[RiskDimension]) -> List[str]:
        """生成市场机会"""
        opportunities = []
        
        # 基于文化维度
        cultural_dim = next((d for d in dimensions if d.name == "文化适配"), None)
        if cultural_dim and cultural_dim.score < 40:
            opportunities.append("文化适配门槛适中，市场接受度高")
        
        # 基于支付维度
        payment_dim = next((d for d in dimensions if d.name == "支付体系"), None)
        if payment_dim and payment_dim.score < 40:
            opportunities.append("支付体系成熟，用户购买转化率高")
        
        # 基于语言维度
        language_dim = next((d for d in dimensions if d.name == "语言本地化"), None)
        if language_dim and language_dim.score < 40:
            opportunities.append("语言障碍小，内容运营成本低")
        
        # 默认机会
        if not opportunities:
            opportunities = [
                "电商市场持续增长",
                "数字化转型加速",
                "中产阶级消费升级"
            ]
        
        return opportunities[:3]
    
    def _generate_challenges(self, country: str, dimensions: List[RiskDimension]) -> List[str]:
        """生成市场挑战"""
        challenges = []
        
        for dim in dimensions:
            if dim.score >= 65:
                if dim.name == "法规合规":
                    challenges.append("法规要求严格，合规成本较高")
                elif dim.name == "文化适配":
                    challenges.append("文化差异大，本地化难度高")
                elif dim.name == "支付体系":
                    challenges.append("支付方式分散，收单成本高")
                elif dim.name == "物流配送":
                    challenges.append("物流基础设施有待完善")
                elif dim.name == "语言本地化":
                    challenges.append("语言本地化要求高，需专业团队支持")
        
        if not challenges:
            challenges.append("市场竞争激烈，需差异化策略")
        
        return challenges[:3]
    
    def _generate_recommendations(self, country: str, dimensions: List[RiskDimension]) -> List[str]:
        """生成建议"""
        recommendations = []
        
        high_risk_dims = [d for d in dimensions if d.score >= 65]
        
        if len(high_risk_dims) >= 3:
            recommendations.append("建议分阶段进入，先小规模试水")
            recommendations.append("重点投入资源解决高风险维度")
        elif len(high_risk_dims) >= 1:
            recommendations.append("针对性解决高风险维度问题")
            recommendations.append("可考虑与本地伙伴合作")
        else:
            recommendations.append("风险可控，建议积极布局")
            recommendations.append("建立本地化运营团队")
        
        return recommendations
    
    def prioritize_markets(self, countries: List[str], 
                           criteria: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """
        市场优先级排序
        
        Args:
            countries: 国家列表
            criteria: 评判标准权重
        
        Returns:
            优先级排序结果
        """
        if criteria is None:
            criteria = {
                "market_size": 0.25,
                "growth_rate": 0.20,
                "competition": 0.15,
                "risk_level": 0.20,
                "strategic_fit": 0.20
            }
        
        results = []
        
        for country in countries:
            # 获取风险评估
            analysis = self.assess_risk(country)
            
            # 计算综合得分
            # 风险分数转换为机会分数（100 - risk）
            risk_opportunity = 100 - analysis.overall_risk
            
            # 市场优先级得分（简化计算）
            priority_score = (
                criteria.get("risk_level", 0.2) * risk_opportunity +
                criteria.get("market_size", 0.25) * 70 +  # 假设
                criteria.get("growth_rate", 0.2) * 65 +    # 假设
                criteria.get("competition", 0.15) * 50 +   # 假设
                criteria.get("strategic_fit", 0.2) * 60   # 假设
            )
            
            results.append({
                "country": country,
                "region": analysis.region,
                "risk_score": analysis.overall_risk,
                "risk_level": analysis.risk_level,
                "priority_score": round(priority_score, 1),
                "priority_tier": self._get_priority_tier(priority_score),
                "recommendation": self._get_market_recommendation(analysis, priority_score)
            })
        
        # 按优先级排序
        results.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return results
    
    def _get_priority_tier(self, score: float) -> str:
        """获取优先级层级"""
        if score >= 80:
            return "S级-优先进入"
        elif score >= 65:
            return "A级-重点关注"
        elif score >= 50:
            return "B级-次优选择"
        else:
            return "C级-暂缓进入"
    
    def _get_market_recommendation(self, analysis: MarketAnalysis, score: float) -> str:
        """获取市场建议"""
        if score >= 80:
            return f"建议优先进入{analysis.country}市场，风险可控且机会显著"
        elif score >= 65:
            return f"建议积极布局{analysis.country}，可作为第二梯队市场"
        elif score >= 50:
            return f"{analysis.country}可作为长期规划，建议进一步调研"
        else:
            return f"{analysis.country}建议暂缓进入，需等待条件成熟"
    
    def analyze_localization_gap(self, country: str, 
                                 current_content: Dict[str, str] = None) -> List[LocalizationGap]:
        """
        本地化差距分析
        
        Args:
            country: 国家/地区
            current_content: 当前内容状态
        
        Returns:
            本地化差距列表
        """
        analysis = self.assess_risk(country)
        
        gaps = []
        
        # 语言差距
        language_dim = next((d for d in analysis.dimensions if d.name == "语言本地化"), None)
        if language_dim:
            current = current_content.get("language", "仅有英文") if current_content else "仅有英文"
            gaps.append(LocalizationGap(
                aspect="语言本地化",
                current_status=current,
                target_status="完整本地化（母语级）",
                gap_level="high" if language_dim.score >= 65 else "medium" if language_dim.score >= 40 else "low",
                effort_required="高" if language_dim.score >= 65 else "中" if language_dim.score >= 40 else "低",
                priority=1
            ))
        
        # 支付方式差距
        payment_dim = next((d for d in analysis.dimensions if d.name == "支付体系"), None)
        if payment_dim:
            current = current_content.get("payment", "仅信用卡") if current_content else "仅信用卡"
            gaps.append(LocalizationGap(
                aspect="支付方式适配",
                current_status=current,
                target_status="支持主流本地支付",
                gap_level="high" if payment_dim.score >= 60 else "medium" if payment_dim.score >= 40 else "low",
                effort_required="中",
                priority=2
            ))
        
        # 文化适配差距
        cultural_dim = next((d for d in analysis.dimensions if d.name == "文化适配"), None)
        if cultural_dim:
            current = current_content.get("cultural", "通用内容") if current_content else "通用内容"
            gaps.append(LocalizationGap(
                aspect="文化内容适配",
                current_status=current,
                target_status="深度本地化内容",
                gap_level="high" if cultural_dim.score >= 60 else "medium" if cultural_dim.score >= 40 else "low",
                effort_required="高",
                priority=3
            ))
        
        # 物流适配差距
        logistics_dim = next((d for d in analysis.dimensions if d.name == "物流配送"), None)
        if logistics_dim:
            current = current_content.get("logistics", "标准配送") if current_content else "标准配送"
            gaps.append(LocalizationGap(
                aspect="物流配送方案",
                current_status=current,
                target_status="本地化配送方案",
                gap_level="high" if logistics_dim.score >= 60 else "medium" if logistics_dim.score >= 40 else "low",
                effort_required="中",
                priority=4
            ))
        
        # 法规合规差距
        regulatory_dim = next((d for d in analysis.dimensions if d.name == "法规合规"), None)
        if regulatory_dim:
            current = current_content.get("regulatory", "基础合规") if current_content else "基础合规"
            gaps.append(LocalizationGap(
                aspect="法规合规适配",
                current_status=current,
                target_status="完全本地合规",
                gap_level="high" if regulatory_dim.score >= 65 else "medium" if regulatory_dim.score >= 45 else "low",
                effort_required="高",
                priority=5
            ))
        
        # 按优先级排序
        gaps.sort(key=lambda x: x.priority)
        
        return gaps
    
    def format_risk_report(self, analysis: MarketAnalysis) -> str:
        """格式化风险报告"""
        output = []
        output.append("=" * 60)
        output.append(f"GEO运营风险评估报告 - {analysis.country}")
        output.append("=" * 60)
        output.append(f"\n【综合风险】{analysis.overall_risk}分 ({analysis.risk_level})")
        output.append(f"【区域分类】{analysis.region}")
        
        output.append(f"\n【各维度风险】")
        for dim in analysis.dimensions:
            bar = "█" * int(dim.score / 5) + "░" * (20 - int(dim.score / 5))
            output.append(f"\n  {dim.name}: [{bar}] {dim.score}分")
            if dim.details:
                output.append(f"    详情: {', '.join(dim.details[:2])}")
        
        output.append(f"\n【市场机会】")
        for opp in analysis.opportunities:
            output.append(f"  • {opp}")
        
        output.append(f"\n【主要挑战】")
        for challenge in analysis.challenges:
            output.append(f"  • {challenge}")
        
        output.append(f"\n【运营建议】")
        for rec in analysis.recommendations:
            output.append(f"  → {rec}")
        
        output.append("\n" + "=" * 60)
        return "\n".join(output)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python geo-ops-analyzer.py <command> [args]")
        print("命令:")
        print("  risk-assess        - 风险评估")
        print("  prioritize         - 市场优先级排序")
        print("  localization-gap   - 本地化差距分析")
        return
    
    command = sys.argv[1]
    analyzer = GeoOpsAnalyzer()
    
    if command == "risk-assess":
        country = sys.argv[2] if len(sys.argv) > 2 else "日本"
        analysis = analyzer.assess_risk(country)
        print(analyzer.format_risk_report(analysis))
        
    elif command == "prioritize":
        countries = sys.argv[2:] if len(sys.argv) > 2 else ["美国", "德国", "日本", "东南亚"]
        results = analyzer.prioritize_markets(countries)
        
        print("=" * 60)
        print("市场优先级排序")
        print("=" * 60)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['country']} ({result['region']})")
            print(f"   优先级: {result['priority_tier']}")
            print(f"   综合得分: {result['priority_score']}分")
            print(f"   风险等级: {result['risk_level']} ({result['risk_score']}分)")
            print(f"   建议: {result['recommendation']}")
        
    elif command == "localization-gap":
        country = sys.argv[2] if len(sys.argv) > 2 else "日本"
        gaps = analyzer.analyze_localization_gap(country)
        
        print("=" * 60)
        print(f"本地化差距分析 - {country}")
        print("=" * 60)
        
        for gap in gaps:
            priority_icon = "🔴" if gap.gap_level == "high" else "🟡" if gap.gap_level == "medium" else "🟢"
            print(f"\n{priority_icon} {gap.aspect} (优先级: {gap.priority})")
            print(f"   当前状态: {gap.current_status}")
            print(f"   目标状态: {gap.target_status}")
            print(f"   差距等级: {gap.gap_level.upper()}")
            print(f"   投入要求: {gap.effort_required}")
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
