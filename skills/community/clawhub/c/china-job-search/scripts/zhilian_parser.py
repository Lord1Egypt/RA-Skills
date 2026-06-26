#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智联招聘解析器
"""

import re
import json
import time
from typing import List, Dict, Optional
from urllib.parse import quote, urljoin
from job_searcher import Job


class ZhilianParser:
    """智联招聘解析器"""
    
    def __init__(self, session):
        self.session = session
        self.base_url = "https://www.zhaopin.com"
        self.search_url = "https://sou.zhaopin.com"
    
    def search(self, keyword: str, city: str, max_results: int = 20) -> List[Job]:
        """搜索智联招聘岗位"""
        jobs = []
        
        # 构建搜索URL
        search_params = {
            'jl': self._get_city_code(city),
            'kw': keyword,
            'p': 1
        }
        
        try:
            response = self.session.get(
                self.search_url,
                params=search_params,
                timeout=10
            )
            
            if response.status_code == 200:
                jobs = self._parse_html_results(response.text, max_results)
            
        except Exception as e:
            print(f"智联招聘搜索错误: {e}")
        
        return jobs[:max_results]
    
    def _get_city_code(self, city_name: str) -> str:
        """获取城市代码（简化版）"""
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
        return city_map.get(city_name, '530')  # 默认北京
    
    def _parse_html_results(self, html: str, max_results: int) -> List[Job]:
        """解析HTML搜索结果"""
        jobs = []
        
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            # 智联招聘的职位列表选择器（需要根据实际页面调整）
            job_items = soup.select('.joblist-box .joblist__item')
            
            for item in job_items[:max_results]:
                try:
                    # 提取职位信息
                    title_elem = item.select_one('.joblist__item__title')
                    company_elem = item.select_one('.company__title')
                    salary_elem = item.select_one('.joblist__item__salary')
                    location_elem = item.select_one('.joblist__item__location')
                    
                    if not all([title_elem, company_elem]):
                        continue
                    
                    # 提取经验和学历（智联的HTML结构可能不同）
                    experience = '经验不限'
                    education = '学历不限'
                    
                    # 尝试从其他元素提取
                    info_elems = item.select('.joblist__item__info span')
                    for info in info_elems:
                        text = info.get_text().strip()
                        if '经验' in text:
                            experience = text
                        elif '学历' in text:
                            education = text
                    
                    job = Job(
                        platform='智联招聘',
                        title=title_elem.get_text().strip(),
                        company=company_elem.get_text().strip(),
                        salary=salary_elem.get_text().strip() if salary_elem else '面议',
                        location=location_elem.get_text().strip() if location_elem else '',
                        experience=experience,
                        education=education,
                        skills=self._extract_skills(item),
                        url=self._extract_job_url(item)
                    )
                    jobs.append(job)
                    
                except Exception as e:
                    print(f"解析智联岗位失败: {e}")
                    continue
                    
        except Exception as e:
            print(f"解析智联HTML失败: {e}")
        
        return jobs
    
    def _extract_skills(self, item) -> List[str]:
        """从职位项提取技能"""
        skills = []
        try:
            # 尝试从描述或标签提取
            desc_elem = item.select_one('.joblist__item__desc')
            if desc_elem:
                desc_text = desc_elem.get_text()
                # 简单关键词匹配
                tech_keywords = ['Python', 'Java', '前端', '后端', '测试', 
                               '运维', '数据库', '云计算', 'AI', '大数据']
                for keyword in tech_keywords:
                    if keyword in desc_text:
                        skills.append(keyword)
        except:
            pass
        
        return skills[:3]
    
    def _extract_job_url(self, item) -> str:
        """提取职位详情URL"""
        try:
            link_elem = item.select_one('a')
            if link_elem and link_elem.get('href'):
                href = link_elem['href']
                if href.startswith('http'):
                    return href
                else:
                    return urljoin(self.base_url, href)
        except:
            pass
        
        return self.base_url
    
    def get_job_detail(self, job_url: str) -> Optional[Dict]:
        """获取岗位详情"""
        try:
            response = self.session.get(job_url, timeout=10)
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 解析详情信息
                detail = {
                    'description': '',
                    'requirements': '',
                    'company_info': ''
                }
                
                # 职位描述
                desc_elem = soup.select_one('.pos-ul')
                if desc_elem:
                    detail['description'] = desc_elem.get_text().strip()
                
                # 公司信息
                company_elem = soup.select_one('.company-info')
                if company_elem:
                    detail['company_info'] = company_elem.get_text().strip()
                
                return detail
                
        except Exception as e:
            print(f"获取智联岗位详情失败: {e}")
        
        return None