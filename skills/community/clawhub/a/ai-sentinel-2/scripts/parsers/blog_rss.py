"""
博客RSS解析器
支持任意RSS/Atom订阅源
"""
import feedparser
import requests
from datetime import datetime
from urllib.parse import urlparse


def fetch_blog_rss(config):
    """
    获取RSS订阅源的最新内容
    
    Args:
        config: 信息源配置，包含:
            - feeds: RSS源列表，每个源包含:
                - name: 源名称
                - url: RSS地址
                - type: rss/atom (可选，自动检测)
            - limit: 每个源返回数量 (默认: 5)
    
    Returns:
        list: 文章列表
    """
    feeds = config.get("feeds", [])
    limit_per_feed = config.get("limit_per_feed", 5)
    
    items = []
    
    for feed_config in feeds:
        name = feed_config.get("name", "Unknown")
        url = feed_config.get("url", "")
        
        if not url:
            continue
        
        feed_items = _fetch_single_feed(name, url, limit_per_feed)
        items.extend(feed_items)
    
    # 按发布日期排序
    items.sort(key=lambda x: x.get("published_parsed") or (0,) * 9, reverse=True)
    
    return items


def _fetch_single_feed(name, url, limit=5, max_retries=2):
    """
    获取单个RSS源的内容
    
    Args:
        name: 源名称
        url: RSS地址
        limit: 返回数量
        max_retries: 最大重试次数
    
    Returns:
        list: 文章列表
    """
    # 设置请求头，模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml, application/atom+xml, */*"
    }
    
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            # 先尝试直接请求，增加超时设置
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 使用feedparser解析
            feed = feedparser.parse(response.text)
            
            items = []
            for entry in feed.entries[:limit]:
                item = _parse_feed_entry(entry, name, url)
                if item:
                    items.append(item)
            
            return items
            
        except requests.exceptions.Timeout:
            last_error = f"超时 (10秒)"
            if attempt < max_retries:
                print(f"RSS请求超时 ({name}), 正在重试 ({attempt + 1}/{max_retries})...")
        except requests.exceptions.ConnectionError as e:
            last_error = f"连接失败"
            if attempt < max_retries:
                print(f"RSS连接失败 ({name}), 正在重试 ({attempt + 1}/{max_retries})...")
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            if attempt < max_retries:
                print(f"RSS请求失败 ({name}): {e}, 正在重试 ({attempt + 1}/{max_retries})...")
            break  # 其他请求错误不重试
        except Exception as e:
            print(f"RSS解析失败 ({name}): {e}")
            return []
    
    # 所有重试都失败后
    print(f"RSS请求最终失败 ({name}): {last_error}")
    return []


def _parse_feed_entry(entry, source_name, source_url):
    """
    解析单个RSS条目
    
    Args:
        entry: feedparser的条目对象
        source_name: 源名称
        source_url: 源URL
    
    Returns:
        dict: 解析后的文章信息
    """
    # 获取标题
    title = getattr(entry, "title", "无标题") or "无标题"
    
    # 获取链接
    link = getattr(entry, "link", "") or ""
    
    # 获取摘要/内容
    summary = getattr(entry, "summary", "") or getattr(entry, "description", "") or ""
    # 清理HTML标签
    summary = _strip_html(summary)
    summary = summary[:300] + "..." if len(summary) > 300 else summary
    
    # 获取发布日期
    published = getattr(entry, "published", "") or getattr(entry, "updated", "") or ""
    published_parsed = getattr(entry, "published_parsed", None)
    
    # 格式化日期
    if published_parsed:
        try:
            pub_date = datetime(*published_parsed[:6])
            published = pub_date.strftime("%Y-%m-%d %H:%M")
        except:
            pass
    
    # 获取作者
    author = getattr(entry, "author", "") or ""
    if not author and hasattr(entry, "authors") and entry.authors:
        author = entry.authors[0].get("name", "")
    
    # 获取分类
    categories = getattr(entry, "tags", [])
    if categories:
        categories = [tag.term for tag in categories]
    
    return {
        "title": title.strip(),
        "url": link,
        "summary": summary,
        "published": published,
        "published_parsed": published_parsed,
        "author": author,
        "categories": categories,
        "source": source_name,
        "source_url": source_url,
        "source_type": "article"
    }


def _strip_html(text):
    """移除HTML标签"""
    import re
    # 移除script和style标签及其内容
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # 移除所有HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 清理多余空白
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# 预设的AI博客RSS源
DEFAULT_BLOGS = [
    {
        "name": "Anthropic News",
        "url": "https://www.anthropic.com/news/rss",
        "category": "AI Company"
    },
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog/rss.xml",
        "category": "AI Company"
    },
    {
        "name": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss/",
        "category": "AI Company"
    },
    {
        "name": "DeepMind Blog",
        "url": "https://deepmind.com/blog/feed/basic/",
        "category": "AI Company"
    },
    {
        "name": "Meta AI Blog",
        "url": "https://ai.meta.com/blog/rss/",
        "category": "AI Company"
    },
    {
        "name": "Microsoft AI Blog",
        "url": "https://blogs.microsoft.com/ai/feed/",
        "category": "AI Company"
    },
    {
        "name": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml",
        "category": "AI Company"
    },
]


def validate_rss_url(url):
    """
    验证RSS URL是否有效
    
    Args:
        url: RSS地址
    
    Returns:
        dict: 验证结果，包含 status, title, item_count
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        feed = feedparser.parse(response.text)
        
        return {
            "status": "valid",
            "title": feed.feed.get("title", "Unknown"),
            "item_count": len(feed.entries),
            "description": feed.feed.get("description", "")
        }
        
    except Exception as e:
        return {
            "status": "invalid",
            "error": str(e)
        }


if __name__ == "__main__":
    # 测试代码
    test_feeds = [
        {"name": "Test", "url": "https://www.anthropic.com/news/rss"}
    ]
    
    config = {"feeds": test_feeds, "limit_per_feed": 3}
    results = fetch_blog_rss(config)
    
    print(f"获取到 {len(results)} 篇文章:")
    for item in results:
        print(f"  - [{item['source']}] {item['title'][:40]}...")
