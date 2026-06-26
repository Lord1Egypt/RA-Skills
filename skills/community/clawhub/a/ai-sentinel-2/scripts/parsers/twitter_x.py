"""
Twitter/X 解析器
获取AI大咖和机构的最新动态

注意: Twitter API v2 需要 Bearer Token
如果没有配置API，将返回空列表
"""
import requests
from datetime import datetime, timedelta


def fetch_twitter(config, api_settings):
    """
    获取Twitter/X动态
    
    Args:
        config: 信息源配置，包含:
            - accounts: 关注的账号列表
            - keywords: 关键词搜索
            - limit: 返回数量 (默认: 20)
        api_settings: API设置，包含:
            - bearer_token: Twitter API Bearer Token
    
    Returns:
        list: 推文列表
    """
    bearer_token = api_settings.get("bearer_token", "")
    
    if not bearer_token:
        print("⚠️  未配置Twitter Bearer Token，跳过Twitter采集")
        print("   请参考 references/api_setup.md 配置Twitter API")
        return []
    
    accounts = config.get("accounts", [])
    keywords = config.get("keywords", ["AI", "machine learning", "LLM", "GPT", "Claude"])
    limit = config.get("limit", 20)
    
    items = []
    
    # 1. 获取指定账号的推文
    if accounts:
        for account in accounts[:5]:  # 限制账号数量避免API限制
            tweets = _fetch_user_tweets(account, bearer_token, limit // len(accounts) if accounts else 10)
            items.extend(tweets)
    
    # 2. 搜索关键词
    if keywords:
        for keyword in keywords[:3]:  # 限制关键词数量
            tweets = _search_tweets(keyword, bearer_token, limit // 3)
            items.extend(tweets)
    
    # 去重
    seen_ids = set()
    unique_items = []
    for item in items:
        if item.get("id") not in seen_ids:
            seen_ids.add(item.get("id"))
            unique_items.append(item)
    
    # 按时间排序
    unique_items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    return unique_items[:limit]


def _fetch_user_tweets(username, bearer_token, limit=10):
    """
    获取指定用户的推文
    
    Args:
        username: 用户名
        bearer_token: API密钥
        limit: 数量限制
    
    Returns:
        list: 推文列表
    """
    # Twitter API v2 endpoint
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "AI-Sentinel/1.0"
    }
    
    try:
        # 先获取用户ID
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        user_data = response.json()
        
        user_id = user_data.get("data", {}).get("id")
        if not user_id:
            return []
        
        # 获取用户推文
        tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
        params = {
            "max_results": min(limit, 100),
            "tweet.fields": "created_at,public_metrics,lang",
            "expansions": "author_id",
            "user.fields": "name,username,profile_image_url"
        }
        
        tweets_response = requests.get(tweets_url, params=params, headers=headers, timeout=30)
        tweets_response.raise_for_status()
        tweets_data = tweets_response.json()
        
        items = []
        includes = tweets_data.get("includes", {})
        users = {u["id"]: u for u in include.get("users", [])}
        
        for tweet in tweets_data.get("data", []):
            author = users.get(tweet.get("author_id", {}), {})
            metrics = tweet.get("public_metrics", {})
            
            items.append({
                "id": tweet.get("id"),
                "text": tweet.get("text", ""),
                "author_name": author.get("name", username),
                "author_username": author.get("username", username),
                "author_url": f"https://twitter.com/{author.get('username', username)}",
                "author_image": author.get("profile_image_url", ""),
                "created_at": tweet.get("created_at", ""),
                "likes": metrics.get("like_count", 0),
                "retweets": metrics.get("retweet_count", 0),
                "replies": metrics.get("reply_count", 0),
                "url": f"https://twitter.com/{author.get('username', username)}/status/{tweet.get('id')}",
                "source": "twitter",
                "source_type": "tweet"
            })
        
        return items
        
    except requests.exceptions.RequestException as e:
        print(f"Twitter API请求失败 ({username}): {e}")
        return []


def _search_tweets(query, bearer_token, limit=10):
    """
    搜索推文
    
    Args:
        query: 搜索关键词
        bearer_token: API密钥
        limit: 数量限制
    
    Returns:
        list: 推文列表
    """
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "AI-Sentinel/1.0"
    }
    params = {
        "query": query,
        "max_results": min(limit, 100),
        "tweet.fields": "created_at,public_metrics,lang,author_id",
        "expansions": "author_id",
        "user.fields": "name,username,profile_image_url"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        items = []
        includes = data.get("includes", {})
        users = {u["id"]: u for u in includes.get("users", [])}
        
        for tweet in data.get("data", []):
            author = users.get(tweet.get("author_id", {}), {})
            metrics = tweet.get("public_metrics", {})
            
            items.append({
                "id": tweet.get("id"),
                "text": tweet.get("text", ""),
                "author_name": author.get("name", "Unknown"),
                "author_username": author.get("username", "unknown"),
                "author_url": f"https://twitter.com/{author.get('username', 'unknown')}",
                "author_image": author.get("profile_image_url", ""),
                "created_at": tweet.get("created_at", ""),
                "likes": metrics.get("like_count", 0),
                "retweets": metrics.get("retweet_count", 0),
                "replies": metrics.get("reply_count", 0),
                "url": f"https://twitter.com/{author.get('username', 'unknown')}/status/{tweet.get('id')}",
                "query": query,  # 记录匹配的搜索词
                "source": "twitter",
                "source_type": "tweet"
            })
        
        return items
        
    except requests.exceptions.RequestException as e:
        print(f"Twitter搜索失败 ({query}): {e}")
        return []


# 推荐的AI领域大咖账号
DEFAULT_AI_ACCOUNTS = [
    "ylecun",        # Yann LeCun (Meta AI)
    "AndrewYNg",     # Andrew Ng
    "sama",          # Sam Altman (OpenAI CEO)
    "gaborcselle",   # 每日AI新闻
    "binduredy",     # Google AI
    "JeffDrewTech",  # Tech新闻
    "emaboros",      # AI研究
    "ylecun",        # Meta AI
    "kaborl",        # AI新闻
]


if __name__ == "__main__":
    # 测试代码 - 需要有效的Bearer Token
    print("Twitter解析器需要配置Bearer Token")
    print("请参考 references/api_setup.md 进行配置")
