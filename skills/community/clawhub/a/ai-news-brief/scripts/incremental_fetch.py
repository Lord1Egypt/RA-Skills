#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据持久化和增量抓取模块
功能：
1. 保存抓取结果到本地
2. 增量抓取 - 只抓取新内容
3. 历史查询支持
"""

import sys
import io
import os
import json
from datetime import datetime, timedelta

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
HISTORY_FILE = os.path.join(DATA_DIR, "news_history.json")
POLICY_HISTORY_FILE = os.path.join(DATA_DIR, "policy_history.json")


def ensure_data_dir():
    """确保数据目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_history(file_path=HISTORY_FILE):
    """加载历史记录"""
    ensure_data_dir()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"articles": [], "last_update": ""}


def save_history(history, articles, file_path=HISTORY_FILE):
    """保存历史记录"""
    ensure_data_dir()
    history["articles"] = articles[:1000]  # 最多保留1000条
    history["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def get_new_articles(articles, history_file=HISTORY_FILE):
    """
    获取新增的文章（增量抓取）
    只返回之前没有抓取过的
    """
    history = load_history(history_file)
    existing_titles = set()
    
    for article in history.get("articles", []):
        key = article.get("title", "")[:30]
        existing_titles.add(key)
    
    new_articles = []
    for article in articles:
        title_key = article.get("title", "")[:30]
        if title_key not in existing_titles:
            new_articles.append(article)
    
    return new_articles, history


def save_with_incremental(new_articles, history_file=HISTORY_FILE):
    """保存新增文章并更新历史"""
    if not new_articles:
        return 0
    
    history = load_history(history_file)
    
    # 合并新旧文章（新的在前）
    all_articles = new_articles + history.get("articles", [])
    
    # 限制保存数量
    if "policy" in history_file:
        max_articles = 500
    else:
        max_articles = 1000
    
    all_articles = all_articles[:max_articles]
    
    # 保存
    history["articles"] = all_articles
    history["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    return len(new_articles)


def get_articles_by_date(days=7, history_file=HISTORY_FILE):
    """
    查询最近几天的资讯
    """
    history = load_history(history_file)
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    recent = []
    for article in history.get("articles", []):
        # 从URL或内容中提取日期
        date = article.get("date", "")
        if date and date >= cutoff:
            recent.append(article)
        elif not date:
            # 如果没有日期，也返回（可能是最近的）
            recent.append(article)
    
    return recent


def get_article_stats(history_file=HISTORY_FILE):
    """获取资讯统计"""
    history = load_history(history_file)
    articles = history.get("articles", [])
    
    # 按来源统计
    source_counts = {}
    for a in articles:
        src = a.get("source", "未知")
        source_counts[src] = source_counts.get(src, 0) + 1
    
    # 按类型统计
    type_counts = {}
    for a in articles:
        t = a.get("type", "news")
        type_counts[t] = type_counts.get(t, 0) + 1
    
    return {
        "total": len(articles),
        "by_source": source_counts,
        "by_type": type_counts,
        "last_update": history.get("last_update", "未知")
    }


# ========== 对外接口 ==========

def fetch_with_incremental(fetch_func, fetch_args, use_incremental=True):
    """
    带增量抓取的获取接口
    
    参数:
        fetch_func: 获取函数
        fetch_args: 获取函数参数
        use_incremental: 是否使用增量模式
    
    返回:
        (new_articles, all_articles)
    """
    print("\n" + "="*50)
    if use_incremental:
        print("📌 增量抓取模式 - 只获取新内容")
        print("="*50)
        
        # 先抓取
        all_articles = fetch_func(*fetch_args)
        
        # 获取新增
        new_articles = get_new_articles(all_articles)
        
        # 保存
        if new_articles:
            saved = save_with_incremental(new_articles)
            print(f"\n✅ 新增 {saved} 条，已保存到历史记录")
        else:
            print(f"\n✅ 没有新增内容")
        
        return new_articles, all_articles
    
    else:
        print("📌 全量抓取模式 - 获取所有内容")
        print("="*50)
        
        articles = fetch_func(*fetch_args)
        
        # 全量保存
        history = load_history()
        save_history(history, articles)
        
        return articles, articles


# ========== 测试 ==========

def test_history():
    """测试历史功能"""
    print("=" * 50)
    print("历史记录测试")
    print("=" * 50)
    
    # 测试统计
    stats = get_article_stats()
    print(f"\n📊 资讯统计:")
    print(f"  总数: {stats['total']}")
    print(f"  最后更新: {stats['last_update']}")
    print(f"  来源分布: {stats['by_source']}")
    
    # 测试查询最近3天
    recent = get_articles_by_date(days=3)
    print(f"\n📅 最近3天资讯: {len(recent)}条")


if __name__ == "__main__":
    test_history()