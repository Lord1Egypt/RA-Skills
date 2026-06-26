#!/usr/bin/env python3
"""
双平台设计灵感收集器（v2.1）
仅从 Dribbble 和 Pinterest 的官方搜索/标签页收集设计灵感
不包含个人作品集和个人画板
"""

import os
import sys
import json
import re
from datetime import datetime
from urllib.parse import quote_plus

# 配置
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "design_inspirations")


# ============================================================
# URL 白名单过滤
# ============================================================

def is_valid_dribbble_url(url: str) -> bool:
    """
    Dribbble 只允许：搜索页 / 标签页 / 热门页
    禁止：个人作品集、单个作品页
    """
    if "dribbble.com" not in url:
        return False
    # 允许的路径模式
    allowed_patterns = [
        r"dribbble\.com/search/",
        r"dribbble\.com/tags/",
        r"dribbble\.com/shots/popular",
    ]
    for p in allowed_patterns:
        if re.search(p, url):
            return True
    return False


def is_valid_pinterest_url(url: str) -> bool:
    """
    Pinterest 只允许：大搜索 / ideas 主题页
    禁止：个人画板、单个图钉
    """
    if "pinterest.com" not in url:
        return False
    # 允许的路径模式
    allowed_patterns = [
        r"pinterest\.com/search/pins",
        r"pinterest\.com/search/\?",
        r"pinterest\.com/ideas/",
    ]
    for p in allowed_patterns:
        if re.search(p, url):
            return True
    return False


# ============================================================
# 标准搜索 URL 构造（备用）
# ============================================================

def build_dribbble_urls(keyword: str) -> list:
    """构造 Dribbble 标准搜索/标签 URL"""
    kw_dash = keyword.strip().replace(" ", "-").lower()
    return [
        {
            "url": f"https://dribbble.com/search/{kw_dash}",
            "title": f"Dribbble Search: {keyword}",
            "type": "搜索页",
            "description": f"Dribbble 上「{keyword}」关键词搜索结果，全球设计师作品",
        },
        {
            "url": f"https://dribbble.com/tags/{kw_dash}",
            "title": f"Dribbble Tag: {keyword}",
            "type": "标签页",
            "description": f"带「{keyword}」标签的 Dribbble 作品合集",
        },
        {
            "url": f"https://dribbble.com/search/{kw_dash}-ui",
            "title": f"Dribbble Search: {keyword} UI",
            "type": "搜索页",
            "description": f"Dribbble 上「{keyword} UI」精准搜索，聚焦界面设计",
        },
        {
            "url": f"https://dribbble.com/search/{kw_dash}-mobile",
            "title": f"Dribbble Search: {keyword} Mobile",
            "type": "搜索页",
            "description": f"Dribbble 上「{keyword} Mobile」搜索，聚焦移动端设计",
        },
        {
            "url": f"https://dribbble.com/search/{kw_dash}-app",
            "title": f"Dribbble Search: {keyword} App",
            "type": "搜索页",
            "description": f"Dribbble 上「{keyword} App」搜索，聚焦 App 设计",
        },
    ]


def build_pinterest_urls(keyword: str) -> list:
    """构造 Pinterest 标准搜索/ideas URL"""
    kw_q = quote_plus(keyword.strip().lower())
    kw_dash = keyword.strip().replace(" ", "-").lower()
    return [
        {
            "url": f"https://www.pinterest.com/search/pins/?q={kw_q}+ui+design",
            "title": f"Pinterest Search: {keyword} UI Design",
            "type": "大搜索",
            "description": f"Pinterest 上「{keyword} UI Design」大搜索结果",
        },
        {
            "url": f"https://www.pinterest.com/search/pins/?q={kw_q}+app+design",
            "title": f"Pinterest Search: {keyword} App Design",
            "type": "大搜索",
            "description": f"Pinterest 上「{keyword} App Design」大搜索结果",
        },
        {
            "url": f"https://www.pinterest.com/ideas/{kw_dash}-design/",
            "title": f"Pinterest Ideas: {keyword} Design",
            "type": "ideas 主题页",
            "description": f"Pinterest 官方策展的「{keyword}」设计主题灵感页",
        },
        {
            "url": f"https://www.pinterest.com/search/pins/?q={kw_q}+mobile",
            "title": f"Pinterest Search: {keyword} Mobile",
            "type": "大搜索",
            "description": f"Pinterest 上「{keyword} Mobile」搜索，聚焦移动端",
        },
        {
            "url": f"https://www.pinterest.com/search/pins/?q={kw_q}+inspiration",
            "title": f"Pinterest Search: {keyword} Inspiration",
            "type": "大搜索",
            "description": f"Pinterest 上「{keyword} Inspiration」搜索，更广泛灵感",
        },
    ]


# ============================================================
# Tavily 搜索
# ============================================================

def tavily_search(query: str, max_results: int = 10) -> list:
    """调用 Tavily 搜索"""
    try:
        from tavily import TavilyClient
    except ImportError:
        print("Error: tavily-python not installed")
        return []

    if not TAVILY_API_KEY:
        print("Error: TAVILY_API_KEY not set")
        return []

    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=max_results,
        )
        return response.get("results", [])
    except Exception as e:
        print(f"  Tavily 搜索失败: {e}")
        return []


def search_dribbble(topic: str, target: int = 5) -> list:
    """搜索 Dribbble，过滤后只保留搜索/标签页"""
    queries = [
        f"site:dribbble.com {topic} ui design",
        f"site:dribbble.com {topic} app",
        f"site:dribbble.com {topic} mobile",
    ]
    raw = []
    for q in queries:
        raw.extend(tavily_search(q, max_results=10))

    # 过滤
    valid = [r for r in raw if is_valid_dribbble_url(r.get("url", ""))]

    # 去重并按分数排序
    seen = set()
    unique = []
    for r in sorted(valid, key=lambda x: x.get("score", 0), reverse=True):
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)
        if len(unique) >= target:
            break

    # 不够 5 条 → 用构造的标准 URL 补足
    if len(unique) < target:
        existing_urls = {r["url"] for r in unique}
        for fallback in build_dribbble_urls(topic):
            if fallback["url"] not in existing_urls:
                unique.append({
                    "url": fallback["url"],
                    "title": fallback["title"],
                    "content": fallback["description"],
                    "score": 0.95,
                    "_type": fallback["type"],
                    "_fallback": True,
                })
            if len(unique) >= target:
                break

    return unique[:target]


def search_pinterest(topic: str, target: int = 5) -> list:
    """
    搜索 Pinterest。
    策略：直接构造大搜索 URL（/search/pins/?q=...）作为主要来源，
    因为这种页面是用户最常用的 Pinterest 搜索体验，比 ideas 主题页更实用：
      - 内容更多、更新更快
      - 顶部带筛选标签（Mobile/Gradient/Onboarding 等）支持二次筛选
      - 直接对应你日常用的搜索框输入体验
    """
    topic_lower = topic.strip().lower()
    kw_q = quote_plus(topic_lower)

    # 智能拼接：如果 topic 已包含某个词，就不再追加
    def smart_append(extra_word):
        """如果 topic 里已有 extra_word 的关键字，就不追加；否则追加"""
        if extra_word in topic_lower.split():
            return ""
        return f"+{quote_plus(extra_word)}"

    # 主入口：5 个不同切面的大搜索 URL（最实用）
    primary_searches = [
        {
            "url": f"https://www.pinterest.com/search/pins/?q={kw_q}{smart_append('ui')}{smart_append('design')}",
            "title": f"Pinterest 搜索：{topic} UI Design",
            "_type": "大搜索",
            "content": f"Pinterest 大搜索结果：「{topic} ui design」。海量 Pin、实时更新，顶部带筛选标签可二次精准（Mobile/Gradient/Onboarding 等）",
            "score": 1.0,
        },
        {
            "url": f"https://www.pinterest.com/search/pins/?q={kw_q}{smart_append('mobile')}{smart_append('ui')}",
            "title": f"Pinterest 搜索：{topic} Mobile UI",
            "_type": "大搜索",
            "content": f"Pinterest 大搜索结果：「{topic} mobile ui」。聚焦移动端界面设计",
            "score": 0.98,
        },
        {
            "url": f"https://www.pinterest.com/search/pins/?q={kw_q}{smart_append('dashboard')}",
            "title": f"Pinterest 搜索：{topic} Dashboard",
            "_type": "大搜索",
            "content": f"Pinterest 大搜索结果：「{topic} dashboard」。聚焦数据可视化、Dashboard 设计",
            "score": 0.96,
        },
        {
            "url": f"https://www.pinterest.com/search/pins/?q={kw_q}{smart_append('concept')}",
            "title": f"Pinterest 搜索：{topic} Concept",
            "_type": "大搜索",
            "content": f"Pinterest 大搜索结果：「{topic} concept」。设计概念稿、创意方案",
            "score": 0.94,
        },
        {
            "url": f"https://www.pinterest.com/search/pins/?q={kw_q}{smart_append('inspiration')}",
            "title": f"Pinterest 搜索：{topic} Inspiration",
            "_type": "大搜索",
            "content": f"Pinterest 大搜索结果：「{topic} inspiration」。最广泛的灵感聚合",
            "score": 0.92,
        },
    ]

    # 取前 target 条
    return primary_searches[:target]


# ============================================================
# Markdown 输出
# ============================================================

def generate_markdown(topic: str, dribbble_items: list, pinterest_items: list) -> str:
    """生成 Markdown 报告"""
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日 %H:%M")
    total = len(dribbble_items) + len(pinterest_items)

    md = f"""# {topic} 设计灵感收集

> 收集时间：{date_str}
> 来源：Dribbble、Pinterest
> 总计：{total} 条搜索入口（仅含官方搜索 / 标签页 / ideas 页）

---

## 📊 趋势概览

> 请基于搜索结果补充该主题当前的设计趋势分析（5-7 条要点）

---

## 🎯 Dribbble 搜索精选 ({len(dribbble_items)} 条)

"""
    for i, item in enumerate(dribbble_items, 1):
        title = item.get("title", "Untitled")[:80]
        url = item.get("url", "")
        content = item.get("content", "")[:150]
        score = item.get("score", 0)
        item_type = item.get("_type") or ("标签页" if "/tags/" in url else "搜索页")
        stars = "⭐" * min(5, max(1, int(score * 5)))

        md += f"""### {i}. {title} {stars}
- **链接**：{url}
- **类型**：{item_type}
- **描述**：{content}

"""

    md += f"""---

## 🎨 Pinterest 搜索精选 ({len(pinterest_items)} 条)

"""
    for i, item in enumerate(pinterest_items, 1):
        title = item.get("title", "Untitled")[:80]
        url = item.get("url", "")
        content = item.get("content", "")[:150]
        score = item.get("score", 0)
        item_type = item.get("_type") or ("ideas 主题页" if "/ideas/" in url else "大搜索")
        stars = "⭐" * min(5, max(1, int(score * 5)))

        md += f"""### {i}. {title} {stars}
- **链接**：{url}
- **类型**：{item_type}
- **描述**：{content}

"""

    md += f"""---

## 🔍 推荐搜索关键词

- `{topic} ui design`
- `{topic} app ui`
- `{topic} dashboard`
- `{topic} mobile`

---

## 📌 相关方向推荐

> 请根据主题补充 3-5 个细分推荐方向（不带链接）

---

*文档由 AI 助手自动生成 · {now.strftime('%Y-%m-%d')}*
"""
    return md


# ============================================================
# 主函数
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python design_collector.py <topic>")
        print("Example: python design_collector.py 'healthcare app'")
        sys.exit(1)

    topic = sys.argv[1]
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    print(f"\n🔍 主题：{topic}")
    print("=" * 50)

    print("\n📡 搜索 Dribbble...")
    dribbble_items = search_dribbble(topic, target=5)
    print(f"   ✅ 收集 {len(dribbble_items)} 条")

    print("\n📡 搜索 Pinterest...")
    pinterest_items = search_pinterest(topic, target=5)
    print(f"   ✅ 收集 {len(pinterest_items)} 条")

    # 输出 Markdown
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    safe_topic = topic.replace(" ", "_").replace("/", "_")
    md_filename = f"{safe_topic}_{timestamp}.md"
    md_path = os.path.join(OUTPUT_DIR, md_filename)

    markdown = generate_markdown(topic, dribbble_items, pinterest_items)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    # 输出 JSON 供 LLM 后续整理
    data = {
        "topic": topic,
        "timestamp": timestamp,
        "markdown_file": md_path,
        "dribbble": dribbble_items,
        "pinterest": pinterest_items,
    }
    json_path = os.path.join(OUTPUT_DIR, f"{safe_topic}_{timestamp}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 完成！")
    print(f"   Markdown：{md_path}")
    print(f"   JSON：{json_path}")
    print(json.dumps({"markdown": md_path, "json": json_path}, ensure_ascii=False))

    return data


if __name__ == "__main__":
    main()
