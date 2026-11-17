# 详细参考 - free-google-search-tool-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import os
from datetime import datetime

class ResultExporter:
    """结果导出器（免费版）"""

    def export_json(self, results, filepath=None):
        """导出为JSON"""
        if filepath is None:
            filepath = f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'query': results[0].get('query', '') if results else '',
                'searched_at': datetime.now().isoformat(),
                'total_results': len(results),
                'results': results
            }, f, ensure_ascii=False, indent=2)

        print(f"已导出JSON：{filepath}")
        return filepath

    def export_csv(self, results, filepath=None):
        """导出为CSV"""
        if filepath is None:
            filepath = f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        import csv
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'URL', 'Snippet', 'Position'])
            for r in results:
                writer.writerow([
                    r.get('title', ''),
                    r.get('url', ''),
                    r.get('snippet', ''),
                    r.get('position', 0)
                ])

        print(f"已导出CSV：{filepath}")
        return filepath

    def export_markdown(self, results, filepath=None, query=""):
        """导出为Markdown"""
        if filepath is None:
            filepath = f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        lines = [
            f"# 搜索结果：{query}",
            f"**搜索时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**结果数量**：{len(results)}",
            "",
            "---",
            ""
        ]

        for i, r in enumerate(results, 1):
            lines.append(f"## {i}. {r.get('title', '无标题')}")
            lines.append(f"**链接**：{r.get('url', '')}")
            if r.get('snippet'):
                lines.append(f"\n{r['snippet']}\n")
            lines.append("---")
            lines.append("")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))

        print(f"已导出Markdown：{filepath}")
        return filepath

exporter = ResultExporter()

if result.get("success"):
    parsed = parser.parse_results(result["results"])

    exporter.export_json(parsed)

    exporter.export_markdown(parsed, query=result.get("query", ""))
```

## 代码示例 (python)

```python
class SearchResultParser:
    """搜索结果解析器（免费版）"""

    def parse_results(self, raw_results):
        """解析原始搜索结果"""
        parsed = []
        for result in raw_results:
            parsed.append({
                'title': self._clean_text(result.get('title', '')),
                'url': result.get('url', ''),
                'snippet': self._clean_text(result.get('snippet', '')),
                'display_url': result.get('displayUrl', ''),
                'position': result.get('position', 0)
            })
        return parsed

    def _clean_text(self, text):
        """清理文本"""
        if not text:
            return ""
        text = ' '.join(text.split())
        text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        return text

    def extract_domains(self, results):
        """提取所有域名"""
        from urllib.parse import urlparse
        domains = set()
        for r in results:
            if r.get('url'):
                domain = urlparse(r['url']).netloc
                domains.add(domain)
        return sorted(domains)

    def format_results(self, results, format_type="text"):
        """格式化结果"""
        if format_type == "text":
            return self._format_text(results)
        elif format_type == "markdown":
            return self._format_markdown(results)
        elif format_type == "json":
            return json.dumps(results, ensure_ascii=False, indent=2)
        return ""

    def _format_text(self, results):
        """文本格式"""
        lines = []
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. {r['title']}")
            lines.append(f"   URL: {r['url']}")
            if r['snippet']:
                lines.append(f"   摘要: {r['snippet'][:200]}")
            lines.append("")
        return "\n".join(lines)

    def _format_markdown(self, results):
        """Markdown格式"""
        lines = ["## 搜索结果\n"]
        for i, r in enumerate(results, 1):
            lines.append(f"### {i}. {r['title']}")
            lines.append(f"**链接**：[{r['url']}]({r['url']})")
            if r['snippet']:
                lines.append(f"\n{r['snippet'][:300]}\n")
            lines.append("---\n")
        return "\n".join(lines)

parser = SearchResultParser()

if result.get("success"):
    parsed = parser.parse_results(result["results"])
    print(parser.format_results(parsed, "text"))

    domains = parser.extract_domains(parsed)
    print(f"\n涉及域名：{len(domains)}个")
    for d in domains[:5]:
        print(f"  {d}")
```

## 代码示例 (python)

```python
class ResultFilter:
    """结果筛选器（免费版）"""

    def filter_by_keyword(self, results, keyword):
        """按关键词筛选"""
        return [
            r for r in results
            if keyword.lower() in r.get('title', '').lower()
            or keyword.lower() in r.get('snippet', '').lower()
        ]

    def filter_by_domain(self, results, domains):
        """按域名筛选"""
        from urllib.parse import urlparse
        return [
            r for r in results
            if any(d in urlparse(r.get('url', '')).netloc for d in domains)
        ]

    def exclude_domains(self, results, exclude_list):
        """排除特定域名"""
        from urllib.parse import urlparse
        return [
            r for r in results
            if not any(d in urlparse(r.get('url', '')).netloc for d in exclude_list)
        ]

    def deduplicate(self, results):
        """去重"""
        seen_urls = set()
        unique = []
        for r in results:
            url = r.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique.append(r)
        return unique

    def sort_by_relevance(self, results, query):
        """按相关性排序"""
        query_words = query.lower().split()
        for r in results:
            score = 0
            title = r.get('title', '').lower()
            snippet = r.get('snippet', '').lower()
            for word in query_words:
                if word in title:
                    score += 2
                if word in snippet:
                    score += 1
            r['relevance_score'] = score

        return sorted(results, key=lambda x: x['relevance_score'], reverse=True)

filterer = ResultFilter()

if result.get("success"):
    parsed = parser.parse_results(result["results"])

    filtered = filterer.filter_by_keyword(parsed, "AI")
    print(f"包含 'AI' 的结果：{len(filtered)} 条")

    cleaned = filterer.exclude_domains(parsed, ['pinterest.com', 'facebook.com'])
    print(f"排除社交媒体后：{len(cleaned)} 条")

    unique = filterer.deduplicate(parsed)
    print(f"去重后：{len(unique)} 条")
```

