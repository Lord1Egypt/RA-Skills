# 详细参考 - feed-to-md-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
class TemplateBasedConverter:
    """基于模板的转换器（专业版）"""

    def __init__(self, template_name="default"):
        self.template_name = template_name
        self.templates = self._load_templates()

    def _load_templates(self):
        """加载模板"""
        return {
            "default": {
                "header": "# {title}\n\n> {description}\n\n**链接**：{link}\n**更新**：{last_build_date}\n\n---\n\n",
                "item": "## {index}. {title}\n\n**日期**：{pub_date}\n**作者**：{author}\n**链接**：[{link}]({link})\n\n{description}\n\n---\n",
                "footer": "\n*转换时间：{converted_at}*\n"
            },
            "academic": {
                "header": "# {title}\n\n**Abstract**: {description}\n\n**Source**: {link}\n**Last Updated**: {last_build_date}\n\n---\n\n## Table of Contents\n\n{toc}\n\n---\n",
                "item": "## {index}. {title}\n\n**Date**: {pub_date}\n**Author**: {author}\n**URL**: {link}\n\n**Abstract**: {description}\n\n---\n",
                "footer": "\n---\n\n*Converted at: {converted_at}*\n"
            },
            "minimal": {
                "header": "# {title}\n",
                "item": "- [{title}]({link})\n",
                "footer": ""
            },
            "detailed": {
                "header": "# {title}\n\n## 订阅源信息\n\n- **描述**：{description}\n- **链接**：{link}\n- **最后更新**：{last_build_date}\n- **条目数**：{item_count}\n\n---\n\n## 条目详情\n\n",
                "item": "### {index}. {title}\n\n#### 元信息\n\n- **发布日期**：{pub_date}\n- **作者**：{author}\n- **原文链接**：{link}\n- **GUID**：{guid}\n\n#### 内容\n\n{description}\n\n---\n",
                "footer": "\n---\n\n## 统计信息\n\n- 总条目数：{item_count}\n- 转换时间：{converted_at}\n- 模板：{template_name}\n"
            }
        }

    def convert(self, feed_info, template_name=None):
        """使用模板转换"""
        template = self.templates.get(template_name or self.template_name, self.templates["default"])

        header_vars = {
            'title': feed_info.get('title', ''),
            'description': feed_info.get('description', ''),
            'link': feed_info.get('link', ''),
            'last_build_date': feed_info.get('last_build_date', ''),
            'item_count': len(feed_info.get('items', [])),
            'converted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'template_name': template_name or self.template_name,
            'toc': self._generate_toc(feed_info)
        }

        lines = [template['header'].format(**header_vars)]

        for i, item in enumerate(feed_info.get('items', []), 1):
            item_vars = {
                'index': i,
                'title': item.get('title', ''),
                'link': item.get('link', ''),
                'description': self._strip_html(item.get('description', ''))[:500],
                'pub_date': item.get('pub_date', ''),
                'author': item.get('author', ''),
                'guid': item.get('guid', '')
            }
            lines.append(template['item'].format(**item_vars))

        footer_vars = {
            'item_count': len(feed_info.get('items', [])),
            'converted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'template_name': template_name or self.template_name
        }
        lines.append(template['footer'].format(**footer_vars))

        return "".join(lines)

    def _generate_toc(self, feed_info):
        """生成目录"""
        toc_lines = []
        for i, item in enumerate(feed_info.get('items', []), 1):
            title = item.get('title', '')[:50]
            toc_lines.append(f"{i}. [{title}](#{i}-{title})")
        return "\n".join(toc_lines)

    def _strip_html(self, text):
        """移除HTML标签"""
        import re
        return re.sub('<.*?>', '', text).strip()

    def add_custom_template(self, name, template_dict):
        """添加自定义模板"""
        self.templates[name] = template_dict
        print(f"已添加模板：{name}")

converter = TemplateBasedConverter("detailed")
markdown = converter.convert(feed, template_name="detailed")
print(markdown[:500])
```

## 代码示例 (python)

```python
import concurrent.futures
import threading
from datetime import datetime

class BatchFeedConverter:
    """批量RSS转换器（专业版）"""

    def __init__(self, max_workers=5):
        self.max_workers = max_workers
        self.lock = threading.Lock()
        self.results = {}
        self.stats = {"success": 0, "failed": 0, "total": 0}

    def convert_batch(self, feed_urls, output_dir="./output"):
        """批量转换多个订阅源"""
        print(f"启动批量转换，共 {len(feed_urls)} 个订阅源，并发数 {self.max_workers}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._convert_single, url, output_dir): url
                for url in feed_urls
            }

            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                try:
                    result = future.result()
                    with self.lock:
                        self.results[url] = result
                        self.stats["total"] += 1
                        if result.get("success"):
                            self.stats["success"] += 1
                        else:
                            self.stats["failed"] += 1
                        status = "成功" if result.get("success") else "失败"
                        print(f"[{status}] {url}")
                except Exception as e:
                    print(f"[异常] {url}: {e}")
                    with self.lock:
                        self.stats["failed"] += 1

        self._print_summary()
        return self.results

    def _convert_single(self, url, output_dir):
        """转换单个订阅源"""
        try:
            parser = RSSParser()
            converter = MarkdownConverter()
            saver = FileSaver(output_dir)

            xml = parser.fetch(url)
            if not xml:
                return {"success": False, "error": "获取失败"}

            feed = parser.parse(xml)
            if not feed:
                return {"success": False, "error": "解析失败"}

            markdown = converter.convert(feed)
            filepath = saver.save(markdown, feed_title=feed.get('title'))

            return {
                "success": True,
                "url": url,
                "title": feed.get('title'),
                "item_count": len(feed.get('items', [])),
                "filepath": filepath
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _print_summary(self):
        print("\n=== 批量转换摘要 ===")
        print(f"总数：{self.stats['total']}")
        print(f"成功：{self.stats['success']}")
        print(f"失败：{self.stats['failed']}")

converter = BatchFeedConverter(max_workers=5)
feeds = [
    "https://example.com/feed1.xml",
    "https://example.com/feed2.xml",
    "https://example.com/feed3.xml",
]
results = converter.convert_batch(feeds, "./archives")
```

## 代码示例 (python)

```python
class MultiFormatExporter:
    """多格式导出器（专业版）"""

    def __init__(self):
        self.md_converter = MarkdownConverter()

    def export_markdown(self, feed_info, output_path):
        """导出Markdown"""
        md = self.md_converter.convert(feed_info)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
        return output_path

    def export_html(self, feed_info, output_path):
        """导出HTML"""
        md = self.md_converter.convert(feed_info)
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{feed_info.get('title', 'Feed')}</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; }}
        a {{ color: #0066cc; }}
    </style>
</head>
<body>
    <pre>{md}</pre>
</body>
</html>"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return output_path

    def export_pdf(self, feed_info, output_path):
        """导出PDF"""
        html_path = output_path.replace('.pdf', '.html')
        self.export_html(feed_info, html_path)

        import subprocess
        try:
            subprocess.run(['wkhtmltopdf', html_path, output_path], check=True)
            return output_path
        except Exception as e:
            print(f"PDF转换失败：{e}")
            return None

    def export_epub(self, feed_info, output_path):
        """导出EPUB"""
        md_path = output_path.replace('.epub', '.md')
        self.export_markdown(feed_info, md_path)

        import subprocess
        try:
            subprocess.run(['pandoc', md_path, '-o', output_path], check=True)
            return output_path
        except Exception as e:
            print(f"EPUB转换失败：{e}")
            return None

    def export_all_formats(self, feed_info, base_path):
        """导出所有格式"""
        formats = {
            'md': f"{base_path}.md",
            'html': f"{base_path}.html",
            'pdf': f"{base_path}.pdf",
            'epub': f"{base_path}.epub"
        }

        results = {}
        results['md'] = self.export_markdown(feed_info, formats['md'])
        results['html'] = self.export_html(feed_info, formats['html'])
        results['pdf'] = self.export_pdf(feed_info, formats['pdf'])
        results['epub'] = self.export_epub(feed_info, formats['epub'])

        return results

exporter = MultiFormatExporter()
results = exporter.export_all_formats(feed, "./output/my_feed")
print(results)
```

## 代码示例 (python)

```python
class AIContentEnhancer:
    """AI内容增强器（专业版）"""

    def __init__(self):
        self.llm_available = True  # 由Agent平台内置提供
    def generate_summary(self, content, max_length=200):
        """生成AI摘要"""
        prompt = f"""请为以下内容生成简洁摘要（不超过{max_length}字）：

{content[:1000]}

要求：
1. 提取核心观点
2. 简洁明了
3. 不超过{max_length}字
"""
        return self._call_llm(prompt)

    def extract_keywords(self, content, top_n=5):
        """提取关键词"""
        prompt = f"""请从以下内容提取{top_n}个关键词：

{content[:1000]}

要求：
1. 提取最重要的{top_n}个关键词
2. 按重要程度排序
3. 每个关键词不超过5字
"""
        return self._call_llm(prompt).split('\n')[:top_n]

    def generate_tags(self, content, top_n=3):
        """生成标签"""
        prompt = f"""请为以下内容生成{top_n}个标签：

{content[:1000]}

要求：
1. 生成{top_n}个最相关的标签
2. 标签用于分类与检索
3. 每个标签2-4字
"""
        return self._call_llm(prompt).split('\n')[:top_n]

    def enhance_entry(self, entry):
        """增强条目内容"""
        content = entry.get('description', '')

        return {
            **entry,
            'ai_summary': self.generate_summary(content),
            'keywords': self.extract_keywords(content),
            'tags': self.generate_tags(content)
        }

    def enhance_feed(self, feed_info):
        """增强整个订阅源"""
        enhanced_items = []
        for item in feed_info.get('items', []):
            enhanced = self.enhance_entry(item)
            enhanced_items.append(enhanced)

        return {
            **feed_info,
            'items': enhanced_items
        }

    def _call_llm(self, prompt):
        """调用LLM"""
        return f"[AI增强结果] 基于输入生成（{len(prompt)}字符）"

enhancer = AIContentEnhancer()
enhanced_feed = enhancer.enhance_feed(feed)
```

## 代码示例 (python)

```python
import schedule
import time

class ScheduledArchiver:
    """定时归档器（专业版）"""

    def __init__(self):
        self.feeds = []
        self.converter = BatchFeedConverter(max_workers=3)
        self.enhancer = AIContentEnhancer()
        self.running = False

    def add_feed(self, url, schedule_str="daily"):
        """添加订阅源"""
        self.feeds.append({
            'url': url,
            'schedule': schedule_str
        })
        print(f"已添加订阅源：{url}（{schedule_str}）")

    def setup_schedule(self):
        """配置定时任务"""
        schedule.every().day.at("02:00").do(self.archive_all)

        print("定时归档已配置：")
        print("  - 每天 02:00 自动归档所有订阅源")

    def archive_all(self):
        """归档所有订阅源"""
        print(f"\n[{datetime.now()}] 开始定时归档...")

        archive_dir = f"./archives/{datetime.now().strftime('%Y%m%d')}"
        os.makedirs(archive_dir, exist_ok=True)

        urls = [f['url'] for f in self.feeds]
        results = self.converter.convert_batch(urls, archive_dir)

        self._generate_report(results, archive_dir)

    def _generate_report(self, results, output_dir):
        """生成归档报告"""
        report = {
            'archived_at': datetime.now().isoformat(),
            'total_feeds': len(results),
            'success_count': sum(1 for r in results.values() if r.get('success')),
            'failed_count': sum(1 for r in results.values() if not r.get('success')),
            'details': results
        }

        import json
        report_file = os.path.join(output_dir, "archive_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n归档完成：成功 {report['success_count']}/{report['total_feeds']}")

    def start(self):
        """启动定时归档"""
        self.running = True
        self.setup_schedule()
        print("\n定时归档器已启动...")
        while self.running:
            schedule.run_pending()
            time.sleep(60)

archiver = ScheduledArchiver()
archiver.add_feed("https://example.com/feed1.xml")
archiver.add_feed("https://example.com/feed2.xml")
```

