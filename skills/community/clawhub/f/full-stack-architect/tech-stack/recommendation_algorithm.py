#!/usr/bin/env python3
"""
技术栈推荐算法
提供智能的技术栈推荐功能
"""

import os
import json
import logging
from datetime import datetime
from .trends_analyzer import TrendsAnalyzer

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TechStackRecommender:
    def __init__(self):
        self.trends_analyzer = TrendsAnalyzer()
        self.industry_preferences = {
            "ecommerce": {
                "frontend": ["React", "Next.js", "Vue"],
                "backend": ["Node.js", "Go", "Python"],
                "database": ["PostgreSQL", "MongoDB", "Redis"],
                "devops": ["Docker", "Kubernetes", "GitHub Actions"]
            },
            "healthcare": {
                "frontend": ["React", "Vue", "Angular"],
                "backend": ["Python", "Java", "Go"],
                "database": ["PostgreSQL", "MongoDB", "Redis"],
                "devops": ["Docker", "Kubernetes", "Terraform"]
            },
            "education": {
                "frontend": ["React", "Vue", "Next.js"],
                "backend": ["Python", "Node.js", "Go"],
                "database": ["PostgreSQL", "MongoDB", "Redis"],
                "devops": ["Docker", "GitHub Actions", "Vercel"]
            },
            "gaming": {
                "frontend": ["React", "Vue", "TypeScript"],
                "backend": ["Go", "Node.js", "Rust"],
                "database": ["PostgreSQL", "MongoDB", "Redis"],
                "devops": ["Docker", "Kubernetes", "GitHub Actions"]
            },
            "finance": {
                "frontend": ["React", "Vue", "Angular"],
                "backend": ["Java", "Go", "Python"],
                "database": ["PostgreSQL", "MySQL", "Redis"],
                "devops": ["Docker", "Kubernetes", "GitLab"]
            },
            "general": {
                "frontend": ["React", "Vue", "Next.js"],
                "backend": ["Python", "Go", "Node.js"],
                "database": ["PostgreSQL", "MongoDB", "Redis"],
                "devops": ["Docker", "GitHub Actions", "Kubernetes"]
            }
        }

    def recommend(self, requirements):
        """根据需求推荐技术栈"""
        project_type = requirements.get("type", "general")
        industry = requirements.get("industry", "general")
        team_size = requirements.get("team_size", "small")
        performance_requirements = requirements.get("performance", "medium")
        budget = requirements.get("budget", "medium")
        
        recommendations = {
            "metadata": {
                "project_type": project_type,
                "industry": industry,
                "team_size": team_size,
                "performance": performance_requirements,
                "budget": budget,
                "timestamp": datetime.now().isoformat()
            },
            "recommendations": {},
            "rationale": []
        }
        
        industry_prefs = self.industry_preferences.get(industry, self.industry_preferences["general"])
        
        for category, techs in industry_prefs.items():
            category_recommendations = []
            
            for tech_name in techs:
                analysis = self.trends_analyzer.analyze_tech(tech_name, category)
                if analysis.get("success"):
                    category_recommendations.append(analysis)
            
            category_recommendations.sort(key=lambda x: x["scores"]["trending"], reverse=True)
            recommendations["recommendations"][category] = category_recommendations[:3]
        
        recommendations["rationale"].append(f"根据 {industry} 行业的最佳实践推荐")
        if team_size == "enterprise":
            recommendations["rationale"].append("考虑企业级需求，选择更成熟稳定的技术")
        else:
            recommendations["rationale"].append("适合小型团队快速开发，选择更灵活的技术")
        
        if performance_requirements == "high":
            recommendations["rationale"].append("考虑高性能需求，优先推荐Go、Rust等高性能技术")
        
        return recommendations

    def generate_comparison(self, options):
        """生成技术比较"""
        comparison = {
            "options": options,
            "comparison": {},
            "recommendation": None
        }
        
        for tech_name, category in options.items():
            analysis = self.trends_analyzer.analyze_tech(tech_name, category)
            if analysis.get("success"):
                comparison["comparison"][tech_name] = analysis
        
        if comparison["comparison"]:
            best_tech = max(
                comparison["comparison"].items(),
                key=lambda x: x[1]["scores"]["trending"]
            )
            comparison["recommendation"] = best_tech[0]
        
        return comparison

    def get_migration_guide(self, current_stack, target_stack):
        """获取迁移指南"""
        return {
            "current_stack": current_stack,
            "target_stack": target_stack,
            "steps": [
                "评估当前技术栈和需求",
                "制定迁移计划和时间表",
                "逐步替换组件而非一次性迁移",
                "保持向后兼容和回滚方案",
                "充分测试和监控",
                "团队培训和知识转移"
            ],
            "risks": [
                "学习曲线和团队适应",
                "迁移期间的性能下降",
                "可能的兼容性问题",
                "额外的开发资源需求"
            ],
            "best_practices": [
                "使用特性标志渐进式发布",
                "保持两个系统并行运行",
                "建立监控和回滚机制",
                "分阶段迁移而非大爆炸式"
            ]
        }

    def generate_full_report(self, requirements):
        """生成完整报告"""
        tech_recommendation = self.recommend(requirements)
        trend_report = self.trends_analyzer.generate_trend_report()
        
        return {
            "project_requirements": requirements,
            "tech_stack_recommendation": tech_recommendation,
            "trend_analysis": trend_report,
            "generated_at": datetime.now().isoformat()
        }

if __name__ == "__main__":
    recommender = TechStackRecommender()
    
    # 测试推荐
    print("测试技术栈推荐:")
    requirements = {
        "type": "web_app",
        "industry": "ecommerce",
        "team_size": "small",
        "performance": "high",
        "budget": "medium"
    }
    recommendation = recommender.recommend(requirements)
    
    print("\n推荐结果:")
    for category, techs in recommendation["recommendations"].items():
        print(f"\n{category}:")
        for i, tech in enumerate(techs, 1):
            print(f"  {i}. {tech['technology']} ({tech['trend_status']})")
            print(f"     {tech['recommendation']}")
    
    print(f"\n推荐理由: {recommendation['rationale']}")
    
    # 测试完整报告
    print("\n\n生成完整报告:")
    report = recommender.generate_full_report(requirements)
    print(f"报告生成时间: {report['generated_at']}")
