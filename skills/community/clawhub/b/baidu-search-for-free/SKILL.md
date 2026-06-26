---
name: baidu-search
description: 使用 baidusearch 库进行百度搜索，并支持解析搜索结果网页内容。Use when: (1) 用户需要进行百度搜索获取信息，(2) 需要检索中文网页内容，(3) 需要获取搜索结果标题、摘要和链接，(4) 需要解析百度搜到的网页内容。触发词：百度搜索、baidu search、搜索百度、用百度查、抓取网页、解析网页。
---

# Baidu Search

使用 baidusearch 库进行百度搜索，并支持解析搜索结果网页内容。

## Quick Start

### 1. 百度搜索

```python
from baidusearch.baidusearch import search

# 基础搜索（默认返回10条结果）
results = search('搜索关键词')

# 指定返回结果数量
results = search('搜索关键词', num_results=20)
```

返回结果格式：
```python
[
    {
        'title': '结果标题',
        'abstract': '结果摘要',
        'url': '结果链接',
        'rank': 1
    },
    ...
]
```

### 2. 解析网页内容

```python
from scripts.fetch_url import fetch_url

# 获取并解析网页内容
content = fetch_url('http://example.com/article')
print(content['title'])
print(content['text'])
```

### 3. 搜索并解析完整流程

```python
from baidusearch.baidusearch import search
from scripts.fetch_url import fetch_url

# 第一步：搜索
results = search('南京江宁龙虾政策', num_results=5)

# 第二步：解析第一条结果的网页内容
if results:
    first_url = results[0]['url']
    content = fetch_url(first_url)
    print(f"标题: {content['title']}")
    print(f"正文: {content['text'][:500]}...")
```

### 命令行使用

**搜索:**
```bash
python3 scripts/baidu_search.py "搜索关键词" --num 10
```

**解析网页:**
```bash
python3 scripts/fetch_url.py "http://example.com"
python3 scripts/fetch_url.py "http://example.com" --max-chars 2000
```

**搜索并解析（完整流程）:**
```bash
python3 scripts/search_and_fetch.py "搜索关键词" --num 5
```

## Workflow

1. **安装依赖**: 确保已安装所需库
   ```bash
   pip3 install --user baidusearch requests beautifulsoup4 lxml
   ```

2. **执行搜索**: 使用 baidusearch 获取搜索结果

3. **解析网页**: 使用 fetch_url 解析搜索结果中的网页内容

4. **注意事项**: 
   - 建议每次搜索间隔 15 秒以上
   - 频繁使用可能导致 IP 被百度封禁
   - 遇到 503 错误请等待 1 分钟后重试
   - 部分网站可能有反爬机制，解析可能失败

## Resources

### scripts/

- `baidu_search.py` - 百度搜索脚本，支持命令行参数调用
- `fetch_url.py` - 网页内容抓取和解析脚本
- `search_and_fetch.py` - 搜索并自动解析网页内容的完整流程脚本
