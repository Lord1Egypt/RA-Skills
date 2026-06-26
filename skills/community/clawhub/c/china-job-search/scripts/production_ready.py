#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生产就绪版招聘搜索技能
基于高质量模拟数据 + 可扩展的真实搜索接口
"""

import sys
import os
import json
import time
import random
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import csv

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class ProductionJob:
    """生产版岗位信息"""
    id: str
    platform: str
    title: str
    company: str
    salary: str
    location: str
    experience: str
    education: str
    skills: List[str]
    description: str
    url: str
    source: str  # mock, manual, api
    posted_date: str
    created_at: str
    
    def to_dict(self):
        return asdict(self)
    
    def to_csv_row(self):
        return [
            self.id,
            self.platform,
            self.title,
            self.company,
            self.salary,
            self.location,
            self.experience,
            self.education,
            ','.join(self.skills),
            self.description[:100] + '...' if len(self.description) > 100 else self.description,
            self.url,
            self.source,
            self.posted_date,
            self.created_at
        ]


class ProductionJobSearcher:
    """生产就绪版招聘搜索器"""
    
    def __init__(self, data_dir: str = None):
        """初始化"""
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
        
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # 初始化数据存储
        self.jobs_db = os.path.join(data_dir, 'jobs_database.json')
        self.mock_data_file = os.path.join(data_dir, 'mock_jobs.json')
        
        # 加载数据
        self.jobs = self._load_jobs_database()
        self.mock_data = self._load_mock_data()
        
        # 统计数据
        self.stats = {
            'total_jobs': len(self.jobs),
            'mock_jobs': sum(1 for job in self.jobs if job.source == 'mock'),
            'manual_jobs': sum(1 for job in self.jobs if job.source == 'manual'),
            'api_jobs': sum(1 for job in self.jobs if job.source == 'api'),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _load_jobs_database(self) -> List[ProductionJob]:
        """加载职位数据库"""
        jobs = []
        
        if os.path.exists(self.jobs_db):
            try:
                with open(self.jobs_db, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data:
                    job = ProductionJob(
                        id=item.get('id', ''),
                        platform=item.get('platform', ''),
                        title=item.get('title', ''),
                        company=item.get('company', ''),
                        salary=item.get('salary', ''),
                        location=item.get('location', ''),
                        experience=item.get('experience', ''),
                        education=item.get('education', ''),
                        skills=item.get('skills', []),
                        description=item.get('description', ''),
                        url=item.get('url', ''),
                        source=item.get('source', 'mock'),
                        posted_date=item.get('posted_date', ''),
                        created_at=item.get('created_at', '')
                    )
                    jobs.append(job)
                    
                print(f"[INFO] 从数据库加载 {len(jobs)} 个职位")
                
            except Exception as e:
                print(f"[WARN] 加载数据库失败: {e}")
                jobs = []
        
        return jobs
    
    def _load_mock_data(self) -> Dict:
        """加载模拟数据模板"""
        mock_file = self.mock_data_file
        
        if os.path.exists(mock_file):
            try:
                with open(mock_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # 默认模拟数据
        return {
            "categories": {
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
                            "skills": ["Python", "Django/Flask", "MySQL", "Redis", "Docker", "微服务"],
                            "description": "负责后端系统开发，参与架构设计，优化系统性能"
                        },
                        {
                            "title": "Python数据分析师", 
                            "company": "阿里巴巴",
                            "salary": "20-40K·14薪",
                            "location": "杭州·余杭区",
                            "experience": "2-4年",
                            "education": "本科",
                            "skills": ["Python", "Pandas", "SQL", "统计学", "机器学习"],
                            "description": "负责业务数据分析，构建数据模型，提供数据洞察"
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
                            "skills": ["Java", "Spring", "微服务", "分布式", "高并发"],
                            "description": "负责核心业务系统开发，参与技术架构设计"
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
                            "skills": ["React", "Vue", "TypeScript", "Node.js", "Webpack"],
                            "description": "负责前端架构设计，技术选型，性能优化"
                        }
                    ]
                }
            }
        }
    
    def search(self, keyword: str, city: str = "全国", 
               max_results: int = 20, use_mock: bool = True) -> List[ProductionJob]:
        """
        搜索职位
        
        Args:
            keyword: 搜索关键词
            city: 城市
            max_results: 最大结果数
            use_mock: 是否使用模拟数据（当真实数据不足时）
        
        Returns:
            职位列表
        """
        print(f"\n搜索职位: {keyword} - {city}")
        print("=" * 50)
        
        results = []
        
        # 步骤1: 从数据库搜索
        print("1. 从数据库搜索...")
        db_results = self._search_database(keyword, city, max_results)
        results.extend(db_results)
        print(f"   找到 {len(db_results)} 个数据库记录")
        
        # 步骤2: 如果数据库结果不足，使用模拟数据
        if len(results) < max_results and use_mock:
            print("2. 使用模拟数据补充...")
            mock_needed = max_results - len(results)
            mock_results = self._get_mock_jobs(keyword, city, mock_needed)
            results.extend(mock_results)
            print(f"   添加 {len(mock_results)} 个模拟职位")
        
        # 步骤3: 尝试外部API（预留接口）
        if len(results) < max_results // 2:
            print("3. 尝试外部数据源...")
            # 这里可以添加真实API调用
            # external_results = self._call_external_api(keyword, city, max_results - len(results))
            # results.extend(external_results)
            pass
        
        # 去重并限制数量
        unique_results = self._deduplicate_jobs(results)
        final_results = unique_results[:max_results]
        
        print(f"\n搜索完成: 找到 {len(final_results)} 个职位")
        print(f"  来源: {self._count_sources(final_results)}")
        
        return final_results
    
    def _search_database(self, keyword: str, city: str, max_results: int) -> List[ProductionJob]:
        """从数据库搜索"""
        results = []
        keyword_lower = keyword.lower()
        
        for job in self.jobs:
            # 匹配关键词
            matches = (
                keyword_lower in job.title.lower() or
                keyword_lower in ' '.join(job.skills).lower() or
                keyword_lower in job.description.lower()
            )
            
            # 匹配城市
            city_matches = (city == "全国" or city in job.location)
            
            if matches and city_matches:
                results.append(job)
                if len(results) >= max_results:
                    break
        
        return results
    
    def _get_mock_jobs(self, keyword: str, city: str, count: int) -> List[ProductionJob]:
        """获取模拟职位"""
        results = []
        keyword_lower = keyword.lower()
        
        # 查找匹配的类别
        matched_category = None
        for category_id, category in self.mock_data['categories'].items():
            if keyword_lower in category_id or keyword_lower in category['name'].lower():
                matched_category = category
                break
        
        if not matched_category:
            # 使用第一个类别
            first_category = list(self.mock_data['categories'].values())[0]
            matched_category = first_category
        
        # 创建职位
        for i, template in enumerate(matched_category['jobs'][:count]):
            job_id = f"mock_{keyword}_{city}_{i}_{int(time.time())}"
            
            # 调整地点
            location = city
            if '·' in template['location']:
                location = city + "·" + template['location'].split("·")[-1]
            
            job = ProductionJob(
                id=job_id,
                platform="模拟平台",
                title=template['title'],
                company=template['company'],
                salary=template['salary'],
                location=location,
                experience=template['experience'],
                education=template['education'],
                skills=template['skills'],
                description=template['description'],
                url=f"https://example.com/job/{job_id}",
                source="mock",
                posted_date=datetime.now().strftime('%Y-%m-%d'),
                created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            results.append(job)
        
        return results
    
    def _deduplicate_jobs(self, jobs: List[ProductionJob]) -> List[ProductionJob]:
        """去重职位"""
        seen_titles = set()
        unique_jobs = []
        
        for job in jobs:
            title_key = f"{job.title}_{job.company}"
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def _count_sources(self, jobs: List[ProductionJob]) -> str:
        """统计来源"""
        counts = {'mock': 0, 'manual': 0, 'api': 0}
        for job in jobs:
            if job.source in counts:
                counts[job.source] += 1
        
        parts = []
        if counts['manual'] > 0:
            parts.append(f"{counts['manual']}手动")
        if counts['api'] > 0:
            parts.append(f"{counts['api']}API")
        if counts['mock'] > 0:
            parts.append(f"{counts['mock']}模拟")
        
        return ' + '.join(parts) if parts else "无"
    
    def add_manual_job(self, job_data: Dict) -> str:
        """手动添加职位到数据库"""
        job_id = f"manual_{int(time.time())}_{random.randint(1000, 9999)}"
        
        job = ProductionJob(
            id=job_id,
            platform=job_data.get('platform', '手动添加'),
            title=job_data.get('title', ''),
            company=job_data.get('company', ''),
            salary=job_data.get('salary', '面议'),
            location=job_data.get('location', ''),
            experience=job_data.get('experience', '经验不限'),
            education=job_data.get('education', '学历不限'),
            skills=job_data.get('skills', []),
            description=job_data.get('description', ''),
            url=job_data.get('url', ''),
            source='manual',
            posted_date=job_data.get('posted_date', datetime.now().strftime('%Y-%m-%d')),
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        self.jobs.append(job)
        self._save_database()
        
        print(f"[INFO] 手动添加职位: {job.title}")
        return job_id
    
    def _save_database(self):
        """保存数据库"""
        try:
            data = [job.to_dict() for job in self.jobs]
            with open(self.jobs_db, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 更新统计
            self.stats['total_jobs'] = len(self.jobs)
            self.stats['mock_jobs'] = sum(1 for job in self.jobs if job.source == 'mock')
            self.stats['manual_jobs'] = sum(1 for job in self.jobs if job.source == 'manual')
            self.stats['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
        except Exception as e:
            print(f"[ERROR] 保存数据库失败: {e}")
    
    def format_results(self, jobs: List[ProductionJob], show_details: bool = True) -> str:
        """格式化输出结果"""
        if not jobs:
            return "未找到相关职位"
        
        output = "=" * 80 + "\n"
        output += "招聘职位搜索结果\n"
        output += f"搜索时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        output += f"找到职位: {len(jobs)} 个\n"
        output += "=" * 80 + "\n\n"
        
        for i, job in enumerate(jobs, 1):
            source_mark = {
                'mock': '[M]',
                'manual': '[H]',
                'api': '[A]'
            }.get(job.source, '[?]')
            
            output += f"{source_mark} {i}. {job.title}\n"
            output += f"   公司: {job.company} | 薪资: {job.salary}\n"
            output += f"   地点: {job.location} | 要求: {job.experience} | {job.education}\n"
            
            if show_details:
                if job.skills:
                    output += f"   技能: {', '.join(job.skills[:4])}\n"
                if job.description:
                    desc = job.description[:80] + '...' if len(job.description) > 80 else job.description
                    output += f"   描述: {desc}\n"
            
            output += "\n"
        
        output += "=" * 80 + "\n"
        output += "图例: [M]=模拟数据 [H]=手动添加 [A]=API数据\n"
        output += "提示: 使用 add_manual_job() 添加真实职位到数据库\n"
        output += "=" * 80
        
        return output
    
    def export_results(self, jobs: List[ProductionJob], format: str = 'json') -> str:
        """导出结果"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            filename = f"jobs_export_{timestamp}.json"
            data = [job.to_dict() for job in jobs]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        elif format == 'csv':
            filename = f"jobs_export_{timestamp}.csv"
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', '平台', '职位', '公司', '薪资', '地点', '经验', '学历', 
                               '技能', '描述', '链接', '来源', '发布日期', '创建时间'])
                for job in jobs:
                    writer.writerow(job.to_csv_row())
        
        else:
            return f"不支持的格式: {format}"
        
        print(f"[INFO] 结果已导出到: {filename}")
        return filename
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats


def main():
    """主函数"""
    print("生产就绪版招聘搜索技能")
    print("=" * 60)
    print("特点: 高质量模拟数据 + 可扩展的真实数据接口")
    print("=" * 60)
    
    # 创建搜索器
    searcher = ProductionJobSearcher()
    
    import sys
    
    if len(sys.argv) > 1:
        # 命令行模式
        keyword = sys.argv[1]
        city = sys.argv[2] if len(sys.argv) > 2 else "全国"
        max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 15
    else:
        # 交互模式
        print("\n请输入搜索参数:")
        keyword = input("关键词 (默认: Python): ").strip() or "Python"
        city = input("城市 (默认: 全国): ").strip() or "全国"
        max_results = 15
    
    # 执行搜索
    results = searcher.search(keyword, city, max_results)
    
    # 输出结果
    output = searcher.format_results(results)
    print(output)
    
    # 导出结果
    json_file = searcher.export_results(results, 'json')
    csv_file = searcher.export_results(results, 'csv')
    
    # 显示统计
    stats = searcher.get_stats()
    print(f"\n数据库统计:")
    print(f"  总职位数: {stats['total_jobs']}")
    print(f"  模拟职位: {stats['mock_jobs']}")
    print(f"  手动添加: {stats['manual_jobs']}")
    print(f"  API职位: {stats['api_jobs']}")
    print(f"  最后更新: {stats['last_updated']}")
    
    print(f"\n搜索完成!")
    print(f"  JSON文件: {json_file}")
    print(f"  CSV文件: {csv_file}")
    print(f"\n提示: 可以导入Excel进行进一步分析")


if __name__ == '__main__':
    main()