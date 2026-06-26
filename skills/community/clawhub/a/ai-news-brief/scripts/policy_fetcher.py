#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
政策资讯抓取模块
专门抓取政府官网的政策、通知、公告
"""

import sys
import io
import os
import json
import re

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import requests
from bs4 import BeautifulSoup

# 政策资讯来源
POLICY_SOURCES = [
    {
        "name": "中国政府网",
        "url": "http://www.gov.cn/xinwen/yaowen.htm",
        "rss": "http://www.gov.cn/rss",
        "keywords": ["政策", "国务院", "办公厅", "通知", "意见"],
        "category": "中央政策"
    },
    {
        "name": "工信部",
        "url": "https://www.miit.gov.cn/gxscytj/wjgs/index.html",
        "rss": None,
        "keywords": ["工信部", "工业和信息化", "通知", "公告", "政策"],
        "category": "部委政策"
    },
    {
        "name": "科技部",
        "url": "https://www.most.gov.cn/zyxw/index.htm",
        "rss": None,
        "keywords": ["科技部", "科技创新", "项目", "通知", "指南"],
        "category": "部委政策"
    },
    {
        "name": "网信办",
        "url": "http://www.cac.gov.cn/",
        "rss": None,
        "keywords": ["网信办", "网络安全", "人工智能", "算法", "规定"],
        "category": "部委政策"
    },
    {
        "name": "发改委",
        "url": "https://www.ndrc.gov.cn/xwzx/zyw/",
        "rss": None,
        "keywords": ["发改委", "发展改革", "项目", "批复", "通知"],
        "category": "部委政策"
    },
    {
        "name": "教育部",
        "url": "http://www.moe.gov.cn/jyb_xwfb/gzdt_gazt/",
        "rss": None,
        "keywords": ["教育部", "教育", "AI", "人工智能", "通知"],
        "category": "部委政策"
    },
    {
        "name": "财政部",
        "url": "http://www.mof.gov.cn/gks/mofed/",
        "rss": None,
        "keywords": ["财政部", "财政", "补贴", "AI", "科技"],
        "category": "部委政策"
    },
    {
        "name": "国家数据局",
        "url": "https://www.ndc.gov.cn/",
        "rss": None,
        "keywords": ["国家数据局", "数据", "AI", "算力", "政策"],
        "category": "新机构"
    }
]

# 扩展的关键词列表 - 针对政策
POLICY_KEYWORDS = [
    '政策', '通知', '公告', '意见', '方案', '规划', '纲要',
    '人工智能', 'AI', '大模型', '算力', '芯片', '半导体',
    '数字经济', '数字化', '智能化', '科技创新',
    '补贴', '扶持', '专项资金', '项目', '申报',
    '管理办法', '实施细则', '工作方案',
    '国务院', '部委', '办公厅', '发文字号'
]


def fetch_policy_via_http(url, source_name, category):
    """通过HTTP获取政策资讯"""
    results = []
    
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        
        resp = session.get(url, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 移除脚本和样式
        for s in soup(['script', 'style', 'nav', 'footer', 'header']):
            s.decompose()
        
        # 查找所有链接
        for a in soup.find_all('a', href=True):
            text = a.get_text(strip=True)
            href = a.get('href', '')
            
            # 过滤条件
            if len(text) < 10 or len(text) > 80:
                continue
            
            # 处理URL
            if href.startswith('//'):
                href = 'https:' + href
            elif href.startswith('/'):
                try:
                    base = '/'.join(url.split('/')[:3])
                    href = base + href
                except:
                    continue
            elif not href.startswith('http'):
                continue
            
            # 检查关键词
            text_lower = text.lower()
            if any(kw in text_lower for kw in POLICY_KEYWORDS):
                results.append({
                    'title': text[:150],
                    'url': href[:300],
                    'source': source_name,
                    'category': category,
                    'type': 'policy',
                    'method': 'http'
                })
        
    except Exception as e:
        print(f"  抓取失败: {str(e)[:50]}")
    
    return results


def fetch_all_policies(days=1):
    """获取所有政策资讯"""
    all_results = []
    
    print("=" * 50)
    print("开始抓取政策资讯...")
    print("=" * 50)
    
    for source in POLICY_SOURCES:
        name = source['name']
        url = source['url']
        category = source['category']
        
        print(f"\n[{name}] 正在抓取...")
        
        try:
            results = fetch_policy_via_http(url, name, category)
            print(f"  -> 找到 {len(results)} 条政策资讯")
            all_results.extend(results)
        except Exception as e:
            print(f"  -> 失败: {str(e)[:30]}")
    
    # 去重
    seen = set()
    unique = []
    for r in all_results:
        key = r['title'][:25]
        if key not in seen:
            seen.add(key)
            unique.append(r)
    
    print(f"\n共抓取 {len(unique)} 条政策资讯")
    
    return unique


# ========== 增量抓取配置 ==========

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
POLICY_HISTORY_FILE = os.path.join(DATA_DIR, "policy_history.json")


def ensure_data_dir():
    """确保数据目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_policy_history():
    """加载历史政策记录"""
    ensure_data_dir()
    try:
        with open(POLICY_HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"articles": [], "last_update": ""}


def save_policy_history(history, articles):
    """保存政策历史"""
    ensure_data_dir()
    history["articles"] = articles[:500]  # 最多保留500条
    history["last_update"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    with open(POLICY_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def get_new_policies(articles):
    """
    获取新增的政策资讯（增量抓取）
    只返回之前没有抓取过的
    """
    history = load_policy_history()
    existing_titles = set()
    
    for article in history.get("articles", []):
        existing_titles.add(article.get("title", "")[:30])
    
    new_articles = []
    for article in articles:
        title_key = article.get("title", "")[:30]
        if title_key not in existing_titles:
            new_articles.append(article)
    
    if new_articles:
        print(f"\n🆕 发现 {len(new_articles)} 条新政策资讯")
        # 更新历史
        all_articles = new_articles + history.get("articles", [])
        save_policy_history(history, all_articles)
    else:
        print("\n✅ 没有新的政策资讯")
    
    return new_articles


def test_policy_fetch():
    """测试政策抓取"""
    print("测试政策资讯抓取...")
    articles = fetch_all_policies()
    
    # 显示部分结果
    print("\n前5条政策资讯:")
    for i, a in enumerate(articles[:5], 1):
        print(f"  {i}. [{a['source']}] {a['title'][:50]}")
    
    return articles


if __name__ == "__main__":
    test_policy_fetch()