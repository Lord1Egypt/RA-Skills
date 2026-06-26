#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版招聘搜索技能测试
非交互式测试
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_searcher import EnhancedJobSearcher


def test_basic_search():
    """测试基础搜索功能"""
    print("=" * 70)
    print("增强版招聘搜索技能测试")
    print("=" * 70)
    
    # 创建搜索器
    searcher = EnhancedJobSearcher()
    
    # 测试用例
    test_cases = [
        ("Python", "北京"),
        ("Java", "上海"),
        ("前端", "广州"),
    ]
    
    for keyword, city in test_cases:
        print(f"\n测试搜索: {keyword} - {city}")
        print("-" * 50)
        
        try:
            # 测试BOSS直聘
            print("1. 测试BOSS直聘...")
            boss_jobs = searcher.search_boss(keyword, city, max_results=5)
            print(f"  找到 {len(boss_jobs)} 个岗位")
            
            # 显示前3个结果
            for i, job in enumerate(boss_jobs[:3], 1):
                print(f"    {i}. {job.title[:30]}... | {job.salary} | {job.company[:15]}...")
            
            # 测试智联招聘
            print("\n2. 测试智联招聘...")
            zhilian_jobs = searcher.search_zhilian(keyword, city, max_results=5)
            print(f"  找到 {len(zhilian_jobs)} 个岗位")
            
            # 显示前3个结果
            for i, job in enumerate(zhilian_jobs[:3], 1):
                print(f"    {i}. {job.title[:30]}... | {job.salary} | {job.company[:15]}...")
            
            # 测试所有平台
            print("\n3. 测试所有平台...")
            all_results = searcher.search_all_platforms(keyword, city, max_results=10)
            
            total_jobs = 0
            for platform, jobs in all_results.items():
                if jobs:
                    total_jobs += len(jobs)
                    print(f"  {platform}: {len(jobs)} 个岗位")
            
            print(f"\n  总计: {total_jobs} 个岗位")
            
        except Exception as e:
            print(f"  搜索失败: {e}")
        
        print("\n" + "=" * 50)


def test_network_connectivity():
    """测试网络连接和各网站可访问性"""
    print("\n" + "=" * 70)
    print("网络连接测试")
    print("=" * 70)
    
    import requests
    from fake_useragent import UserAgent
    
    ua = UserAgent()
    session = requests.Session()
    session.headers.update({'User-Agent': ua.random})
    
    test_urls = [
        ("BOSS直聘", "https://www.zhipin.com"),
        ("智联招聘", "https://www.zhaopin.com"),
        ("前程无忧", "https://www.51job.com"),
    ]
    
    for name, url in test_urls:
        try:
            print(f"\n测试 {name} ({url})...")
            response = session.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"  ✓ 连接成功 (状态码: {response.status_code})")
                print(f"  页面大小: {len(response.text)} 字符")
                
                # 检查是否有反爬提示
                if "验证" in response.text or "captcha" in response.text.lower():
                    print("  ⚠️ 可能触发了反爬验证")
                else:
                    print("  ✓ 页面内容正常")
            else:
                print(f"  ✗ 连接失败 (状态码: {response.status_code})")
                
        except requests.exceptions.Timeout:
            print("  ✗ 连接超时")
        except requests.exceptions.ConnectionError:
            print("  ✗ 连接错误")
        except Exception as e:
            print(f"  ✗ 错误: {e}")


def test_html_structure():
    """测试各网站HTML结构"""
    print("\n" + "=" * 70)
    print("HTML结构测试")
    print("=" * 70)
    
    import requests
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent
    
    ua = UserAgent()
    session = requests.Session()
    session.headers.update({'User-Agent': ua.random})
    
    # 测试BOSS直聘搜索页面
    print("\n测试BOSS直聘搜索页面结构...")
    try:
        search_url = "https://www.zhipin.com/web/geek/job?query=Python&city=101010100"
        response = session.get(search_url, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 保存HTML供分析
            with open('boss_search_page.html', 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            
            print(f"  ✓ 页面获取成功，已保存到 boss_search_page.html")
            
            # 分析页面结构
            print("  分析页面元素...")
            
            # 查找可能的职位列表容器
            containers = soup.find_all(['div', 'ul', 'section'])
            job_containers = []
            
            for container in containers:
                if container.get('class'):
                    class_str = ' '.join(container.get('class'))
                    if 'job' in class_str.lower() or 'list' in class_str.lower():
                        job_containers.append(container)
                        print(f"    发现可能容器: class='{class_str}'")
            
            print(f"  找到 {len(job_containers)} 个可能的职位容器")
            
        else:
            print(f"  ✗ 页面获取失败 (状态码: {response.status_code})")
            
    except Exception as e:
        print(f"  ✗ 错误: {e}")


def create_quick_fix():
    """创建快速修复方案"""
    print("\n" + "=" * 70)
    print("快速修复方案")
    print("=" * 70)
    
    print("""
基于测试结果，建议的快速修复方案：

1. 当前问题:
   - BOSS直聘API有反爬机制
   - 需要更新HTML解析选择器
   - 需要更好的请求头伪装

2. 立即修复步骤:
   
   A. 更新BOSS直聘解析器:
      - 检查 boss_search_page.html 文件
      - 找到正确的职位列表选择器
      - 更新 boss_parser.py 中的选择器
   
   B. 增强请求头:
      - 添加更多请求头字段
      - 实现User-Agent轮换
      - 添加Referer和Cookie
   
   C. 添加延迟:
      - 请求间添加随机延迟
      - 避免频繁请求

3. 备用方案:
   如果HTML解析太困难，考虑:
   - 使用Selenium浏览器自动化
   - 寻找第三方API
   - 使用现成的爬虫库
    """)
    
    # 创建修复脚本
    fix_script = """
# 快速修复脚本 - 增强请求头
import requests
import random
import time

class EnhancedRequester:
    def __init__(self):
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        
    def get_enhanced_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
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
        }
    
    def get_with_retry(self, url, max_retries=3):
        for attempt in range(max_retries):
            try:
                headers = self.get_enhanced_headers()
                response = self.session.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    return response
                else:
                    print(f"尝试 {attempt+1} 失败，状态码: {response.status_code}")
                    
            except Exception as e:
                print(f"尝试 {attempt+1} 失败: {e}")
            
            # 重试前等待
            if attempt < max_retries - 1:
                wait_time = random.uniform(2, 5)
                print(f"等待 {wait_time:.1f} 秒后重试...")
                time.sleep(wait_time)
        
        return None
"""
    
    with open('quick_fix.py', 'w', encoding='utf-8') as f:
        f.write(fix_script)
    
    print(f"\n快速修复脚本已保存到: quick_fix.py")


def main():
    """主测试函数"""
    print("开始测试招聘搜索技能...")
    
    # 测试基础搜索功能
    test_basic_search()
    
    # 测试网络连接
    test_network_connectivity()
    
    # 测试HTML结构
    test_html_structure()
    
    # 创建快速修复方案
    create_quick_fix()
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)
    
    print("""
下一步行动:

1. 查看生成的测试文件:
   - boss_search_page.html - BOSS直聘页面结构
   - quick_fix.py - 快速修复脚本

2. 根据页面结构更新解析器:
   - 打开 boss_search_page.html 查看HTML结构
   - 找到正确的职位列表选择器
   - 更新 boss_parser.py 中的选择器

3. 应用修复:
   - 使用 quick_fix.py 中的增强请求头
   - 添加请求延迟
   - 测试修复效果

4. 如果仍然失败，考虑:
   - 使用Selenium进行浏览器自动化
   - 寻找第三方招聘数据API
   - 使用现成的爬虫框架
    """)


if __name__ == '__main__':
    main()