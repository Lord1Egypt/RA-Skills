#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实用版招聘搜索技能
结合多种策略确保可用性
"""

import sys
import os
import json
import time
import random
from typing import List, Dict, Optional
from dataclasses import dataclass
from urllib.parse import quote, urljoin

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import requests
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent
except ImportError:
    print("请安装依赖: pip install requests beautifulsoup4 fake-useragent")
    sys.exit(1)


@dataclass
class PracticalJob:
    """实用版岗位信息"""
    platform: str
    title: str
    company: str
    salary: str
    location: str
    experience: str
    education: str
    skills: List[str]
    url: str
    source: str = "real"  # real: 真实数据, mock: 模拟数据, fallback: 备用数据


class PracticalJobSearcher:
    """实用版招聘搜索器 - 混合策略确保可用性"""
    
    def __init__(self, config_path: str = None):
        """初始化"""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.ua = UserAgent()
        self.session = requests.Session()
        self._setup_session()
        
        # 加载模拟数据
        self.mock_data = self._load_mock_data()
    
    def _setup_session(self):
        """设置会话参数"""
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.google.com/',
            'Cache-Control': 'max-age=0',
        })
    
    def _load_mock_data(self) -> Dict:
        """加载模拟数据"""
        return {
            "Python": [
                {"title": "Python后端开发工程师", "company": "字节跳动", "salary": "25-50K·16薪", 
                 "location": "北京·海淀区", "experience": "3-5年", "education": "本科",
                 "skills": ["Python", "Django", "MySQL", "Redis", "Docker"]},
                {"title": "Python数据分析师", "company": "阿里巴巴", "salary": "20-40K·14薪",
                 "location": "杭州·余杭区", "experience": "2-4年", "education": "本科",
                 "skills": ["Python", "Pandas", "SQL", "统计学", "机器学习"]},
            ],
            "Java": [
                {"title": "Java高级开发工程师", "company": "腾讯", "salary": "30-60K·15薪",
                 "location": "深圳·南山区", "experience": "5-8年", "education": "本科",
                 "skills": ["Java", "Spring", "微服务", "分布式", "高并发"]},
                {"title": "Java架构师", "company": "百度", "salary": "40-80K",
                 "location": "北京·海淀区", "experience": "8年以上", "education": "本科",
                 "skills": ["Java", "架构设计", "系统优化", "团队管理"]},
            ],
            "前端": [
                {"title": "前端开发专家", "company": "美团", "salary": "25-45K·15薪",
                 "location": "上海·浦东新区", "experience": "4-7年", "education": "本科",
                 "skills": ["React", "Vue", "TypeScript", "Node.js", "Webpack"]},
                {"title": "前端开发工程师", "company": "滴滴", "salary": "18-35K·14薪",
                 "location": "北京·朝阳区", "experience": "2-5年", "education": "本科",
                 "skills": ["JavaScript", "Vue", "小程序", "移动端"]},
            ]
        }
    
    def search_qiancheng(self, keyword: str, city: str, max_results: int = 10) -> List[PracticalJob]:
        """搜索前程无忧 - 当前最可能工作的平台"""
        jobs = []
        
        try:
            # 前程无忧搜索URL
            city_code = self._get_qiancheng_city_code(city)
            search_url = f"https://search.51job.com/list/{city_code},000000,0000,00,9,99,{quote(keyword)},2,1.html"
            
            # 添加延迟避免请求过快
            time.sleep(random.uniform(1, 2))
            
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                jobs = self._parse_qiancheng_html(response.text, max_results)
                print(f"[INFO] 前程无忧搜索成功: 找到 {len(jobs)} 个真实岗位")
            else:
                print(f"[WARN] 前程无忧搜索失败，状态码: {response.status_code}")
                # 使用备用数据
                jobs = self._get_fallback_data(keyword, city, "前程无忧", max_results)
                
        except Exception as e:
            print(f"[ERROR] 前程无忧搜索错误: {e}")
            # 使用备用数据
            jobs = self._get_fallback_data(keyword, city, "前程无忧", max_results)
        
        return jobs[:max_results]
    
    def _parse_qiancheng_html(self, html: str, max_results: int) -> List[PracticalJob]:
        """解析前程无忧HTML"""
        jobs = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 前程无忧的选择器（根据当前页面结构调整）
            # 常见的选择器:
            job_items = soup.select('.j_joblist .e')
            
            if not job_items:
                # 尝试其他可能的选择器
                job_items = soup.select('.dw_table .el')
            
            for item in job_items[:max_results]:
                try:
                    # 提取职位信息
                    title_elem = item.select_one('.jname')
                    company_elem = item.select_one('.cname')
                    salary_elem = item.select_one('.sal')
                    location_elem = item.select_one('.d.at')
                    
                    if not (title_elem and company_elem):
                        continue
                    
                    # 提取经验和学历
                    experience = "经验不限"
                    education = "学历不限"
                    
                    info_elem = item.select_one('.jtag .t1')
                    if info_elem:
                        info_text = info_elem.get_text()
                        # 简单解析
                        import re
                        exp_match = re.search(r'(\d+[-]?\d*年?)经验', info_text)
                        if exp_match:
                            experience = exp_match.group(1) + "经验"
                        
                        edu_keywords = ['中专', '高中', '大专', '本科', '硕士', '博士']
                        for edu in edu_keywords:
                            if edu in info_text:
                                education = edu
                                break
                    
                    # 提取技能标签
                    skills = []
                    tag_elems = item.select('.jtag .t2 span')
                    for tag in tag_elems:
                        skill = tag.get_text().strip()
                        if skill and len(skill) < 15:
                            skills.append(skill)
                    
                    # 提取URL
                    url = self._extract_qiancheng_url(item)
                    
                    job = PracticalJob(
                        platform="前程无忧",
                        title=title_elem.get_text().strip(),
                        company=company_elem.get_text().strip(),
                        salary=salary_elem.get_text().strip() if salary_elem else "面议",
                        location=location_elem.get_text().strip() if location_elem else city,
                        experience=experience,
                        education=education,
                        skills=skills[:5],
                        url=url,
                        source="real"
                    )
                    jobs.append(job)
                    
                except Exception as e:
                    print(f"[DEBUG] 解析前程无忧岗位失败: {e}")
                    continue
                    
        except Exception as e:
            print(f"[ERROR] 解析前程无忧HTML失败: {e}")
        
        return jobs
    
    def _extract_qiancheng_url(self, item) -> str:
        """提取前程无忧职位URL"""
        try:
            link_elem = item.select_one('a')
            if link_elem and link_elem.get('href'):
                href = link_elem['href']
                if href.startswith('http'):
                    return href
                else:
                    return urljoin("https://www.51job.com", href)
        except:
            pass
        
        return "https://www.51job.com"
    
    def _get_qiancheng_city_code(self, city: str) -> str:
        """获取前程无忧城市代码"""
        city_map = {
            '北京': '010000',
            '上海': '020000',
            '广州': '030200',
            '深圳': '030300',
            '杭州': '080200',
            '成都': '090200',
            '武汉': '180200',
            '南京': '070200',
            '西安': '200200',
            '重庆': '040000'
        }
        return city_map.get(city, '010000')
    
    def _get_fallback_data(self, keyword: str, city: str, platform: str, max_results: int) -> List[PracticalJob]:
        """获取备用数据（当真实搜索失败时）"""
        jobs = []
        
        # 从模拟数据获取
        mock_jobs = self.mock_data.get(keyword, [])
        if not mock_jobs:
            # 如果没有匹配的关键词，使用第一个关键词的数据
            first_key = next(iter(self.mock_data))
            mock_jobs = self.mock_data[first_key]
        
        for i, mock in enumerate(mock_jobs[:max_results]):
            job = PracticalJob(
                platform=platform,
                title=mock["title"],
                company=mock["company"],
                salary=mock["salary"],
                location=city + "·" + mock["location"].split("·")[-1] if "·" in mock["location"] else city,
                experience=mock["experience"],
                education=mock["education"],
                skills=mock["skills"],
                url=f"https://www.example.com/job{i}",
                source="fallback"
            )
            jobs.append(job)
        
        return jobs
    
    def search_with_mixed_strategy(self, keyword: str, city: str, max_results: int = 20) -> Dict[str, List[PracticalJob]]:
        """混合策略搜索"""
        results = {}
        
        print(f"\n开始搜索: {keyword} - {city}")
        print("=" * 50)
        
        # 策略1: 尝试前程无忧（当前最可能工作）
        print("\n1. 尝试前程无忧（真实数据）...")
        qiancheng_jobs = self.search_qiancheng(keyword, city, max_results)
        results["前程无忧"] = qiancheng_jobs
        
        # 策略2: 尝试BOSS直聘（可能失败）
        print("\n2. 尝试BOSS直聘...")
        try:
            # 这里可以添加BOSS直聘的真实搜索逻辑
            # 目前使用模拟数据
            boss_jobs = self._get_fallback_data(keyword, city, "BOSS直聘", max_results // 2)
            results["BOSS直聘"] = boss_jobs
            print(f"  使用模拟数据: {len(boss_jobs)} 个岗位")
        except Exception as e:
            print(f"  搜索失败: {e}")
            results["BOSS直聘"] = []
        
        # 策略3: 尝试智联招聘（可能失败）
        print("\n3. 尝试智联招聘...")
        try:
            # 这里可以添加智联招聘的真实搜索逻辑
            # 目前使用模拟数据
            zhilian_jobs = self._get_fallback_data(keyword, city, "智联招聘", max_results // 2)
            results["智联招聘"] = zhilian_jobs
            print(f"  使用模拟数据: {len(zhilian_jobs)} 个岗位")
        except Exception as e:
            print(f"  搜索失败: {e}")
            results["智联招聘"] = []
        
        # 统计
        real_count = sum(1 for jobs in results.values() for job in jobs if job.source == "real")
        fallback_count = sum(1 for jobs in results.values() for job in jobs if job.source == "fallback")
        
        print(f"\n搜索完成:")
        print(f"  真实数据: {real_count} 个岗位")
        print(f"  备用数据: {fallback_count} 个岗位")
        print(f"  总计: {real_count + fallback_count} 个岗位")
        
        return results
    
    def format_results(self, results: Dict[str, List[PracticalJob]]) -> str:
        """格式化输出结果"""
        if not results:
            return "未找到任何岗位"
        
        output = "=" * 80 + "\n"
        output += "招聘搜索结果\n"
        output += "=" * 80 + "\n\n"
        
        total_real = 0
        total_fallback = 0
        
        for platform, jobs in results.items():
            if not jobs:
                continue
            
            real_jobs = [j for j in jobs if j.source == "real"]
            fallback_jobs = [j for j in jobs if j.source == "fallback"]
            
            real_count = len(real_jobs)
            fallback_count = len(fallback_jobs)
            
            total_real += real_count
            total_fallback += fallback_count
            
            source_info = ""
            if real_count > 0 and fallback_count > 0:
                source_info = f" ({real_count}真实 + {fallback_count}模拟)"
            elif real_count > 0:
                source_info = " (真实数据)"
            elif fallback_count > 0:
                source_info = " (模拟数据)"
            
            output += f"{platform}{source_info}:\n"
            output += "-" * 60 + "\n"
            
            # 显示真实数据优先
            display_jobs = real_jobs + fallback_jobs
            
            for i, job in enumerate(display_jobs[:5], 1):
                source_mark = "[R]" if job.source == "real" else "[M]"
                output += f"{source_mark} {i}. {job.title}\n"
                output += f"   公司: {job.company} | 薪资: {job.salary}\n"
                output += f"   地点: {job.location} | 要求: {job.experience} | {job.education}\n"
                if job.skills:
                    output += f"   技能: {', '.join(job.skills[:3])}\n"
                output += "\n"
            
            if len(display_jobs) > 5:
                output += f"  ... 还有 {len(display_jobs)-5} 个岗位\n"
            output += "\n"
        
        output += "=" * 80 + "\n"
        output += f"统计: {total_real} 个真实岗位 + {total_fallback} 个模拟岗位 = {total_real + total_fallback} 个岗位\n"
        
        if total_fallback > 0:
            output += "注: [R] 表示真实数据，[M] 表示模拟数据（当真实搜索失败时使用）\n"
        
        output += "=" * 80
        
        return output
    
    def save_results(self, results: Dict[str, List[PracticalJob]], filename: str = None):
        """保存结果到文件"""
        if filename is None:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"job_search_results_{timestamp}.json"
        
        data = []
        for platform, jobs in results.items():
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
                    "url": job.url,
                    "source": job.source,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n结果已保存到: {filename}")
        return filename


def main():
    """主函数"""
    print("实用版招聘搜索技能")
    print("=" * 60)
    print("说明: 此版本使用混合策略，优先获取真实数据，失败时使用模拟数据")
    print("=" * 60)
    
    # 创建搜索器
    searcher = PracticalJobSearcher()
    
    # 获取用户输入
    import sys
    
    if len(sys.argv) > 1:
        # 命令行参数模式
        keyword = sys.argv[1]
        city = sys.argv[2] if len(sys.argv) > 2 else "北京"
    else:
        # 交互模式
        print("\n请输入搜索参数:")
        keyword = input("关键词 (默认: Python): ").strip() or "Python"
        city = input("城市 (默认: 北京): ").strip() or "北京"
    
    print(f"\n开始搜索: {keyword} - {city}")
    
    # 执行搜索
    results = searcher.search_with_mixed_strategy(keyword, city, max_results=20)
    
    # 输出结果
    output = searcher.format_results(results)
    print(output)
    
    # 保存结果
    filename = searcher.save_results(results)
    
    print(f"\n搜索完成! 详细数据已保存到: {filename}")


if __name__ == '__main__':
    main()
