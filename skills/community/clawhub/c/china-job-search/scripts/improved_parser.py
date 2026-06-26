#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进版前程无忧解析器
处理Cookie和反爬机制
"""

import requests
import time
import random
from bs4 import BeautifulSoup
import re


class Improved51JobParser:
    """改进版前程无忧解析器"""
    
    def __init__(self):
        self.session = requests.Session()
        self._setup_session()
        
    def _setup_session(self):
        """设置会话"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.51job.com/',
        })
    
    def search_jobs(self, keyword, city='北京', max_results=10):
        """搜索职位"""
        print(f"搜索: {keyword} - {city}")
        
        # 先访问首页获取Cookie
        print("1. 访问首页获取Cookie...")
        try:
            home_response = self.session.get('https://www.51job.com/', timeout=10)
            print(f"   首页状态码: {home_response.status_code}")
            print(f"   首页大小: {len(home_response.text)} 字符")
            
            # 等待一下
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            print(f"   访问首页失败: {e}")
            return []
        
        # 构建搜索URL
        city_code = self._get_city_code(city)
        search_url = f"https://search.51job.com/list/{city_code},000000,0000,00,9,99,{keyword},2,1.html"
        
        print(f"2. 访问搜索页面: {search_url}")
        
        try:
            response = self.session.get(search_url, timeout=15)
            print(f"   搜索页面状态码: {response.status_code}")
            print(f"   搜索页面大小: {len(response.text)} 字符")
            
            if response.status_code == 200 and len(response.text) > 1000:
                # 保存页面供分析
                with open('51job_search_page.html', 'w', encoding='utf-8') as f:
                    f.write(response.text[:5000])
                print("   页面已保存到: 51job_search_page.html")
                
                # 解析职位
                jobs = self._parse_jobs(response.text, max_results)
                return jobs
            else:
                print(f"   页面内容异常，可能被反爬")
                # 尝试查看页面内容
                if len(response.text) < 1000:
                    print(f"   页面内容: {response.text[:500]}")
                
        except Exception as e:
            print(f"   搜索失败: {e}")
        
        return []
    
    def _get_city_code(self, city):
        """获取城市代码"""
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
    
    def _parse_jobs(self, html, max_results):
        """解析职位"""
        jobs = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            print("3. 解析页面结构...")
            
            # 方法1: 尝试直接查找职位信息
            job_elements = []
            
            # 查找包含职位信息的div
            for div in soup.find_all('div'):
                class_attr = div.get('class', [])
                class_str = ' '.join(class_attr)
                
                # 检查是否包含职位相关信息
                text = div.get_text().strip()
                if len(text) > 50 and ('Python' in text or '开发' in text or '工程师' in text):
                    job_elements.append(div)
                    print(f"   找到可能职位元素: {class_str[:50]}...")
            
            print(f"   找到 {len(job_elements)} 个可能职位元素")
            
            if job_elements:
                # 尝试从这些元素提取信息
                for i, element in enumerate(job_elements[:max_results]):
                    try:
                        job_info = self._extract_job_info(element)
                        if job_info:
                            jobs.append(job_info)
                            print(f"   解析成功: {job_info['title'][:30]}...")
                    except Exception as e:
                        print(f"   解析失败: {e}")
                        continue
            
            # 方法2: 查找所有链接
            if not jobs:
                print("   尝试方法2: 分析链接...")
                links = soup.find_all('a')
                job_links = []
                
                for link in links:
                    href = link.get('href', '')
                    text = link.get_text().strip()
                    
                    # 检查是否是职位链接
                    if ('jobs.51job.com' in href or 'job' in href) and len(text) > 5:
                        job_links.append((text, href))
                
                print(f"   找到 {len(job_links)} 个职位链接")
                
                for i, (text, href) in enumerate(job_links[:max_results]):
                    jobs.append({
                        'title': text,
                        'company': '未知',
                        'salary': '面议',
                        'location': '未知',
                        'experience': '经验不限',
                        'education': '学历不限',
                        'skills': [],
                        'url': href
                    })
            
            # 方法3: 查找特定模式
            if not jobs:
                print("   尝试方法3: 查找特定模式...")
                # 查找包含薪资信息的文本
                salary_pattern = r'(\d+[kK千]?-?\d*[kK千]?)'
                for text in soup.stripped_strings:
                    if 'Python' in text and ('k' in text.lower() or 'K' in text or '千' in text):
                        print(f"   找到薪资信息: {text[:50]}...")
            
        except Exception as e:
            print(f"   解析错误: {e}")
            import traceback
            traceback.print_exc()
        
        return jobs
    
    def _extract_job_info(self, element):
        """从元素提取职位信息"""
        try:
            # 获取所有文本
            text = element.get_text().strip()
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            if len(lines) < 3:
                return None
            
            # 简单解析
            title = lines[0] if lines else "未知职位"
            company = "未知公司"
            salary = "面议"
            location = "未知"
            
            # 尝试从文本中提取信息
            for line in lines:
                if '公司' in line and len(line) < 30:
                    company = line.replace('公司', '').strip()
                elif 'k' in line.lower() or 'K' in line or '千' in line:
                    salary_match = re.search(r'(\d+[kK千]?-?\d*[kK千]?)', line)
                    if salary_match:
                        salary = salary_match.group(1)
                elif '北京' in line or '上海' in line or '广州' in line or '深圳' in line:
                    location = line
            
            return {
                'title': title[:50],
                'company': company[:30],
                'salary': salary,
                'location': location[:20],
                'experience': '经验不限',
                'education': '学历不限',
                'skills': [],
                'url': 'https://www.51job.com'
            }
            
        except Exception:
            return None


def main():
    """主函数"""
    print("改进版前程无忧解析器测试")
    print("=" * 60)
    
    parser = Improved51JobParser()
    
    # 测试搜索
    test_cases = [
        ("Python", "北京"),
        ("Java", "上海"),
        ("前端", "广州"),
    ]
    
    for keyword, city in test_cases:
        print(f"\n测试: {keyword} - {city}")
        print("-" * 40)
        
        jobs = parser.search_jobs(keyword, city, max_results=5)
        
        print(f"\n找到 {len(jobs)} 个职位:")
        for i, job in enumerate(jobs, 1):
            print(f"  {i}. {job['title']}")
            print(f"     公司: {job['company']} | 薪资: {job['salary']}")
            print(f"     地点: {job['location']}")
        
        if not jobs:
            print("  未找到职位，可能需要进一步优化解析器")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("\n下一步:")
    print("1. 查看生成的 51job_search_page.html 文件")
    print("2. 根据实际页面结构调整解析逻辑")
    print("3. 可能需要处理JavaScript渲染的内容")


if __name__ == '__main__':
    main()