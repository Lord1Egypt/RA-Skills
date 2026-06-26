#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
招聘搜索主程序
支持BOSS直聘、智联招聘、前程无忧三大平台
"""

import json
import time
import argparse
from typing import Dict, List, Optional
from dataclasses import dataclass
import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import requests
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent
except ImportError as e:
    print(f"缺少依赖库: {e}")
    print("请运行: pip install -r requirements.txt")
    sys.exit(1)


@dataclass
class Job:
    """岗位信息数据类"""
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


class JobSearcher:
    """招聘搜索器"""
    
    def __init__(self, config_path: str = None):
        """初始化搜索器"""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        
        # 导入平台解析器
        self.parsers = {}
        self._load_parsers()
    
    def _load_parsers(self):
        """动态加载平台解析器"""
        try:
            from boss_parser import BossParser
            self.parsers['boss'] = BossParser(self.session)
        except ImportError:
            print("警告: BOSS直聘解析器加载失败")
        
        try:
            from zhilian_parser import ZhilianParser
            self.parsers['zhilian'] = ZhilianParser(self.session)
        except ImportError:
            print("警告: 智联招聘解析器加载失败")
        
        try:
            from qiancheng_parser import QianchengParser
            self.parsers['qiancheng'] = QianchengParser(self.session)
        except ImportError:
            print("警告: 前程无忧解析器加载失败")
    
    def search(self, keyword: str, city: str = None, 
               platforms: List[str] = None, max_results: int = 20) -> List[Job]:
        """
        搜索岗位
        
        Args:
            keyword: 搜索关键词
            city: 城市名称
            platforms: 平台列表，默认全部
            max_results: 最大结果数
        
        Returns:
            岗位列表
        """
        if city is None:
            city = self.config['search']['default_city']
        
        if platforms is None:
            platforms = [p for p in self.config['platforms'] 
                        if self.config['platforms'][p]['enabled']]
        
        all_jobs = []
        
        for platform in platforms:
            if platform not in self.parsers:
                print(f"跳过 {platform}，解析器未加载")
                continue
            
            print(f"正在搜索 {self.config['platforms'][platform]['name']}...")
            
            try:
                parser = self.parsers[platform]
                jobs = parser.search(keyword, city, max_results)
                all_jobs.extend(jobs)
                
                # 避免请求过快
                time.sleep(self.config['search']['request_delay'])
                
            except Exception as e:
                print(f"{platform} 搜索失败: {e}")
                continue
        
        return all_jobs
    
    def format_results(self, jobs: List[Job], format_type: str = None) -> str:
        """格式化输出结果"""
        if format_type is None:
            format_type = self.config['output']['format']
        
        if format_type == 'table':
            return self._format_table(jobs)
        elif format_type == 'list':
            return self._format_list(jobs)
        else:
            return self._format_simple(jobs)
    
    def _format_table(self, jobs: List[Job]) -> str:
        """表格格式输出"""
        if not jobs:
            return "未找到相关岗位"
        
        # 确定显示字段
        fields = self.config['output']['show_fields']
        
        # 构建表头
        headers = []
        for field in fields:
            if field == '职位':
                headers.append('职位')
            elif field == '公司':
                headers.append('公司')
            elif field == '薪资':
                headers.append('薪资')
            elif field == '地点':
                headers.append('地点')
            elif field == '经验':
                headers.append('经验')
            elif field == '学历':
                headers.append('学历')
            elif field == '平台':
                headers.append('平台')
        
        # 构建表格行
        rows = []
        for job in jobs:
            row = []
            for field in fields:
                if field == '职位':
                    row.append(job.title[:20] + '...' if len(job.title) > 20 else job.title)
                elif field == '公司':
                    row.append(job.company[:15] + '...' if len(job.company) > 15 else job.company)
                elif field == '薪资':
                    row.append(job.salary)
                elif field == '地点':
                    row.append(job.location)
                elif field == '经验':
                    row.append(job.experience)
                elif field == '学历':
                    row.append(job.education)
                elif field == '平台':
                    row.append(job.platform)
            rows.append(row)
        
        # 按配置排序
        sort_field = self.config['output']['sort_by']
        if sort_field == '薪资':
            rows.sort(key=lambda x: self._parse_salary(x[fields.index('薪资')]), reverse=True)
        
        # 生成表格字符串
        result = "=" * 80 + "\n"
        result += "招聘搜索结果\n"
        result += "=" * 80 + "\n\n"
        
        # 表头
        header_line = " | ".join(headers)
        result += header_line + "\n"
        result += "-" * len(header_line) + "\n"
        
        # 数据行
        for row in rows:
            result += " | ".join(row) + "\n"
        
        result += f"\n共找到 {len(jobs)} 个岗位\n"
        
        return result
    
    def _parse_salary(self, salary_str: str) -> float:
        """解析薪资字符串为数值（用于排序）"""
        try:
            # 提取数字部分
            import re
            numbers = re.findall(r'\d+', salary_str)
            if numbers:
                return float(numbers[0])
        except:
            pass
        return 0.0
    
    def _format_list(self, jobs: List[Job]) -> str:
        """列表格式输出"""
        if not jobs:
            return "未找到相关岗位"
        
        result = f"找到 {len(jobs)} 个相关岗位：\n\n"
        
        for i, job in enumerate(jobs, 1):
            result += f"{i}. 【{job.platform}】{job.title}\n"
            result += f"   公司：{job.company}\n"
            result += f"   薪资：{job.salary} | 地点：{job.location}\n"
            result += f"   要求：{job.experience} | {job.education}\n"
            if job.skills:
                result += f"   技能：{', '.join(job.skills[:3])}\n"
            result += "\n"
        
        return result
    
    def _format_simple(self, jobs: List[Job]) -> str:
        """简单格式输出"""
        if not jobs:
            return "未找到相关岗位"
        
        result = f"共找到 {len(jobs)} 个岗位：\n"
        
        platforms = {}
        for job in jobs:
            if job.platform not in platforms:
                platforms[job.platform] = 0
            platforms[job.platform] += 1
        
        for platform, count in platforms.items():
            result += f"- {platform}: {count} 个\n"
        
        # 显示薪资范围
        salaries = [self._parse_salary(job.salary) for job in jobs if job.salary]
        if salaries:
            avg_salary = sum(salaries) / len(salaries)
            result += f"\n平均薪资：{avg_salary:.1f}K\n"
        
        return result


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='招聘岗位搜索')
    parser.add_argument('keyword', help='搜索关键词')
    parser.add_argument('-c', '--city', default='北京', help='城市名称')
    parser.add_argument('-p', '--platforms', default='all', 
                       help='平台: boss,zhilian,qiancheng 或 all')
    parser.add_argument('-n', '--number', type=int, default=20, 
                       help='每个平台最大结果数')
    parser.add_argument('-f', '--format', default='table', 
                       choices=['table', 'list', 'simple'], help='输出格式')
    
    args = parser.parse_args()
    
    # 解析平台参数
    if args.platforms == 'all':
        platforms = None
    else:
        platforms = [p.strip() for p in args.platforms.split(',')]
    
    # 执行搜索
    searcher = JobSearcher()
    jobs = searcher.search(args.keyword, args.city, platforms, args.number)
    
    # 输出结果
    if args.format == 'table':
        output = searcher.format_results(jobs, 'table')
    elif args.format == 'list':
        output = searcher.format_results(jobs, 'list')
    else:
        output = searcher.format_results(jobs, 'simple')
    
    print(output)


if __name__ == '__main__':
    main()