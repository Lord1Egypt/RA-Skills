#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版招聘搜索器
基于压力测试结果的改进版本
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
from functools import lru_cache

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class OptimizedJob:
    """优化版职位信息"""
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
    search_score: float = 0.0  # 搜索匹配分数
    quality_score: float = 0.0  # 职位质量分数
    
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
            f"{self.search_score:.2f}",
            f"{self.quality_score:.2f}",
            self.posted_date,
            self.created_at
        ]


class OptimizedJobSearcher:
    """优化版招聘搜索器"""
    
    def __init__(self, data_dir: str = None):
        """初始化"""
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
        
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # 文件路径
        self.jobs_db = os.path.join(data_dir, 'jobs_database.json')
        self.mock_data_file = os.path.join(data_dir, 'mock_jobs.json')
        self.cache_file = os.path.join(data_dir, 'search_cache.json')
        
        # 加载数据
        self.jobs = self._load_jobs_database()
        self.mock_data = self._load_mock_data()
        
        # 初始化缓存
        self.search_cache = {}
        self._load_cache()
        
        # 性能统计
        self.stats = {
            'total_searches': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'avg_search_time': 0.0,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _load_jobs_database(self) -> List[OptimizedJob]:
        """加载职位数据库"""
        jobs = []
        
        if os.path.exists(self.jobs_db):
            try:
                with open(self.jobs_db, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data:
                    job = OptimizedJob(
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
                        search_score=item.get('search_score', 0.0),
                        quality_score=item.get('quality_score', 0.0)
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
    
    def _load_cache(self):
        """加载搜索缓存"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.search_cache = json.load(f)
                print(f"[INFO] 加载缓存: {len(self.search_cache)} 条记录")
            except Exception:
                self.search_cache = {}
    
    def _save_cache(self):
        """保存搜索缓存"""
        try:
            # 限制缓存大小
            if len(self.search_cache) > 100:
                # 保留最近100条
                items = list(self.search_cache.items())
                items.sort(key=lambda x: x[1].get('timestamp', 0), reverse=True)
                self.search_cache = dict(items[:100])
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.search_cache, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"[WARN] 保存缓存失败: {e}")
    
    def _get_cache_key(self, keyword: str, city: str, max_results: int, 
                      min_salary: int = 0, experience: str = "") -> str:
        """生成缓存键"""
        key_parts = [
            keyword.lower(),
            city,
            str(max_results),
            str(min_salary),
            experience
        ]
        return '_'.join(key_parts)
    
    @lru_cache(maxsize=50)
    def _cached_search(self, cache_key: str) -> Optional[List[Dict]]:
        """缓存搜索（使用LRU缓存）"""
        if cache_key in self.search_cache:
            cache_data = self.search_cache[cache_key]
            # 检查缓存是否过期（1小时）
            if time.time() - cache_data.get('timestamp', 0) < 3600:
                self.stats['cache_hits'] += 1
                return cache_data.get('results', [])
        
        self.stats['cache_misses'] += 1
        return None
    
    def search(self, keyword: str, city: str = "全国", 
               max_results: int = 20, min_salary: int = 0,
               experience: str = "", use_cache: bool = True) -> List[OptimizedJob]:
        """
        优化搜索
        
        Args:
            keyword: 搜索关键词
            city: 城市
            max_results: 最大结果数
            min_salary: 最低薪资要求
            experience: 经验要求
            use_cache: 是否使用缓存
        
        Returns:
            优化版职位列表
        """
        start_time = time.time()
        self.stats['total_searches'] += 1
        
        # 检查缓存
        cache_key = self._get_cache_key(keyword, city, max_results, min_salary, experience)
        
        if use_cache:
            cached_results = self._cached_search(cache_key)
            if cached_results is not None:
                # 从缓存恢复职位对象
                jobs = []
                for item in cached_results:
                    job = OptimizedJob(
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
                        search_score=item.get('search_score', 0.0),
                        quality_score=item.get('quality_score', 0.0)
                    )
                    jobs.append(job)
                
                end_time = time.time()
                search_time = end_time - start_time
                
                # 更新平均搜索时间
                prev_avg = self.stats['avg_search_time']
                total_searches = self.stats['total_searches']
                self.stats['avg_search_time'] = (prev_avg * (total_searches - 1) + search_time) / total_searches
                
                print(f"[CACHE HIT] 搜索: {keyword} - {city}, 时间: {search_time:.3f}秒")
                return jobs[:max_results]
        
        print(f"\n优化搜索: {keyword} - {city}")
        if min_salary > 0:
            print(f"最低薪资: {min_salary}K")
        if experience:
            print(f"经验要求: {experience}")
        print("=" * 50)
        
        results = []
        
        # 步骤1: 从数据库搜索（优化查询）
        print("1. 优化数据库搜索...")
        db_results = self._optimized_database_search(keyword, city, max_results * 2)
        results.extend(db_results)
        print(f"   找到 {len(db_results)} 个数据库记录")
        
        # 步骤2: 使用模拟数据补充
        if len(results) < max_results:
            print("2. 使用优化模拟数据...")
            mock_needed = max_results - len(results)
            mock_results = self._get_optimized_mock_jobs(keyword, city, mock_needed)
            results.extend(mock_results)
            print(f"   添加 {len(mock_results)} 个优化模拟职位")
        
        # 步骤3: 应用筛选条件
        print("3. 智能筛选...")
        filtered_results = self._smart_filter(results, min_salary, experience)
        
        # 步骤4: 计算分数并排序
        print("4. 计算综合分数...")
        scored_results = self._calculate_scores(filtered_results, keyword, city)
        
        # 步骤5: 去重并限制数量
        final_results = self._deduplicate_and_limit(scored_results, max_results)
        
        # 保存到缓存
        cache_data = {
            'results': [job.to_dict() for job in final_results],
            'timestamp': time.time(),
            'count': len(final_results)
        }
        self.search_cache[cache_key] = cache_data
        self._save_cache()
        
        end_time = time.time()
        search_time = end_time - start_time
        
        # 更新统计
        prev_avg = self.stats['avg_search_time']
        total_searches = self.stats['total_searches']
        self.stats['avg_search_time'] = (prev_avg * (total_searches - 1) + search_time) / total_searches
        
        print(f"\n搜索完成: 找到 {len(final_results)} 个职位")
        print(f"  搜索时间: {search_time:.3f}秒")
        print(f"  缓存命中: {self.stats['cache_hits']}, 未命中: {self.stats['cache_misses']}")
        
        return final_results
    
    def _optimized_database_search(self, keyword: str, city: str, max_results: int) -> List[OptimizedJob]:
        """优化数据库搜索"""
        results = []
        keyword_lower = keyword.lower()
        
        # 预计算关键词分词（简单实现）
        keywords = keyword_lower.split()
        if not keywords:
            keywords = [keyword_lower]
        
        for job in self.jobs:
            # 快速预筛选
            if city != "全国" and city not in job.location:
                continue
            
            # 多关键词匹配
            match_score = 0
            job_text = f"{job.title} {' '.join(job.skills)} {job.description}".lower()
            
            for kw in keywords:
                if kw in job_text:
                    match_score += 1
            
            if match_score > 0:
                job.search_score = match_score / len(keywords)
                results.append(job)
                if len(results) >= max_results:
                    break
        
        return results
    
    def _get_optimized_mock_jobs(self, keyword: str, city: str, count: int) -> List[OptimizedJob]:
        """获取优化版模拟职位"""
        results = []
        keyword_lower = keyword.lower()
        
        # 查找匹配的类别
        matched_categories = []
        for category_id, category in self.mock_data.get('categories', {}).items():
            category_name_lower = category['name'].lower()
            
            # 计算类别匹配度
            category_score = 0
            if keyword_lower in category_id:
                category_score += 2
            if keyword_lower in category_name_lower:
                category_score += 1
            
            if category_score > 0:
                matched_categories.append((category, category_score))
        
        # 按匹配度排序
        matched_categories.sort(key=lambda x: x[1], reverse=True)
        
        # 从高匹配度类别中选择职位
        selected_templates = []
        for category, score in matched_categories:
            if len(selected_templates) >= count:
                break
            
            for job_template in category['jobs']:
                if len(selected_templates) >= count:
                    break
                
                # 计算职位匹配度
                template_text = f"{job_template['title']} {' '.join(job_template['skills'])}".lower()
                if keyword_lower in template_text:
                    selected_templates.append((job_template, category['name'], score))
        
        # 如果还不够，从所有类别随机选择
        if len(selected_templates) < count:
            all_templates = []
            for category in self.mock_data.get('categories', {}).values():
                for job_template in category['jobs']:
                    all_templates.append((job_template, category['name'], 0))
            
            while len(selected_templates) < count and all_templates:
                template = random.choice(all_templates)
                if template not in selected_templates:
                    selected_templates.append(template)
        
        # 创建职位
        for i, (template, category_name, category_score) in enumerate(selected_templates):
            job_id = f"optimized_mock_{keyword}_{city}_{i}_{int(time.time())}"
            
            # 调整薪资
            salary = self._optimize_salary(template['salary'], city)
            
            # 调整地点
            location = self._optimize_location(template['location'], city)
            
            # 计算质量分数
            quality_score = self._calculate_quality_score(template)
            
            job = OptimizedJob(
                id=job_id,
                platform="优化模拟平台",
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
                posted_date=datetime.now().strftime('%Y-%m-%d'),
                created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                quality_score=quality_score
            )
            results.append(job)
        
        return results
    
    def _optimize_salary(self, base_salary: str, city: str) -> str:
        """优化薪资计算"""
        # 这里可以添加更复杂的薪资调整逻辑
        return base_salary
    
    def _optimize_location(self, base_location: str, target_city: str) -> str:
        """优化地点"""
        if '·' in base_location:
            area = base_location.split('·')[-1]
            return f"{target_city}·{area}"
        return target_city
    
    def _calculate_quality_score(self, job_template: Dict) -> float:
        """计算职位质量分数"""
        score = 0.0
        
        # 基于薪资
        salary = job_template['salary']
        if 'K' in salary:
            try:
                import re
                numbers = re.findall(r'\d+', salary)
                if numbers:
                    max_salary = max(map(int, numbers))
                    if max_salary >= 30:
                        score += 0.3
                    elif max_salary >= 20:
                        score += 0.2
                    else:
                        score += 0.1
            except:
                pass
        
        # 基于经验要求
        experience = job_template['experience']
        if '3-5' in experience or '3年' in experience or '5年' in experience:
            score += 0.2  # 适中经验要求
        
        # 基于技能数量
        skills_count = len(job_template['skills'])
        if skills_count >= 5:
            score += 0.3
        elif skills_count >= 3:
            score += 0.2
        else:
            score += 0.1
        
        # 基于公司知名度（简单判断）
        company = job_template['company']
        famous_companies = ['字节跳动', '阿里巴巴', '腾讯', '百度', '华为', '美团', '京东']
        if company in famous_companies:
            score += 0.2
        
        return min(score, 1.0)
    
    def _smart_filter(self, jobs: List[OptimizedJob], min_salary: int, experience: str) -> List[OptimizedJob]:
        """智能筛选"""
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
    
    def _calculate_scores(self, jobs: List[OptimizedJob], keyword: str, city: str) -> List[OptimizedJob]:
        """计算综合分数"""
        keyword_lower = keyword.lower()
        
        for job in jobs:
            search_score = 0.0
            
            # 搜索匹配分数
            if keyword_lower in job.title.lower():
                search_score += 0.4
            
            skill_match_count = sum(1 for skill in job.skills if keyword_lower in skill.lower())
            if skill_match_count > 0:
                search_score += 0.3 * min(skill_match_count / 3, 1.0)
            
            if keyword_lower in job.description.lower():
                search_score += 0.2
            
            if city != "全国" and city in job.location:
                search_score += 0.1
            
            job.search_score = min(search_score, 1.0)
            
            # 如果没有质量分数，计算一个
            if job.quality_score == 0.0:
                job.quality_score = self._calculate_quality_score({
                    'salary': job.salary,
                    'experience': job.experience,
                    'skills': job.skills,
                    'company': job.company
                })
        
        # 按综合分数排序（搜索分数70% + 质量分数30%）
        jobs.sort(key=lambda x: x.search_score * 0.7 + x.quality_score * 0.3, reverse=True)
        
        return jobs
    
    def _deduplicate_and_limit(self, jobs: List[OptimizedJob], max_results: int) -> List[OptimizedJob]:
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
    
    def format_results(self, jobs: List[OptimizedJob], show_details: bool = True) -> str:
        """格式化输出结果"""
        if not jobs:
            return "未找到相关职位"
        
        output = "=" * 80 + "\n"
        output += "优化版招聘职位搜索结果\n"
        output += f"搜索时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        output += f"找到职位: {len(jobs)} 个\n"
        output += "=" * 80 + "\n\n"
        
        for i, job in enumerate(jobs, 1):
            source_mark = {
                'mock': '[M]',
                'manual': '[H]',
                'api': '[A]'
            }.get(job.source, '[?]')
            
            total_score = job.search_score * 0.7 + job.quality_score * 0.3
            score_str = f"(搜索:{job.search_score:.2f}/质量:{job.quality_score:.2f}/综合:{total_score:.2f})"
            
            output += f"{source_mark} {i}. {score_str} {job.title}\n"
            output += f"   公司: {job.company} | 薪资: {job.salary}\n"
            output += f"   地点: {job.location} | 要求: {job.experience} | {job.education}\n"
            
            if show_details:
                if job.skills:
                    output += f"   技能: {', '.join(job.skills[:4])}\n"
                if job.description:
                    desc = job.description[:80] + '...' if len(job.description) > 80 else job.description
                    output += f"   描述: {desc}\n"
            
            output += "\n"
        
        # 统计信息
        avg_search_score = sum(job.search_score for job in jobs) / len(jobs)
        avg_quality_score = sum(job.quality_score for job in jobs) / len(jobs)
        
        output += "=" * 80 + "\n"
        output += f"统计: 平均搜索分数 {avg_search_score:.2f} | 平均质量分数 {avg_quality_score:.2f}\n"
        output += f"性能: 平均搜索时间 {self.stats['avg_search_time']:.3f}秒 | 缓存命中率 {self.stats['cache_hits']/(self.stats['cache_hits']+self.stats['cache_misses'])*100:.1f}%\n"
        output += "图例: [M]=模拟数据 [H]=手动添加 [A]=API数据\n"
        output += "=" * 80
        
        return output
    
    def export_results(self, jobs: List[OptimizedJob], format: str = 'json') -> str:
        """导出结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == 'json':
            filename = f"optimized_jobs_export_{timestamp}.json"
            data = [job.to_dict() for job in jobs]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        elif format == 'csv':
            filename = f"optimized_jobs_export_{timestamp}.csv"
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', '平台', '职位', '公司', '薪资', '地点', '经验', '学历', 
                               '技能', '描述', '链接', '来源', '搜索分数', '质量分数', '发布日期', '创建时间'])
                for job in jobs:
                    writer.writerow(job.to_csv_row())
        
        else:
            return f"不支持的格式: {format}"
        
        print(f"[INFO] 结果已导出到: {filename}")
        return filename
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats
    
    def clear_cache(self):
        """清空缓存"""
        self.search_cache = {}
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        print("[INFO] 缓存已清空")


def main():
    """主函数"""
    print("优化版招聘搜索器")
    print("=" * 60)
    print("特点: 智能缓存 + 综合评分 + 性能优化")
    print("=" * 60)
    
    import sys
    
    # 创建搜索器
    searcher = OptimizedJobSearcher()
    
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
    print(f"\n系统统计:")
    print(f"  总搜索次数: {stats['total_searches']}")
    print(f"  缓存命中: {stats['cache_hits']}")
    print(f"  缓存未命中: {stats['cache_misses']}")
    print(f"  平均搜索时间: {stats['avg_search_time']:.3f}秒")
    
    print(f"\n搜索完成!")
    print(f"  JSON文件: {json_file}")
    print(f"  CSV文件: {csv_file}")
    print(f"\n提示: 使用 clear_cache() 方法清空缓存")


if __name__ == '__main__':
    main()
