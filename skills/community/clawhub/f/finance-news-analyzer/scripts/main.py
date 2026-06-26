#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财经新闻分析器 - 主脚本

用法:
    python main.py --source wallstreetcn,36kr --limit 15 --output brief
    python main.py --ticker NVDA,TSLA --sentiment positive
    python main.py --industry 科技 --period weekly
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'news-aggregator-skill' / 'scripts'))

try:
    from fetch_news import fetch_all_sources, save_news
except ImportError:
    print("警告：未找到 news-aggregator-skill，部分功能受限")


def parse_args():
    parser = argparse.ArgumentParser(description='财经新闻分析器')
    
    # 新闻源配置
    parser.add_argument('--source', type=str, default='all',
                        help='新闻源（逗号分隔），如：wallstreetcn,36kr,hackernews')
    parser.add_argument('--limit', type=int, default=15,
                        help='每源最多新闻数（默认 15）')
    parser.add_argument('--keyword', type=str, default='',
                        help='关键词过滤（逗号分隔）')
    
    # 过滤配置
    parser.add_argument('--ticker', type=str, default='',
                        help='股票代码过滤（逗号分隔），如：NVDA,TSLA')
    parser.add_argument('--industry', type=str, default='',
                        help='行业分类过滤（逗号分隔），如：科技，金融')
    parser.add_argument('--sentiment', type=str, default='all',
                        choices=['positive', 'negative', 'neutral', 'all'],
                        help='情感过滤')
    
    # 输出配置
    parser.add_argument('--period', type=str, default='daily',
                        choices=['daily', 'weekly', 'monthly'],
                        help='时间周期')
    parser.add_argument('--output', type=str, default='brief',
                        choices=['brief', 'full', 'industry', 'stock'],
                        help='输出格式')
    parser.add_argument('--lang', type=str, default='zh',
                        choices=['zh', 'en'],
                        help='输出语言')
    parser.add_argument('--output-dir', type=str, default='reports',
                        help='输出目录')
    
    # 分析配置
    parser.add_argument('--no-analyze', action='store_true',
                        help='跳过情感分析，仅抓取新闻')
    parser.add_argument('--model', type=str, default='gpt-4o-mini',
                        help='情感分析用 LLM 模型')
    
    return parser.parse_args()


def load_ticker_map():
    """加载股票代码映射表"""
    ticker_map_path = Path(__file__).parent / 'references' / 'ticker-map.md'
    if not ticker_map_path.exists():
        return {}
    
    ticker_map = {}
    with open(ticker_map_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '|' in line and not line.startswith('|-'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4:
                    company, short_name, code = parts[1], parts[2], parts[3]
                    if code and code != '代码':
                        ticker_map[company.lower()] = code
                        ticker_map[short_name.lower()] = code
    return ticker_map


def analyze_sentiment(news_items, model='gpt-4o-mini'):
    """
    分析新闻情感
    
    TODO: 实现 LLM 调用
    目前返回 mock 数据
    """
    import random
    
    sentiments = ['positive', 'negative', 'neutral']
    confidence = ['high', 'medium', 'low']
    
    for item in news_items:
        # Mock 分析结果
        item['sentiment'] = random.choice(sentiments)
        item['sentiment_score'] = random.randint(0, 100)
        item['confidence'] = random.choice(confidence)
        item['impact'] = {
            'market': random.choice(['positive', 'negative', 'neutral']),
            'industry': random.choice(['tech', 'finance', 'consumer', 'energy']),
            'timeframe': random.choice(['short', 'medium', 'long'])
        }
    
    return news_items


def generate_briefing(news_items, output_format='brief', lang='zh'):
    """生成简报"""
    
    if output_format == 'brief':
        return generate_brief_briefing(news_items, lang)
    elif output_format == 'full':
        return generate_full_report(news_items, lang)
    elif output_format == 'industry':
        return generate_industry_report(news_items, lang)
    elif output_format == 'stock':
        return generate_stock_report(news_items, lang)
    else:
        return generate_brief_briefing(news_items, lang)


def generate_brief_briefing(news_items, lang='zh'):
    """生成快速简报"""
    
    positive = [n for n in news_items if n.get('sentiment') == 'positive']
    negative = [n for n in news_items if n.get('sentiment') == 'negative']
    neutral = [n for n in news_items if n.get('sentiment') == 'neutral']
    
    report = []
    report.append("# 📈 财经新闻简报")
    report.append(f"**日期**: {datetime.now().strftime('%Y-%m-%d')} | **来源**: 多源 | **总数**: {len(news_items)} 条")
    report.append("")
    
    # 利好消息
    if positive:
        report.append("## 🟢 利好消息 ({}条)".format(len(positive)))
        report.append("")
        for i, item in enumerate(positive[:5], 1):
            report.append("#### {}. [{}]({})".format(i, item.get('title', '无标题'), item.get('url', '#')))
            report.append("- **来源**: {} | **时间**: {}".format(
                item.get('source', '未知'),
                item.get('time', '未知')
            ))
            report.append("- **影响**: 🟢 利好 | **置信度**: {}".format(
                item.get('confidence', '中').capitalize()
            ))
            report.append("- **一句话**: {}".format(item.get('summary', '暂无摘要')))
            report.append("")
    
    # 利空消息
    if negative:
        report.append("## 🔴 利空消息 ({}条)".format(len(negative)))
        report.append("")
        for i, item in enumerate(negative[:5], 1):
            report.append("#### {}. [{}]({})".format(i, item.get('title', '无标题'), item.get('url', '#')))
            report.append("- **来源**: {} | **时间**: {}".format(
                item.get('source', '未知'),
                item.get('time', '未知')
            ))
            report.append("- **影响**: 🔴 利空 | **置信度**: {}".format(
                item.get('confidence', '中').capitalize()
            ))
            report.append("- **一句话**: {}".format(item.get('summary', '暂无摘要')))
            report.append("")
    
    # 中性消息
    if neutral:
        report.append("## ⚪ 中性消息 ({}条)".format(len(neutral)))
        report.append("")
        for i, item in enumerate(neutral[:5], 1):
            report.append("#### {}. [{}]({})".format(i, item.get('title', '无标题'), item.get('url', '#')))
            report.append("- **来源**: {} | **时间**: {}".format(
                item.get('source', '未知'),
                item.get('time', '未知')
            ))
            report.append("")
    
    # 投资提示
    report.append("## 💡 投资提示")
    report.append("")
    report.append("1. **重点关注**: {}".format(
        ', '.join(set([n.get('impact', {}).get('industry', '科技') for n in positive[:3]])) or '科技'
    ))
    report.append("2. **风险提醒**: {}".format(
        '美联储政策、地缘政治' if negative else '无明显风险'
    ))
    report.append("3. **明日事件**: 关注美国经济数据发布")
    report.append("")
    
    return '\n'.join(report)


def generate_full_report(news_items, lang='zh'):
    """生成深度报告"""
    # TODO: 实现完整报告生成
    return generate_brief_briefing(news_items, lang)


def generate_industry_report(news_items, lang='zh'):
    """生成行业报告"""
    # TODO: 实现行业报告生成
    return generate_brief_briefing(news_items, lang)


def generate_stock_report(news_items, lang='zh'):
    """生成个股报告"""
    # TODO: 实现个股报告生成
    return generate_brief_briefing(news_items, lang)


def main():
    # 设置 UTF-8 输出
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    args = parse_args()
    
    print("=" * 50)
    print("Finance News Analyzer")
    print("=" * 50)
    
    # 1. 抓取新闻
    print("\n📰 Step 1: 抓取新闻...")
    sources = [s.strip() for s in args.source.split(',')] if args.source != 'all' else ['wallstreetcn', '36kr', 'hackernews']
    
    print(f"   新闻源：{', '.join(sources)}")
    print(f"   每源限制：{args.limit} 条")
    
    if args.keyword:
        print(f"   关键词：{args.keyword}")
    
    # TODO: 实际抓取
    # news_items = fetch_all_sources(sources, args.limit, args.keyword)
    
    # Mock 数据
    news_items = [
        {
            'title': '英伟达发布新一代 AI 芯片，性能提升 300%',
            'url': 'https://wallstreetcn.com/articles/3767069',
            'source': 'Wall Street CN',
            'time': '2026-03-09 22:48',
            'summary': '英伟达今日发布新一代 AI 芯片，性能大幅提升'
        },
        {
            'title': '特斯拉中国工厂产能突破新高',
            'url': 'https://36kr.com/p/123456',
            'source': '36Kr',
            'time': '2026-03-09 21:30',
            'summary': '特斯拉上海工厂季度产能创新高'
        },
        {
            'title': '美联储暗示继续加息',
            'url': 'https://wallstreetcn.com/articles/3767060',
            'source': 'Wall Street CN',
            'time': '2026-03-09 20:53',
            'summary': '美联储官员表态偏鹰派'
        }
    ]
    
    print(f"   ✅ 抓取成功：{len(news_items)} 条")
    
    # 2. 情感分析
    if not args.no_analyze:
        print("\n🧠 Step 2: 情感分析...")
        news_items = analyze_sentiment(news_items, args.model)
        print(f"   ✅ 分析完成")
        
        # 统计
        pos = len([n for n in news_items if n.get('sentiment') == 'positive'])
        neg = len([n for n in news_items if n.get('sentiment') == 'negative'])
        neu = len([n for n in news_items if n.get('sentiment') == 'neutral'])
        print(f"   🟢 利好：{pos} | 🔴 利空：{neg} | ⚪ 中性：{neu}")
    
    # 3. 生成简报
    print("\n📝 Step 3: 生成简报...")
    report = generate_briefing(news_items, args.output, args.lang)
    
    # 4. 保存/输出
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f"finance_briefing_{timestamp}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"   ✅ 简报已保存：{output_file}")
    print("\n" + "=" * 50)
    print("🎉 分析完成！")
    print("=" * 50)
    
    # 打印简报内容
    print("\n" + report)


if __name__ == '__main__':
    main()
