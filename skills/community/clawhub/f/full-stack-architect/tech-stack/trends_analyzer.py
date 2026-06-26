#!/usr/bin/env python3
"""
技术趋势分析模块
用于分析和评估技术趋势
"""

import os
import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TrendsAnalyzer:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), 'tech_database.json')
        self.trends_path = os.path.join(os.path.dirname(__file__), 'tech_trends.json')
        self.tech_database = self._load_tech_database()
        self.trends_data = self._load_trends_data()

    def _load_tech_database(self):
        """加载技术数据库"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载技术数据库失败: {str(e)}")
                return {}
        return {}

    def _load_trends_data(self):
        """加载趋势数据"""
        if os.path.exists(self.trends_path):
            try:
                with open(self.trends_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载趋势数据失败: {str(e)}")
        return self._default_trends_data()

    def _default_trends_data(self):
        """默认趋势数据"""
        return {
            "trending_tech": [
                "Rust", "Go", "TypeScript", "SolidJS", "Svelte", 
                "Next.js", "FastAPI", "CockroachDB", "InfluxDB",
                "Terraform", "GitHub Actions", "LangChain"
            ],
            "growing_tech": [
                "Kotlin", "Deno", "Nuxt.js", "Nest.js", 
                "CockroachDB", "Cue", "Pulumi"
            ],
            "declining_tech": [
                "jQuery", "Ruby on Rails", "MongoDB (legacy)",
                "PHP (legacy)", "AngularJS"
            ],
            "enterprise_preference": {
                "frontend": ["React", "Vue", "Angular"],
                "backend": ["Java", "Go", "Python"],
                "database": ["PostgreSQL", "MySQL", "MongoDB"],
                "devops": ["Docker", "Kubernetes", "GitLab"]
            },
            "startup_preference": {
                "frontend": ["React", "Vue", "Svelte"],
                "backend": ["Python", "Go", "Node.js"],
                "database": ["PostgreSQL", "MongoDB", "Redis"],
                "devops": ["Docker", "GitHub Actions", "Vercel"]
            }
        }

    def analyze_tech(self, tech_name, category=None):
        """分析技术的趋势和适用性"""
        tech_info = None
        
        if category:
            if category in self.tech_database and tech_name in self.tech_database[category]:
                tech_info = self.tech_database[category][tech_name]
        else:
            for cat, techs in self.tech_database.items():
                if tech_name in techs:
                    tech_info = techs[tech_name]
                    category = cat
                    break
        
        if not tech_info:
            return {
                "success": False,
                "message": f"技术 {tech_name} 未在数据库中找到"
            }
        
        trending_score = self._calculate_trending_score(tech_name, tech_info)
        
        return {
            "success": True,
            "technology": tech_name,
            "category": category,
            "description": tech_info.get("description", ""),
            "pros": tech_info.get("pros", []),
            "cons": tech_info.get("cons", []),
            "use_cases": tech_info.get("use_cases", []),
            "scores": {
                "popularity": tech_info.get("popularity", 0),
                "community": tech_info.get("community", 0),
                "maintenance": tech_info.get("maintenance", 0),
                "trending": trending_score
            },
            "trend_status": self._get_trend_status(tech_name),
            "recommendation": self._generate_recommendation(tech_name, tech_info, trending_score)
        }

    def _calculate_trending_score(self, tech_name, tech_info):
        """计算技术的趋势分数"""
        base_score = (tech_info.get("popularity", 50) + 
                     tech_info.get("community", 50) + 
                     tech_info.get("maintenance", 50)) / 3
        
        trending_bonus = 0
        if tech_name in self.trends_data.get("trending_tech", []):
            trending_bonus = 30
        elif tech_name in self.trends_data.get("growing_tech", []):
            trending_bonus = 15
        elif tech_name in self.trends_data.get("declining_tech", []):
            trending_bonus = -20
        
        return min(100, max(0, base_score + trending_bonus))

    def _get_trend_status(self, tech_name):
        """获取技术的趋势状态"""
        if tech_name in self.trends_data.get("trending_tech", []):
            return "Trending"
        elif tech_name in self.trends_data.get("growing_tech", []):
            return "Growing"
        elif tech_name in self.trends_data.get("declining_tech", []):
            return "Declining"
        else:
            return "Stable"

    def _generate_recommendation(self, tech_name, tech_info, trending_score):
        """生成技术推荐"""
        if trending_score >= 80:
            return f"强烈推荐使用 {tech_name}，它具有优秀的生态系统和强烈的增长趋势"
        elif trending_score >= 60:
            return f"推荐考虑使用 {tech_name}，它具有良好的社区支持和稳定的发展"
        elif trending_score >= 40:
            return f"可以考虑使用 {tech_name}，但建议评估团队熟悉度和项目需求"
        else:
            return f"建议谨慎使用 {tech_name}，考虑更成熟的替代方案"

    def recommend_tech_stack(self, project_type="general", team_size="small"):
        """推荐技术栈"""
        if team_size == "enterprise":
            preferences = self.trends_data.get("enterprise_preference", {})
        else:
            preferences = self.trends_data.get("startup_preference", {})
        
        recommendations = {}
        
        for category, preferred_techs in preferences.items():
            if category in self.tech_database:
                category_recommendations = []
                for tech_name in preferred_techs:
                    if tech_name in self.tech_database[category]:
                        analysis = self.analyze_tech(tech_name, category)
                        if analysis.get("success"):
                            category_recommendations.append(analysis)
                recommendations[category] = category_recommendations
        
        return {
            "project_type": project_type,
            "team_size": team_size,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }

    def get_trending_technologies(self, category=None):
        """获取热门技术"""
        if category:
            if category in self.tech_database:
                techs = list(self.tech_database[category].keys())
                scored = []
                for tech in techs:
                    analysis = self.analyze_tech(tech, category)
                    if analysis.get("success"):
                        scored.append((tech, analysis["scores"]["trending"]))
                scored.sort(key=lambda x: x[1], reverse=True)
                return [tech for tech, score in scored[:5]]
        else:
            return self.trends_data.get("trending_tech", [])

    def update_trend_data(self, updates):
        """更新趋势数据"""
        self.trends_data.update(updates)
        try:
            with open(self.trends_path, 'w', encoding='utf-8') as f:
                json.dump(self.trends_data, f, ensure_ascii=False, indent=2)
            logger.info("趋势数据更新成功")
            return True
        except Exception as e:
            logger.error(f"更新趋势数据失败: {str(e)}")
            return False

    def generate_trend_report(self):
        """生成趋势报告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "trending": self.get_trending_technologies(),
            "growing": self.trends_data.get("growing_tech", []),
            "declining": self.trends_data.get("declining_tech", []),
            "recommendations": {
                "startup": self.recommend_tech_stack("startup", "small"),
                "enterprise": self.recommend_tech_stack("enterprise", "enterprise")
            }
        }
        return report

if __name__ == "__main__":
    analyzer = TrendsAnalyzer()
    
    # 测试分析单个技术
    print("分析 React:")
    analysis = analyzer.analyze_tech("React", "frontend")
    if analysis["success"]:
        print(f"趋势状态: {analysis['trend_status']}")
        print(f"趋势分数: {analysis['scores']['trending']}")
        print(f"推荐: {analysis['recommendation']}")
    print()
    
    # 测试推荐技术栈
    print("推荐技术栈 (Startup):")
    recommendations = analyzer.recommend_tech_stack("startup", "small")
    for category, techs in recommendations["recommendations"].items():
        print(f"\n{category}:")
        for tech in techs:
            print(f"  - {tech['technology']}: {tech['trend_status']}")
    print()
    
    # 测试生成趋势报告
    print("生成趋势报告:")
    report = analyzer.generate_trend_report()
    print(f"热门技术: {report['trending']}")
    print(f"增长技术: {report['growing']}")
    print(f"下降技术: {report['declining']}")
