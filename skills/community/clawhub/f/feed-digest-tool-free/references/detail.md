# 详细参考 - feed-digest-tool-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
class FeedFilter:
    """订阅内容筛选器（免费版）"""

    HIGH_VALUE_KEYWORDS = [
        'AI', '人工智能', '大模型', 'LLM', 'GPT',
        '系统设计', '架构', '性能优化', '分布式',
        '开发工具', 'DevOps', 'CI/CD', 'Kubernetes',
        '反直觉', '颠覆', '突破', '创新',
        '深度分析', '长文', '思考',
    ]

    SKIP_KEYWORDS = [
        '广告', '推广', '赞助', 'sponsored',
        '订阅', '关注', '转发', '抽奖',
    ]

    def __init__(self, limit=10):
        self.limit = limit

    def filter_entries(self, entries_text):
        """筛选高价值条目"""
        entries = self._parse_entries(entries_text)
        scored = []

        for entry in entries:
            score = self._score_entry(entry)
            if score > 0:
                entry['score'] = score
                scored.append(entry)

        scored.sort(key=lambda x: x['score'], reverse=True)
        return scored[:self.limit]

    def _score_entry(self, entry):
        """计算条目得分"""
        title = entry.get('title', '').lower()
        summary = entry.get('summary', '').lower()
        text = title + ' ' + summary

        for kw in self.SKIP_KEYWORDS:
            if kw.lower() in text:
                return 0

        score = 0
        for kw in self.HIGH_VALUE_KEYWORDS:
            if kw.lower() in text:
                score += 1

        for kw in self.HIGH_VALUE_KEYWORDS:
            if kw.lower() in title:
                score += 1

        return score

    def _parse_entries(self, entries_text):
        """解析条目列表"""
        entries = []
        lines = entries_text.strip().split('\n')
        for line in lines[1:]:  # 跳过表头
            parts = line.split('\t')
            if len(parts) >= 4:
                entries.append({
                    'id': parts[0],
                    'title': parts[1],
                    'feed': parts[2],
                    'date': parts[3],
                    'summary': parts[4] if len(parts) > 4 else ''
                })
        return entries

filterer = FeedFilter(limit=10)
entries_text = fetcher.get_entries(limit=50)
filtered = filterer.filter_entries(entries_text)

print(f"\n=== 筛选Top {len(filtered)} 条 ===")
for i, entry in enumerate(filtered, 1):
    print(f"{i}. [{entry['feed']}] {entry['title']} (score: {entry['score']})")
```

## 代码示例 (python)

```python
class DigestGenerator:
    """摘要生成器（免费版）"""

    def generate(self, filtered_entries, fetcher):
        """生成摘要"""
        lines = []
        lines.append("=" * 50)
        lines.append("  订阅摘要 | 今日精选")
        lines.append("=" * 50)
        lines.append("")

        grouped = self._group_by_theme(filtered_entries)

        for theme, entries in grouped.items():
            if entries:
                lines.append(f"【{theme}】")
                lines.append("-" * 40)
                for entry in entries:
                    lines.append(f"  {entry['title']}")
                    lines.append(f"  来源：{entry.get('feed', '未知')}")

                    full_content = fetcher.get_entry(entry['id'])
                    summary = self._extract_summary(full_content, max_length=200)
                    if summary:
                        lines.append(f"  摘要：{summary}")
                    lines.append("")

        lines.append("=" * 50)
        lines.append(f"  共 {len(filtered_entries)} 条精选")
        lines.append("=" * 50)

        return "\n".join(lines)

    def _group_by_theme(self, entries):
        """按主题分组"""
        themes = {
            'AI与机器学习': ['AI', '机器学习', 'LLM', 'GPT', '大模型'],
            '系统与架构': ['架构', '系统', '分布式', '微服务'],
            '开发工具': ['工具', 'DevOps', 'CI/CD', 'Kubernetes'],
            '行业洞察': ['趋势', '分析', '思考', '洞察'],
            '其他': []
        }

        grouped = {theme: [] for theme in themes}
        for entry in entries:
            title = entry.get('title', '')
            matched = False
            for theme, keywords in themes.items():
                if any(kw in title for kw in keywords):
                    grouped[theme].append(entry)
                    matched = True
                    break
            if not matched:
                grouped['其他'].append(entry)

        return {k: v for k, v in grouped.items() if v}

    def _extract_summary(self, content, max_length=200):
        """提取摘要"""
        if not content:
            return ""

        content = content.strip()
        if len(content) <= max_length:
            return content
        return content[:max_length] + "..."

generator = DigestGenerator()
digest = generator.generate(filtered, fetcher)
print(digest)
```

