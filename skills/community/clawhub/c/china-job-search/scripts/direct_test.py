#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试招聘网站可访问性
"""

import requests
import time
import random
from bs4 import BeautifulSoup

print("=" * 70)
print("直接测试招聘网站可访问性")
print("=" * 70)

# 增强的请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0',
}

session = requests.Session()
session.headers.update(headers)

# 测试各网站
websites = [
    {
        'name': 'BOSS直聘首页',
        'url': 'https://www.zhipin.com',
        'test_search': True,
        'search_url': 'https://www.zhipin.com/web/geek/job?query=Python&city=101010100'
    },
    {
        'name': '智联招聘首页',
        'url': 'https://www.zhaopin.com',
        'test_search': True,
        'search_url': 'https://sou.zhaopin.com/?jl=530&kw=Python'
    },
    {
        'name': '前程无忧首页',
        'url': 'https://www.51job.com',
        'test_search': True,
        'search_url': 'https://search.51job.com/list/010000,000000,0000,00,9,99,Python,2,1.html'
    }
]

for site in websites:
    print(f"\n测试 {site['name']}...")
    print(f"URL: {site['url']}")
    
    try:
        # 测试首页
        print("  1. 访问首页...")
        response = session.get(site['url'], timeout=10)
        
        if response.status_code == 200:
            print(f"    [OK] 成功 (状态码: {response.status_code})")
            print(f"    页面大小: {len(response.text)} 字符")
            
            # 检查是否有反爬提示
            content_lower = response.text.lower()
            if '验证' in response.text or 'captcha' in content_lower or 'access denied' in content_lower:
                print("    [WARN] 检测到反爬验证")
            else:
                print("    [OK] 页面内容正常")
                
            # 保存首页HTML
            with open(f"{site['name'].replace(' ', '_')}_homepage.html", 'w', encoding='utf-8') as f:
                f.write(response.text[:5000])  # 只保存前5000字符
            
        else:
            print(f"    [FAIL] 失败 (状态码: {response.status_code})")
        
        # 随机延迟
        delay = random.uniform(1, 2)
        time.sleep(delay)
        
        # 测试搜索页面
        if site['test_search']:
            print(f"  2. 测试搜索页面...")
            print(f"    搜索URL: {site['search_url']}")
            
            try:
                search_response = session.get(site['search_url'], timeout=15)
                
                if search_response.status_code == 200:
                    print(f"    [OK] 搜索页面成功 (状态码: {search_response.status_code})")
                    print(f"    搜索页面大小: {len(search_response.text)} 字符")
                    
                    # 保存搜索页面
                    with open(f"{site['name'].replace(' ', '_')}_search.html", 'w', encoding='utf-8') as f:
                        f.write(search_response.text[:10000])  # 只保存前10000字符
                    
                    # 简单分析页面结构
                    soup = BeautifulSoup(search_response.text, 'html.parser')
                    
                    # 查找可能的职位相关元素
                    job_keywords = ['job', 'position', '职位', '招聘', '工作', 'career']
                    found_elements = []
                    
                    for tag in soup.find_all(True):  # 所有标签
                        if tag.get('class'):
                            classes = ' '.join(tag.get('class')).lower()
                            for keyword in job_keywords:
                                if keyword in classes:
                                    found_elements.append((tag.name, classes))
                                    break
                        
                        if tag.get('id'):
                            id_str = tag.get('id').lower()
                            for keyword in job_keywords:
                                if keyword in id_str:
                                    found_elements.append((tag.name, f"id={id_str}"))
                                    break
                    
                    # 去重
                    unique_elements = list(set(found_elements))
                    if unique_elements:
                        print(f"    发现 {len(unique_elements)} 个可能包含职位的元素:")
                        for elem_type, elem_id in unique_elements[:10]:  # 只显示前10个
                            print(f"      - <{elem_type}> class/id包含职位关键词")
                    
                else:
                    print(f"    [FAIL] 搜索页面失败 (状态码: {search_response.status_code})")
                    
            except Exception as e:
                print(f"    [FAIL] 搜索页面错误: {e}")
        
        # 再次延迟
        time.sleep(random.uniform(1, 3))
        
    except requests.exceptions.Timeout:
        print("    [FAIL] 连接超时")
    except requests.exceptions.ConnectionError:
        print("    [FAIL] 连接错误")
    except Exception as e:
        print(f"    [FAIL] 错误: {e}")

print("\n" + "=" * 70)
print("测试总结")
print("=" * 70)

print("""
生成的文件:
1. BOSS直聘首页_homepage.html - BOSS直聘首页
2. BOSS直聘首页_search.html - BOSS直聘搜索页面
3. 智联招聘首页_homepage.html - 智联招聘首页
4. 智联招聘首页_search.html - 智联招聘搜索页面
5. 前程无忧首页_homepage.html - 前程无忧首页
6. 前程无忧首页_search.html - 前程无忧搜索页面

下一步:
1. 查看生成的HTML文件，分析页面结构
2. 根据实际结构更新解析器中的选择器
3. 如果遇到反爬，考虑:
   - 添加更多请求头
   - 使用代理IP
   - 使用Selenium浏览器自动化
""")

# 创建简单的解析器更新示例
print("\n解析器更新示例:")
example_code = '''
# 在 boss_parser.py 中更新选择器
def _parse_html_results(self, html: str):
    soup = BeautifulSoup(html, 'html.parser')
    
    # 根据实际页面结构调整这些选择器
    # 查看生成的HTML文件，找到正确的选择器
    
    # 示例（需要根据实际页面调整）:
    # job_items = soup.select('.job-list li')
    # job_items = soup.select('.job-card-wrapper')
    # job_items = soup.select('[class*="job-item"]')
    
    jobs = []
    for item in job_items:
        try:
            # 提取信息
            title_elem = item.select_one('.job-title')  # 需要验证
            company_elem = item.select_one('.company-name')  # 需要验证
            salary_elem = item.select_one('.salary')  # 需要验证
            location_elem = item.select_one('.location')  # 需要验证
            
            if title_elem and company_elem:
                job = Job(
                    platform="BOSS直聘",
                    title=title_elem.get_text().strip(),
                    company=company_elem.get_text().strip(),
                    salary=salary_elem.get_text().strip() if salary_elem else "面议",
                    location=location_elem.get_text().strip() if location_elem else "",
                    experience="经验不限",  # 需要根据实际页面提取
                    education="学历不限",  # 需要根据实际页面提取
                    skills=[],
                    url=self._extract_job_url(item)
                )
                jobs.append(job)
                
        except Exception as e:
            print(f"解析岗位失败: {e}")
            continue
    
    return jobs
'''

print(example_code)