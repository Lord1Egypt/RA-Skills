#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
招聘搜索技能快速开始
演示完整功能（使用模拟数据）
"""

import sys
import os
import json

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("招聘搜索技能 - 快速开始")
print("支持平台: BOSS直聘、智联招聘、前程无忧")
print("=" * 70)

# 创建模拟数据演示功能
def create_mock_jobs():
    """创建模拟岗位数据"""
    from job_searcher import Job
    
    mock_jobs = [
        # BOSS直聘
        Job("BOSS直聘", "Python高级开发工程师", "字节跳动", "30-60K·16薪", "北京·海淀区", "5-10年", "本科", 
            ["Python", "Go", "微服务", "K8s", "Redis"], "https://www.zhipin.com/job1"),
        Job("BOSS直聘", "Java架构师", "阿里巴巴", "40-70K", "杭州·余杭区", "8年以上", "本科", 
            ["Java", "Spring Cloud", "分布式", "高并发"], "https://www.zhipin.com/job2"),
        
        # 智联招聘
        Job("智联招聘", "前端开发专家", "腾讯", "25-50K·14薪", "深圳·南山区", "5-8年", "本科",
            ["React", "Vue", "TypeScript", "Node.js"], "https://www.zhaopin.com/job3"),
        Job("智联招聘", "测试开发工程师", "百度", "20-40K", "北京·海淀区", "3-5年", "本科",
            ["自动化测试", "Python", "Selenium", "性能测试"], "https://www.zhaopin.com/job4"),
        
        # 前程无忧
        Job("前程无忧", "运维工程师", "华为", "18-35K·15薪", "深圳·龙岗区", "3-7年", "大专",
            ["Linux", "Docker", "K8s", "Shell"], "https://www.51job.com/job5"),
        Job("前程无忧", "数据分析师", "美团", "15-30K", "上海·浦东新区", "2-5年", "本科",
            ["Python", "SQL", "统计学", "机器学习"], "https://www.51job.com/job6"),
    ]
    return mock_jobs

def demo_table_format(jobs):
    """演示表格格式输出"""
    print("\n" + "=" * 70)
    print("表格格式输出演示")
    print("=" * 70)
    
    # 表头
    print(f"{'平台':<10} | {'职位':<20} | {'公司':<10} | {'薪资':<12} | {'地点':<10} | {'经验':<8} | {'学历':<4}")
    print("-" * 90)
    
    for job in jobs:
        platform = job.platform[:10]
        title = job.title[:18] + ".." if len(job.title) > 18 else job.title.ljust(20)
        company = job.company[:8] + ".." if len(job.company) > 8 else job.company.ljust(10)
        salary = job.salary.ljust(12)
        location = job.location[:8] + ".." if len(job.location) > 8 else job.location.ljust(10)
        experience = job.experience.ljust(8)
        education = job.education.ljust(4)
        
        print(f"{platform:<10} | {title:<20} | {company:<10} | {salary:<12} | {location:<10} | {experience:<8} | {education:<4}")

def demo_list_format(jobs):
    """演示列表格式输出"""
    print("\n" + "=" * 70)
    print("列表格式输出演示")
    print("=" * 70)
    
    for i, job in enumerate(jobs, 1):
        print(f"{i}. 【{job.platform}】{job.title}")
        print(f"   公司：{job.company}")
        print(f"   薪资：{job.salary} | 地点：{job.location}")
        print(f"   要求：{job.experience} | {job.education}")
        print(f"   技能：{', '.join(job.skills[:3])}")
        print()

def demo_platform_stats(jobs):
    """演示平台统计"""
    print("\n" + "=" * 70)
    print("平台统计信息")
    print("=" * 70)
    
    stats = {}
    for job in jobs:
        if job.platform not in stats:
            stats[job.platform] = 0
        stats[job.platform] += 1
    
    for platform, count in stats.items():
        print(f"{platform}: {count} 个岗位")
    
    # 薪资分析
    salaries = []
    for job in jobs:
        # 简单提取薪资数字
        import re
        numbers = re.findall(r'\d+', job.salary)
        if numbers:
            avg = sum(map(int, numbers)) / len(numbers)
            salaries.append(avg)
    
    if salaries:
        print(f"\n平均薪资范围: {min(salaries):.1f}K - {max(salaries):.1f}K")
        print(f"整体平均薪资: {sum(salaries)/len(salaries):.1f}K")

def demo_export(jobs):
    """演示数据导出"""
    print("\n" + "=" * 70)
    print("数据导出演示")
    print("=" * 70)
    
    # JSON导出
    data = []
    for job in jobs:
        data.append({
            "platform": job.platform,
            "title": job.title,
            "company": job.company,
            "salary": job.salary,
            "location": job.location,
            "experience": job.experience,
            "education": job.education,
            "skills": job.skills,
            "url": job.url
        })
    
    # 保存到文件
    with open('demo_jobs.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"已导出 {len(data)} 个岗位到 demo_jobs.json")
    print("文件内容预览:")
    print(json.dumps(data[0], ensure_ascii=False, indent=2))

def show_usage():
    """显示使用说明"""
    print("\n" + "=" * 70)
    print("使用说明")
    print("=" * 70)
    
    print("""
1. 命令行搜索:
   python job_searcher.py "Python开发" -c 北京
   python job_searcher.py "Java开发" -c 上海 -p boss,zhilian
   python job_searcher.py "前端开发" -c 广州 -n 30 -f list

2. OpenClaw集成使用:
   python openclaw_integration.py
   python openclaw_integration.py "搜索 Python 北京"
   python openclaw_integration.py --stats
   python openclaw_integration.py --export json

3. 在OpenClaw工作流中:
   from skills.job_search import JobSearchSkill
   skill = JobSearchSkill()
   result = skill.handle_command("搜索 Java 上海")

4. 实际网站搜索说明:
   当前技能框架已完整，但需要:
   - 根据各网站当前结构调整解析器
   - 处理反爬机制（已预留接口）
   - 可能需要添加代理支持
    """)

def main():
    """主函数"""
    # 创建模拟数据
    mock_jobs = create_mock_jobs()
    
    # 演示各种功能
    demo_table_format(mock_jobs)
    demo_list_format(mock_jobs)
    demo_platform_stats(mock_jobs)
    demo_export(mock_jobs)
    show_usage()
    
    print("\n" + "=" * 70)
    print("快速开始完成")
    print("下一步:")
    print("1. 查看 config.json 调整配置")
    print("2. 运行 python job_searcher.py 'Python' -c 北京 测试实际搜索")
    print("3. 根据网站结构调整解析器代码")
    print("=" * 70)

if __name__ == '__main__':
    main()