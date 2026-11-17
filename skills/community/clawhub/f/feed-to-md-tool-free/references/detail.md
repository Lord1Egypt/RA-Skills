# 详细参考 - feed-to-md-tool-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

class RSSParser:
    """RSS解析器（免费版）"""

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def fetch(self, url, timeout=10):
        """获取RSS源"""
        try:
            response = requests.get(url, timeout=timeout, headers=self.headers)
            if response.status_code == 200:
                return response.content
            return None
        except Exception as e:
            print(f"获取失败：{e}")
            return None

    def parse(self, xml_content):
        """解析RSS XML"""
        try:
            root = ET.fromstring(xml_content)
            channel = root.find('channel')

            if channel is None:
                return self._parse_atom(root)

            return self._parse_rss(channel)
        except ET.ParseError as e:
            print(f"解析失败：{e}")
            return None

    def _parse_rss(self, channel):
        """解析RSS 2.0格式"""
        feed_info = {
            'title': self._get_text(channel, 'title'),
            'description': self._get_text(channel, 'description'),
            'link': self._get_text(channel, 'link'),
            'last_build_date': self._get_text(channel, 'lastBuildDate'),
            'items': []
        }

        for item in channel.findall('item'):
            entry = {
                'title': self._get_text(item, 'title'),
                'link': self._get_text(item, 'link'),
                'description': self._get_text(item, 'description'),
                'pub_date': self._get_text(item, 'pubDate'),
                'guid': self._get_text(item, 'guid'),
                'author': self._get_text(item, 'author') or self._get_text(item, '{http://purl.org/dc/elements/1.1/}creator')
            }
            feed_info['items'].append(entry)

        return feed_info

    def _parse_atom(self, root):
        """解析Atom格式"""
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        feed_info = {
            'title': self._get_text(root, 'atom:title', ns),
            'description': self._get_text(root, 'atom:subtitle', ns),
            'link': '',
            'last_build_date': self._get_text(root, 'atom:updated', ns),
            'items': []
        }

        link_elem = root.find('atom:link', ns)
        if link_elem is not None:
            feed_info['link'] = link_elem.get('href', '')

        for entry in root.findall('atom:entry', ns):
            item = {
                'title': self._get_text(entry, 'atom:title', ns),
                'link': '',
                'description': self._get_text(entry, 'atom:summary', ns) or self._get_text(entry, 'atom:content', ns),
                'pub_date': self._get_text(entry, 'atom:updated', ns) or self._get_text(entry, 'atom:published', ns),
                'guid': self._get_text(entry, 'atom:id', ns),
                'author': ''
            }

            link_elem = entry.find('atom:link', ns)
            if link_elem is not None:
                item['link'] = link_elem.get('href', '')

            author_elem = entry.find('atom:author', ns)
            if author_elem is not None:
                item['author'] = self._get_text(author_elem, 'atom:name', ns)

            feed_info['items'].append(item)

        return feed_info

    def _get_text(self, parent, tag, ns=None):
        """安全获取元素文本"""
        elem = parent.find(tag, ns) if ns else parent.find(tag)
        return elem.text.strip() if elem is not None and elem.text else ''

parser = RSSParser()
xml_content = parser.fetch("https://example.com/feed.xml")
if xml_content:
    feed = parser.parse(xml_content)
    if feed:
        print(f"订阅源：{feed['title']}")
        print(f"条目数：{len(feed['items'])}")
```

## 代码示例 (bash)

```bash
pip install requests

cat > feed_to_md.py << 'PYEOF'
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os

def fetch_rss(url):
    r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    return r.content

def parse_rss(xml):
    root = ET.fromstring(xml)
    channel = root.find('channel')
    return {
        'title': channel.find('title').text,
        'description': channel.find('description').text,
        'link': channel.find('link').text,
        'items': [
            {
                'title': item.find('title').text,
                'link': item.find('link').text,
                'description': item.find('description').text if item.find('description') is not None else '',
                'pub_date': item.find('pubDate').text if item.find('pubDate') is not None else ''
            }
            for item in channel.findall('item')
        ]
    }

def to_markdown(feed):
    lines = [f"# {feed['title']}\n"]
    if feed.get('description'):
        lines.append(f"> {feed['description']}\n")
    lines.append(f"**链接**：{feed.get('link', '')}\n---\n")

    for i, item in enumerate(feed['items'], 1):
        lines.append(f"## {i}. {item['title']}")
        if item.get('pub_date'):
            lines.append(f"**日期**：{item['pub_date']}")
        if item.get('link'):
            lines.append(f"**链接**：{item['link']}")
        if item.get('description'):
            lines.append(f"\n{item['description'][:500]}")
        lines.append("\n---\n")

    return "\n".join(lines)

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/feed.xml"
    xml = fetch_rss(url)
    feed = parse_rss(xml)
    md = to_markdown(feed)

    os.makedirs("./output", exist_ok=True)
    filename = f"feed_{datetime.now().strftime('%Y%m%d')}.md"
    with open(f"./output/{filename}", "w", encoding="utf-8") as f:
        f.write(md)
    print(f"已保存：./output/{filename}")
PYEOF

python3 feed_to_md.py "https://example.com/feed.xml"
```

