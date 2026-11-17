# 详细参考 - free-google-search-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import schedule
import time
from datetime import datetime

class SearchMonitor:
    """搜索监控器（专业版）"""

    def __init__(self):
        self.monitored_keywords = {}
        self.last_results = {}
        self.notifier = WebhookNotifier()
        self.running = False

    def add_keyword(self, keyword, interval=3600, webhook_url=None):
        """添加监控关键词"""
        self.monitored_keywords[keyword] = {
            'interval': interval,
            'webhook': webhook_url,
            'last_check': None
        }
        print(f"已添加监控：{keyword}（间隔 {interval}s）")

    def check_changes(self):
        """检查所有关键词的变化"""
        for keyword, config in self.monitored_keywords.items():
            print(f"\n检查关键词：{keyword}")

            searcher = GoogleSearcher()
            result = searcher.search(keyword, num_results=10)

            if result.get("success"):
                current_results = result["results"]

                if keyword in self.last_results:
                    changes = self._detect_changes(
                        self.last_results[keyword], current_results
                    )
                    if changes:
                        self._alert_changes(keyword, changes, config.get('webhook'))

                self.last_results[keyword] = current_results

    def _detect_changes(self, old_results, new_results):
        """检测变化"""
        old_urls = {r.get('url') for r in old_results}
        new_urls = {r.get('url') for r in new_results}

        added = new_urls - old_urls
        removed = old_urls - new_urls

        changes = {
            'added': [r for r in new_results if r.get('url') in added],
            'removed': [r for r in old_results if r.get('url') in removed]
        }

        return changes if (changes['added'] or changes['removed']) else None

    def _alert_changes(self, keyword, changes, webhook_url):
        """发送变化告警"""
        message = f"关键词 '{keyword}' 检测到变化：\n"
        if changes['added']:
            message += f"\n新增结果 ({len(changes['added'])} 条)："
            for r in changes['added'][:3]:
                message += f"\n  - {r.get('title', '')}"

        if changes['removed']:
            message += f"\n消失结果 ({len(changes['removed'])} 条)："
            for r in changes['removed'][:3]:
                message += f"\n  - {r.get('title', '')}"

        print(f"\n[ALERT] {message}")

        if webhook_url:
            self.notifier.notify("default", "搜索监控告警", message)

    def start(self):
        """启动监控"""
        self.running = True
        print("搜索监控已启动...")

        while self.running:
            self.check_changes()
            time.sleep(3600)

monitor = SearchMonitor()
monitor.add_keyword("我的品牌名", interval=3600, webhook_url="REDACTED-SECRET")
monitor.add_keyword("竞争对手动态", interval=7200)
```

## 代码示例 (python)

```python
import concurrent.futures
import threading

class BatchGoogleSearcher:
    """批量Google搜索器（专业版）"""

    def __init__(self, max_workers=3, cache_enabled=True):
        self.max_workers = max_workers
        self.cache_enabled = cache_enabled
        self.cache = {}
        self.lock = threading.Lock()
        self.stats = {"success": 0, "failed": 0, "total": 0, "cached": 0}

    def search_batch(self, queries, num_results=10, language="zh-CN"):
        """批量搜索多个查询"""
        print(f"启动批量搜索，共 {len(queries)} 个查询，并发数 {self.max_workers}")

        all_results = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._search_single, query, num_results, language): query
                for query in queries
            }

            for future in concurrent.futures.as_completed(futures):
                query = futures[future]
                try:
                    result = future.result()
                    all_results[query] = result
                    with self.lock:
                        self.stats["total"] += 1
                        if result.get("success"):
                            if result.get("cached"):
                                self.stats["cached"] += 1
                            else:
                                self.stats["success"] += 1
                        else:
                            self.stats["failed"] += 1
                except Exception as e:
                    all_results[query] = {"success": False, "error": str(e)}
                    with self.lock:
                        self.stats["failed"] += 1

        self._print_summary()
        return all_results

    def _search_single(self, query, num_results, language):
        """搜索单个查询（带缓存）"""
        cache_key = f"{query}_{num_results}_{language}"
        if self.cache_enabled and cache_key in self.cache:
            return {**self.cache[cache_key], "cached": True}

        searcher = GoogleSearcher()
        result = searcher.search(query, num_results=num_results, language=language)

        if result.get("success"):
            if self.cache_enabled:
                with self.lock:
                    self.cache[cache_key] = result

        return result

    def _print_summary(self):
        print("\n=== 批量搜索摘要 ===")
        print(f"总数：{self.stats['total']}")
        print(f"成功：{self.stats['success']}")
        print(f"缓存命中：{self.stats['cached']}")
        print(f"失败：{self.stats['failed']}")

batch = BatchGoogleSearcher(max_workers=3, cache_enabled=True)

queries = [
    "人工智能最新进展",
    "机器学习框架对比",
    "深度学习应用场景",
    "自然语言处理趋势",
    "计算机视觉突破"
]

results = batch.search_batch(queries, num_results=10)
for query, result in results.items():
    if result.get("success"):
        print(f"\n{query}: {len(result['results'])} 条结果")
```

## 代码示例 (python)

```python
class AISearchSummarizer:
    """AI搜索摘要生成器（专业版）"""

    def __init__(self):
        self.llm_available = True  # 由Agent平台内置提供
    def generate_summary(self, query, results):
        """生成搜索结果AI摘要"""
        results_text = self._prepare_input(results)

        prompt = f"""请基于以下Google搜索结果，为查询"{query}"生成结构化AI摘要：

{results_text}

要求：
1. 提取3-5个核心观点
2. 整合不同来源的信息
3. 标注信息来源（域名）
4. 识别信息矛盾点
5. 生成200字整体概述
6. 推荐最值得深入阅读的Top 3
"""
        return self._call_llm(prompt)

    def generate_comparison(self, topic, multi_query_results):
        """生成多查询对比分析"""
        prompt = f"""请基于以下关于"{topic}"的多角度搜索结果，生成对比分析：

{self._format_multi_results(multi_query_results)}

要求：
1. 不同角度的观点对比
2. 共识与分歧分析
3. 趋势与走向判断
4. 300字综合分析
"""
        return self._call_llm(prompt)

    def extract_key_insights(self, results):
        """提取关键洞察"""
        prompt = f"""请从以下搜索结果中提取关键洞察：

{self._prepare_input(results)}

要求：
1. 5个关键洞察
2. 每个洞察标注来源
3. 评估洞察的可靠性与重要性
4. 标注潜在偏见或局限
"""
        return self._call_llm(prompt)

    def _prepare_input(self, results):
        lines = []
        for i, r in enumerate(results[:10], 1):
            lines.append(f"{i}. {r.get('title', '')}")
            lines.append(f"   URL: {r.get('url', '')}")
            if r.get('snippet'):
                lines.append(f"   摘要: {r['snippet'][:200]}")
        return "\n".join(lines)

    def _format_multi_results(self, multi_results):
        lines = []
        for query, result in multi_results.items():
            lines.append(f"\n【查询：{query}】")
            if result.get("success"):
                for r in result.get("results", [])[:3]:
                    lines.append(f"  - {r.get('title', '')}")
        return "\n".join(lines)

    def _call_llm(self, prompt):
        """调用LLM"""
        return f"[AI摘要] 基于输入生成（{len(prompt)}字符）"

summarizer = AISearchSummarizer()

if result.get("success"):
    summary = summarizer.generate_summary("人工智能", result["results"])
    print(summary)
```

## 代码示例 (python)

```python
import os
import json
from datetime import datetime, timedelta

class SearchCache:
    """搜索缓存（专业版）"""

    def __init__(self, cache_dir="./cache", ttl_hours=24):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)

    def get(self, query, num_results, language):
        """获取缓存"""
        cache_key = self._generate_key(query, num_results, language)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")

        if os.path.exists(cache_file):
            mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if datetime.now() - mtime < self.ttl:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    data['cached'] = True
                    return data
            else:
                os.remove(cache_file)

        return None

    def set(self, query, num_results, language, results):
        """设置缓存"""
        cache_key = self._generate_key(query, num_results, language)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")

        data = {
            'query': query,
            'num_results': num_results,
            'language': language,
            'cached_at': datetime.now().isoformat(),
            'results': results
        }

        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _generate_key(self, query, num_results, language):
        """生成缓存键"""
        import hashlib
        key = f"{query}_{num_results}_{language}"
        return hashlib.md5(key.encode()).hexdigest()

    def clear_expired(self):
        """清理过期缓存"""
        cleared = 0
        for filename in os.listdir(self.cache_dir):
            if not filename.endswith('.json'):
                continue
            filepath = os.path.join(self.cache_dir, filename)
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if datetime.now() - mtime > self.ttl:
                os.remove(filepath)
                cleared += 1
        print(f"已清理 {cleared} 个过期缓存")

cache = SearchCache("./cache", ttl_hours=24)

cached = cache.get("人工智能", 10, "zh-CN")
if cached:
    print(f"命中缓存：{len(cached['results'])} 条结果")
else:
    searcher = GoogleSearcher()
    result = searcher.search("人工智能", num_results=10)
    if result.get("success"):
        cache.set("人工智能", 10, "zh-CN", result["results"])
```

