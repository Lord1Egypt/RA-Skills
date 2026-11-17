---
name: finet-news-lite
description: "获取财华社（finet.com.cn）最新财经新闻的最小工具：实时拉取，统一输出扁平的标准文章字段，内置超时重试，纯标准库零依赖。"
version: "1.0.1"
user-invocable: true
---

# finet-news-lite · 财华财经新闻（最小版）

实时获取财华社最新财经新闻。只做一件事：拉取最新资讯，统一输出扁平、可直接消费的标准文章字段。

- 纯 Python 标准库，**零第三方依赖**，装上即用
- 内置请求超时与失败重试（指数退避）
- 不做本地缓存，每次实时拉取
- 输出统一文章结构，无需二次字段转换

## 环境要求

- Python 3.8 及以上
- 可访问财华社接口（`cps.finet.com.cn`）

## 安装

从 ClawHub 安装：

```bash
clawhub install @finet8317/finet-news-lite
```

或直接下载本 skill 目录，通过 `scripts/fetch_news.py` 调用，无需安装任何依赖。

## 快速开始

```python
import sys
sys.path.insert(0, "scripts")
from fetch_news import fetch_news

news = fetch_news(limit=5)            # 最新 5 条
news = fetch_news(limit=5, days=3)    # 最近 3 天窗口内的最新 5 条
print(news[0]["title"])
```

## 命令行

```bash
python3 scripts/fetch_news.py --limit 5
python3 scripts/fetch_news.py --limit 5 --days 3
```

输出为 JSON 数组（UTF-8，缩进 2 空格）。

## API

### fetch_news(limit=None, days=None, timeout=8, retries=3, retry_backoff=1.5)

实时获取财华社财经新闻，返回统一文章结构列表。

**参数**

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `limit` | int / None | None | 取返回结果的前 N 条；None 或 ≤0 表示不截断（返回时间窗口内全部）。此截断在本地完成，不是服务端分页 |
| `days` | int / None | None | 时间窗口（最近 N 天）。None 或不传 = 由服务端按默认值 1 天处理。服务端强制限制在 1–7：小于 1 按 1，大于 7 按 7（已实测 days=10 与 days=7 结果一致） |
| `timeout` | int | 8 | 单次请求超时秒数 |
| `retries` | int | 3 | 失败重试次数（含首次，默认共请求 3 次） |
| `retry_backoff` | float | 1.5 | 重试指数退避底数，第 n 次重试等待 `1.5^(n-1)` 秒 |

**返回**：`list[dict]`，每条为统一文章字段（见下）。

**异常**：

- 网络错误重试耗尽 —— 抛出最后一次底层异常
- 接口返回 `code` 非 200 —— 抛出 `RuntimeError`，含 code 与 message
- 不做静默降级，失败即明确报错

> 关于 `days`：它表示服务端的时间窗口（最近 N 天），默认 1 天，并被强制限制在 1–7（`max(1, min(7, days))`）。该窗口按发布时间过滤，并非严格"过去 24 小时滚动"，因此返回结果可能包含略早于 24 小时的文章，以接口实际数据为准。

## 输出字段（统一文章结构）

| 字段 | 类型 | 说明 |
|------|------|------|
| `source_id` | str | 文章唯一 ID（24 位 hex） |
| `title` | str | 标题 |
| `content` | str | 正文 HTML，图片域名已替换为可直连地址 |
| `summary` | str | 摘要 |
| `cover_image` | str | 封面图 URL；源无封面时使用默认封面 |
| `content_img_urls` | list[str] | 正文中的图片 URL，保序去重 |
| `keywords` | list[str] | 关键词列表，按中/英文逗号拆分 |
| `creator` | str | 作者 |
| `publish_time` | str | 发布时间，ISO 8601 带 `+08:00` |
| `category` | list[str] | 分类列表 |
| `news_url` | str | 财华网文章页地址 |

**返回示例**

```json
[
  {
    "source_id": "6abb2d27230829b8a72bc533",
    "title": "一图解码：港股IPO一周回顾 5家公司递表……",
    "content": "<p>正文 HTML……</p>",
    "summary": "过去一周，港股IPO市场共有5家公司递交上市申请……",
    "cover_image": "https://fs.finet.com.cn/photoLib/title/202609_1/xxx.jpg",
    "content_img_urls": ["https://fs.finet.com.cn/photoLib/content/202609_1/xxx.jpg"],
    "keywords": ["一图解码", "IPO", "奥比中光"],
    "creator": "一图解码",
    "publish_time": "2026-09-29T03:13:23+08:00",
    "category": ["深度", "一图解码", "IPO", "要闻"],
    "news_url": "https://www.finet.com.cn/news/6abb2d27230829b8a72bc533.html"
  }
]
```

## 数据来源

财华社公开接口 `https://cps.finet.com.cn/cps_api/news/recent-list`，无需鉴权。

**环境变量**

- `FINET_API_HOST` —— 覆盖接口 host（默认 `https://cps.finet.com.cn`）

## 许可

数据版权归财华社所有，本工具仅用于资讯获取与内部技术用途。
