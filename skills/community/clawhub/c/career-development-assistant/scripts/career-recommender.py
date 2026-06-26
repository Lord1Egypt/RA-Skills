#!/usr/bin/env python3
"""
职业推荐引擎
基于用户特点推荐职业方向
"""

import json
import sys
from typing import Dict, List, Optional


# 职业数据库（与careers.md对应）
CAREER_DATABASE = [
    {"name": "软件工程师", "category": "IT", "skills": ["编程", "算法", "数据库"],
     "interests": ["计算机", "编程", "逻辑", "技术"],
     "personality": ["分析型", "逻辑型", "专注型"],
     "min_degree": "大专", "salary": "8K-30K"},
    {"name": "数据分析师", "category": "IT", "skills": ["SQL", "Python", "统计"],
     "interests": ["数据", "分析", "商业", "逻辑"],
     "personality": ["分析型", "细致型", "逻辑型"],
     "min_degree": "大专", "salary": "7K-25K"},
    {"name": "网络工程师", "category": "IT", "skills": ["网络", "安全", "设备配置"],
     "interests": ["网络", "通信", "搭建", "硬件"],
     "personality": ["实操型", "技术型", "耐心型"],
     "min_degree": "中专", "salary": "6K-20K"},
    {"name": "信息安全工程师", "category": "IT", "skills": ["渗透测试", "安全运维", "密码学"],
     "interests": ["安全", "黑客", "防护", "逆向"],
     "personality": ["谨慎型", "探索型", "技术型"],
     "min_degree": "大专", "salary": "10K-35K"},
    {"name": "护士", "category": "医疗", "skills": ["护理操作", "急救", "沟通"],
     "interests": ["医疗", "护理", "人文关怀", "生命科学"],
     "personality": ["耐心型", "细心型", "助人型"],
     "min_degree": "中专", "salary": "5K-15K"},
    {"name": "康复治疗师", "category": "医疗", "skills": ["康复评定", "手法治疗", "理疗"],
     "interests": ["康复", "运动", "健康", "帮助他人"],
     "personality": ["耐心型", "助人型", "沟通型"],
     "min_degree": "大专", "salary": "5K-15K"},
    {"name": "医学检验技术员", "category": "医疗", "skills": ["检验操作", "仪器使用", "实验室管理"],
     "interests": ["医疗", "实验", "分析", "生物"],
     "personality": ["细致型", "谨慎型", "专注型"],
     "min_degree": "大专", "salary": "5K-12K"},
    {"name": "智能制造工程师", "category": "制造", "skills": ["PLC", "机器人", "MES"],
     "interests": ["机械", "自动化", "制造", "电子"],
     "personality": ["实操型", "技术型", "动手型"],
     "min_degree": "大专", "salary": "7K-20K"},
    {"name": "新能源汽车维修技师", "category": "制造", "skills": ["高压电", "电池诊断", "CAN总线"],
     "interests": ["汽车", "电动", "维修", "机械"],
     "personality": ["动手型", "技术型", "实操型"],
     "min_degree": "中专", "salary": "6K-18K"},
    {"name": "无人机操作员", "category": "制造", "skills": ["飞行操作", "测绘", "植保"],
     "interests": ["无人机", "飞行", "航拍", "户外"],
     "personality": ["户外型", "技术型", "专注型"],
     "min_degree": "中专", "salary": "6K-15K"},
    {"name": "电子商务运营", "category": "商业", "skills": ["电商操作", "数据分析", "营销"],
     "interests": ["电商", "营销", "运营", "互联网"],
     "personality": ["沟通型", "创意型", "细致型"],
     "min_degree": "中专", "salary": "5K-15K"},
    {"name": "新媒体运营", "category": "商业", "skills": ["文案", "视频剪辑", "社群运营"],
     "interests": ["内容创作", "社交媒体", "营销", "创意"],
     "personality": ["创意型", "沟通型", "紧跟潮流型"],
     "min_degree": "不限", "salary": "5K-20K"},
    {"name": "物流管理师", "category": "商业", "skills": ["WMS", "运输规划", "仓储管理"],
     "interests": ["物流", "供应链", "管理", "规划"],
     "personality": ["条理型", "规划型", "管理型"],
     "min_degree": "中专", "salary": "5K-12K"},
    {"name": "平面设计师", "category": "文创", "skills": ["PS", "AI", "排版"],
     "interests": ["设计", "艺术", "视觉", "美学"],
     "personality": ["创意型", "审美型", "细致型"],
     "min_degree": "中专", "salary": "5K-15K"},
    {"name": "数字媒体制作", "category": "文创", "skills": ["剪辑", "特效", "摄影"],
     "interests": ["视频", "动画", "拍摄", "创作"],
     "personality": ["创意型", "技术型", "审美型"],
     "min_degree": "中专", "salary": "5K-20K"},
    {"name": "会计", "category": "专业服务", "skills": ["账务", "税务", "财务软件"],
     "interests": ["财务", "数字", "规则", "细致"],
     "personality": ["细致型", "条理型", "耐心型"],
     "min_degree": "中专", "salary": "5K-20K"},
    {"name": "人力资源管理", "category": "专业服务", "skills": ["招聘", "培训", "劳动法"],
     "interests": ["人力资源", "管理", "沟通", "组织"],
     "personality": ["沟通型", "管理型", "组织型"],
     "min_degree": "大专", "salary": "5K-15K"},
    {"name": "酒店管理", "category": "生活服务", "skills": ["运营", "接待", "外语"],
     "interests": ["酒店", "服务", "管理", "旅游"],
     "personality": ["服务型", "沟通型", "管理型"],
     "min_degree": "中专", "salary": "4K-12K"},
    {"name": "食品检验员", "category": "农业", "skills": ["检验", "质量管理", "实验室"],
     "interests": ["食品安全", "实验", "质量", "生物"],
     "personality": ["细致型", "谨慎型", "条理型"],
     "min_degree": "大专", "salary": "4K-10K"},
    {"name": "现代农业技术员", "category": "农业", "skills": ["智慧农业", "无人机", "数据分析"],
     "interests": ["农业", "科技", "种植", "生态"],
     "personality": ["户外型", "探索型", "动手型"],
     "min_degree": "大专", "salary": "5K-12K"},
    {"name": "幼儿教师", "category": "教育", "skills": ["教学", "保育", "艺术"],
     "interests": ["教育", "幼儿", "音乐", "绘画"],
     "personality": ["耐心型", "爱心型", "活泼型"],
     "min_degree": "中专", "salary": "4K-10K"},
    {"name": "社会体育指导员", "category": "教育", "skills": ["健身指导", "运动技能", "培训"],
     "interests": ["运动", "健身", "体育", "健康"],
     "personality": ["运动型", "指导型", "外向型"],
     "min_degree": "中专", "salary": "5K-20K"},
    {"name": "家政服务管理", "category": "生活服务", "skills": ["家政管理", "培训", "运营"],
     "interests": ["家政", "服务", "管理", "家庭"],
     "personality": ["管理型", "服务型", "条理型"],
     "min_degree": "不限", "salary": "5K-15K"},
]


def recommend_by_interests(interests: List[str], top_n: int = 5) -> List[Dict]:
    """
    根据用户兴趣推荐职业

    Args:
        interests: 用户兴趣关键词列表
        top_n: 返回数量

    Returns:
        推荐职业列表
    """
    scores = []
    for career in CAREER_DATABASE:
        score = 0
        for interest in interests:
            if interest in career["interests"]:
                score += 2
            # 模糊匹配：兴趣关键词出现在技能或人格描述中
            for skill in career["skills"]:
                if interest in skill:
                    score += 1
            for trait in career["personality"]:
                if interest in trait:
                    score += 1
        if score > 0:
            scores.append((score, career))
    
    scores.sort(key=lambda x: x[0], reverse=True)
    return [c for s, c in scores[:top_n]]


def recommend_by_degree(degree: str, top_n: int = 5) -> List[Dict]:
    """
    根据学历推荐职业

    Args:
        degree: 学历 (不限/中专/大专/本科)
    
    Returns:
        推荐职业列表
    """
    degree_levels = {"不限": 0, "中专": 1, "大专": 2, "本科": 3}
    level = degree_levels.get(degree, 2)
    
    matches = []
    for career in CAREER_DATABASE:
        career_level = degree_levels.get(career["min_degree"], 2)
        if career_level <= level:
            matched = f"{career['name']}（学历要求：{career['min_degree']}）"
            matches.append(career)
    
    return matches[:top_n]


def recommend_by_category(category: str, top_n: int = 10) -> List[Dict]:
    """
    根据职业类别推荐

    Args:
        category: 类别 (IT/医疗/制造/商业/文创/专业服务/生活服务/农业/教育)
    
    Returns:
        推荐职业列表
    """
    return [c for c in CAREER_DATABASE if c["category"] == category][:top_n]


def get_career_detail(name: str) -> Optional[Dict]:
    """
    获取单个职业的详细信息

    Args:
        name: 职业名称
    
    Returns:
        职业详情
    """
    for career in CAREER_DATABASE:
        if name in career["name"]:
            return career
    return None


def list_all_categories() -> List[str]:
    """列出所有职业类别"""
    categories = set()
    for career in CAREER_DATABASE:
        categories.add(career["category"])
    return sorted(list(categories))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python career-recommender.py interest 编程,计算机,技术")
        print("  python career-recommender.py degree 中专")
        print("  python career-recommender.py category IT")
        print("  python career-recommender.py detail 软件工程师")
        print("  python career-recommender.py categories")
        sys.exit(1)

    action = sys.argv[1]

    if action == "interest" and len(sys.argv) >= 3:
        interests = sys.argv[2].split(",")
        results = recommend_by_interests(interests)
        print(f"基于兴趣 [{', '.join(interests)}] 推荐职业:\n")
        for i, c in enumerate(results, 1):
            print(f"  {i}. {c['name']}（{c['category']}）— 薪资参考：{c['salary']}")
    elif action == "degree" and len(sys.argv) >= 3:
        results = recommend_by_degree(sys.argv[2])
        print(f"{sys.argv[2]}学历可从事的职业:\n")
        for c in results:
            print(f"  • {c['name']}（{c['category']}）— 最低学历：{c['min_degree']} — 薪资：{c['salary']}")
    elif action == "category" and len(sys.argv) >= 3:
        results = recommend_by_category(sys.argv[2])
        print(f"{sys.argv[2]}类职业:\n")
        for c in results:
            print(f"  • {c['name']} — 薪资参考：{c['salary']}")
    elif action == "detail" and len(sys.argv) >= 3:
        result = get_career_detail(sys.argv[2])
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"未找到职业: {sys.argv[2]}")
    elif action == "categories":
        cats = list_all_categories()
        print("职业类别:")
        for c in cats:
            count = len(recommend_by_category(c, 999))
            print(f"  • {c}（{count}个职业）")
    else:
        print("未知参数")
        sys.exit(1)
