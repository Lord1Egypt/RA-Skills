"""
HackerNews 解析器
获取热门讨论和链接
"""
import requests
from datetime import datetime


# HackerNews Firebase API基础URL
HN_API_BASE = "https://hacker-news.firebaseio.com/v0"


def fetch_hackernews(config):
    """
    获取HackerNews热门内容
    
    Args:
        config: 信息源配置，包含:
            - item_type: 获取类型 (top/new/best/ask/show)
            - limit: 返回数量 (默认: 20)
            - keywords: 关键词过滤，用于筛选AI相关内容
    
    Returns:
        list: 项目列表，每项包含 title, url, score, comments, author, time
    """
    item_type = config.get("item_type", "top")
    limit = config.get("limit", 20)
    keywords = config.get("keywords", ["AI", "ML", "machine learning", "neural", "LLM", "GPT", "deep learning"])
    
    # 获取对应的故事ID列表
    endpoint_map = {
        "top": "topstories",
        "new": "newstories",
        "best": "beststories",
        "ask": "askstories",
        "show": "showstories"
    }
    
    endpoint = endpoint_map.get(item_type, "topstories")
    url = f"{HN_API_BASE}/{endpoint}.json"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        story_ids = response.json()
        
        # 获取每个故事的详细信息
        items = []
        count = 0
        for story_id in story_ids[:limit * 3]:  # 预取更多以便过滤
            if count >= limit:
                break
            
            item = _fetch_hn_item(story_id)
            if item and _filter_by_keywords(item, keywords):
                items.append(item)
                count += 1
        
        return items
        
    except requests.exceptions.RequestException as e:
        print(f"HackerNews API请求失败: {e}")
        return []


def _fetch_hn_item(item_id):
    """
    获取单个HackerNews项目详情
    
    Args:
        item_id: 项目ID
    
    Returns:
        dict: 项目信息
    """
    url = f"{HN_API_BASE}/item/{item_id}.json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        item = response.json()
        
        if not item or item.get("type") != "story":
            return None
        
        # 格式化时间
        timestamp = item.get("time", 0)
        time_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M") if timestamp else ""
        
        return {
            "title": item.get("title", "无标题"),
            "url": item.get("url", ""),
            "hn_url": f"https://news.ycombinator.com/item?id={item_id}",
            "score": item.get("score", 0),
            "comments": item.get("descendants", 0),
            "author": item.get("by", "anonymous"),
            "author_url": f"https://news.ycombinator.com/user?id={item.get('by', 'anonymous')}",
            "time": time_str,
            "timestamp": timestamp,
            "type": item.get("type", "story"),
            "text": item.get("text", ""),  # 用于Ask HN等
            "source": "hackernews",
            "source_type": "discussion"
        }
        
    except requests.exceptions.RequestException:
        return None


def _filter_by_keywords(item, keywords):
    """
    根据关键词过滤项目
    
    Args:
        item: 项目信息
        keywords: 关键词列表
    
    Returns:
        bool: 是否匹配
    """
    if not keywords:
        return True
    
    title = item.get("title", "").lower()
    url = item.get("url", "").lower()
    text = item.get("text", "").lower()
    
    content = f"{title} {url} {text}"
    
    for keyword in keywords:
        if keyword.lower() in content:
            return True
    
    return False


def fetch_hn_comments(story_id, limit=10):
    """
    获取故事的评论
    
    Args:
        story_id: 故事ID
        limit: 评论数量限制
    
    Returns:
        list: 评论列表
    """
    url = f"{HN_API_BASE}/item/{story_id}.json"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        story = response.json()
        
        comments = []
        for kid in story.get("kids", [])[:limit]:
            comment = _fetch_hn_item(kid)
            if comment:
                comments.append(comment)
        
        return comments
        
    except requests.exceptions.RequestException:
        return []


if __name__ == "__main__":
    # 测试代码
    config = {
        "item_type": "top",
        "limit": 5,
        "keywords": ["AI", "ML", "GPT"]
    }
    results = fetch_hackernews(config)
    print(f"获取到 {len(results)} 条讨论:")
    for item in results:
        print(f"  - {item['title'][:50]}... ({item['score']} points)")
