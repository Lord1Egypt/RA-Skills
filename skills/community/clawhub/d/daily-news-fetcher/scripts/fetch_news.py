#!/usr/bin/env python3
"""
Daily News Fetcher - Fetch top 5 news headlines with summaries from mainstream sources
"""

import json
import urllib.request
import urllib.error
from datetime import datetime
from html.parser import HTMLParser


class NewsHTMLParser(HTMLParser):
    """Simple HTML parser to extract text content"""
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.current_tag = None
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        
    def handle_data(self, data):
        if self.current_tag not in ['script', 'style']:
            text = data.strip()
            if text and len(text) > 20:
                self.text_content.append(text)


def fetch_rss_feed(url, source_name):
    """Fetch and parse RSS feed"""
    news_items = []
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)',
                'Accept': 'application/rss+xml, application/xml, text/xml'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
            
        # Simple RSS parsing
        items = content.split('<item>')
        for item in items[1:]:  # Skip header
            title = ''
            link = ''
            description = ''
            
            # Extract title
            if '<title>' in item and '</title>' in item:
                start = item.find('<title>') + 7
                end = item.find('</title>')
                title = item[start:end].strip()
                # Remove CDATA if present
                title = title.replace('<![CDATA[', '').replace(']]>', '')
            
            # Extract link
            if '<link>' in item and '</link>' in item:
                start = item.find('<link>') + 6
                end = item.find('</link>')
                link = item[start:end].strip()
            
            # Extract description
            if '<description>' in item and '</description>' in item:
                start = item.find('<description>') + 13
                end = item.find('</description>')
                description = item[start:end].strip()
                # Remove HTML tags and CDATA
                description = description.replace('<![CDATA[', '').replace(']]>', '')
                # Simple tag removal
                import re
                description = re.sub(r'<[^>]+>', '', description)
                if len(description) > 150:
                    description = description[:150] + '...'
            
            if title and link:
                news_items.append({
                    'title': title,
                    'link': link,
                    'description': description if description else '暂无摘要',
                    'source': source_name
                })
                
    except Exception as e:
        pass
    
    return news_items


def fetch_news():
    """Fetch news from multiple sources"""
    all_news = []
    
    # RSS feeds - using public RSS endpoints
    feeds = [
        ('https://feeds.bbci.co.uk/news/rss.xml', 'BBC'),
        ('http://www.xinhuanet.com/english/news_english.xml', '新华网'),
        ('https://rss.nytimes.com/services/xml/rss/nyt/World.xml', 'NYTimes'),
    ]
    
    for url, source in feeds:
        try:
            items = fetch_rss_feed(url, source)
            all_news.extend(items)
        except:
            continue
    
    # Deduplicate by title similarity
    unique_news = []
    seen_titles = set()
    
    for item in all_news:
        title_lower = item['title'].lower()
        # Check if similar title already exists
        is_duplicate = False
        for seen in seen_titles:
            # Simple similarity check
            common_words = set(title_lower.split()) & set(seen.split())
            if len(common_words) > 3:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_news.append(item)
            seen_titles.add(title_lower)
    
    # Return top 5
    return unique_news[:5]


def format_output(news_items):
    """Format news items for output"""
    if not news_items:
        return "⚠️ 暂时无法获取新闻，请稍后再试。"
    
    today = datetime.now().strftime('%Y年%m月%d日')
    
    lines = [
        f"📰 今日新闻摘要 ({today})",
        "━━━━━━━━━━━━━━━━━━━━",
        ""
    ]
    
    for i, item in enumerate(news_items, 1):
        emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣'][i-1]
        lines.append(f"{emoji} {item['title']}")
        lines.append(f"   来源：{item['source']}")
        if item['description'] and item['description'] != '暂无摘要':
            lines.append(f"   摘要：{item['description']}")
        lines.append("")
    
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("💡 数据来源：BBC、新华网、NYTimes")
    
    return '\n'.join(lines)


def main():
    """Main entry point"""
    news = fetch_news()
    output = format_output(news)
    print(output)


if __name__ == '__main__':
    main()
