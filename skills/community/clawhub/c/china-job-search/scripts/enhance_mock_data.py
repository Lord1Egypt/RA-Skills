#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强模拟数据 - 基于测试结果优化
"""

import json
import os
from datetime import datetime

def enhance_mock_data():
    """增强模拟数据"""
    print("增强模拟数据...")
    
    # 数据目录
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    mock_file = os.path.join(data_dir, 'mock_jobs.json')
    
    # 读取现有数据
    if os.path.exists(mock_file):
        with open(mock_file, 'r', encoding='utf-8') as f:
            mock_data = json.load(f)
    else:
        mock_data = {"categories": {}}
    
    # 增强数据
    enhanced_categories = {
        "python": {
            "name": "Python开发",
            "jobs": [
                {
                    "title": "Python高级开发工程师",
                    "company": "字节跳动",
                    "salary": "25-50K·16薪",
                    "location": "北京·海淀区",
                    "experience": "3-5年",
                    "education": "本科",
                    "skills": ["Python", "Django/Flask", "MySQL", "Redis", "Docker", "微服务", "Linux"],
                    "description": "负责核心业务系统开发，参与架构设计，优化系统性能"
                },
                {
                    "title": "Python数据分析师",
                    "company": "阿里巴巴",
                    "salary": "20-40K·14薪",
                    "location": "杭州·余杭区",
                    "experience": "2-4年",
                    "education": "本科",
                    "skills": ["Python", "Pandas", "SQL", "统计学", "机器学习", "数据可视化"],
                    "description": "负责业务数据分析，构建数据模型，提供数据洞察"
                },
                {
                    "title": "Python后端开发",
                    "company": "腾讯",
                    "salary": "22-45K·15薪",
                    "location": "深圳·南山区",
                    "experience": "3-6年",
                    "education": "本科",
                    "skills": ["Python", "FastAPI", "PostgreSQL", "Redis", "K8s", "消息队列"],
                    "description": "负责后端服务开发，保证系统高可用和高性能"
                }
            ]
        },
        "java": {
            "name": "Java开发",
            "jobs": [
                {
                    "title": "Java高级开发工程师",
                    "company": "腾讯",
                    "salary": "30-60K·15薪",
                    "location": "深圳·南山区",
                    "experience": "5-8年",
                    "education": "本科",
                    "skills": ["Java", "Spring", "微服务", "分布式", "高并发", "Redis", "MySQL"],
                    "description": "负责核心业务系统开发，参与技术架构设计"
                },
                {
                    "title": "Java架构师",
                    "company": "百度",
                    "salary": "40-80K",
                    "location": "北京·海淀区",
                    "experience": "8年以上",
                    "education": "本科",
                    "skills": ["Java", "架构设计", "系统优化", "团队管理", "云计算"],
                    "description": "负责系统架构设计，技术选型，团队技术指导"
                },
                {
                    "title": "Java开发工程师",
                    "company": "京东",
                    "salary": "20-40K·14薪",
                    "location": "北京·朝阳区",
                    "experience": "3-6年",
                    "education": "本科",
                    "skills": ["Java", "Spring Boot", "MySQL", "消息队列", "分布式", "Docker"],
                    "description": "负责电商业务系统开发，参与需求分析和系统设计"
                }
            ]
        },
        "frontend": {
            "name": "前端开发",
            "jobs": [
                {
                    "title": "前端开发专家",
                    "company": "美团",
                    "salary": "25-45K·15薪",
                    "location": "上海·浦东新区",
                    "experience": "4-7年",
                    "education": "本科",
                    "skills": ["React", "Vue", "TypeScript", "Node.js", "Webpack", "性能优化"],
                    "description": "负责前端架构设计，技术选型，性能优化"
                },
                {
                    "title": "前端开发工程师",
                    "company": "滴滴",
                    "salary": "18-35K·14薪",
                    "location": "北京·朝阳区",
                    "experience": "2-5年",
                    "education": "本科",
                    "skills": ["JavaScript", "Vue", "小程序", "移动端", "CSS3", "HTML5"],
                    "description": "负责移动端和Web端前端开发，参与产品迭代"
                },
                {
                    "title": "全栈开发工程师",
                    "company": "小米",
                    "salary": "22-42K·14薪",
                    "location": "北京·海淀区",
                    "experience": "3-6年",
                    "education": "本科",
                    "skills": ["React", "Node.js", "Python", "MySQL", "Docker", "Redis"],
                    "description": "负责全栈开发，参与产品设计和架构"
                }
            ]
        },
        "test": {
            "name": "软件测试",
            "jobs": [
                {
                    "title": "测试开发工程师",
                    "company": "字节跳动",
                    "salary": "20-40K·16薪",
                    "location": "北京·海淀区",
                    "experience": "3-5年",
                    "education": "本科",
                    "skills": ["Python", "自动化测试", "性能测试", "接口测试", "CI/CD", "Selenium"],
                    "description": "负责测试框架开发，自动化测试，质量保障"
                },
                {
                    "title": "软件测试工程师",
                    "company": "阿里巴巴",
                    "salary": "15-30K·14薪",
                    "location": "杭州·余杭区",
                    "experience": "2-4年",
                    "education": "本科",
                    "skills": ["功能测试", "自动化测试", "SQL", "Linux", "测试用例", "缺陷管理"],
                    "description": "负责软件功能测试，编写测试用例，缺陷跟踪"
                },
                {
                    "title": "性能测试工程师",
                    "company": "腾讯",
                    "salary": "18-35K·15薪",
                    "location": "深圳·南山区",
                    "experience": "3-6年",
                    "education": "本科",
                    "skills": ["性能测试", "压力测试", "JMeter", "Python", "监控", "调优"],
                    "description": "负责系统性能测试，性能调优，容量规划"
                }
            ]
        },
        "devops": {
            "name": "运维开发",
            "jobs": [
                {
                    "title": "运维开发工程师",
                    "company": "腾讯",
                    "salary": "22-45K·15薪",
                    "location": "深圳·南山区",
                    "experience": "3-7年",
                    "education": "本科",
                    "skills": ["Linux", "Python", "Docker", "K8s", "CI/CD", "监控", "Shell"],
                    "description": "负责运维平台开发，自动化运维，系统监控"
                },
                {
                    "title": "云计算工程师",
                    "company": "华为",
                    "salary": "25-50K·15薪",
                    "location": "深圳·龙岗区",
                    "experience": "4-8年",
                    "education": "本科",
                    "skills": ["云计算", "K8s", "Docker", "网络", "安全", "自动化", "Terraform"],
                    "description": "负责云平台建设，容器化部署，云原生技术"
                },
                {
                    "title": "SRE工程师",
                    "company": "字节跳动",
                    "salary": "25-48K·16薪",
                    "location": "北京·海淀区",
                    "experience": "3-6年",
                    "education": "本科",
                    "skills": ["SRE", "可观测性", "故障处理", "容量规划", "自动化", "Go/Python"],
                    "description": "负责系统可靠性工程，故障应急，容量管理"
                }
            ]
        },
        "data": {
            "name": "数据分析",
            "jobs": [
                {
                    "title": "数据分析师",
                    "company": "美团",
                    "salary": "18-35K·15薪",
                    "location": "北京·朝阳区",
                    "experience": "2-5年",
                    "education": "本科",
                    "skills": ["SQL", "Python", "统计学", "数据可视化", "业务分析", "Excel"],
                    "description": "负责业务数据分析，数据报表，业务洞察"
                },
                {
                    "title": "数据挖掘工程师",
                    "company": "百度",
                    "salary": "25-50K·14薪",
                    "location": "北京·海淀区",
                    "experience": "3-6年",
                    "education": "硕士",
                    "skills": ["Python", "机器学习", "数据挖掘", "算法", "Spark", "Hadoop"],
                    "description": "负责数据挖掘算法开发，模型构建，特征工程"
                },
                {
                    "title": "大数据开发工程师",
                    "company": "阿里巴巴",
                    "salary": "25-55K·14薪",
                    "location": "杭州·余杭区",
                    "experience": "3-7年",
                    "education": "本科",
                    "skills": ["Hadoop", "Spark", "Flink", "Java/Scala", "数据仓库", "ETL"],
                    "description": "负责大数据平台开发，数据管道建设，数据治理"
                }
            ]
        },
        "ai": {
            "name": "人工智能",
            "jobs": [
                {
                    "title": "机器学习工程师",
                    "company": "字节跳动",
                    "salary": "30-60K·16薪",
                    "location": "北京·海淀区",
                    "experience": "3-6年",
                    "education": "硕士",
                    "skills": ["Python", "机器学习", "深度学习", "TensorFlow/PyTorch", "算法", "大数据"],
                    "description": "负责机器学习算法开发，模型训练，算法优化"
                },
                {
                    "title": "自然语言处理工程师",
                    "company": "百度",
                    "salary": "28-55K·14薪",
                    "location": "北京·海淀区",
                    "experience": "3-6年",
                    "education": "硕士",
                    "skills": ["NLP", "深度学习", "Python", "Transformer", "大语言模型", "算法"],
                    "description": "负责自然语言处理算法开发，模型优化，应用落地"
                },
                {
                    "title": "计算机视觉工程师",
                    "company": "商汤科技",
                    "salary": "30-65K·15薪",
                    "location": "上海·徐汇区",
                    "experience": "3-7年",
                    "education": "硕士",
                    "skills": ["计算机视觉", "深度学习", "Python", "OpenCV", "目标检测", "图像分割"],
                    "description": "负责计算机视觉算法开发，模型训练，产品集成"
                }
            ]
        },
        "product": {
            "name": "产品经理",
            "jobs": [
                {
                    "title": "产品经理",
                    "company": "腾讯",
                    "salary": "25-50K·15薪",
                    "location": "深圳·南山区",
                    "experience": "3-7年",
                    "education": "本科",
                    "skills": ["产品设计", "需求分析", "项目管理", "用户体验", "数据分析", "沟通协调"],
                    "description": "负责产品规划，需求分析，项目推进，产品迭代"
                },
                {
                    "title": "高级产品经理",
                    "company": "阿里巴巴",
                    "salary": "35-70K·14薪",
                    "location": "杭州·余杭区",
                    "experience": "5-10年",
                    "education": "本科",
                    "skills": ["产品战略", "团队管理", "商业分析", "市场调研", "产品运营", "创新"],
                    "description": "负责产品战略规划，团队管理，商业成功"
                },
                {
                    "title": "产品运营",
                    "company": "美团",
                    "salary": "20-40K·15薪",
                    "location": "北京·朝阳区",
                    "experience": "2-5年",
                    "education": "本科",
                    "skills": ["产品运营", "用户增长", "数据分析", "活动策划", "内容运营", "渠道运营"],
                    "description": "负责产品运营，用户增长，活动策划，数据分析"
                }
            ]
        },
        "design": {
            "name": "UI/UX设计",
            "jobs": [
                {
                    "title": "UI设计师",
                    "company": "字节跳动",
                    "salary": "18-35K·16薪",
                    "location": "北京·海淀区",
                    "experience": "2-5年",
                    "education": "本科",
                    "skills": ["UI设计", "视觉设计", "Sketch/Figma", "设计规范", "交互设计", "动效设计"],
                    "description": "负责产品UI设计，视觉设计，设计规范制定"
                },
                {
                    "title": "UX设计师",
                    "company": "腾讯",
                    "salary": "20-40K·15薪",
                    "location": "深圳·南山区",
                    "experience": "3-6年",
                    "education": "本科",
                    "skills": ["用户体验", "用户研究", "交互设计", "原型设计", "可用性测试", "用户画像"],
                    "description": "负责用户体验设计，用户研究，交互设计"
                },
                {
                    "title": "视觉设计师",
                    "company": "阿里巴巴",
                    "salary": "18-38K·14薪",
                    "location": "杭州·余杭区",
                    "experience": "2-5年",
                    "education": "本科",
                    "skills": ["视觉设计", "品牌设计", "平面设计", "动效设计", "创意设计", "设计工具"],
                    "description": "负责品牌视觉设计，创意设计，视觉传达"
                }
            ]
        },
        "operation": {
            "name": "运营",
            "jobs": [
                {
                    "title": "用户运营",
                    "company": "滴滴",
                    "salary": "15-30K·14薪",
                    "location": "北京·朝阳区",
                    "experience": "2-5年",
                    "education": "本科",
                    "skills": ["用户运营", "用户增长", "数据分析", "活动策划", "社群运营", "内容运营"],
                    "description": "负责用户运营，用户增长，活动策划，数据分析"
                },
                {
                    "title": "内容运营",
                    "company": "知乎",
                    "salary": "15-32K·14薪",
                    "location": "北京·海淀区",
                    "experience": "2-5年",
                    "education": "本科",
                    "skills": ["内容运营", "内容策划", "文案写作", "新媒体", "数据分析", "用户互动"],
                    "description": "负责内容运营，内容策划，文案创作，用户互动"
                },
                {
                    "title": "市场运营",
                    "company": "美团",
                    "salary": "18-35K·15薪",
                    "location": "上海·浦东新区",
                    "experience": "3-6年",
                    "education": "本科",
                    "skills": ["市场运营", "品牌推广", "渠道运营", "市场营销", "数据分析", "活动策划"],
                    "description": "负责市场运营，品牌推广，渠道管理，营销活动"
                }
            ]
        }
    }
    
    # 更新数据
    mock_data["categories"] = enhanced_categories
    mock_data["metadata"] = {
        "version": "2.0",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_categories": len(enhanced_categories),
        "total_jobs": sum(len(cat["jobs"]) for cat in enhanced_categories.values()),
        "description": "增强版模拟数据，基于市场调研和测试结果优化"
    }
    
    # 保存数据
    with open(mock_file, 'w', encoding='utf-8') as f:
        json.dump(mock_data, f, ensure_ascii=False, indent=2)
    
    print(f"模拟数据已增强并保存到: {mock_file}")
    
    # 统计信息
    total_jobs = mock_data["metadata"]["total_jobs"]
    total_categories = mock_data["metadata"]["total_categories"]
    
    print(f"\n增强后的模拟数据统计:")
    print(f"  类别数量: {total_categories}")
    print(f"  职位总数: {total_jobs}")
    
    # 各类别统计
    print("\n各类别职位分布:")
    for category_id, category in enhanced_categories.items():
        job_count = len(category["jobs"])
        print(f"  {category['name']:10} -> {job_count} 个职位")
    
    return mock_data

def create_city_salary_data():
    """创建城市薪资数据"""
    print("\n创建城市薪资参考数据...")
    
    # 各城市薪资系数（相对于北京）
    city_salary_factors = {
        "北京": 1.0,
        "上海": 0.95,
        "深圳": 0.90,
        "广州": 0.80,
        "杭州": 0.85,
        "成都": 0.70,
        "武汉": 0.65,
        "南京": 0.75,
        "西安": 0.60,
        "重庆": 0.65
    }
    
    city_data_file = os.path.join(os.path.dirname(__file__), 'data', 'city_salary_data.json')
    
    city_data = {
        "factors": city_salary_factors,
        "base_city": "北京",
        "description": "各城市薪资系数（相对于北京）",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(city_data_file, 'w', encoding='utf-8') as f:
        json.dump(city_data, f, ensure_ascii=False, indent=2)
    
    print(f"城市薪资数据已保存到: {city_data_file}")
    
    print("\n各城市薪资系数（相对于北京）:")
    for city, factor in city_salary_factors.items():
        print(f"  {city:4} -> {factor:.2f}")
    
    return city_data


def create_skill_database():
    """创建技能数据库"""
    print("\n创建技能数据库...")
    
    # 技能分类
    skill_categories = {
        "programming": {
            "name": "编程语言",
            "skills": ["Python", "Java", "JavaScript", "Go", "C++", "C#", "PHP", "Swift", "Kotlin", "Rust"]
        },
        "frontend": {
            "name": "前端技术",
            "skills": ["React", "Vue", "Angular", "TypeScript", "Webpack", "Vite", "小程序", "移动端", "CSS3", "HTML5"]
        },
        "backend": {
            "name": "后端技术",
            "skills": ["Spring", "Django", "Flask", "FastAPI", "Node.js", "微服务", "分布式", "高并发", "消息队列", "RESTful"]
        },
        "database": {
            "name": "数据库",
            "skills": ["MySQL", "PostgreSQL", "Redis", "MongoDB", "Elasticsearch", "SQL", "NoSQL", "数据仓库", "数据湖"]
        },
        "devops": {
            "name": "运维部署",
            "skills": ["Docker", "K8s", "CI/CD", "Linux", "Shell", "监控", "日志", "安全", "网络", "云计算"]
        },
        "data": {
            "name": "数据科学",
            "skills": ["数据分析", "数据挖掘", "机器学习", "深度学习", "统计学", "数据可视化", "大数据", "Spark", "Hadoop", "Pandas"]
        },
        "ai": {
            "name": "人工智能",
            "skills": ["自然语言处理", "计算机视觉", "大语言模型", "强化学习", "推荐系统", "语音识别", "图像处理", "算法优化"]
        },
        "soft": {
            "name": "软技能",
            "skills": ["沟通能力", "团队协作", "问题解决", "项目管理", "产品思维", "用户思维", "学习能力", "创新能力"]
        }
    }
    
    skill_db_file = os.path.join(os.path.dirname(__file__), 'data', 'skill_database.json')
    
    skill_data = {
        "categories": skill_categories,
        "total_skills": sum(len(cat["skills"]) for cat in skill_categories.values()),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": "技能分类数据库，用于职位匹配和技能分析"
    }
    
    with open(skill_db_file, 'w', encoding='utf-8') as f:
        json.dump(skill_data, f, ensure_ascii=False, indent=2)
    
    print(f"技能数据库已保存到: {skill_db_file}")
    
    print("\n技能分类统计:")
    for category_id, category in skill_categories.items():
        skill_count = len(category["skills"])
        print(f"  {category['name']:10} -> {skill_count} 种技能")
    
    return skill_data


def main():
    """主函数"""
    print("增强招聘搜索技能的数据...")
    print("=" * 60)
    
    # 执行增强
    mock_data = enhance_mock_data()
    city_data = create_city_salary_data()
    skill_data = create_skill_database()
    
    print("\n" + "=" * 60)
    print("数据增强完成!")
    
    # 总结
    total_jobs = mock_data["metadata"]["total_jobs"]
    total_categories = mock_data["metadata"]["total_categories"]
    total_skills = skill_data["total_skills"]
    
    print(f"\n增强后的数据规模:")
    print(f"  职位类别: {total_categories} 类")
    print(f"  模拟职位: {total_jobs} 个")
    print(f"  技能分类: {len(skill_data['categories'])} 类")
    print(f"  技能总数: {total_skills} 种")
    print(f"  城市数据: {len(city_data['factors'])} 个")
    
    print("\n下一步:")
    print("1. 运行测试验证增强效果")
    print("2. 手动添加更多真实职位")
    print("3. 集成到搜索器中使用")


if __name__ == '__main__':
    main()