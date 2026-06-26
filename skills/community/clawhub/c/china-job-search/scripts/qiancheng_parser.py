#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前程无忧解析器
"""

import re
import json
import time
from typing import List, Dict, Optional
from urllib.parse import quote, urljoin
from job_searcher import Job


class QianchengParser:
    """前程无忧解析器"""
    
    def __init__(self, session):
        self.session = session
        self.base_url = "https://www.51job.com"
        self.search_url = "https://search.51job.com"
    
    def search(self, keyword: str, city: str, max_results: int = 20) -> List[Job]:
        """搜索前程无忧岗位"""
        jobs = []
        
        # 构建搜索参数
        search_params = {
            'keyword': keyword,
            'searchType': 2,
            'postchannel': '0000',
            'jobarea': self._get_city_code(city),
            'curr_page': 1
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
            print(f"前程无忧搜索错误: {e}")
        
        return jobs[:max_results]
    
    def _get_city_code(self, city_name: str) -> str:
        """获取城市代码（简化版）"""
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
        return city_map.get(city_name, '010000')  # 默认北京
    
    def _parse_html_results(self, html: str, max_results: int) -> List[Job]:
        """解析HTML搜索结果"""
        jobs = []
        
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            # 前程无忧的职位列表选择器（需要根据实际页面调整）
            job_items = soup.select('.j_joblist .e')
            
            for item in job_items[:max_results]:
                try:
                    # 提取职位信息
                    title_elem = item.select_one('.jname')
                    company_elem = item.select_one('.cname')
                    salary_elem = item.select_one('.sal')
                    location_elem = item.select_one('.d.at')
                    
                    if not all([title_elem, company_elem]):
                        continue
                    
                    # 提取经验和学历
                    experience = '经验不限'
                    education = '学历不限'
                    
                    # 前程无忧通常将经验、学历等信息放在一起
                    info_elem = item.select_one('.jtag .t1')
                    if info_elem:
                        info_text = info_elem.get_text()
                        # 尝试解析经验和学历
                        exp_match = re.search(r'(\d+[-]?\d*年?)经验', info_text)
                        if exp_match:
                            experience = exp_match.group(1) + '经验'
                        
                        edu_match = re.search(r'(中专|高中|大专|本科|硕士|博士)', info_text)
                        if edu_match:
                            education = edu_match.group(1)
                    
                    job = Job(
                        platform='前程无忧',
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
                    print(f"解析前程无忧岗位失败: {e}")
                    continue
                    
        except Exception as e:
            print(f"解析前程无忧HTML失败: {e}")
        
        return jobs
    
    def _extract_skills(self, item) -> List[str]:
        """从职位项提取技能"""
        skills = []
        try:
            # 前程无忧通常有关键词标签
            tag_elems = item.select('.jtag .t2 span')
            for tag in tag_elems:
                skill = tag.get_text().strip()
                if skill and len(skill) < 10:  # 避免过长的标签
                    skills.append(skill)
            
            # 如果标签不够，尝试从职位名称提取
            if len(skills) < 2:
                title_elem = item.select_one('.jname')
                if title_elem:
                    title = title_elem.get_text()
                    tech_keywords = ['Java', 'Python', '前端', '后端', '测试', 
                                   '运维', 'Android', 'iOS', '大数据', 'AI']
                    for keyword in tech_keywords:
                        if keyword in title and keyword not in skills:
                            skills.append(keyword)
                            
        except:
            pass
        
        return skills[:5]
    
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
                    'company_info': '',
                    'welfare': ''  # 福利待遇
                }
                
                # 职位描述（前程无忧通常有明确的class）
                desc_elem = soup.select_one('.job_msg')
                if desc_elem:
                    detail['description'] = desc_elem.get_text().strip()
                
                # 公司信息
                company_elem = soup.select_one('.com_tag')
                if company_elem:
                    detail['company_info'] = company_elem.get_text().strip()
                
                # 福利待遇
                welfare_elem = soup.select_one('.jtag .t1')
                if welfare_elem:
                    detail['welfare'] = welfare_elem.get_text().strip()
                
                return detail
                
        except Exception as e:
            print(f"获取前程无忧岗位详情失败: {e}")
        
        return None