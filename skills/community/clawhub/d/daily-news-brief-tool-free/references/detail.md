# 详细参考 - daily-news-brief-tool-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
class BriefGenerator:
    """简报生成器（免费版）"""

    def generate(self, filtered_news, date_str=None):
        """生成新闻简报"""
        if date_str is None:
            now = datetime.now()
            weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
            date_str = f"{now.strftime('%Y年%m月%d日')} | {weekdays[now.weekday()]}"

        lines = []
        lines.append(f"# 每日新闻简报 | {date_str}")
        lines.append("")
        lines.append("---")
        lines.append("")

        intl = filtered_news.get('international', [])
        if intl:
            lines.append("## 国际时事")
            lines.append("")
            for i, news in enumerate(intl[:5], 1):
                lines.append(f"{i}. {news['title']}")
            lines.append("")

        econ = filtered_news.get('economic', [])
        if econ:
            lines.append("## 经济形势")
            lines.append("")
            for i, news in enumerate(econ[:5], 1):
                lines.append(f"{i}. {news['title']}")
            lines.append("")

        tech = filtered_news.get('technology', [])
        if tech:
            lines.append("## 科技发展")
            lines.append("")
            for i, news in enumerate(tech[:5], 1):
                lines.append(f"{i}. {news['title']}")
            lines.append("")

        lines.append("## 今日关注")
        lines.append("")
        if intl:
            lines.append(f"- {intl[0]['title']}")
        if econ:
            lines.append(f"- {econ[0]['title']}")
        if tech:
            lines.append(f"- {tech[0]['title']}")
        lines.append("")

        lines.append("---")
        lines.append(f"*简报生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return "\n".join(lines)

    def save_to_file(self, content, output_dir="."):
        """保存到文件"""
        import os
        filename = f"news_brief_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"简报已保存：{filepath}")
        return filepath

generator = BriefGenerator()
brief = generator.generate(filtered)
print(brief[:500])
generator.save_to_file(brief)
```

## 代码示例 (python)

```python
import requests
from datetime import datetime
from bs4 import BeautifulSoup

class NewsCollector:
    """新闻搜集器（免费版）"""

    def __init__(self):
        self.sources = {
            'international': [
                'https://news.cctv.com/world',
                'https://www.reuters.com/world',
                'https://www.bbc.com/news/world'
            ],
            'economic': [
                'https://finance.sina.com.cn',
                'https://www.bloomberg.com/markets',
                'https://www.ft.com/markets'
            ],
            'technology': [
                'https://tech.sina.com.cn',
                'https://techcrunch.com',
                'https://www.theverge.com/tech'
            ]
        }
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def collect_all(self):
        """搜集所有领域的新闻"""
        all_news = {}
        for category, urls in self.sources.items():
            print(f"搜集 {category} 新闻...")
            news_items = []
            for url in urls:
                items = self.collect_single(url, category)
                news_items.extend(items)
            all_news[category] = news_items
        return all_news

    def collect_single(self, url, category):
        """搜集单个源"""
        try:
            response = requests.get(url, timeout=10, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            items = []
            for link in soup.find_all('a', href=True)[:20]:
                title = link.get_text(strip=True)
                if title and len(title) > 10 and len(title) < 100:
                    items.append({
                        'title': title,
                        'url': link['href'],
                        'category': category
                    })
            return items
        except Exception as e:
            print(f"  获取失败：{url} - {e}")
            return []

collector = NewsCollector()
all_news = collector.collect_all()
for category, items in all_news.items():
    print(f"\n{category}: {len(items)} 条")
```

## 代码示例 (python)

```python
class NewsFilter:
    """新闻筛选器（免费版）"""

    INTERNATIONAL_PRIORITIES = [
        '中美关系', '中东', '欧洲', '亚太', '朝鲜', '俄罗斯', '乌克兰',
        '贸易', '外交', '峰会', '联合国', '北约'
    ]

    ECONOMIC_KEYWORDS = [
        'GDP', '通胀', '就业', '利率', '美联储', '央行', '股市',
        '汇市', '大宗商品', '贸易', '投资', '新能源', '数字经济'
    ]

    TECHNOLOGY_KEYWORDS = [
        'AI', '人工智能', '大模型', '芯片', '半导体', '新能源',
        '电动汽车', '光伏', '储能', '生物科技', '太空', '商业航天'
    ]

    def filter_news(self, all_news):
        """筛选重要新闻"""
        filtered = {}
        for category, items in all_news.items():
            keywords = self._get_keywords(category)
            scored = []

            for item in items:
                score = self._score_item(item, keywords)
                if score > 0:
                    item['score'] = score
                    scored.append(item)

            scored.sort(key=lambda x: x['score'], reverse=True)
            filtered[category] = scored[:5]

        return filtered

    def _get_keywords(self, category):
        if category == 'international':
            return self.INTERNATIONAL_PRIORITIES
        elif category == 'economic':
            return self.ECONOMIC_KEYWORDS
        elif category == 'technology':
            return self.TECHNOLOGY_KEYWORDS
        return []

    def _score_item(self, item, keywords):
        """计算新闻得分"""
        title = item.get('title', '')
        score = 0
        for kw in keywords:
            if kw in title:
                score += 1
        return score

filterer = NewsFilter()
filtered = filterer.filter_news(all_news)
for category, items in filtered.items():
    print(f"\n{category} 筛选后：{len(items)} 条")
```

