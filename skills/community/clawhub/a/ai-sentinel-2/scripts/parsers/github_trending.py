"""
GitHub Trending 解析器
获取AI领域热门开源项目
"""
import requests
from datetime import datetime, timedelta


def fetch_github_trending(config):
    """
    获取GitHub Trending项目
    
    Args:
        config: 信息源配置，包含:
            - language: 编程语言 (默认: python)
            - date_range: 时间范围 (daily/weekly/monthly)，用于筛选新项目
            - limit: 返回数量 (默认: 20)
            - keywords: 关键词过滤列表
    
    Returns:
        list: 项目列表，每项包含 title, description, url, stars, forks, language
    """
    language = config.get("language", "python")
    date_range = config.get("date_range", "weekly")
    limit = config.get("limit", 20)
    keywords = config.get("keywords", [])
    
    # GitHub API请求
    # 使用搜索API按star排序获取热门项目
    # 构建查询：按语言获取热门项目
    query = f"language:{language}"
    
    # 如果设置了关键词，添加关键词过滤
    if keywords:
        keyword_query = " OR ".join(keywords)
        query = f"({query}) AND ({keyword_query})"
    
    # 设置时间参数（只在需要筛选新项目时使用）
    date_filter = ""
    if date_range:
        if date_range == "daily":
            since = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        elif date_range == "weekly":
            since = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        else:
            since = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        date_filter = f" created:>{since}"
    
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query + date_filter,
        "sort": "stars",
        "order": "desc",
        "per_page": min(limit, 100)
    }
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AI-Sentinel/1.0"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        items = []
        for repo in data.get("items", [])[:limit]:
            # 如果没有设置关键词过滤但有结果，返回
            items.append({
                "title": repo.get("full_name", ""),
                "description": repo.get("description", "") or "无描述",
                "url": repo.get("html_url", ""),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "language": repo.get("language", "Unknown"),
                "author": repo.get("owner", {}).get("login", ""),
                "author_url": repo.get("owner", {}).get("html_url", ""),
                "created_at": repo.get("created_at", ""),
                "updated_at": repo.get("updated_at", ""),
                "source": "github",
                "source_type": "repository"
            })
        
        # 按URL去重，确保每个项目只出现一次
        seen_urls = set()
        unique_items = []
        for item in items:
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                unique_items.append(item)
        
        return unique_items
        
    except requests.exceptions.RequestException as e:
        print(f"GitHub API请求失败: {e}")
        # 尝试使用备用方案：直接爬取Trending页面
        return _fetch_github_trending_fallback(limit)


def _fetch_github_trending_fallback(limit=20):
    """
    备用方案：直接爬取GitHub Trending页面
    当API受限或失败时使用
    """
    url = "https://github.com/trending/python"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # 简单的HTML解析（实际项目中建议使用BeautifulSoup）
        items = []
        # 这里简化处理，实际需要解析HTML
        return items
        
    except requests.exceptions.RequestException:
        return []


def search_github_repos(query, language=None, sort="stars", limit=10):
    """
    搜索GitHub仓库
    
    Args:
        query: 搜索关键词
        language: 编程语言过滤
        sort: 排序方式 (stars/forks/updated)
        limit: 返回数量
    
    Returns:
        list: 仓库列表
    """
    url = "https://api.github.com/search/repositories"
    q = query
    if language:
        q += f"+language:{language}"
    
    params = {
        "q": q,
        "sort": sort,
        "order": "desc",
        "per_page": min(limit, 100)
    }
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AI-Sentinel/1.0"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        return [{
            "title": repo.get("full_name"),
            "description": repo.get("description"),
            "url": repo.get("html_url"),
            "stars": repo.get("stargazers_count"),
            "language": repo.get("language"),
            "source": "github",
            "source_type": "search"
        } for repo in data.get("items", [])[:limit]]
        
    except requests.exceptions.RequestException:
        return []


if __name__ == "__main__":
    # 测试代码
    config = {
        "language": "python",
        "date_range": "daily",
        "limit": 10
    }
    results = fetch_github_trending(config)
    print(f"获取到 {len(results)} 个项目:")
    for item in results:
        print(f"  - {item['title']} ⭐{item['stars']}")
