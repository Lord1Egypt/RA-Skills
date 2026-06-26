#!/usr/bin/env python3
"""
Bilibili 视频数据分析脚本
使用方法: python analyze_data.py data.json
"""

import json
import sys
from datetime import datetime
from collections import Counter
import re

def parse_count(count_str):
    """解析播放量和评论数（支持万、亿单位）"""
    count_str = count_str.strip()
    if not count_str:
        return 0
    
    # 移除单位并转换
    if '万' in count_str:
        return float(count_str.replace('万', '').strip()) * 10000
    elif '亿' in count_str:
        return float(count_str.replace('亿', '').strip()) * 100000000
    else:
        try:
            return float(count_str)
        except:
            return 0

def parse_date(date_str):
    """解析日期字符串"""
    date_str = date_str.strip().replace('·', '').strip()
    
    # 处理相对时间
    if '小时前' in date_str:
        return datetime.now().strftime('%Y-%m-%d')
    elif '昨天' in date_str:
        from datetime import timedelta
        return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    elif '前天' in date_str:
        from datetime import timedelta
        return (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    elif '天前' in date_str:
        days = int(re.search(r'\d+', date_str).group())
        from datetime import timedelta
        return (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    elif '周前' in date_str:
        weeks = int(re.search(r'\d+', date_str).group())
        from datetime import timedelta
        return (datetime.now() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')
    elif re.match(r'\d{2}-\d{2}', date_str):
        # 格式: MM-DD
        year = datetime.now().year
        return f"{year}-{date_str}"
    elif re.match(r'\d{4}-\d{2}-\d{2}', date_str):
        return date_str
    else:
        return date_str

def analyze_data(data):
    """分析视频数据"""
    total = len(data)
    
    # 作者统计
    authors = Counter([v['author'] for v in data])
    top_authors = authors.most_common(10)
    
    # 时间分布
    dates = [parse_date(v['date']) for v in data]
    date_counter = Counter(dates)
    
    # 评论数分布
    comments = [parse_count(v['commentCount']) for v in data]
    comment_ranges = {
        '0评论': sum(1 for c in comments if c == 0),
        '1-10评论': sum(1 for c in comments if 1 <= c <= 10),
        '11-50评论': sum(1 for c in comments if 11 <= c <= 50),
        '51-100评论': sum(1 for c in comments if 51 <= c <= 100),
        '100+评论': sum(1 for c in comments if c > 100)
    }
    
    # 播放量分布
    plays = [parse_count(v['playCount']) for v in data]
    play_ranges = {
        '0-500': sum(1 for p in plays if p <= 500),
        '500-1K': sum(1 for p in plays if 500 < p <= 1000),
        '1K-5K': sum(1 for p in plays if 1000 < p <= 5000),
        '5K-1万': sum(1 for p in plays if 5000 < p <= 10000),
        '1万+': sum(1 for p in plays if p > 10000)
    }
    
    # 热门视频
    hot_videos = sorted(data, key=lambda x: parse_count(x['commentCount']), reverse=True)[:5]
    most_played = sorted(data, key=lambda x: parse_count(x['playCount']), reverse=True)[:5]
    
    return {
        'total': total,
        'top_authors': top_authors,
        'comment_ranges': comment_ranges,
        'play_ranges': play_ranges,
        'hot_videos': hot_videos,
        'most_played': most_played,
        'date_counter': date_counter
    }

def generate_report(analysis, keyword):
    """生成Markdown格式报告"""
    report = f"""## 📊 Bilibili "{keyword}" 搜索结果统计报告

### 📈 总体数据
- **视频总数**: {analysis['total']}个
- **采集时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

### 👥 活跃作者 TOP 10

| 排名 | 作者 | 视频数 |
|------|------|--------|
"""
    for i, (author, count) in enumerate(analysis['top_authors'], 1):
        report += f"| {i} | **{author}** | {count} |\n"
    
    report += """
---

### 💬 评论数分布

| 评论数范围 | 视频数 | 占比 |
|------------|--------|------|
"""
    for range_name, count in analysis['comment_ranges'].items():
        percentage = (count / analysis['total'] * 100) if analysis['total'] > 0 else 0
        report += f"| **{range_name}** | {count} | {percentage:.1f}% |\n"
    
    report += """
---

### 👁️ 播放量分布

| 播放量范围 | 视频数 | 占比 |
|------------|--------|------|
"""
    for range_name, count in analysis['play_ranges'].items():
        percentage = (count / analysis['total'] * 100) if analysis['total'] > 0 else 0
        report += f"| **{range_name}** | {count} | {percentage:.1f}% |\n"
    
    report += """
---

### 🔥 热门视频（评论数TOP 5）

| 排名 | 标题 | 作者 | 评论数 |
|------|------|------|--------|
"""
    for i, video in enumerate(analysis['hot_videos'], 1):
        report += f"| {i} | {video['title'][:30]}... | {video['author']} | **{video['commentCount']}** |\n"
    
    report += """
---

### 🎬 高播放量视频TOP 5

| 排名 | 标题 | 作者 | 播放量 |
|------|------|------|--------|
"""
    for i, video in enumerate(analysis['most_played'], 1):
        report += f"| {i} | {video['title'][:30]}... | {video['author']} | **{video['playCount']}** |\n"
    
    report += """
---

### 🎯 关键发现

1. **内容活跃度**: 根据发帖时间分布分析
2. **头部作者**: TOP 3作者贡献了主要内容
3. **互动情况**: 评论互动分布分析
4. **播放表现**: 播放量分布分析

---

### 📝 建议

- **创作方向**: 基于热门内容分析
- **发布时间**: 选择合适的时间发布
- **互动策略**: 提高用户参与度
"""
    
    return report

def main():
    if len(sys.argv) < 2:
        print("使用方法: python analyze_data.py data.json")
        sys.exit(1)
    
    data_file = sys.argv[1]
    
    # 读取数据
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 分析数据
    analysis = analyze_data(data)
    
    # 生成报告
    parts = data_file.split('_')
    keyword = parts[2] if len(parts) >= 3 else "Unknown"
    report = generate_report(analysis, keyword)
    
    # 输出报告
    print(report)
    
    # 保存报告
    report_file = f"bilibili_report_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n报告已保存到: {report_file}")

if __name__ == "__main__":
    main()
