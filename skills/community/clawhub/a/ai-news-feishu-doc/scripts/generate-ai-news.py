#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 早报生成器
功能：RSS订阅 + 智能摘要 + 多语言支持 + 媒体预览
"""

import os
import sys
import re
import yaml
from datetime import datetime
from xml.etree import ElementTree as ET
import urllib.request
import urllib.error


def get_rss_feed(url):
    """获取 RSS 订阅内容"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read()
    except Exception as e:
        print(f"警告: 无法获取 RSS: {url} - {e}")
        return None


def extract_images(html_content, max_images=3):
    """从 HTML 提取图片"""
    images = []
    pattern = r'<img[^>]+src="([^"]+)"[^>]*>'
    matches = re.findall(pattern, html_content)
    
    for img_url in matches[:max_images]:
        if not re.search(r'icon|logo|avatar|placeholder|1x1', img_url, re.I):
            images.append(img_url)
    
    return images


def get_smart_summary(content, max_length=200):
    """生成智能摘要"""
    # 清理 HTML 标签
    text = re.sub(r'<[^>]+>', '', content)
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&quot;', '"')
    text = text.replace('&amp;', '&')
    
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text.strip()


def test_keyword_match(title, description, keywords):
    """关键词匹配评分"""
    text = f"{title} {description}".lower()
    score = 0
    for keyword in keywords:
        if keyword.lower() in text:
            score += 1
    return score


def parse_rss(xml_content):
    """解析 RSS XML"""
    articles = []
    try:
        root = ET.fromstring(xml_content)
        # 处理 RSS 2.0
        if root.tag == 'rss':
            channel = root.find('channel')
            if channel is not None:
                for item in channel.findall('item'):
                    title = item.findtext('title', '')
                    link = item.findtext('link', '')
                    pub_date = item.findtext('pubDate', '')
                    desc = item.findtext('description', '')
                    articles.append({
                        'title': title,
                        'link': link,
                        'pubDate': pub_date,
                        'description': desc
                    })
        # 处理 Atom
        elif 'feed' in root.tag:
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                title = entry.findtext('{http://www.w3.org/2005/Atom}title', '')
                link = entry.find('{http://www.w3.org/2005/Atom}link')
                link_href = link.get('href', '') if link is not None else ''
                pub_date = entry.findtext('{http://www.w3.org/2005/Atom}updated', '')
                desc = entry.findtext('{http://www.w3.org/2005/Atom}summary', '')
                articles.append({
                    'title': title,
                    'link': link_href,
                    'pubDate': pub_date,
                    'description': desc
                })
    except Exception as e:
        print(f"解析 RSS 失败: {e}")
    
    return articles


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'assets', 'ai-news-rss.yaml')
    
    today = datetime.now().strftime('%Y年%m月%d日')
    output_path = os.path.join(script_dir, f'AI早报_{today}.md')
    
    # 读取配置
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    print("🦞 AI 早报生成器启动...\n")
    
    all_articles = []
    
    for feed in config.get('feeds', []):
        print(f"📡 正在获取: {feed['name']} ...", end='')
        
        xml_content = get_rss_feed(feed['url'])
        if xml_content:
            articles = parse_rss(xml_content)
            max_per_feed = config.get('output', {}).get('max_articles_per_feed', 5)
            
            for article in articles[:max_per_feed]:
                # 解析日期
                pub_date = article.get('pubDate', '')
                try:
                    # 尝试解析 RSS 日期格式
                    dt = datetime.strptime(pub_date[:16], '%a, %d %b %Y')
                    pub_date = dt.strftime('%m-%d')
                except:
                    pub_date = '未知时间'
                
                title = article.get('title', '')
                desc = article.get('description', '')
                
                # 关键词匹配
                keywords = config.get('filters', {}).get('keywords', [])
                score = test_keyword_match(title, desc, keywords)
                
                # 提取图片
                images = extract_images(desc, config.get('media', {}).get('max_images', 3))
                
                # 生成摘要
                summary = get_smart_summary(desc, config.get('summary', {}).get('max_length', 200))
                
                all_articles.append({
                    'title': title,
                    'link': article.get('link', ''),
                    'pubDate': pub_date,
                    'summary': summary,
                    'images': images,
                    'source': feed['name'],
                    'category': feed.get('category', ''),
                    'language': feed.get('language', 'zh'),
                    'score': score
                })
            
            print(f" ✅ 获取 {len(articles[:max_per_feed])} 篇")
        else:
            print(" ❌ 失败")
    
    print(f"\n📝 共获取 {len(all_articles)} 篇文章，正在生成早报...")
    
    # 排序并选取 Top N
    all_articles.sort(key=lambda x: x['score'], reverse=True)
    total_max = config.get('output', {}).get('total_max_articles', 15)
    top_articles = all_articles[:total_max]
    
    # 分类
    cn_articles = [a for a in top_articles if a['language'] == 'zh']
    en_articles = [a for a in top_articles if a['language'] in ('en', 'mixed')]
    
    # 生成 Markdown
    content = f"""# 📰 AI 早报 | {today}

> 自动采集 {len(config.get('feeds', []))} 个信源 | 精选 {len(top_articles)} 篇 | 由 OpenClaw 驱动

---

## 🔥 头版头条

"""
    
    # 头版头条
    for article in top_articles[:3]:
        content += f"""### {article['title']}
📍 **{article['source']}** | 🕐 {article['pubDate']}

💡 {article['summary']}

🔗 [阅读全文]({article['link']})

"""
        if article['images']:
            for img in article['images']:
                content += f"![图片]({img})\n"
            content += "\n"
    
    # 国内 AI 动态
    if cn_articles:
        content += "---\n\n## 🇨🇳 国内 AI 动态\n\n"
        for article in cn_articles[:5]:
            content += f"""### {article['title']}
**来源：** {article['source']} | **时间：** {article['pubDate']}

{article['summary']}

🔗 [阅读原文]({article['link']})

"""
    
    # 海外 AI 动态
    if en_articles:
        content += "---\n\n## 🌍 海外 AI 动态\n\n"
        for article in en_articles[:5]:
            content += f"""### {article['title']}
**Source:** {article['source']} | **Time:** {article['pubDate']}

{article['summary']}

🔗 [Read Original]({article['link']})

"""
    
    # 总结
    if top_articles:
        content += f"""---

## 🎯 今日总结

> 今日 AI 圈最值得关注的是：**{top_articles[0]['title']}**

---

*🦞 由 大龙虾 AI 早报系统自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # 保存文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ 早报已生成: {output_path}")
    print(f"📊 统计信息:")
    print(f"   - 国内文章: {len(cn_articles)} 篇")
    print(f"   - 海外文章: {len(en_articles)} 篇")
    print(f"   - 头版头条: 3 篇")
    
    return output_path


if __name__ == '__main__':
    main()
