#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS直聘解析器
"""

import re
import json
import time
from typing import List, Dict, Optional
from urllib.parse import quote, urljoin
from job_searcher import Job


class BossParser:
    """BOSS直聘解析器"""
    
    def __init__(self, session):
        self.session = session
        self.base_url = "https://www.zhipin.com"
        self.search_url = "https://www.zhipin.com/web/geek/job"
    
    def search(self, keyword: str, city: str, max_results: int = 20) -> List[Job]:
        """搜索BOSS直聘岗位"""
        jobs = []
        
        # 构建搜索参数
        params = {
            'query': keyword,
            'city': self._get_city_code(city),
            'page': 1,
            'pageSize': max_results if max_results <= 30 else 30
        }
        
        try:
            # 设置请求头
            headers = {
                'Referer': f'{self.base_url}/',
                'Accept': 'application/json, text/plain, */*',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            response = self.session.get(
                self.search_url,
                params=params,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    jobs = self._parse_search_results(data)
                except json.JSONDecodeError:
                    print("BOSS直聘返回非JSON数据，可能触发了反爬机制")
                    # 可以尝试解析HTML版本
                    jobs = self._parse_html_fallback(response.text)
            
        except Exception as e:
            print(f"BOSS直聘搜索错误: {e}")
        
        return jobs[:max_results]
    
    def _get_city_code(self, city_name: str) -> str:
        """获取城市代码（简化版）"""
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
        return city_map.get(city_name, '101010100')  # 默认北京
    
    def _parse_search_results(self, data: Dict) -> List[Job]:
        """解析搜索结果"""
        jobs = []
        
        if not data or 'jobList' not in data:
            return jobs
        
        for item in data['jobList']:
            try:
                job = Job(
                    platform='BOSS直聘',
                    title=item.get('jobName', ''),
                    company=item.get('brandName', ''),
                    salary=item.get('salaryDesc', ''),
                    location=item.get('cityName', ''),
                    experience=item.get('jobExperience', ''),
                    education=item.get('jobDegree', ''),
                    skills=self._parse_skills(item),
                    url=urljoin(self.base_url, f"/job_detail/{item.get('encryptJobId', '')}.html"),
                    publish_time=item.get('publishTime', '')
                )
                jobs.append(job)
            except Exception as e:
                print(f"解析BOSS岗位失败: {e}")
                continue
        
        return jobs
    
    def _parse_skills(self, item: Dict) -> List[str]:
        """解析技能标签"""
        skills = []
        
        # 从职位描述中提取关键词
        job_desc = item.get('jobDesc', '')
        if job_desc:
            # 简单提取技术关键词
            tech_keywords = ['Python', 'Java', 'JavaScript', 'React', 'Vue', 
                           'Node.js', 'MySQL', 'Redis', 'Docker', 'Kubernetes',
                           'AWS', '阿里云', '腾讯云', '机器学习', '深度学习']
            
            for keyword in tech_keywords:
                if keyword in job_desc:
                    skills.append(keyword)
        
        # 限制技能数量
        return skills[:5]
    
    def get_job_detail(self, job_url: str) -> Optional[Dict]:
        """获取岗位详情（如果需要更多信息）"""
        try:
            response = self.session.get(job_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 这里可以解析更多详细信息
                detail = {
                    'description': '',
                    'requirements': '',
                    'benefits': ''
                }
                
                return detail
        except Exception as e:
            print(f"获取BOSS岗位详情失败: {e}")
        
        return None
    
    def _parse_html_fallback(self, html: str) -> List[Job]:
        """HTML回退解析（当API不可用时）"""
        jobs = []
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            # 这里添加BOSS直聘HTML页面的解析逻辑
            # 由于网站结构可能变化，这里只返回空列表
            print("注意: BOSS直聘API不可用，需要更新HTML解析逻辑")
            
        except Exception as e:
            print(f"HTML回退解析失败: {e}")
        
        return jobs