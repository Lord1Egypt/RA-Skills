#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
招聘搜索技能简单演示
展示技能的基本结构和使用方法
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("招聘搜索技能演示")
print("=" * 60)

# 演示1：技能结构
print("\n1. 技能文件结构:")
files = os.listdir('.')
for file in sorted(files):
    if file.endswith('.py') or file.endswith('.md') or file in ['config.json', 'requirements.txt']:
        size = os.path.getsize(file)
        print(f"  - {file:30} ({size} bytes)")

# 演示2：模块导入
print("\n2. 模块导入测试:")
try:
    from job_searcher import JobSearcher, Job
    print("  [OK] JobSearcher 导入成功")
    print("  [OK] Job 数据类导入成功")
    
    from openclaw_integration import JobSearchSkill
    print("  [OK] JobSearchSkill 导入成功")
    
except ImportError as e:
    print(f"  ✗ 导入失败: {e}")

# 演示3：创建模拟数据展示格式
print("\n3. 输出格式演示:")

# 创建模拟岗位数据
mock_jobs = [
    Job(
        platform="BOSS直聘",
        title="Python后端开发工程师",
        company="某科技公司",
        salary="20-30K·15薪",
        location="北京·海淀区",
        experience="3-5年",
        education="本科",
        skills=["Python", "Django", "MySQL", "Redis"],
        url="https://www.zhipin.com/job1"
    ),
    Job(
        platform="智联招聘",
        title="Java高级开发工程师",
        company="某互联网企业",
        salary="25-40K",
        location="上海·浦东新区",
        experience="5-8年",
        education="本科",
        skills=["Java", "Spring", "微服务", "Kafka"],
        url="https://www.zhaopin.com/job2"
    ),
    Job(
        platform="前程无忧",
        title="前端开发工程师",
        company="某软件公司",
        salary="15-25K·14薪",
        location="广州·天河区",
        experience="2-4年",
        education="大专",
        skills=["Vue.js", "React", "TypeScript", "Webpack"],
        url="https://www.51job.com/job3"
    )
]

# 演示表格输出
print("\n表格格式输出:")
print("-" * 80)
print("职位                     | 公司         | 薪资         | 地点         | 经验    | 学历")
print("-" * 80)
for job in mock_jobs:
    title = job.title[:20] + '...' if len(job.title) > 20 else job.title.ljust(20)
    company = job.company[:10] + '...' if len(job.company) > 10 else job.company.ljust(10)
    salary = job.salary.ljust(12)
    location = job.location[:10] + '...' if len(job.location) > 10 else job.location.ljust(10)
    experience = job.experience.ljust(8)
    education = job.education.ljust(4)
    print(f"{title} | {company} | {salary} | {location} | {experience} | {education}")

# 演示4：使用方式
print("\n4. 使用方式:")
print("""
命令行使用:
  python job_searcher.py "Python开发" -c 北京
  python job_searcher.py "Java开发" -c 上海 -p boss,zhilian
  python job_searcher.py "前端开发" -c 广州 -n 30 -f list

OpenClaw集成:
  python openclaw_integration.py
  python openclaw_integration.py "搜索 Python 北京"
  python openclaw_integration.py --stats
  python openclaw_integration.py --export json --output jobs.json

在OpenClaw中调用:
  from skills.job_search import JobSearchSkill
  skill = JobSearchSkill()
  result = skill.handle_command("搜索 Python 北京")
""")

# 演示5：配置说明
print("\n5. 配置说明:")
try:
    import json
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print(f"  默认城市: {config['search']['default_city']}")
    print(f"  最大结果数: {config['search']['max_results']}")
    print(f"  输出格式: {config['output']['format']}")
    print(f"  显示字段: {', '.join(config['output']['show_fields'])}")
    
    platforms = []
    for key, value in config['platforms'].items():
        if value['enabled']:
            platforms.append(value['name'])
    print(f"  启用平台: {', '.join(platforms)}")
    
except Exception as e:
    print(f"  读取配置失败: {e}")

print("\n" + "=" * 60)
print("演示完成")
print("=" * 60)
print("\n下一步:")
print("1. 安装依赖: pip install -r requirements.txt")
print("2. 测试搜索: python job_searcher.py \"Python\" -c 北京")
print("3. 集成到OpenClaw工作流中")