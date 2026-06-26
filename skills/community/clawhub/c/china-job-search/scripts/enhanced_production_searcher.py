#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版生产就绪招聘搜索器
使用增强的模拟数据和技能数据库
"""

import sys
import os
import json
import time
import random
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import csv

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class EnhancedJob:
    """增强版职位信息"""
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
    category: str = ""
    match_score: float = 0.0  # 匹配分数
    
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
            self.category,
            f"{self.match_score:.2f}",
            self.posted_date,
            self.created_at
        ]


class EnhancedProductionSearcher:
    """增强版生产就绪招聘搜索器"""
    
    def __init__(self, data_dir: str = None):
        """初始化"""
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
        
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # 文件路径
        self.jobs_db = os.path.join(data_dir, 'jobs_database.json')
        self.mock_data_file = os.path.join(data_dir, 'mock_jobs.json')
        self.city_data_file = os.path.join(data_dir, 'city_salary_data.json')
        self.skill_db_file = os.path.join(data_dir, 'skill_database.json')
        
        # 加载数据
        self.jobs = self._load_jobs_database()
        self.mock_data = self._load_mock_data()
        self.city_data = self._load_city_data()
        self.skill_data = self._load_skill_data()
        
        # 统计数据
        self.stats = {
            'total_jobs': len(self.jobs),
            'mock_jobs': sum(1 for job in self.jobs if job.source == 'mock'),
            'manual_jobs': sum(1 for job in self.jobs if job.source == 'manual'),
            'api_jobs': sum(1 for job in self.jobs if job.source == 'api'),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'mock_categories': len(self.mock_data.get('categories', {})),
            'total_mock_jobs': sum(len(cat['jobs']) for cat in self.mock_data.get('categories', {}).values()),
            'skill_categories': len(self.skill_data.get('categories', {})),
            'total_skills': self.skill_data.get('total_skills', 0)
        }
    
    def _load_jobs_database(self) -> List[EnhancedJob]:
        """加载职位数据库"""
        jobs = []
        
        if os.path.exists(self.jobs_db):
            try:
                with open(self.jobs_db, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data:
                    job = EnhancedJob(
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
                        created_at=item.get('created_at', ''),
                        category=item.get('category', ''),
                        match_score=item.get('match_score', 0.0)
                    )
                    jobs.append(job)
                    
                print(f"[INFO] 从数据库加载 {len(jobs)} 个职位")
                
            except Exception as e:
                print(f"[WARN] 加载数据库失败: {e}")
                jobs = []
        
        return jobs
    
    def _load_mock_data(self) -> Dict:
        """加载模拟数据"""
        if os.path.exists(self.mock_data_file):
            try:
                with open(self.mock_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARN] 加载模拟数据失败: {e}")
        
        return {"categories": {}}
    
    def _load_city_data(self) -> Dict:
        """加载城市数据"""
        if os.path.exists(self.city_data_file):
            try:
                with open(self.city_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARN] 加载城市数据失败: {e}")
        
        return {"factors": {}, "base_city": "北京"}
    
    def _load_skill_data(self) -> Dict:
        """加载技能数据"""
        if os.path.exists(self.skill_db_file):
            try:
                with open(self.skill_db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARN] 加载技能数据失败: {e}")
        
        return {"categories": {}, "total_skills": 0}
    
    def search(self, keyword: str, city: str = "全国", 
               max_results: int = 20, use_mock: bool = True,
               min_salary: int = 0, experience: str = "") -> List[EnhancedJob]:
        """
        增强搜索
        
        Args:
            keyword: 搜索关键词
            city: 城市
            max_results: 最大结果数
            use_mock: 是否使用模拟数据
            min_salary: 最低薪资要求（K）
            experience: 经验要求
        
        Returns:
            增强版职位列表
        """
        print(f"\n增强搜索: {keyword} - {city}")
        if min_salary > 0:
            print(f"最低薪资: {min_salary}K")
        if experience:
            print(f"经验要求: {experience}")
        print("=" * 50)
        
        results = []
        
        # 步骤1: 从数据库搜索
        print("1. 从数据库搜索...")
        db_results = self._search_database(keyword, city, max_results * 2)
        results.extend(db_results)
        print(f"   找到 {len(db_results)} 个数据库记录")
        
        # 步骤2: 使用模拟数据补充
        if len(results) < max_results and use_mock:
            print("2. 使用增强模拟数据补充...")
            mock_needed = max_results - len(results)
            mock_results = self._get_enhanced_mock_jobs(keyword, city, mock_needed)
            results.extend(mock_results)
            print(f"   添加 {len(mock_results)} 个增强模拟职位")
        
        # 步骤3: 应用筛选条件
        print("3. 应用筛选条件...")
        filtered_results = self._apply_filters(results, min_salary, experience)
        
        # 步骤4: 计算匹配分数并排序
        print("4. 计算匹配分数...")
        scored_results = self._calculate_match_scores(filtered_results, keyword, city)
        
        # 步骤5: 去重并限制数量
        final_results = self._deduplicate_and_limit(scored_results, max_results)
        
        print(f"\n搜索完成: 找到 {len(final_results)} 个职位")
        print(f"  来源: {self._count_sources(final_results)}")
        print(f"  平均匹配分数: {self._average_match_score(final_results):.2f}")
        
        return final_results
    
    def _search_database(self, keyword: str, city: str, max_results: int) -> List[EnhancedJob]:
        """从数据库搜索"""
        results = []
        keyword_lower = keyword.lower()
        
        for job in self.jobs:
            # 匹配关键词
            matches = (
                keyword_lower in job.title.lower() or
                keyword_lower in ' '.join(job.skills).lower() or
                keyword_lower in job.description.lower() or
                keyword_lower in job.category.lower()
            )
            
            # 匹配城市
            city_matches = (city == "全国" or city in job.location)
            
            if matches and city_matches:
                results.append(job)
                if len(results) >= max_results:
                    break
        
        return results
    
    def _get_enhanced_mock_jobs(self, keyword: str, city: str, count: int) -> List[EnhancedJob]:
        """获取增强版模拟职位"""
        results = []
        keyword_lower = keyword.lower()
        
        # 查找匹配的类别
        matched_categories = []
        for category_id, category in self.mock_data.get('categories', {}).items():
            category_name_lower = category['name'].lower()
            
            # 检查关键词是否匹配类别
            if (keyword_lower in category_id or 
                keyword_lower in category_name_lower or
                any(keyword_lower in skill.lower() for skill in category.get('common_skills', []))):
                matched_categories.append(category)
        
        # 如果没有匹配的类别，使用所有类别
        if not matched_categories:
            matched_categories = list(self.mock_data.get('categories', {}).values())
        
        # 从匹配的类别中随机选择职位
        all_job_templates = []
        for category in matched_categories:
            for job_template in category['jobs']:
                all_job_templates.append((job_template, category['name']))
        
        # 随机选择但确保多样性
        selected_templates = []
        if all_job_templates:
            # 先尝试选择与关键词更相关的
            for template, category_name in all_job_templates:
                if len(selected_templates) >= count:
                    break
                
                # 检查模板是否包含关键词
                template_text = f"{template['title']} {template['description']} {' '.join(template['skills'])}".lower()
                if keyword_lower in template_text:
                    selected_templates.append((template, category_name))
            
            # 如果还不够，随机选择
            while len(selected_templates) < count and all_job_templates:
                template, category_name = random.choice(all_job_templates)
                if (template, category_name) not in selected_templates:
                    selected_templates.append((template, category_name))
        
        # 创建职位
        for i, (template, category_name) in enumerate(selected_templates):
            job_id = f"enhanced_mock_{keyword}_{city}_{i}_{int(time.time())}"
            
            # 调整薪资基于城市
            salary = self._adjust_salary_for_city(template['salary'], city)
            
            # 调整地点
            location = self._adjust_location(template['location'], city)
            
            job = EnhancedJob(
                id=job_id,
                platform="增强模拟平台",
                title=template['title'],
                company=template['company'],
                salary=salary,
                location=location,
                experience=template['experience'],
                education=template['education'],
                skills=template['skills'],
                description=template['description'],
                url=f"https://example.com/job/{job_id}",
                source="mock",
                category=category_name,
                posted_date=datetime.now().strftime('%Y-%m-%d'),
                created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            results.append(job)
        
        return results
    
    def _adjust_salary_for_city(self, base_salary: str, city: str) -> str:
        """根据城市调整薪资"""
        try:
            # 提取基础薪资数字
            import re
            numbers = re.findall(r'\d+', base_salary)
            
            if numbers and city in self.city_data.get('factors', {}):
                factor = self.city_data['factors'][city]
                base_city_factor = self.city_data['factors'].get(self.city_data.get('base_city', '北京'), 1.0)
                
                # 调整薪资
                adjusted_numbers = []
                for num in numbers:
                    adjusted = int(int(num) * factor / base_city_factor)
                    adjusted_numbers.append(str(adjusted))
                
                # 替换原数字
                parts = re.split(r'(\d+)', base_salary)
                result = []
                num_index = 0
                
                for part in parts:
                    if part.isdigit() and num_index < len(adjusted_numbers):
                        result.append(adjusted_numbers[num_index])
                        num_index += 1
                    else:
                        result.append(part)
                
                return ''.join(result)
            
        except Exception:
            pass
        
        return base_salary
    
    def _adjust_location(self, base_location: str, target_city: str) -> str:
        """调整地点"""
        if '·' in base_location:
            # 保留区域信息，替换城市
            area = base_location.split('·')[-1]
            return f"{target_city}·{area}"
        else:
            return target_city
    
    def _apply_filters(self, jobs: List[EnhancedJob], min_salary: int, experience: str) -> List[EnhancedJob]:
        """应用筛选条件"""
        filtered = []
        
        for job in jobs:
            # 薪资筛选
            if min_salary > 0:
                try:
                    import re
                    numbers = re.findall(r'\d+', job.salary)
                    if numbers:
                        max_salary = max(map(int, numbers))
                        if max_salary < min_salary:
                            continue
                except:
                    pass
            
            # 经验筛选
            if experience:
                # 简单经验匹配
                exp_map = {
                    '应届生': ['应届', '无经验', '经验不限'],
                    '1-3年': ['1年', '2年', '3年', '1-3'],
                    '3-5年': ['3年', '4年', '5年', '3-5'],
                    '5年以上': ['5年', '6年', '7年', '8年', '5-8', '5+', '资深', '高级']
                }
                
                if experience in exp_map:
                    exp_keywords = exp_map[experience]
                    if not any(exp in job.experience for exp in exp_keywords):
                        continue
            
            filtered.append(job)
        
        return filtered
    
    def _calculate_match_scores(self, jobs: List[EnhancedJob], keyword: str, city: str) -> List[EnhancedJob]:
        """计算匹配分数"""
        keyword_lower = keyword.lower()
        
        for job in jobs:
            score = 0.0
            
            # 标题匹配（最高权重）
            if keyword_lower in job.title.lower():
                score += 0.4
            
            # 技能匹配
            skill_match_count = sum(1 for skill in job.skills if keyword_lower in skill.lower())
            if skill_match_count > 0:
                score += 0.3 * min(skill_match_count / 3, 1.0)
            
            # 描述匹配
            if keyword_lower in job.description.lower():
                score += 0.2
            
            # 类别匹配
            if keyword_lower in job.category.lower():
                score += 0.1
            
            # 城市匹配（如果指定了具体城市）
            if city != "全国" and city in job.location:
                score += 0.1
            
            job.match_score = min(score, 1.0)
        
        # 按匹配分数排序
        jobs.sort(key=lambda x: x.match_score, reverse=True)
        
        return jobs
    
    def _deduplicate_and_limit(self, jobs: List[EnhancedJob], max_results: int) -> List[EnhancedJob]:
        """去重并限制数量"""
        seen = set()
        unique = []
        
        for job in jobs:
            key = (job.title, job.company, job.location)
            if key not in seen:
                seen.add(key)
                unique.append(job)
                if len(unique) >= max_results:
                    break
        
        return unique
    
    def _count_sources(self, jobs: List[EnhancedJob]) -> str:
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
    
    def _average_match_score(self, jobs: List[EnhancedJob]) -> float:
        """计算平均匹配分数"""
        if not jobs:
            return 0.0
        return sum(job.match_score for job in jobs) / len(jobs)
    
    def format_results(self, jobs: List[EnhancedJob], show_details: bool = True) -> str:
        """格式化输出结果"""
        if not jobs:
            return "未找到相关职位"
        
        output = "=" * 80 + "\n"
        output += "增强版招聘职位搜索结果\n"
        output += f"搜索时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        output += f"找到职位: {len(jobs)} 个\n"
        output += "=" * 80 + "\n\n"
        
        for i, job in enumerate(jobs, 1):
            source_mark = {
                'mock': '[M]',
                'manual': '[H]',
                'api': '[A]'
            }.get(job.source, '[?]')
            
            score_str = f"({job.match_score:.2f})" if job.match_score > 0 else ""
            
            output += f"{source_mark} {i}. {score_str} {job.title}\n"
            output += f"   公司: {job.company} | 薪资: {job.salary} | 类别: {job.category}\n"
            output += f"   地点: {job.location} | 要求: {job.experience} | {job.education}\n"
            
            if show_details:
                if job.skills:
                    output += f"   技能: {', '.join(job.skills[:4])}\n"
                if job.description:
                    desc = job.description[:80] + '...' if len(job.description) > 80 else job.description
                    output += f"   描述: {desc}\n"
            
            output += "\n"
        
        # 统计信息
        avg_score = self._average_match_score(jobs)
        source_counts = self._count_sources(jobs)
        
        output += "=" * 80 + "\n"
        output += f"统计: 平均匹配分数 {avg_score:.2f} | 来源: {source_counts}\n"
        output += "图例: [M]=模拟数据 [H]=手动添加 [A]=API数据 (分数)=匹配度\n"
        output += "=" * 80
        
        return output
    
    def export_results(self, jobs: List[EnhancedJob], format: str = 'json') -> str:
        """导出结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == 'json':
            filename = f"enhanced_jobs_export_{timestamp}.json"
            data = [job.to_dict() for job in jobs]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        elif format == 'csv':
            filename = f"enhanced_jobs_export_{timestamp}.csv"
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', '平台', '职位', '公司', '薪资', '地点', '经验', '学历', 
                               '技能', '描述', '链接', '来源', '类别', '匹配分数', '发布日期', '创建时间'])
                for job in jobs:
                    writer.writerow(job.to_csv_row())
        
        else:
            return f"不支持的格式: {format}"
        
        print(f"[INFO] 结果已导出到: {filename}")
        return filename
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats
    
    def add_manual_job(self, job_data: Dict) -> str:
        """手动添加职位到数据库"""
        job_id = f"manual_{int(time.time())}_{random.randint(1000, 9999)}"
        
        # 计算匹配分数
        match_score = 0.0
        if 'title' in job_data:
            # 简单计算，可以根据需要增强
            match_score = random.uniform(0.5, 0.9)
        
        job = EnhancedJob(
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
            category=job_data.get('category', ''),
            match_score=match_score,
            posted_date=job_data.get('posted_date', datetime.now().strftime('%Y-%m-%d')),
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        self.jobs.append(job)
        self._save_database()
        
        print(f"[INFO] 手动添加职位: {job.title} (匹配分数: {match_score:.2f})")
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


def main():
    """主函数"""
    print("增强版生产就绪招聘搜索器")
    print("=" * 60)
    print("特点: 增强模拟数据 + 技能匹配 + 城市薪资调整")
    print("=" * 60)
    
    import sys
    
    # 创建搜索器
    searcher = EnhancedProductionSearcher()
    
    # 处理命令行参数
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
        city = sys.argv[2] if len(sys.argv) > 2 else "全国"
        max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 15
        min_salary = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    else:
        # 交互模式
        print("\n请输入搜索参数:")
        keyword = input("关键词 (默认: Python): ").strip() or "Python"
        city = input("城市 (默认: 全国): ").strip() or "全国"
        max_results = 15
        min_salary = 0
    
    # 执行搜索
    results = searcher.search(keyword, city, max_results, min_salary=min_salary)
    
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
    print(f"\n提示: CSV文件可以导入Excel进行高级分析")


if __name__ == '__main__':
    main()