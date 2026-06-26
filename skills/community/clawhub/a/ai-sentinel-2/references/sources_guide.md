# 信息源添加指南

本文档说明如何为AI前沿哨兵添加新的信息源。

## 添加新的解析器

### 步骤1：创建解析器文件

在 `scripts/parsers/` 目录下创建新的Python文件，例如 `custom_source.py`：

```python
"""
自定义信息源解析器
"""
import requests
from datetime import datetime


def fetch_custom_source(config):
    """
    获取自定义信息源内容
    
    Args:
        config: 信息源配置，来自 sources.yaml
    
    Returns:
        list: 内容列表，每项包含:
            - title: 标题
            - url: 链接
            - description: 描述
            - published: 发布时间
            - source: 源名称
            - source_type: 内容类型 (paper/project/discussion/article/tweet)
    """
    url = config.get("url", "")
    limit = config.get("limit", 20)
    
    items = []
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # 根据返回的数据格式解析
        data = response.json()  # 或 response.text 用 re/BeautifulSoup 解析
        
        for item in data[:limit]:
            items.append({
                "title": item.get("title", "无标题"),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
                "published": item.get("published", ""),
                "author": item.get("author", ""),
                "source": "custom",
                "source_type": "article"
            })
            
    except Exception as e:
        print(f"采集失败: {e}")
    
    return items


# 如果需要导出搜索功能
def search_custom_source(query, limit=10):
    """搜索自定义源"""
    # 实现搜索逻辑
    pass


if __name__ == "__main__":
    # 测试代码
    config = {"url": "https://example.com/api", "limit": 10}
    results = fetch_custom_source(config)
    print(f"获取到 {len(results)} 条内容")
```

### 步骤2：在 sources.yaml 中注册

```yaml
# config/sources.yaml

custom_source:
  enabled: true
  url: "https://example.com/api"
  limit: 20
  # 其他自定义配置...
```

### 步骤3：在 collect.py 中注册

编辑 `scripts/collect.py`，在 `_collect_source` 方法中添加：

```python
elif source_name == "custom_source":
    items = fetch_custom_source(source_config)
```

### 步骤4：更新 __init__.py

在 `scripts/parsers/__init__.py` 中添加导出：

```python
from .custom_source import fetch_custom_source, search_custom_source

__all__ = [
    # ... 其他
    'fetch_custom_source',
    'search_custom_source'
]
```

## 常见数据格式处理

### JSON API

```python
def fetch_json_api(config):
    response = requests.get(config["url"])
    data = response.json()
    
    items = []
    for item in data.get("items", []):
        items.append({
            "title": item["title"],
            "url": item["url"],
            "source_type": "article"
        })
    return items
```

### HTML网页解析

需要安装 BeautifulSoup：

```bash
pip install beautifulsoup4 lxml
```

```python
from bs4 import BeautifulSoup

def fetch_html_page(config):
    response = requests.get(config["url"])
    soup = BeautifulSoup(response.text, "lxml")
    
    items = []
    for element in soup.select(".article-list .item"):
        items.append({
            "title": element.select_one(".title").text.strip(),
            "url": element.select_one("a")["href"],
            "source_type": "article"
        })
    return items
```

### RSS/Atom订阅

使用已有的 `blog_rss.py` 解析器，只需在配置中添加：

```yaml
blogs:
  enabled: true
  feeds:
    - name: "自定义源"
      url: "https://example.com/feed.xml"
      category: "自定义分类"
```

## 高级：实现认证

如果API需要认证：

```python
def fetch_authenticated_api(config, auth_settings):
    api_key = auth_settings.get("api_key", "")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "AI-Sentinel/1.0"
    }
    
    response = requests.get(
        config["url"],
        headers=headers,
        timeout=30
    )
    response.raise_for_status()
    
    return response.json()
```

然后在 `collect.py` 中调用时传入认证信息：

```python
auth_settings = self.settings.get("custom_source_auth", {})
items = fetch_authenticated_api(source_config, auth_settings)
```

## 数据标准化

解析后的数据应该遵循以下格式：

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| title | string | ✅ | 内容标题 |
| url | string | ✅ | 原文链接 |
| description | string | ❌ | 简短描述/摘要 |
| published | string | ❌ | 发布时间 |
| author | string | ❌ | 作者 |
| source | string | ✅ | 来源名称 |
| source_type | string | ✅ | 内容类型 |

**source_type 可选值**：
- `paper` - 学术论文
- `repository` - 开源项目
- `discussion` - 社区讨论
- `article` - 博客文章
- `tweet` - 社交动态
- `news` - 新闻

## 测试解析器

```bash
cd scripts/parsers
python -c "
from custom_source import fetch_custom_source
config = {'url': 'https://example.com/api', 'limit': 5}
results = fetch_custom_source(config)
print(f'获取到 {len(results)} 条内容')
for item in results:
    print(f'  - {item[\"title\"]}')"
```

## 常见问题

### Q: API返回429 Too Many Requests怎么办？

A: 添加请求间隔和重试机制：

```python
import time

def fetch_with_retry(url, max_retries=3):
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 429:
                time.sleep(60 * (i + 1))  # 递增等待
                continue
            response.raise_for_status()
            return response
        except Exception as e:
            if i == max_retries - 1:
                raise
            time.sleep(2 ** i)
```

### Q: 数据量很大怎么处理？

A: 使用分页和流式处理：

```python
def fetch_with_pagination(config):
    items = []
    page = 1
    per_page = 100
    
    while True:
        response = requests.get(
            f"{config['url']}?page={page}&per_page={per_page}"
        )
        data = response.json()
        
        if not data.get("items"):
            break
            
        items.extend(data["items"])
        
        if len(data["items"]) < per_page:
            break
            
        page += 1
        time.sleep(1)  # 避免过快
        
    return items
```
