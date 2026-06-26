# 360 搜索技能

使用 360 搜索引擎进行网页、新闻、图片搜索。

## 功能

- 网页搜索
- 新闻搜索
- 图片搜索

## 配置

复制 `.env.example` 到 `.env` 并配置参数。

## 使用方法

```bash
# 普通搜索
python scripts/search.py '{"query":"Python 编程"}'

# 新闻搜索
python scripts/news.py '{"query":"人工智能"}'

# 图片搜索
python scripts/image.py '{"query":"风景"}'
```

## API

```python
from 360_search_client import Search360Client

client = Search360Client()
client.start()

# 网页搜索
results = client.search("关键词", max_results=10)

# 新闻搜索
news = client.search_news("关键词", max_results=10)

# 图片搜索
images = client.search_image("关键词", max_results=20)

client.stop()
```
