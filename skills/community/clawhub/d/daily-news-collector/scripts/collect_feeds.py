#!/usr/bin/env python3
"""
RSS源数据收集脚本
从配置文件读取RSS源列表，解析并获取最新文章
"""

import json
import argparse
from datetime import datetime
from feedparser import parse
from typing import List, Dict, Any


def load_config(config_path: str) -> Dict[str, Any]:
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise ValueError(f"配置文件不存在: {config_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"配置文件格式错误: {e}")


def collect_rss_source(source: Dict[str, str], limit: int = 20) -> List[Dict[str, Any]]:
    """
    收集单个RSS源的文章

    参数:
        source: RSS源配置，包含url、name、category等字段
        limit: 每个源最多收集的文章数

    返回:
        文章列表
    """
    url = source.get('url')
    name = source.get('name', '未知来源')
    category = source.get('category', '未分类')

    if not url:
        print(f"警告: 来源 {name} 缺少URL配置")
        return []

    try:
        feed = parse(url)
        if feed.bozo:
            print(f"警告: RSS源 {name} 解析错误: {feed.bozo_exception}")
            return []

        articles = []
        for entry in feed.entries[:limit]:
            article = {
                'title': entry.get('title', '无标题'),
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
                'summary': entry.get('summary', '')[:500],  # 限制摘要长度
                'source': name,
                'category': category,
                'collected_at': datetime.now().isoformat()
            }
            articles.append(article)

        print(f"成功收集 {name}: {len(articles)} 篇文章")
        return articles

    except Exception as e:
        print(f"错误: 收集 {name} 失败: {str(e)}")
        return []


def main():
    parser = argparse.ArgumentParser(description='收集RSS源数据')
    parser.add_argument('--config', required=True, help='配置文件路径（JSON格式）')
    parser.add_argument('--output', required=True, help='输出文件路径（JSON格式）')
    parser.add_argument('--limit', type=int, default=20, help='每个源最多收集的文章数')
    args = parser.parse_args()

    # 加载配置
    config = load_config(args.config)
    sources = config.get('sources', [])

    if not sources:
        raise ValueError("配置文件中未定义任何RSS源")

    # 收集所有源的数据
    all_articles = []
    for source in sources:
        articles = collect_rss_source(source, args.limit)
        all_articles.extend(articles)

    # 输出结果
    output_data = {
        'collected_at': datetime.now().isoformat(),
        'total_articles': len(all_articles),
        'sources_count': len(sources),
        'articles': all_articles
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n收集完成: 共 {len(all_articles)} 篇文章，来自 {len(sources)} 个RSS源")
    print(f"结果已保存到: {args.output}")


if __name__ == '__main__':
    main()
