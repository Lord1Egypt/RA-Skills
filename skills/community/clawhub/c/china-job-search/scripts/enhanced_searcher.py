#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版招聘搜索技能
包含更好的反爬处理和实际使用建议
"""

import sys
import os
import time
import random
import json
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
class EnhancedJob:
    """增强版岗位信息"""
    platform: str
    title: str
    company: str
    salary: str
    location: str
    experience: str
    education: str
    skills: List[str]
    url: str
    publish_time: str = ""
    company_size: str = ""
    company_type: str = ""
    welfare: List[str] = None  # 福利待遇
    
    def __post_init__(self):
        if self.welfare is None:
            self.welfare = []


class EnhancedJobSearcher:
    """增强版招聘搜索器"""
    
    def __init__(self, config_path: str = None):
        """初始化"""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.ua = UserAgent()
        self.session = requests.Session()
        self._setup_session()
        
        # 用户代理轮换列表
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        ]
    
    def _setup_session(self):
        """设置会话参数"""
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        })
        
        # 设置超时和重试
        self.session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        self.session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
    
    def _rotate_user_agent(self):
        """轮换User-Agent"""
        agent = random.choice(self.user_agents)
        self.session.headers['User-Agent'] = agent
        return agent
    
    def _add_delay(self):
        """添加随机延迟，避免请求过快"""
        delay = random.uniform(1.0, 3.0)
        time.sleep(delay)
    
    def search_boss(self, keyword: str, city: str, max_results: int = 10) -> List[EnhancedJob]:
        """搜索BOSS直聘（增强版）"""
        jobs = []
        
        try:
            # 方法1: 尝试API搜索
            api_url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json"
            params = {
                'query': keyword,
                'city': self._get_boss_city_code(city),
                'page': 1,
                'pageSize': min(max_results, 30)
            }
            
            headers = {
                'Referer': 'https://www.zhipin.com/',
                'Accept': 'application/json, text/plain, */*',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            self._rotate_user_agent()
            response = self.session.get(api_url, params=params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'jobList' in data:
                        jobs = self._parse_boss_api(data['jobList'])
                except:
                    # API失败，尝试HTML搜索
                    jobs = self._search_boss_html(keyword, city, max_results)
            
            self._add_delay()
            
        except Exception as e:
            print(f"BOSS直聘搜索错误: {e}")
        
        return jobs[:max_results]
    
    def _search_boss_html(self, keyword: str, city: str, max_results: int) -> List[EnhancedJob]:
        """HTML方式搜索BOSS直聘"""
        jobs = []
        
        try:
            search_url = "https://www.zhipin.com/web/geek/job"
            params = {
                'query': keyword,
                'city': self._get_boss_city_code(city)
            }
            
            self._rotate_user_agent()
            response = self.session.get(search_url, params=params, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 这里需要根据实际页面结构调整选择器
                # 示例选择器（可能需要调整）:
                # job_items = soup.select('.job-list li')
                
                print("注意: BOSS直聘HTML解析需要根据当前页面结构调整选择器")
                
        except Exception as e:
            print(f"BOSS直聘HTML搜索错误: {e}")
        
        return jobs
    
    def _parse_boss_api(self, job_list: List[Dict]) -> List[EnhancedJob]:
        """解析BOSS直聘API数据"""
        jobs = []
        
        for item in job_list:
            try:
                job = EnhancedJob(
                    platform="BOSS直聘",
                    title=item.get('jobName', ''),
                    company=item.get('brandName', ''),
                    salary=item.get('salaryDesc', '面议'),
                    location=item.get('cityName', ''),
                    experience=item.get('jobExperience', '经验不限'),
                    education=item.get('jobDegree', '学历不限'),
                    skills=self._extract_boss_skills(item),
                    url=urljoin("https://www.zhipin.com", f"/job_detail/{item.get('encryptJobId', '')}.html"),
                    publish_time=item.get('publishTime', ''),
                    company_size=item.get('scaleName', ''),
                    company_type=item.get('industryName', '')
                )
                jobs.append(job)
            except Exception as e:
                print(f"解析BOSS岗位失败: {e}")
                continue
        
        return jobs
    
    def _extract_boss_skills(self, item: Dict) -> List[str]:
        """提取BOSS直聘技能"""
        skills = []
        
        # 从职位标签提取
        labels = item.get('labels', [])
        for label in labels:
            if label and len(label) < 20:  # 避免过长的标签
                skills.append(label)
        
        # 从描述中提取关键词
        desc = item.get('jobDesc', '')
        if desc:
            tech_keywords = ['Python', 'Java', 'Go', 'C++', 'JavaScript',
                           'React', 'Vue', 'Angular', 'Node.js',
                           'MySQL', 'Redis', 'MongoDB', 'PostgreSQL',
                           'Docker', 'K8s', 'AWS', '阿里云', '腾讯云',
                           '机器学习', '深度学习', 'AI', '大数据']
            
            for keyword in tech_keywords:
                if keyword in desc and keyword not in skills:
                    skills.append(keyword)
        
        return skills[:5]
    
    def _get_boss_city_code(self, city: str) -> str:
        """获取BOSS直聘城市代码"""
        city_map = {
            '北京': '101010100',
            '上海': '101020100',
            '广州': '101280100',
            '深圳': '101280600',
            '杭州': '101210100',
            '成都': '101270100',
            '武汉': '101200100',
            '南京': '101190100',
            '西安': '101110100',
            '重庆': '101040100'
        }
        return city_map.get(city, '101010100')
    
    def search_zhilian(self, keyword: str, city: str, max_results: int = 10) -> List[EnhancedJob]:
        """搜索智联招聘"""
        jobs = []
        
        try:
            # 构建搜索URL
            city_code = self._get_zhilian_city_code(city)
            search_url = f"https://sou.zhaopin.com/?jl={city_code}&kw={quote(keyword)}"
            
            self._rotate_user_agent()
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                jobs = self._parse_zhilian_html(soup, max_results)
            
            self._add_delay()
            
        except Exception as e:
            print(f"智联招聘搜索错误: {e}")
        
        return jobs[:max_results]
    
    def _parse_zhilian_html(self, soup: BeautifulSoup, max_results: int) -> List[EnhancedJob]:
        """解析智联招聘HTML"""
        jobs = []
        
        try:
            # 智联招聘的选择器（需要根据实际页面调整）
            # 常见的选择器:
            # job_items = soup.select('.joblist__item')  # 新版本
            # job_items = soup.select('.joblist-box .joblist__item')  # 可能的结构
            # job_items = soup.select('.contentpile__content__wrapper')  # 另一种可能
            
            print("注意: 智联招聘HTML解析需要根据当前页面结构调整选择器")
            
            # 这里可以添加实际的解析逻辑
            # 示例:
            # for item in job_items[:max_results]:
            #     title = item.select_one('.joblist__item__title').text.strip()
            #     company = item.select_one('.company__title').text.strip()
            #     ...
            
        except Exception as e:
            print(f"解析智联招聘HTML错误: {e}")
        
        return jobs
    
    def _get_zhilian_city_code(self, city: str) -> str:
        """获取智联招聘城市代码"""
        city_map = {
            '北京': '530',
            '上海': '538',
            '广州': '763',
            '深圳': '765',
            '杭州': '653',
            '成都': '801',
            '武汉': '736',
            '南京': '635',
            '西安': '854',
            '重庆': '551'
        }
        return city_map.get(city, '530')
    
    def search_all_platforms(self, keyword: str, city: str, max_results: int = 20) -> Dict[str, List[EnhancedJob]]:
        """搜索所有平台"""
        results = {}
        
        platforms = [
            ('boss', 'BOSS直聘', self.search_boss),
            ('zhilian', '智联招聘', self.search_zhilian),
            # 可以添加更多平台
        ]
        
        for platform_id, platform_name, search_func in platforms:
            if self.config['platforms'].get(platform_id, {}).get('enabled', True):
                print(f"正在搜索 {platform_name}...")
                try:
                    jobs = search_func(keyword, city, max_results)
                    results[platform_name] = jobs
                    print(f"  → 找到 {len(jobs)} 个岗位")
                except Exception as e:
                    print(f"  → 搜索失败: {e}")
                    results[platform_name] = []
        
        return results
    
    def format_results(self, results: Dict[str, List[EnhancedJob]]) -> str:
        """格式化输出结果"""
        if not results:
            return "未找到任何岗位"
        
        output = "=" * 80 + "\n"
        output += "招聘搜索结果\n"
        output += "=" * 80 + "\n\n"
        
        total_jobs = 0
        for platform, jobs in results.items():
            if jobs:
                total_jobs += len(jobs)
                output += f"{platform} ({len(jobs)}个):\n"
                output += "-" * 60 + "\n"
                
                for i, job in enumerate(jobs[:5], 1):  # 每个平台显示前5个
                    output += f"{i}. {job.title}\n"
                    output += f"   公司: {job.company} | 薪资: {job.salary}\n"
                    output += f"   地点: {job.location} | 要求: {job.experience} | {job.education}\n"
                    if job.skills:
                        output += f"   技能: {', '.join(job.skills[:3])}\n"
                    output += "\n"
                
                if len(jobs) > 5:
                    output += f"  ... 还有 {len(jobs)-5} 个岗位\n"
                output += "\n"
        
        output += f"总计: {total_jobs} 个岗位\n"
        output += "=" * 80
        
        return output


def main():
    """主函数"""
    print("增强版招聘搜索技能")
    print("=" * 60)
    
    # 创建搜索器
    searcher = EnhancedJobSearcher()
    
    # 测试搜索
    keyword = input("请输入搜索关键词 (默认: Python): ").strip() or "Python"
    city = input("请输入城市 (默认: 北京): ").strip() or "北京"
    
    print(f"\n搜索: {keyword} - {city}")
    print("正在搜索各平台...")
    
    results = searcher.search_all_platforms(keyword, city, max_results=10)
    
    # 输出结果
    output = searcher.format_results(results)
    print(output)
    
    # 保存结果
    save = input("\n是否保存结果到文件? (y/n): ").strip().lower()
    if save == 'y':
        filename = f"jobs_{keyword}_{city}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"结果已保存到: {filename}")


if __name__ == '__main__':
    main()